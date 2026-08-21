// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  // scratch.pages.dev belongs to MIT Scratch, not this project — a Pages project only
  // gets its requested *.pages.dev name if it is free, and it was not.
  site: 'https://scratch.yuson.au',
  integrations: [
    starlight({
      title: 'SCRATCH',
      description: 'Skin & Challenge Reference for Allergy Testing Clinical Handbook — RPAH Clinical Immunology & Allergy',
      sidebar: [
        {
          label: 'Cephalosporins',
          items: [
            { label: 'Cefazolin', slug: 'drugs/cefazolin' },
          ],
        },
      ],
    }),
  ],
});
