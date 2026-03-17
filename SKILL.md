---
name: wechat-xiaohongshu-converter
description: Convert WeChat public account articles to Xiaohongshu (小红书) style posts + auto-generate cover/images via Google Gemini (Nano Banana 2 / Gemini 3.1 Flash Image API. Uses Doubao 2.0 for style rewriting. Use when: (1) need to split long public account articles into multiple Xiaohongshu posts, (2) auto-generate images from article structure, (3) multi-platform content distribution.
---

# WeChat to Xiaohongshu Converter

Converts long-form WeChat public account articles into multiple Xiaohongshu-style posts, and auto-generates images (cover, section images) based on article structure using Google Gemini (Nano Banana 2 / Gemini 3.1 Flash Image API. Uses Doubao 2.0 rewrites formal content to casual Xiaohongshu style.

## Workflow

1. **Input**: WeChat public account article URL
2. **Extract content**: Get full article text and structure (headings, sections) using feishu-fetch-doc
3. **Split into posts**: Split article into multiple Xiaohongshu-sized chunks (1 per post)
4. **Rewrite style**: Doubao 2.0 converts formal public account language to casual Xiaohongshu style (add emojis, line breaks, hashtags)
5. **Generate prompts**: For each post / main section, generate image prompt for Gemini
6. **Call API**: Generate images via Gemini API
7. **Output**: Final Xiaohongshu posts + image prompts + generated image files

## Configuration

- Set `GOOGLE_API_KEY` environment variable for Gemini image generation
- Set `DOUBAO_API_KEY` environment variable for Doubao 0
- Configure `config.json` for output format, number of posts, image sizes

## Gemini Image Models Supported

- `gemini-3-nano-banana-001 (Nano Banana 2)
- `gemini-3.1-flash-image-preview (Gemini 3.1 Flash Image)

## Examples

Input: 1 long public account article (2000+ words) about AI industry trends
Output:
- 3-4 Xiaohongshu posts, each 300-500 words
- 1 cover image + 1-2 section images
- Ready-to-copy text + image files for posting
