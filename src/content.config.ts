import fs from 'node:fs';
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const titleOverrides: Record<string, string> = {
  index: 'Home',
  testing: 'Testing',
  'reference/anaphylaxis': 'Anaphylaxis Management',
  'reference/changelog': 'Changelog',
  'reference/mixing-guide': 'Mixing & Dilution Guide',
};

function scratchDocsLoader() {
  const baseLoader = glob({ pattern: ['**/*.md', '!includes/**'], base: './docs' });
  return {
    name: 'scratch-docs-loader',
    load: async (context: any) => {
      const origParseData = context.parseData;
      const wrappedContext = {
        ...context,
        parseData: async (entry: any) => {
          let title = entry.data?.title;
          if (!title) {
            if (titleOverrides[entry.id]) {
              title = titleOverrides[entry.id];
            } else if (entry.filePath) {
              try {
                const raw = fs.readFileSync(entry.filePath, 'utf-8');
                const match = raw.match(/^#\s+(.+)$/m);
                if (match) {
                  title = match[1].trim();
                }
              } catch {
                // ignore
              }
            }
            if (!title) {
              title = entry.id;
            }
          }
          return origParseData({
            ...entry,
            data: {
              ...entry.data,
              title,
            },
          });
        },
      };
      return baseLoader.load(wrappedContext);
    },
  };
}

export const collections = {
  docs: defineCollection({
    loader: scratchDocsLoader(),
    schema: docsSchema({
      extend: z.object({
        tags: z.array(z.string()).optional(),
        reviewed_by: z.string().optional(),
        last_reviewed: z.union([z.string(), z.date()]).optional(),
        version: z.union([z.number(), z.string()]).optional(),
        dream: z.record(z.string(), z.any()).optional(),
        protocols: z.array(z.record(z.string(), z.any())).optional(),
      }).passthrough(),
    }),
  }),
};
