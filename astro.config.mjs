import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import { rehypePhoneWrap } from './plugins/rehype-phone-wrap.mjs';
import { readdirSync, readFileSync } from 'node:fs';

// Blog posts with `unlisted: true` in frontmatter are review pages (noindex, off the blog
// index). Keep them out of the sitemap too. Read from disk because the content collection
// API isn't available inside the config.
const blogDir = new URL('./src/content/blog/', import.meta.url);
const unlistedBlogUrls = new Set(
  readdirSync(blogDir)
    .filter((f) => f.endsWith('.md') && !f.startsWith('_'))
    .filter((f) => {
      const fm = readFileSync(new URL(f, blogDir), 'utf8').match(/^---\n([\s\S]*?)\n---/);
      return fm && /^unlisted:\s*true\s*$/m.test(fm[1]);
    })
    .map((f) => `https://accuriteexcavation.com/blog/${f.replace(/\.md$/, '')}`)
);

export default defineConfig({
  site: 'https://accuriteexcavation.com',
  integrations: [sitemap({ filter: (page) => !unlistedBlogUrls.has(page.replace(/\/$/, '')) })],
  trailingSlash: 'never',
  markdown: {
    rehypePlugins: [rehypePhoneWrap],
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
