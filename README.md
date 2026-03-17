# wechat-xiaohongshu-converter

> OpenClaw Skill - 将公众号文章自动转换为小红书格式，并通过 Gemini API 自动生成配图

## 📋 功能

- ✅ 公众号长文自动拆分为多篇小红书笔记
- ✅ 豆包 2.0 将正式文风转换为小红书口语化风格
- ✅ 支持两种语气：`casual` 日常可爱 / `professional` 专业严谨老师分享
- ✅ Google Gemini (`gemini-3.1-flash-image-preview` / `Nano Banana 2`) 自动根据标题生成小红书封面图
- ✅ 可配置：每篇字数、默认 hashtags、配图风格
- ✅ 输出：Markdown 文案 + PNG 配图 + JSON 汇总，直接可用

## 🔧 依赖

- Python 3.8+
- `requests` 库
- OpenClaw (可选，用于 skill 调用)
- 豆包 API key (火山引擎 - 文字改写)
- Google Gemini API key (图片生成)

## 🚀 安装

### 作为 OpenClaw Skill 安装

```bash
# 克隆到 OpenClaw skills 目录
cd ~/AppData/Roaming/npm/node_modules/openclaw/skills
git clone https://github.com/<your-username>/wechat-xiaohongshu-converter.git
```

### 独立使用

```bash
git clone https://github.com/<your-username>/wechat-xiaohongshu-converter.git
cd wechat-xiaohongshu-converter
pip install requests
```

## ⚙️ 配置

编辑 `scripts/config.json`：

```json
{
  "xiaohongshu": {
    "max_words_per_post": 500,
    "default_hashtags": ["交易", "投资", "复盘"],
    "include_hashtags": true,
    "style": "professional"  // "casual" 日常可爱 / "professional" 专业严谨
  },
  "image_generation": {
    "generate_cover_per_post": true,
    "style": "Xiaohongshu minimalist modern aesthetic",
    "aspect_ratio": "3:4"
  },
  "nano_banana": {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64
  }
}
```

### 环境变量设置

**必须设置以下环境变量**：

```bash
# 豆包 API (火山引擎 - OpenAI 兼容模式)
export DOUBAO_API_KEY="your-doubao-api-key"
export DOUBAO_MODEL="Doubao-Seed-2.0-lite"  # 模型名称
export DOUBAO_ENDPOINT="https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions"  # 端点

# Google Gemini API (图片生成)
export GOOGLE_API_KEY="your-google-api-key"
```

## 📖 使用

```bash
# 准备：把公众号文章保存为 txt 文件
python scripts/convert.py \
  --input article.txt \
  --output ./output \
  --max-words 500 \
  --model "gemini-3.1-flash-image-preview" \
  --doubao-model "Doubao-Seed-2.0-lite"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` | 是 | 输入文章 txt 文件路径 |
| `--output` | 是 | 输出目录 |
| `--max-words` | 否 | 每篇小红书最大字数 (默认 500) |
| `--model` | 否 | Gemini 模型名称 (默认 `gemini-3.1-flash-image-preview`) |
| `--doubao-model` | 否 | 豆包模型名称 (默认 `Doubao-Seed-2.0-lite`) |

## 📦 输出

输出目录结构：

```
output/
├── post_1.md          # 第一篇小红书文案
├── post_1_cover.png   # 第一篇封面图
├── post_2.md
├── post_2_cover.png
└── result.json        # 结果汇总
```

## ✨ 示例

输入：一篇 1000 字公众号交易复盘文章 → 输出：

1. 一篇拆分后的小红书文案（专业风格）：
```markdown
# 做交易时，你最先盯住的，是不是那一根突然转强或转弱的K线？🤔

今天分享我的实盘分析逻辑，全是干货👇

先看大结构：我们得先明确30分钟结构处在什么位置。

从定式形态来说，3F反弹受阻转弱，看起来好像没有问题。
但此时30F级别K线的多空消耗力度极大，如果多头迫不及待平仓，在足够弱势的情况下，价格也会迅速向下脉冲。

...

#交易复盘 #K线技术分析 #交易心得 #投资感悟
```

2. 一张 Gemini 生成的 3:4 小红书封面图

## 📝 说明

- 公众号文章提取需要自行处理，或者配合 `bb-browser` 抓取
- API key 由用户自行提供，请妥善保管，不要提交到代码仓库
- 默认配图风格为小红书极简现代风，可在 `config.json` 中修改

## 📄 License

MIT
