#!/usr/bin/env python3
"""
Export clinical protocol data from markdown frontmatter to JSON.
Walks docs/drugs/*.md, validates with Pydantic, and writes docs/api/protocols.json.

Usage:
  python scripts/export_protocols.py          # Generate docs/api/protocols.json
  python scripts/export_protocols.py --check  # Check if docs/api/protocols.json is up to date
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


class CrossReactivityItem(BaseModel):
    category: str
    info: str
    alternatives: str

    model_config = {"extra": "forbid"}


class CrossReactivityFrontmatter(BaseModel):
    title: Optional[str] = None
    version: Union[float, str]
    last_reviewed: Optional[Union[date, str]]
    reviewed_by: Optional[str]
    under_review: bool
    provenance: str
    items: List[CrossReactivityItem]

    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def validate_governance(self) -> "CrossReactivityFrontmatter":
        if not self.under_review:
            reviewed_by = str(self.reviewed_by or "").strip()
            last_reviewed = str(self.last_reviewed or "").strip()
            if not reviewed_by or not last_reviewed:
                raise ValueError(
                    "When under_review is false, both reviewed_by and last_reviewed must be non-empty."
                )
        return self


class TestType(str, Enum):
    SKIN = "skin"
    CHALLENGE = "challenge"
    CONTROL = "control"
    EXPERIMENTAL = "experimental"


class DreamCategory(str, Enum):
    MUSCLE_RELAXANTS = "Muscle Relaxants"
    REVERSAL_AGENTS = "Reversal Agents"
    PENICILLINS = "Penicillins"
    CEPHALOSPORINS = "Cephalosporins"
    HYPNOTICS = "Hypnotics"
    LOCAL_ANAESTHETICS = "Local Anaesthetics"
    OPIOIDS = "Opioids"
    ANTISEPTICS = "Antiseptics"
    PROTON_PUMP_INHIBITORS = "Proton Pump Inhibitors"
    OTHERS = "Others"


class DreamConfig(BaseModel):
    category: Optional[DreamCategory] = None
    drug_name: Optional[str] = None

    model_config = {"extra": "forbid"}


class SptConfig(BaseModel):
    dilution: Optional[str] = None
    concentration: Optional[str] = None
    positive_control: Optional[str] = None
    negative_control: Optional[str] = None

    model_config = {"extra": "forbid"}


class IdtStep(BaseModel):
    dilution: str
    concentration: str
    preparation: Optional[str] = ""

    model_config = {"extra": "forbid"}


class ChallengeStep(BaseModel):
    dose: str
    cumulative: Optional[str] = None
    volume: Optional[str] = None
    interval: Optional[str] = None

    model_config = {"extra": "forbid"}


class ChallengeConfig(BaseModel):
    interval: Optional[str] = None
    steps: List[ChallengeStep] = Field(default_factory=list)

    model_config = {"extra": "forbid"}


class Protocol(BaseModel):
    id: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    label: str
    test_type: TestType
    presentation: Optional[str] = None
    diluent: Optional[str] = None
    spt: Optional[SptConfig] = None
    idt: Optional[List[IdtStep]] = None
    challenge: Optional[ChallengeConfig] = None
    under_review: bool = False
    review_note: Optional[str] = ""
    needs_pharmacy_verification: bool = False

    model_config = {"extra": "forbid"}


class DrugFrontmatter(BaseModel):
    title: str
    tags: Optional[List[str]] = None
    reviewed_by: Optional[str] = None
    last_reviewed: Optional[Union[date, str]] = None
    version: Optional[Union[float, str]] = None
    dream: Optional[DreamConfig] = None
    protocols: Optional[List[Protocol]] = None

    model_config = {"extra": "allow"}

    @field_validator("protocols")
    @classmethod
    def validate_unique_protocol_ids(cls, v: Optional[List[Protocol]]) -> Optional[List[Protocol]]:
        if not v:
            return v
        seen = set()
        duplicates = []
        for p in v:
            if p.id in seen:
                duplicates.append(p.id)
            seen.add(p.id)
        if duplicates:
            raise ValueError(f"Duplicate protocol id(s) found: {', '.join(set(duplicates))}")
        return v


def parse_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract and parse YAML frontmatter from a markdown file."""
    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    raw_yaml = parts[1]
    return yaml.safe_load(raw_yaml) or {}


def format_validation_error(file_path: Path, error: ValidationError) -> List[str]:
    """Format Pydantic validation errors into clear, actionable messages."""
    messages = []
    rel_path = file_path.as_posix()
    for err in error.errors():
        loc = err.get("loc", ())
        field_name = ".".join(str(x) for x in loc)
        msg = err.get("msg", "")

        # Try to identify protocol id if the error is inside a protocol
        proto_info = ""
        if len(loc) >= 2 and loc[0] == "protocols" and isinstance(loc[1], int):
            proto_index = loc[1]
            proto_info = f" [protocol index: {proto_index}]"

        # Specialized error messages for nurses and maintainers
        if "test_type" in field_name:
            valid_types = ", ".join(t.value for t in TestType)
            messages.append(
                f"ERROR in {rel_path}{proto_info}: field '{field_name}' has invalid value. "
                f"Must be one of: {valid_types}."
            )
        elif "category" in field_name:
            valid_cats = ", ".join(c.value for c in DreamCategory)
            messages.append(
                f"ERROR in {rel_path}: field '{field_name}' has invalid value. "
                f"Must be exactly one of: {valid_cats}."
            )
        elif "id" in field_name and "pattern" in err.get("type", ""):
            messages.append(
                f"ERROR in {rel_path}{proto_info}: field '{field_name}' must be slug-style "
                f"(lowercase letters, numbers, hyphens, underscores only, matching '^[a-z0-9_-]+$')."
            )
        else:
            messages.append(f"ERROR in {rel_path}{proto_info}: field '{field_name}' - {msg}")
    return messages


def get_source_commit(repo_root: Path) -> str:
    """Get the current git commit hash (short)."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            env=dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null"),
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def load_meta_defaults(drugs_dir: Path) -> Dict[str, Any]:
    """Load default metadata from docs/drugs/.meta.yml."""
    meta_file = drugs_dir / ".meta.yml"
    if meta_file.exists():
        try:
            return yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}


def serialize_drug(slug: str, fm: DrugFrontmatter) -> Dict[str, Any]:
    """Serialize a validated DrugFrontmatter into a dictionary with stable keys."""
    drug_data: Dict[str, Any] = {
        "slug": slug,
        "title": fm.title,
        "version": str(fm.version) if fm.version is not None else "",
        "last_reviewed": str(fm.last_reviewed) if fm.last_reviewed is not None else "",
    }
    if fm.dream:
        dream_dict: Dict[str, Any] = {}
        if fm.dream.category:
            dream_dict["category"] = fm.dream.category.value
        if fm.dream.drug_name:
            dream_dict["drug_name"] = fm.dream.drug_name
        if dream_dict:
            drug_data["dream"] = dream_dict

    protocols_list = []
    for p in fm.protocols or []:
        p_dict: Dict[str, Any] = {
            "id": p.id,
            "label": p.label,
            "test_type": p.test_type.value,
        }
        if p.presentation is not None:
            p_dict["presentation"] = p.presentation
        if p.diluent is not None:
            p_dict["diluent"] = p.diluent
        if p.spt is not None:
            spt_dict: Dict[str, Any] = {}
            if p.spt.dilution is not None:
                spt_dict["dilution"] = p.spt.dilution
            if p.spt.concentration is not None:
                spt_dict["concentration"] = p.spt.concentration
            if p.spt.positive_control is not None:
                spt_dict["positive_control"] = p.spt.positive_control
            if p.spt.negative_control is not None:
                spt_dict["negative_control"] = p.spt.negative_control
            p_dict["spt"] = spt_dict
        if p.idt is not None:
            idt_list = []
            for step in p.idt:
                idt_list.append({
                    "dilution": step.dilution,
                    "concentration": step.concentration,
                    "preparation": step.preparation or "",
                })
            p_dict["idt"] = idt_list
        if p.challenge is not None:
            c_dict: Dict[str, Any] = {}
            if p.challenge.interval is not None:
                c_dict["interval"] = p.challenge.interval
            steps_list = []
            for step in p.challenge.steps:
                s_item: Dict[str, Any] = {"dose": step.dose}
                if step.volume is not None:
                    s_item["volume"] = step.volume
                if step.interval is not None:
                    s_item["interval"] = step.interval
                if step.cumulative is not None:
                    s_item["cumulative"] = step.cumulative
                steps_list.append(s_item)
            c_dict["steps"] = steps_list
            p_dict["challenge"] = c_dict

        p_dict["under_review"] = p.under_review
        p_dict["review_note"] = p.review_note or ""
        p_dict["needs_pharmacy_verification"] = p.needs_pharmacy_verification
        protocols_list.append(p_dict)

    drug_data["protocols"] = protocols_list
    return drug_data


def serialize_cross_reactivity(cr: CrossReactivityFrontmatter) -> Dict[str, Any]:
    """Serialize a validated CrossReactivityFrontmatter into a dictionary with stable keys."""
    return {
        "version": str(cr.version) if cr.version is not None else "1.0",
        "last_reviewed": str(cr.last_reviewed) if cr.last_reviewed is not None else "",
        "reviewed_by": str(cr.reviewed_by) if cr.reviewed_by is not None else "",
        "under_review": cr.under_review,
        "provenance": cr.provenance,
        "items": [
            {
                "category": item.category,
                "info": item.info,
                "alternatives": item.alternatives,
            }
            for item in cr.items
        ],
    }


def load_cross_reactivity(repo_root: Path) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """Load and validate docs/reference/cross-reactivity.md frontmatter."""
    cr_file = repo_root / "docs" / "reference" / "cross-reactivity.md"
    if not cr_file.exists():
        return None, [f"ERROR: {cr_file.relative_to(repo_root)} does not exist."]

    raw_meta = parse_frontmatter(cr_file)
    if not raw_meta:
        return None, [f"ERROR in {cr_file.relative_to(repo_root)}: Missing or invalid YAML frontmatter."]

    try:
        cr_fm = CrossReactivityFrontmatter.model_validate(raw_meta)
        return serialize_cross_reactivity(cr_fm), []
    except ValidationError as val_err:
        errors = format_validation_error(cr_file.relative_to(repo_root), val_err)
        return None, errors
    except Exception as e:
        return None, [f"ERROR in {cr_file.relative_to(repo_root)}: {str(e)}"]


def export_protocols(repo_root: Path, check_mode: bool = False) -> int:
    drugs_dir = repo_root / "docs" / "drugs"
    output_file = repo_root / "docs" / "api" / "protocols.json"

    meta_defaults = load_meta_defaults(drugs_dir)
    meta_spt = meta_defaults.get("spt") if isinstance(meta_defaults.get("spt"), dict) else {}
    default_pos = meta_spt.get("positive_control") or meta_defaults.get("positive_control")
    default_neg = meta_spt.get("negative_control") or meta_defaults.get("negative_control")

    validation_errors = []
    drugs_data = []

    # Iterate deterministically over sorted markdown files
    for md_file in sorted(drugs_dir.glob("*.md")):
        slug = md_file.stem
        try:
            raw_meta = parse_frontmatter(md_file)
            if not raw_meta:
                continue

            # Skip silently if no protocols block
            if "protocols" not in raw_meta or not raw_meta.get("protocols"):
                continue

            # Apply defaults from .meta.yml if not explicitly defined
            if "reviewed_by" not in raw_meta and "reviewed_by" in meta_defaults:
                raw_meta["reviewed_by"] = meta_defaults["reviewed_by"]

            if isinstance(raw_meta.get("protocols"), list):
                for proto in raw_meta["protocols"]:
                    if isinstance(proto, dict) and "spt" in proto and isinstance(proto["spt"], dict):
                        if "positive_control" not in proto["spt"] and default_pos:
                            proto["spt"]["positive_control"] = default_pos
                        if "negative_control" not in proto["spt"] and default_neg:
                            proto["spt"]["negative_control"] = default_neg

            fm = DrugFrontmatter.model_validate(raw_meta)
            drug_dict = serialize_drug(slug, fm)
            drugs_data.append(drug_dict)
        except ValidationError as val_err:
            validation_errors.extend(format_validation_error(md_file.relative_to(repo_root), val_err))
        except Exception as e:
            validation_errors.append(f"ERROR in {md_file.relative_to(repo_root)}: {str(e)}")

    cr_data, cr_errors = load_cross_reactivity(repo_root)
    if cr_errors:
        validation_errors.extend(cr_errors)

    if validation_errors:
        print("\n".join(validation_errors), file=sys.stderr)
        return 1

    # Check existing file for timestamp/commit determinism
    existing_content = None
    existing_generated_at = None
    existing_commit = None
    if output_file.exists():
        try:
            existing_content = output_file.read_text(encoding="utf-8")
            existing_json = json.loads(existing_content)
            existing_generated_at = existing_json.get("generated_at")
            existing_commit = existing_json.get("source_commit")
        except Exception:
            pass

    # Check if data matches existing
    data_changed = True
    if existing_content and existing_json:
        if (
            existing_json.get("schema_version") == "1.1"
            and existing_json.get("drugs") == drugs_data
            and existing_json.get("cross_reactivity") == cr_data
        ):
            data_changed = False

    if data_changed or not existing_generated_at:
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        source_commit = get_source_commit(repo_root)
    else:
        generated_at = existing_generated_at
        source_commit = existing_commit or get_source_commit(repo_root)

    payload = {
        "schema_version": "1.1",
        "generated_at": generated_at,
        "source_commit": source_commit,
        "drugs": drugs_data,
        "cross_reactivity": cr_data,
    }

    new_json_str = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    if check_mode:
        if not output_file.exists():
            print(f"ERROR: {output_file.relative_to(repo_root)} does not exist. Run without --check to generate.", file=sys.stderr)
            return 1

        if existing_content != new_json_str:
            print(f"ERROR: {output_file.relative_to(repo_root)} is out of date vs frontmatter sources.", file=sys.stderr)
            diff = difflib.unified_diff(
                existing_content.splitlines(keepends=True),
                new_json_str.splitlines(keepends=True),
                fromfile="committed",
                tofile="generated",
            )
            sys.stderr.writelines(diff)
            return 1
        print(f"OK: {output_file.relative_to(repo_root)} is up to date ({len(drugs_data)} drugs, cross_reactivity included).")
        return 0

    # Ensure output directory exists and write file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(new_json_str, encoding="utf-8")
    print(f"Successfully exported {len(drugs_data)} drug protocol(s) and cross-reactivity reference to {output_file.relative_to(repo_root)}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Export SCRATCH drug protocols to JSON.")
    parser.add_argument("--check", action="store_true", help="Check if exported protocols.json is up to date.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    exit_code = export_protocols(repo_root, check_mode=args.check)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
