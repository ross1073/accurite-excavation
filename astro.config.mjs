import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import { rehypePhoneWrap } from './plugins/rehype-phone-wrap.mjs';

export default defineConfig({
  site: 'https://accuriteexcavation.com',
  integrations: [sitemap()],
  trailingSlash: 'never',
  markdown: {
    rehypePlugins: [rehypePhoneWrap],
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
