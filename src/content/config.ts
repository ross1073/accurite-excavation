import { defineCollection, z } from 'astro:content';

const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    keywords: z.object({
      primary: z.string(),
      secondary: z.array(z.string()),
    }),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
    relatedServices: z.array(z.string()).optional(),
    heroImage: z.string().optional(),
    galleryImages: z.array(z.string()).optional(),
  }),
});

const locations = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    city: z.string(),
    county: z.string(),
    metaTitle: z.string(),
    metaDescription: z.string(),
    localIntro: z.string(),
    permitInfo: z.string().optional(),
    soilInfo: z.string().optional(),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
    projects: z.array(z.object({
      name: z.string(),
      description: z.string(),
      images: z.array(z.string()).optional(),
    })).optional(),
    testimonials: z.array(z.string()).optional(),
    heroImage: z.string().optional(),
    landmarkImage: z.string().optional(),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().default('AccuRite Excavation'),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).optional(),
    relatedServices: z.array(z.string()).optional(),
    relatedLocations: z.array(z.string()).optional(),
  }),
});

export const collections = { services, locations, blog };
