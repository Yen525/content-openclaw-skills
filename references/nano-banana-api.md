# Gemini (Nano Banana 2 / Gemini 3.1 Flash Image) API Reference

## Supported Models

- `gemini-3-nano-banana-001` — Nano Banana 2 (original)
- `gemini-3.1-flash-image-preview` — Gemini 3.1 Flash Image (recommended for Xiaohongshu)

## Endpoint

```
https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=API_KEY
```

## Request Format

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "[your image prompt here]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["image", "text"],
    "temperature": 1.0,
    "topP": 0.95,
    "topK": 64
  }
}
```

## Authentication

Set API key in:
- Environment variable `GOOGLE_API_KEY`

## Doubao 2.0 API for Style Rewriting

- Set `DOUBAO_API_KEY` environment variable
- Endpoint: `https://aquasearch.ai.bytedance.net/api/v1/chat/completions` (OpenAI compatible)
- Model: `doubao-2.0`

## Prompt Engineering for Xiaohongshu

Good prompts for Xiaohongshu images:
- Style: "minimalist clean background, modern flat design, Xiaohongshu aesthetic"
- Add context: "cover image for tech sharing about [topic], vibrant colors"
- Aspect ratio: Generally 3:4 (vertical) works best for Xiaohongshu

## Example Prompt

Input section: "GTC 2026 黄仁勋展示 OpenClaw"

Generated prompt:
> "Xiaohongshu cover image for article section: 'GTC 2026 黄仁勋展示 OpenClaw'. 
> Content topic: 国产AI框架登上英伟达主场...
> Style: Xiaohongshu minimalist modern aesthetic, vibrant colors, vertical 3:4 composition.
> Professional social media cover, typography friendly, easy to read on mobile.
"
