# article2ticktick

[English](#english) | [中文](#chinese)

---

<a id="english"></a>

A Claude Skill that converts technical newsletter articles (batch or single) into [TickTick](https://ticktick.com/) todos with automatic categorization and tagging.

<p align="center">
  <img width="800" alt="功能截图" src="https://github.com/user-attachments/assets/9dbcd7e9-b3e5-443c-a86f-efa386143390">
  <br>
  <em>Effect after adding to TickTick</em>
</p>

<p align="center">
  <img width="800" alt="效果演示" src="https://github.com/user-attachments/assets/e699bd9c-d267-4afd-b712-fb497ec0a50a">
  <br>
  <em>Batch add to-dos to TickTick</em>
</p>

## Features

- **Branch A: Batch Newsletter** — Paste an entire newsletter issue (Fatbobman's Swift Weekly, iOS Weekly, etc.), AI auto-categorizes and batch-adds to TickTick
- **Branch B: Single Article** — Share any article URL, AI infers category, generates a recommendation, and adds it to TickTick in one click

## Installation

> Requires [Claude Code](https://code.claude.com) with `/plugin` command support.

In Claude Code, run:

```
/plugin marketplace add balabalabalading/article2ticktick
/plugin install article2ticktick@article2ticktick
```

Update to the latest version:

```
/plugin marketplace update article2ticktick
```

## Usage

### Create Lists in TickTick

TickTick does not support creating lists via URL scheme. Please manually create the required lists in TickTick first — otherwise all todos will fall into the Inbox.

### Trigger the Skill

After installation, describe your needs directly to Claude:

- `Help me add this newsletter to TickTick` → triggers Branch A
- `Add this article to TickTick: [URL]` → triggers Branch B

The Skill guides you through the full workflow: organize → preview (dry-run) → confirm → execute.

## Local Testing

After cloning the repo, test with a local path in Claude Code:

```
/plugin marketplace add ./path/to/article2ticktick
/plugin install article2ticktick@article2ticktick
```

Validate marketplace config:

```
/plugin validate .
```

## Classification System

Level-2 categories map to TickTick list names; Level-3 categories map to tags.

The Skill constrains AI to use predefined Level-2 categories (matching fixed TickTick lists), while Level-3 categories are flexible. Since the newsletters I follow focus on the Swift ecosystem, the list names reflect that. You can modify the categories in `SKILL.md` to fit your own technical focus — just make sure Level-2 names exactly match your TickTick lists.

| Level-2 Category (TickTick list) | Common Level-3 Categories (tags) |
|---|---|
| SwiftUI | Basic components & API, Layout & animation, State management & observation, Navigation & interaction, System integration, Performance & debugging, App architecture |
| Swift 语言 | Concurrency & async, Language features & internals, Cross-platform & embedded |
| 数据与持久化 | SwiftData, CloudKit & data sync, Database |
| iOS 与 macOS 工程实践 | System capabilities & platform integration, App Store & publishing, Resource management, App architecture |
| 开发工具与工作流 | Package managers & dependencies, Xcode & project setup, Testing & debugging, CLI & server-side |
| AI 辅助开发 | Agent coding practices, Tools & configuration, On-device AI |
| 行业思考与视野 | Hardware products |

## Repository Structure

```
article2ticktick/
├── .claude-plugin/
│   └── marketplace.json           # Claude Code Marketplace config
├── skills/
│   └── article2ticktick/
│       ├── SKILL.md               # Skill instruction file
│       └── scripts/
│           └── add_articles.py    # Main script (batch + single)
└── README.md
```

## Standalone Script Usage

The script can also run independently without Claude:

```bash
# Batch mode
python3 skills/article2ticktick/scripts/add_articles.py \
  --input my_weekly.md --dry-run

# Single article mode
python3 skills/article2ticktick/scripts/add_articles.py \
  --task \
  --title "[Article Title](https://example.com)" \
  --list "SwiftUI" \
  --tags "State management & observation" \
  --desc "A brief intro of the article..."
```

## License

[MIT](LICENSE)

---

<a id="chinese"></a>

将技术周报文章（批量或单篇）转换为 [滴答清单](https://dida365.com/) 待办事项的 Claude Skill，支持自动分类和标签。

<p align="center">
  <img width="800" alt="功能截图" src="https://github.com/user-attachments/assets/9dbcd7e9-b3e5-443c-a86f-efa386143390">
  <br>
  <em>添加到滴答清单后的效果</em>
</p>

<p align="center">
  <img width="800" alt="效果演示" src="https://github.com/user-attachments/assets/e699bd9c-d267-4afd-b712-fb497ec0a50a">
  <br>
  <em>批量添加待办至滴答清单</em>
</p>

[English](#english) | **中文**

## 功能

- **分支 A：批量周报** — 粘贴一整期周报（肘子 Swift 周刊、老司机 iOS 周报等），AI 自动整理分类，批量添加到[滴答清单](https://dida365.com/)
- **分支 B：单篇文章** — 分享任意文章 URL，AI 推断分类、生成推荐语，一键添加到[滴答清单](https://dida365.com/)

## 安装

> 需要 [Claude Code](https://code.claude.com)（版本支持 `/plugin` 命令）。

在 Claude Code 中运行：

```
/plugin marketplace add balabalabalading/article2ticktick
/plugin install article2ticktick@article2ticktick
```

更新到最新版本：

```
/plugin marketplace update article2ticktick
```

## 使用

### 在滴答清单创建列表

由于[滴答清单](https://dida365.com/)不支持通过 Scheme URL 来创建列表，请先在滴答清单中手动创建好列表，否则待办都会创建至收集箱中。

### 触发 Skill

安装后，直接向 Claude 描述你的需求：

- `帮我把这期周报添加到滴答清单` → 触发分支 A
- `把这篇文章添加到滴答清单：[URL]` → 触发分支 B

Skill 会引导你完成整理、预览（dry-run）、确认、执行全流程。

## 本地测试安装

克隆仓库后，可在 Claude Code 中用本地路径测试：

```
/plugin marketplace add ./path/to/article2ticktick
/plugin install article2ticktick@article2ticktick
```

验证 marketplace 配置：

```
/plugin validate .
```

## 分类体系

二级分类对应[滴答清单](https://dida365.com/)列表名，三级分类对应标签。

在 Skill 中，我约束 AI 必须使用预设的二级分类，因为对应滴答清单中的列表是固定的；三级分类则比较灵活，可以根据文章内容自由添加标签。

由于我订阅的周报偏向 Swift 生态，因此列表名也都与之相关。你可以在 SKILL.md 文档中修改这些分类来适配你关注的技术领域，但要确保二级分类与滴答清单中的列表完全一致。

| 二级分类（滴答清单列表名） | 常见三级分类（标签） |
|---|---|
| SwiftUI | 基础组件与 API、布局视觉与动画、状态管理与观察、导航与交互、系统集成与实战、性能与调试、应用架构 |
| Swift 语言 | 并发与异步、语言特性与底层原理、跨平台与嵌入式 |
| 数据与持久化 | SwiftData、CloudKit 与数据同步、数据库 |
| iOS 与 macOS 工程实践 | 系统能力与平台集成、App Store 与发布、资源管理、应用架构 |
| 开发工具与工作流 | 包管理器与依赖、Xcode 与项目工程、测试与调试、命令行与服务端 |
| AI 辅助开发 | Agent 编码实践、工具与配置、端侧 AI |
| 行业思考与视野 | 硬件产品 |

## 仓库结构

```
article2ticktick/
├── .claude-plugin/
│   └── marketplace.json           # Claude Code Marketplace 配置
├── skills/
│   └── article2ticktick/
│       ├── SKILL.md               # Skill 指令文件
│       └── scripts/
│           └── add_articles.py    # 主脚本（批量 + 单篇）
└── README.md
```

## 脚本直接使用

脚本也可以脱离 Claude 独立运行：

```bash
# 批量模式
python3 skills/article2ticktick/scripts/add_articles.py \
  --input my_weekly.md --dry-run

# 单篇模式
python3 skills/article2ticktick/scripts/add_articles.py \
  --task \
  --title "[文章标题](https://example.com)" \
  --list "SwiftUI" \
  --tags "状态管理与观察" \
  --desc "这篇文章介绍了..."
```

## License

[MIT](LICENSE)
