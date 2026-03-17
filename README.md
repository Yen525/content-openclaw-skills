# wechat-xiaohongshu-converter

> OpenClaw Skill - 将公众号文章自动转换为小红书格式，并通过 Google Gemini API 自动生成配图

## 📋 功能

- ✅ 公众号长文自动拆分为多篇小红书笔记
- ✅ 豆包 2.0 将正式文风转换为小红书口语化风格
- ✅ 支持两种语气可配置：`casual` 日常可爱 / `professional` 专业严谨老师分享
- ✅ Google Gemini (`gemini-3.1-flash-image-preview` / `Nano Banana 2`) 自动根据标题生成小红书封面图
- ✅ 可配置：每篇字数、默认 hashtags、配图风格
- ✅ 输出：Markdown 文案 + PNG 配图 + JSON 汇总，直接可用

## 🔧 依赖

- Python 3.8+
- `requests` 库
- OpenClaw (可选，用于 skill 自动调用)
- 豆包 API key (火山引擎 - 文字改写)
- Google Gemini API key (图片生成)

## 🚀 安装

### 作为 OpenClaw Skill 安装

```bash
# 克隆到 OpenClaw skills 目录
cd ~/AppData/Roaming/npm/node_modules/openclaw/skills
git clone https://github.com/Yen525/content-openclaw-skills
```

### 独立使用

```bash
git clone https://github.com/Yen525/content-openclaw-skills
cd content-openclaw-skills
pip install requests
```

### npm 安装

```bash
npm install wechat-xiaohongshu-converter
```

## ⚙️ 配置

编辑 `scripts/config.json`：

```json
{
  "xiaohongshu": {
    "max_words_per_post": 500,
    "default_hashtags": ["交易复盘", "K线分析", "交易心得", "投资感悟"],
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

### 输入
一篇公众号文章：https://mp.weixin.qq.com/s/WVMq8PiFmcKR37IIHK3RXQ

### 输出（两种风格）

#### 1️⃣ 日常口语化风格 (`style: casual`)

```markdown
做交易的宝子们🙋‍♀️
你们开仓前，是不是最先盯住那根突然转强/转弱的K线，忍不住就急着进场了？🤔

今天来唠唠我最新的实操感悟👇

看完小级别信号后
我一定会再拉去看30分钟的结构位置✍️

这次3F反弹受阻转弱
单看小级别好像完全没问题对不对？
但我一看30分钟K线
发现多空消耗已经特别大了

就算多头急着平仓，行情向下脉冲
也得等30分钟结构真的松动
日线层面的转弱才更容易延续呀💡

这就是为什么很多位置只能看，不能急着做：
结构没破，价格分分钟就打回原来的震荡区间
白白亏手续费送钱！🤯

之前行情已经摸到30分钟震荡的结构边界
还做过一次破边界的尝试
这时候小级别再跌破左侧低点
才是真的顺着大结构完成转弱

今天收盘后看结果：
30f级别依然还在单K震荡里，没有实质性跌破结构
忍住没进场，直接躲过一次无效开仓✅

当然，如果之后真的顺势跌破，我也会错过这波机会
这就是交易里的舍得呀～

💬免责声明：仅为个人交易日志记录，不构成任何投资建议，若能给你带来启发，欢迎一起交流进步✨

#交易心得 #技术分析 #交易日志 #炒股经验 #短线交易
```

#### 2️⃣ 专业严谨老师风格 (`style: professional`)

```markdown
# 做交易时，你最先盯住的，是不是那一根突然转强或转弱的K线？📊

今天分享我的实盘分析逻辑，全是干货👇

先来看30分钟的结构在什么位置

从定式形态上来说
3F反弹受阻转弱，看起来好像没什么问题

但此时30分钟K线的多空力量消耗非常大
如果多头迫不及待平仓，足够弱势的情况下，价格确实会迅速向下脉冲

只有30分钟结构松动，日线层面的转弱才更容易延续
这就是为什么有些位置只能看，不能急着做
结构没有破，价格就还可能回到原来的震荡里。

为什么要等结构确认？
前一波价格已经站在30分钟震荡结构的边界，还出现过打破边界的动作
说明市场已经不是单纯在区间中部震荡了
这时候小级别再跌破左侧低点，才更像是顺着大结构完成一次转弱。

今日收盘后复盘：
30F级别依然在单K震荡中，没有出现实质性结构跌破，刚好避开一次无效进场✅
当然如果后续直接顺势跌破，也可能错过这段下跌机会
这就是交易的舍得，有舍才有得。

*免责声明：仅为个人交易日志记录，不构成任何投资建议。若能让您悟到些许交易技巧，欢迎关注共同进步！*

#交易分析 #K线技术分析 #交易心得 #实盘复盘 #交易认知
```

### 🖼️ 配图
自动生成一张小红书 3:4 封面图，保存在输出目录中

## 📝 说明

- 公众号文章提取需要自行处理，或者配合 `bb-browser` 抓取
- API key 由用户自行配置，请妥善保管，不要提交到代码仓库
- 默认配图风格为小红书极简现代风，可在 `config.json` 中修改

## 📄 License

MIT
