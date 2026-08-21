// @ts-check
process.env.ASTRO_TELEMETRY_DISABLED = '1';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { remarkRenderProtocols } from './src/plugins/remark-render-protocols';
import { remarkMkdocsAdmonitions } from './src/plugins/remark-mkdocs-admonitions';

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
      sidebar: [
        {
          label: 'Cephalosporins',
          items: [
            { label: 'Cefazolin', slug: 'drugs/cefazolin' },
          ],
        },
      ],
    }),
    scratchProtocolsIntegration(),
  ],
});
