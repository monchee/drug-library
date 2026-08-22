import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import { visit } from 'unist-util-visit';
import { fromMarkdown } from 'mdast-util-from-markdown';
import { gfmFromMarkdown } from 'mdast-util-gfm';
import { gfm } from 'micromark-extension-gfm';
import { transformTreeAdmonitions } from './remark-mkdocs-admonitions';

export interface Protocol {
  id?: string;
  label?: string;
  test_type?: string;
  presentation?: string;
  diluent?: string;
  spt?: {
    dilution?: string;
    concentration?: string;
    positive_control?: string;
    negative_control?: string;
  };
  idt?: Array<{
    dilution?: string;
    concentration?: string;
    preparation?: string;
  }>;
  challenge?: {
    interval?: string;
    steps?: Array<{
      dose?: string;
      volume?: string;
      interval?: string;
      cumulative?: string;
    }>;
  };
  under_review?: boolean;
  review_note?: string;
  needs_pharmacy_verification?: boolean;
}

export function renderReviewBanner(protocols: Protocol[]): string {
  const underReviewProtocols = (protocols || []).filter(p => p && p.under_review);
  if (underReviewProtocols.length === 0) {
    return '';
  }

  const notes = underReviewProtocols
    .map(p => p.review_note)
    .filter(Boolean)
    .map(n => String(n).trim());
  const noteText = notes.length > 0 ? notes.join(' ').trim() : 'This protocol is currently under clinical review.';

  return (
    '!!! warning "Protocol under clinical review"\n' +
    `    ${noteText}\n\n` +
    '    See [Protocols for Review](../reference/protocols-for-review.md) for details.\n\n'
  );
}

export function renderOverviewTable(protocol: Protocol): string {
  const rows: string[] = [];
  if (protocol.presentation) {
    rows.push(`| Presentation | ${protocol.presentation} |`);
  }
  if (protocol.diluent) {
    rows.push(`| Diluent | ${protocol.diluent} |`);
  }

  if (rows.length === 0) {
    return '';
  }

  return '| Field | Detail |\n|---|---|\n' + rows.join('\n') + '\n';
}

export function renderSptTable(protocol: Protocol, pageMeta?: any): string {
  const spt = protocol.spt;
  if (!spt) {
    return '';
  }

  const dilution = String(spt.dilution ?? '').trim();
  const concentration = String(spt.concentration ?? '').trim();

  let testSolution = '';
  if (dilution && concentration) {
    if (dilution.includes(concentration)) {
      testSolution = dilution;
    } else {
      testSolution = `${dilution} (${concentration})`;
    }
  } else if (concentration) {
    testSolution = concentration;
  } else if (dilution) {
    testSolution = dilution;
  } else {
    return '';
  }

  const meta = pageMeta || {};
  const metaSpt = (meta.spt && typeof meta.spt === 'object') ? meta.spt : {};

  const posControl =
    spt.positive_control ||
    metaSpt.positive_control ||
    meta.positive_control ||
    '';
  const negControl =
    spt.negative_control ||
    metaSpt.negative_control ||
    meta.negative_control ||
    '';

  const rows = [
    '| Reagent | Concentration |',
    '|---|---|',
    `| Test solution | ${testSolution} |`,
  ];
  if (posControl) {
    rows.push(`| Positive control | ${posControl} |`);
  }
  if (negControl) {
    rows.push(`| Negative control | ${negControl} |`);
  }

  return rows.join('\n') + '\n';
}

export function renderIdtTable(protocol: Protocol): string {
  const idt = protocol.idt;
  if (!idt || !Array.isArray(idt) || idt.length === 0) {
    return '';
  }

  const lines = [
    '| Step | Dilution | Concentration | Preparation |',
    '|---|---|---|---|',
  ];
  for (let idx = 0; idx < idt.length; idx++) {
    const step = idt[idx] || {};
    const dilution = String(step.dilution ?? '');
    const concentration = String(step.concentration ?? '');
    const prep = String(step.preparation ?? '');
    lines.push(`| ${idx + 1} | ${dilution} | ${concentration} | ${prep} |`);
  }

  return lines.join('\n') + '\n';
}

export function renderChallengeTable(protocol: Protocol): string {
  const challenge = protocol.challenge;
  if (!challenge) {
    return '';
  }

  const steps = challenge.steps;
  if (!steps || !Array.isArray(steps) || steps.length === 0) {
    return '';
  }

  const defaultInterval = challenge.interval || '';

  const hasVolume = steps.some(s => Boolean(s && s.volume));
  const hasCumulative = steps.some(s => Boolean(s && s.cumulative));
  const hasInterval = steps.some(s => Boolean(s && (s.interval || defaultInterval)));

  let headers: string[];
  if (hasVolume && hasCumulative && hasInterval) {
    headers = ['Step', 'Dose', 'Volume', 'Interval', 'Cumulative Dose'];
  } else if (hasVolume && hasCumulative) {
    headers = ['Step', 'Dose', 'Volume', 'Cumulative Dose'];
  } else if (hasVolume && hasInterval) {
    headers = ['Step', 'Dose', 'Volume', 'Interval'];
  } else if (hasInterval) {
    headers = ['Step', 'Dose', 'Interval'];
  } else if (hasCumulative) {
    headers = ['Step', 'Dose', 'Cumulative Dose'];
  } else {
    headers = ['Step', 'Dose'];
  }

  const headerLine = '| ' + headers.join(' | ') + ' |';
  const sepLine = '| ' + headers.map(() => '---').join(' | ') + ' |';
  const lines = [headerLine, sepLine];

  for (let idx = 0; idx < steps.length; idx++) {
    const step = steps[idx] || {};
    const row = [String(idx + 1), String(step.dose ?? '')];
    if (headers.includes('Volume')) {
      row.push(String(step.volume ?? ''));
    }
    if (headers.includes('Interval')) {
      row.push(String(step.interval || defaultInterval || ''));
    }
    if (headers.includes('Cumulative Dose')) {
      row.push(String(step.cumulative ?? ''));
    }
    lines.push('| ' + row.join(' | ') + ' |');
  }

  return lines.join('\n') + '\n';
}

export function renderCrossReactivity(meta: any): string {
  const items = meta?.items || [];
  if (!items || !Array.isArray(items) || items.length === 0) {
    return '';
  }

  const blocks: string[] = [];

  if (meta.under_review) {
    const provenance = String(meta.provenance ?? '').trim();
    const warningText = provenance || 'This reference is currently under review and awaits formal clinical sign-off.';
    blocks.push(
      '!!! warning "Clinical review pending"\n' +
      `    ${warningText}\n`
    );
  }

  const lines = [
    '| Category | Clinical considerations | Alternatives |',
    '|---|---|---|',
  ];
  for (const item of items) {
    const cat = String(item.category ?? '').replace(/\|/g, '\\|');
    let info = String(item.info ?? '').replace(/\|/g, '\\|');
    let alts = String(item.alternatives ?? '').replace(/\|/g, '\\|');
    info = info.replace(/</g, '&lt;');
    alts = alts.replace(/</g, '&lt;');
    lines.push(`| **${cat}** | ${info} | ${alts} |`);
  }

  blocks.push(lines.join('\n'));
  return blocks.join('\n\n') + '\n';
}

function replaceSmartSymbols(text: string): string {
  return text
    .replace(/(?<!\d)1\/2(?!\d)/g, '½')
    .replace(/(?<!\d)1\/4(?!\d)/g, '¼')
    .replace(/(?<!\d)3\/4(?!\d)/g, '¾')
    .replace(/\(c\)/gi, '©')
    .replace(/\(r\)/gi, '®')
    .replace(/\(tm\)/gi, '™')
    .replace(/\+\/-/g, '±')
    .replace(/=\/=/g, '≠')
    .replace(/-->/g, '→')
    .replace(/<--/g, '←')
    .replace(/<-->/g, '↔');
}

const MARKER_PATTERN = /<!--\s*scratch:([a-z-]+)(?::([a-z0-9_-]+))?\s*-->/g;

export function remarkRenderProtocols() {
  return (tree: any, file: any) => {
    let meta = file.data?.astro?.frontmatter;
    const filePath = file.path || (file.history && file.history[0]);
    if (!meta && filePath && fs.existsSync(filePath)) {
      try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        if (fileContent.startsWith('---')) {
          const parts = fileContent.split('---', 3);
          meta = yaml.load(parts[1]) || {};
        }
      } catch (e) {}
    }
    meta = meta || {};

    let dirMeta: any = {};
    if (filePath) {
      const dir = path.dirname(filePath);
      const metaPath = path.join(dir, '.meta.yml');
      if (fs.existsSync(metaPath)) {
        try {
          dirMeta = yaml.load(fs.readFileSync(metaPath, 'utf8')) || {};
        } catch (e) {}
      }
    }
    const mergedMeta = { ...dirMeta, ...meta };
    const protocols = mergedMeta.protocols || [];

    function getProtocol(protoId?: string): Protocol | null {
      if (!protocols || !Array.isArray(protocols) || protocols.length === 0) {
        return null;
      }
      if (protoId) {
        for (const p of protocols) {
          if (p && typeof p === 'object' && p.id === protoId) {
            return p;
          }
        }
        return null;
      }
      return (typeof protocols[0] === 'object' && protocols[0] !== null) ? protocols[0] : null;
    }

    function replaceMarkerString(marker: string, protoId?: string): string {
      if (marker === 'cross-reactivity') {
        return renderCrossReactivity(mergedMeta);
      }
      if (marker === 'review-banner') {
        return renderReviewBanner(protocols);
      }
      const proto = getProtocol(protoId);
      if (!proto) {
        return '';
      }
      if (marker === 'overview') {
        return renderOverviewTable(proto);
      } else if (marker === 'spt') {
        return renderSptTable(proto, mergedMeta);
      } else if (marker === 'idt') {
        return renderIdtTable(proto);
      } else if (marker === 'challenge') {
        return renderChallengeTable(proto);
      }
      return '';
    }

    // First, expand scratch markers
    visit(tree, (node: any, index: number | undefined, parent: any) => {
      if (node.type === 'html' && typeof node.value === 'string' && node.value.includes('scratch:')) {
        const matches = [...node.value.matchAll(MARKER_PATTERN)];
        if (matches.length > 0 && parent && typeof index === 'number') {
          const replacementMd = node.value.replace(MARKER_PATTERN, (_fullMatch: string, marker: string, protoId?: string) => {
            return replaceMarkerString(marker.trim(), protoId);
          });

          if (replacementMd.trim() === '') {
            parent.children.splice(index, 1);
            return index;
          } else {
            const parsed = fromMarkdown(replacementMd, {
              extensions: [gfm()],
              mdastExtensions: [gfmFromMarkdown()],
            });
            transformTreeAdmonitions(parsed, replacementMd);
            parent.children.splice(index, 1, ...parsed.children);
            return index + parsed.children.length;
          }
        }
      }
    });

    // Second, convert smartsymbols in text nodes (matching pymdownx.smartsymbols)
    visit(tree, (node: any) => {
      if (node.type === 'text' && typeof node.value === 'string') {
        node.value = replaceSmartSymbols(node.value);
      }
    });
  };
}

export default remarkRenderProtocols;
