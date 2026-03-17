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

#### 1️⃣ 日常口语化风格 (`style: casual`) - AI创业案例

```markdown
# 21岁小哥无团队月入50万🤯真正值得学的是他的做事逻辑！

刷到外网这个年轻人的操作，我直接拍大腿说太绝了👏

21岁的Ernesto，和合伙人一共两个人
运营11个B2C App，月收入约50万人民币😱
更狠的是：没融资！没大团队！
他们的「第三名成员」，居然是AI Agent叫Eddie

别人用AI都在想「怎么把事做更快」，本质还是用时间换钱
但他的思路完全不一样：「哪些事根本不需要我自己做？」

他说过一句话特别关键👇
「要让AI自动化，得先自己手动把系统跑通，先手动再AI，顺序不能反」

他看到竞品做十多个无脸号引流，月入2万刀，但是内容团队月薪就要3万，本质亏钱
他一看流程全是标准化重复工作，直接训练Eddie接管：找素材→写文案→做图→发内容全自动化🤖
找网红建联、客服回邮件、每天做数据报表这些耗时间的活，全交给Eddie，只有搞不定才需要他出马，这种情况还极少

拆解开他的模式其实超简单，一共五步：
1️⃣找有真实需求的领域
2️⃣观察成熟玩家怎么赚钱
3️⃣拆解对方的增长流程
4️⃣自己先手动跑一遍验证
5️⃣把重复环节全扔给AI自动化

原来普通人用AI只提了一倍效率，人家直接用AI把赚钱天花板拉高了不知道多少✨

#AI创业 #AI工具 #搞钱思路 #商业思维 #自媒体运营
```

#### 2️⃣ 专业严谨老师风格 (`style: professional`) - 交易复盘案例

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
