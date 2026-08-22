import { visit } from 'unist-util-visit';

/**
 * MkDocs rewrites relative links ending in `.md` into clean page URLs at
 * build time; Starlight leaves them untouched. Every cross-page link
 * inherited from the MkDocs source therefore shipped pointing at raw
 * `.md` paths that 404 in production (13 built pages at cutover).
 *
 * Rewrites internal hrefs to route URLs:
 *   drugs/amoxicillin.md          -> drugs/amoxicillin
 *   ../reference/changelog.md     -> ../reference/changelog
 *   ../index.md                   -> ../   (directory index pages)
 *
 * External URLs, protocol-relative URLs, and same-page anchors are left
 * untouched. Only inline markdown `link` nodes are visited — the sources
 * carry no `.md` image or reference-style links.
 */
export const remarkMkdocsLinks = () => (tree: unknown) => {
  visit(tree as never, 'link', (node: { url: string }) => {
    const url = node.url;
    if (typeof url !== 'string' || url === '') return;
    // Skip external, protocol-relative, scheme'd (mailto:, tel:) and anchor-only URLs
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.startsWith('//') || url.startsWith('#')) {
      return;
    }
    if (!/\.md(?=$|#)/i.test(url)) return;

    let next = url.replace(/\.md(?=$|#)/i, '');
    // Directory index pages resolve to their folder, never to a literal /index path
    next = next.replace(/(^|\/)index$/i, '$1');
    if (next === '') next = '.';
    node.url = next;
  });
};
