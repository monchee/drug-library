// @ts-check
process.env.ASTRO_TELEMETRY_DISABLED = '1';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { remarkRenderProtocols } from './src/plugins/remark-render-protocols';
import { remarkMkdocsAdmonitions } from './src/plugins/remark-mkdocs-admonitions';
import { remarkMkdocsLinks } from './src/plugins/remark-mkdocs-links';

function scratchProtocolsIntegration() {
  return {
    name: 'scratch-protocols-integration',
    hooks: {
      'astro:config:setup': ({ config, updateConfig }) => {
        updateConfig({
          markdown: {
            remarkPlugins: [
              ...(config.markdown.remarkPlugins || []),
              remarkRenderProtocols,
              remarkMkdocsAdmonitions,
              remarkMkdocsLinks,
            ],
          },
        });
      },
    },
  };
}

// https://astro.build/config
export default defineConfig({
  // scratch.pages.dev belongs to MIT Scratch, not this project — a Pages project only
  // gets its requested *.pages.dev name if it is free, and it was not.
  site: 'https://scratch.yuson.au',
  integrations: [
    starlight({
      title: 'SCRATCH',
      description: 'Skin & Challenge Reference for Allergy Testing Clinical Handbook — RPAH Clinical Immunology & Allergy',
      components: {
        SiteTitle: './src/components/SiteTitle.astro',
        Header: './src/components/Header.astro',
        Footer: './src/components/Footer.astro',
      },
      customCss: [
        './src/styles/custom.css',
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'robots',
            content: 'noindex, nofollow',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'preconnect',
            href: 'https://fonts.googleapis.com',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'preconnect',
            href: 'https://fonts.gstatic.com',
            crossorigin: '',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            href: 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400..700;1,400..700&family=Public+Sans:ital,wght@0,300..900;1,300..900&display=swap',
          },
        },
      ],
      sidebar: [
        { label: 'Home', link: '/' },
        {
          label: 'Drug Index',
          items: [
            { label: 'Drug Protocols', slug: 'drugs' },
            {
              label: 'Penicillins',
              items: [
                  { label: 'Amoxycillin Suspension', slug: 'drugs/amoxycillin-suspension' },
                  { label: 'Amoxycillin/Clavulanic Acid', slug: 'drugs/amoxycillin-clavulanic-acid' },
                { label: 'Amoxicillin', slug: 'drugs/amoxicillin' },
                { label: 'Ampicillin', slug: 'drugs/ampicillin' },
                { label: 'Augmentin (Amoxicillin/Clavulanate)', slug: 'drugs/augmentin' },
                { label: 'Benzylpenicillin', slug: 'drugs/benzylpenicillin' },
                { label: 'Flucloxacillin', slug: 'drugs/flucloxacillin' },
                { label: 'Penicillin Major (PPL)', slug: 'drugs/penicillin-major-ppl' },
                { label: 'Penicillin Minor (MD)', slug: 'drugs/penicillin-minor-md' },
                { label: 'Phenoxymethylpenicillin', slug: 'drugs/phenoxymethylpenicillin' },
                { label: 'Tazocin (Piperacillin/Tazobactam)', slug: 'drugs/tazocin' },
              ],
            },
            {
              label: 'Cephalosporins',
              items: [
                  { label: 'Cefuroxime Suspension', slug: 'drugs/cefuroxime-suspension' },
                { label: 'Cefazolin', slug: 'drugs/cefazolin' },
                { label: 'Cefepime', slug: 'drugs/cefepime' },
                { label: 'Cefotaxime', slug: 'drugs/cefotaxime' },
                { label: 'Ceftazidime', slug: 'drugs/ceftazidime' },
                { label: 'Ceftriaxone', slug: 'drugs/ceftriaxone' },
                { label: 'Cefuroxime', slug: 'drugs/cefuroxime' },
                { label: 'Cephalexin', slug: 'drugs/cephalexin' },
              ],
            },
            {
              label: 'Antibiotics — Other',
              items: [
                  { label: 'Trimethoprim', slug: 'drugs/trimethoprim' },
                { label: 'Azithromycin', slug: 'drugs/azithromycin' },
                { label: 'Bactrim (Trimethoprim/Sulfa)', slug: 'drugs/bactrim' },
                { label: 'Ciprofloxacin', slug: 'drugs/ciprofloxacin' },
                { label: 'Clindamycin', slug: 'drugs/clindamycin' },
                { label: 'Doxycycline', slug: 'drugs/doxycycline' },
                { label: 'Fluconazole', slug: 'drugs/fluconazole' },
                { label: 'Gentamicin', slug: 'drugs/gentamicin' },
                { label: 'Levofloxacin', slug: 'drugs/levofloxacin' },
                { label: 'Metronidazole', slug: 'drugs/metronidazole' },
                { label: 'Vancomycin', slug: 'drugs/vancomycin' },
              ],
            },
            {
              label: 'Antiemetics',
              items: [
                { label: 'Droperidol', slug: 'drugs/droperidol' },
                { label: 'Granisetron', slug: 'drugs/granisetron' },
                { label: 'Metoclopramide', slug: 'drugs/metoclopramide' },
                { label: 'Ondansetron', slug: 'drugs/ondansetron' },
              ],
            },
            {
              label: 'Anticoagulants',
              items: [
                { label: 'Dalteparin', slug: 'drugs/dalteparin' },
                { label: 'Enoxaparin', slug: 'drugs/enoxaparin' },
                { label: 'Heparin', slug: 'drugs/heparin' },
              ],
            },
            {
              label: 'Corticosteroids',
              items: [
                { label: 'Betamethasone', slug: 'drugs/betamethasone' },
                { label: 'Celestone Chronodose', slug: 'drugs/celestone-chronodose' },
                { label: 'Dexamethasone', slug: 'drugs/dexamethasone' },
                { label: 'Hydrocortisone', slug: 'drugs/hydrocortisone' },
                { label: 'Methylprednisolone', slug: 'drugs/methylprednisolone' },
                { label: 'Triamcinolone', slug: 'drugs/triamcinolone' },
              ],
            },
            {
              label: 'Hormonal Contraceptives',
              items: [
                { label: 'Cyproterone/Ethinylestradiol', slug: 'drugs/cyproterone-ethinylestradiol' },
                { label: 'Drospirenone/Ethinylestradiol', slug: 'drugs/drospirenone-ethinylestradiol' },
                { label: 'Ethinylestradiol/Levonorgestrel', slug: 'drugs/ethinylestradiol-levonorgestrel' },
                { label: 'Ethinylestradiol/Norethisterone', slug: 'drugs/ethinylestradiol-norethisterone' },
                { label: 'Levonorgestrel', slug: 'drugs/levonorgestrel' },
                { label: 'Medroxyprogesterone', slug: 'drugs/medroxyprogesterone' },
              ],
            },
            {
              label: 'Hypnotics & Sedatives',
              items: [
                { label: 'Ketamine', slug: 'drugs/ketamine' },
                { label: 'Midazolam', slug: 'drugs/midazolam' },
                { label: 'Propofol', slug: 'drugs/propofol' },
                { label: 'Thiopental', slug: 'drugs/thiopental' },
              ],
            },
            {
              label: 'Insulins',
              items: [
                { label: 'Actrapid', slug: 'drugs/actrapid' },
                { label: 'Humulin NPH', slug: 'drugs/humulin-nph' },
                { label: 'Humulin R', slug: 'drugs/humulin-r' },
                { label: 'Novorapid', slug: 'drugs/novorapid' },
                { label: 'Optisulin', slug: 'drugs/optisulin' },
                { label: 'Protaphane', slug: 'drugs/protaphane' },
              ],
            },
            {
              label: 'Local Anaesthetics',
              items: [
                { label: 'Bupivacaine', slug: 'drugs/bupivacaine' },
                { label: 'Lignocaine', slug: 'drugs/lignocaine' },
                { label: 'Mepivacaine', slug: 'drugs/mepivacaine' },
                { label: 'Ropivacaine', slug: 'drugs/ropivacaine' },
                { label: 'Xylocaine', slug: 'drugs/xylocaine' },
              ],
            },
            {
              label: 'Neuromuscular Blocking Agents',
              items: [
                { label: 'Cis-Atracurium', slug: 'drugs/cis-atracurium' },
                { label: 'Pancuronium', slug: 'drugs/pancuronium' },
                { label: 'Rocuronium', slug: 'drugs/rocuronium' },
                { label: 'Suxamethonium', slug: 'drugs/suxamethonium' },
                { label: 'Vecuronium', slug: 'drugs/vecuronium' },
              ],
            },
            {
              label: 'Neuromuscular Reversal Agents',
              items: [
                  { label: 'Sugammadex (+ Rocuronium)', slug: 'drugs/sugammadex-rocuronium' },
                { label: 'Glycopyrronium', slug: 'drugs/glycopyrronium' },
                { label: 'Neostigmine', slug: 'drugs/neostigmine' },
                { label: 'Protamine', slug: 'drugs/protamine' },
                { label: 'Sugammadex', slug: 'drugs/sugammadex' },
              ],
            },
            {
              label: 'NSAIDs & Analgesics',
              items: [
                  { label: 'Meloxicam', slug: 'drugs/meloxicam' },
                  { label: 'Voltaren (Diclofenac)', slug: 'drugs/voltaren-diclofenac' },
                { label: 'Aspirin', slug: 'drugs/aspirin' },
                { label: 'Paracetamol', slug: 'drugs/paracetamol' },
                { label: 'Parecoxib', slug: 'drugs/parecoxib' },
              ],
            },
            {
              label: 'Opioids',
              items: [
                { label: 'Alfentanil', slug: 'drugs/alfentanil' },
                { label: 'Fentanyl', slug: 'drugs/fentanyl' },
                { label: 'Morphine', slug: 'drugs/morphine' },
                { label: 'Oxycodone', slug: 'drugs/oxycodone' },
                { label: 'Remifentanil', slug: 'drugs/remifentanil' },
                { label: 'Tramadol', slug: 'drugs/tramadol' },
              ],
            },
            {
              label: 'Proton Pump Inhibitors',
              items: [
                { label: 'Esomeprazole', slug: 'drugs/esomeprazole' },
                { label: 'Lansoprazole', slug: 'drugs/lansoprazole' },
                { label: 'Omeprazole', slug: 'drugs/omeprazole' },
                { label: 'Pantoprazole', slug: 'drugs/pantoprazole' },
                { label: 'Rabeprazole', slug: 'drugs/rabeprazole' },
              ],
            },
            {
              label: 'Contrast Media',
              items: [
                { label: 'Omnipaque (Iohexol)', slug: 'drugs/omnipaque' },
                { label: 'Ultravist (Iopromide)', slug: 'drugs/ultravist' },
                { label: 'Urografin', slug: 'drugs/urografin' },
                { label: 'Visipaque (Iodixanol)', slug: 'drugs/visipaque' },
              ],
            },
            {
              label: 'Other',
              items: [
                { label: 'Chlorhexidine', slug: 'drugs/chlorhexidine' },
                { label: 'Latex', slug: 'drugs/latex' },
                { label: 'Metacresol', slug: 'drugs/metacresol' },
                { label: 'Patent Blue', slug: 'drugs/patent-blue' },
                { label: 'Povidone-Iodine', slug: 'drugs/povidone-iodine' },
                { label: 'Rosuvastatin', slug: 'drugs/rosuvastatin' },
                { label: 'Tranexamic Acid', slug: 'drugs/tranexamic-acid' },
              ],
            },
          ],
        },
        {
          label: 'Reference',
          items: [
            { label: 'Anaphylaxis Management', slug: 'reference/anaphylaxis' },
            { label: 'Cross-Reactivity Guidance', slug: 'reference/cross-reactivity' },
            { label: 'Mixing & Dilution Guide', slug: 'reference/mixing-guide' },
            { label: 'Protocols for Review', slug: 'reference/protocols-for-review' },
            { label: 'Tags', slug: 'reference/tags' },
            { label: 'Changelog', slug: 'reference/changelog' },
          ],
        },
        { label: 'Testing', slug: 'testing' },
      ],
    }),
    scratchProtocolsIntegration(),
  ],
});
