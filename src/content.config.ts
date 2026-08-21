import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: glob({ pattern: 'drugs/*.md', base: './docs' }),
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
