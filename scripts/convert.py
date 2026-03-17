#!/usr/bin/env python3
"""
Convert WeChat public article to Xiaohongshu posts + auto generate images
Supports:
- Doubao 2.0 for style rewriting (formal → Xiaohongshu casual)
- Gemini 3.1 Flash Image / Nano Banana 2 for image generation
"""

import argparse
import json
import os
import re
import requests
import base64
from typing import List, Dict

# Gemini API endpoints
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

class WechatXiaohongshuConverter:
    def __init__(self, google_api_key=None, doubao_api_key=None, doubao_model=None, gemini_model="gemini-3.1-flash-image-preview"):
        self.google_api_key = google_api_key or os.environ.get('GOOGLE_API_KEY') or os.environ.get('NANO_BANANA_API_KEY')
        self.doubao_api_key = doubao_api_key or os.environ.get('DOUBAO_API_KEY')
        self.doubao_model = doubao_model or os.environ.get('DOUBAO_MODEL', 'Doubao-Seed-2.0-lite')
        self.gemini_model = gemini_model
        
        if not self.google_api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
    
    def extract_article_structure(self, content: str) -> List[Dict]:
        """Split article into sections based on headings"""
        lines = content.split('\n')
        sections = []
        current_section = {"title": "", "content": []}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect headings (simple heuristic: all caps or starting with # or numbered)
            if (line.startswith('#') or 
                line.isupper() or 
                re.match(r'^\d+\.?\s+', line) or
                len(line) < 50 and line.endswith('。')):
                # Save previous section
                if current_section["title"]:
                    sections.append({
                        "title": current_section["title"],
                        "content": '\n'.join(current_section["content"])
                    })
                current_section = {"title": line.lstrip('# ').strip(), "content": []}
            else:
                current_section["content"].append(line)
        
        # Add last section
        if current_section["title"] and current_section["content"]:
            sections.append({
                "title": current_section["title"],
                "content": '\n'.join(current_section["content"])
            })
        
        # If no sections found, treat whole article as one section
        if not sections:
            sections.append({
                "title": "Summary",
                "content": content
            })
        
        return sections
    
    def split_into_posts(self, sections: List[Dict], max_words_per_post=500) -> List[Dict]:
        """Split sections into multiple Xiaohongshu posts"""
        posts = []
        current_post = {"title": "", "sections": [], "word_count": 0}
        
        for section in sections:
            word_count = len(section["content"].split())
            if current_post["word_count"] + word_count > max_words_per_post and current_post["word_count"] > 0:
                # Start new post
                posts.append(current_post)
                current_post = {"title": "", "sections": [], "word_count": 0}
            
            if not current_post["title"]:
                current_post["title"] = section["title"]
            
            current_post["sections"].append(section)
            current_post["word_count"] += word_count
        
        if current_post["sections"]:
            posts.append(current_post)
        
        return posts
    
    def rewrite_to_xiaohongshu(self, post: Dict, config: Dict) -> str:
        """Use Doubao 2.0 to rewrite formal content to Xiaohongshu casual style"""
        if not self.doubao_api_key:
            # Fallback to basic template if no Doubao API key
            return self._basic_rewrite(post, config)
        
        full_content = "\n\n".join([s["content"] for s in post["sections"]])
        # Get style config
        style = config.get("xiaohongshu", {}).get("style", "casual")
        # style options: casual (日常可爱)/ professional (专业严谨老师分享)
        
        if style == "professional":
            prompt = f"""Rewrite the following article section into Xiaohongshu (小红书) format:

Title: {post['title']}

Content:
{full_content}

Requirements:
1. Use **Chinese** (中文), maintain a professional, rigorous tone like an experienced teacher sharing knowledge
2. Add a small number of appropriate emojis, don't overdo it
3. Keep paragraphs short, lots of line breaks, suitable for mobile reading
4. Keep the original key technical information and analysis logic completely intact
5. Length should be around 300-500 words
6. End with relevant Chinese hashtags
7. Focus on delivering value, don't use too much internet slang or overly cute language

Output only the final rewritten content in Chinese."""
        else:
            # casual style (default)
            prompt = f"""Rewrite the following article section into Xiaohongshu (小红书) style:

Title: {post['title']}

Content:
{full_content}

Requirements:
1. Use **Chinese** (中文), casual, friendly, conversational language like a Xiaohongshu creator
2. Add appropriate emojis throughout
3. Keep paragraphs short, lots of line breaks,适合手机阅读
4. Keep the original key information intact
5. Length should be around 300-500 words
6. End with relevant Chinese hashtags

Output only the final rewritten content in Chinese."""

        headers = {
            "Authorization": f"Bearer {self.doubao_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.doubao_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8
        }
        
        # Doubao endpoint may vary - use default openai-compatible endpoint
        endpoint = os.environ.get("DOUBAO_ENDPOINT", "https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions")
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        return data["choices"][0]["message"]["content"].strip()
    
    def _basic_rewrite(self, post: Dict, config: Dict) -> str:
        """Basic template-based rewriting when no LLM available"""
        content = f"# {post['title']}\n\n"
        
        for section in post["sections"]:
            content += f"{section['content']}\n\n"
        
        # Add hashtags
        default_tags = config.get("xiaohongshu", {}).get("default_hashtags", ["AI", "科技", "干货分享", "互联网"])
        for tag in default_tags:
            content += f"#{tag} "
        
        return content.strip()
    
    def generate_image_prompt(self, title: str, content: str, config: Dict) -> str:
        """Generate optimized image prompt for Gemini"""
        style = config.get("image_generation", {}).get("style", "Xiaohongshu minimalist modern aesthetic")
        ratio = config.get("image_generation", {}).get("aspect_ratio", "3:4")
        
        prompt = f"""Xiaohongshu cover image for article section: '{title}'. 
Content topic: {content[:100]}...
Style: {style}, vibrant colors, vertical {ratio} composition.
Professional social media cover, typography friendly, easy to read on mobile.
"""
        return prompt.strip()
    
    def generate_image(self, prompt: str) -> Dict:
        """Call Gemini API to generate image"""
        url = GEMINI_API_ENDPOINT.format(model=self.gemini_model) + f"?key={self.google_api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
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
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract image from response
        try:
            candidates = data.get('candidates', [])
            if not candidates:
                return {"error": "No candidates returned"}
            
            parts = candidates[0]['content']['parts']
            image_part = next((p for p in parts if 'inlineData' in p), None)
            
            if not image_part:
                return {"error": "No image in response", "full_response": data}
            
            return {
                "prompt": prompt,
                "image_base64": image_part['inlineData']['data'],
                "mime_type": image_part['inlineData'].get('mimeType', 'image/png')
            }
        except Exception as e:
            return {"error": f"Failed to parse response: {str(e)}", "full_response": data}
    
    def save_image(self, generated: Dict, output_path: str) -> str:
        """Save base64 image to file"""
        if 'image_base64' not in generated:
            raise ValueError("No image data found")
        
        image_data = base64.b64decode(generated['image_base64'])
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        return output_path
    
    def process_article(self, content: str, output_dir: str, config: Dict) -> Dict:
        """Process full article"""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Split into sections
        max_words = config.get("xiaohongshu", {}).get("max_words_per_post", 500)
        sections = self.extract_article_structure(content)
        
        # Split into posts
        posts = self.split_into_posts(sections, max_words)
        
        result = {
            "posts": [],
            "images": []
        }
        
        # Process each post
        for i, post in enumerate(posts):
            # Rewrite to Xiaohongshu style
            xhs_content = self.rewrite_to_xiaohongshu(post, config)
            
            # Generate image for this post
            generate_cover = config.get("image_generation", {}).get("generate_cover_per_post", True)
            if generate_cover:
                first_content = post['sections'][0]['content'] if post['sections'] else content
                prompt = self.generate_image_prompt(post['title'], first_content, config)
                generated = self.generate_image(prompt)
                
                if 'error' not in generated:
                    ext = 'png' if generated['mime_type'] == 'image/png' else 'jpg'
                    image_path = os.path.join(output_dir, f"post_{i+1}_cover.{ext}")
                    self.save_image(generated, image_path)
                    result["images"].append({
                        "post_index": i+1,
                        "prompt": prompt,
                        "path": image_path
                    })
                else:
                    result["images"].append({
                        "post_index": i+1,
                        "prompt": prompt,
                        "error": generated['error']
                    })
            
            # Save post content
            post_path = os.path.join(output_dir, f"post_{i+1}.md")
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(xhs_content)
            
            result["posts"].append({
                "index": i+1,
                "title": post['title'],
                "path": post_path,
                "word_count": post['word_count'],
                "content": xhs_content
            })
        
        # Save full result
        with open(os.path.join(output_dir, 'result.json'), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result

def main():
    parser = argparse.ArgumentParser(description='Convert WeChat article to Xiaohongshu posts')
    parser.add_argument('--input', help='Input text file', required=True)
    parser.add_argument('--output', help='Output directory', required=True)
    parser.add_argument('--max-words', type=int, default=500, help='Max words per post')
    parser.add_argument('--model', default='gemini-3.1-flash-image-preview', help='Gemini model for image generation')
    parser.add_argument('--doubao-model', default='Doubao-Seed-2.0-lite', help='Doubao model for text rewriting')
    args = parser.parse_args()
    
    # Read input
    if os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("Input file not found")
        exit(1)
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = json.load(open(config_path, 'r', encoding='utf-8')) if os.path.exists(config_path) else {}
    
    converter = WechatXiaohongshuConverter(gemini_model=args.model, doubao_model=args.doubao_model)
    result = converter.process_article(content, args.output, config)
    
    # For Windows encoding compatibility
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"\n✅ Conversion complete!")
    print(f"Generated {len(result['posts'])} posts")
    print(f"Generated {len([img for img in result['images'] if 'path' in img])} images")
    print(f"Output saved to: {args.output}")
    print("\nPosts:")
    for post in result["posts"]:
        print(f"  {post['index']}. {post['title']} -> {post['path']}")

if __name__ == "__main__":
    main()
