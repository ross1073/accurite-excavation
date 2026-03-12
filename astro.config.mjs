import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://accuriteexcavation.com',
  integrations: [sitemap()],
  trailingSlash: 'never',
  vite: {
    plugins: [tailwindcss()],
  },
});
