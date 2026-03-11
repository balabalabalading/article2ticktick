#!/usr/bin/env python3
"""
generate_ticktick_urls.py

批量解析技术周报文章汇总 markdown，生成 run_ticktick.sh 可执行脚本（备用方案）。

字段映射：
  title   : **[文章标题](链接)** → 去掉 **，保留 [文章标题](链接)
  content : 所有 - bullet 行 → 去掉 "- " 前缀、去掉 [[]]，逗号合并为单行
  list    : ## 二级标题
  tags    : ### 三级标题（无 H3 则不传此参数）

用法：
  python3 generate_ticktick_urls.py --input 某文件.md      # 指定输入文件
  python3 generate_ticktick_urls.py --input 某文件.md --output ./run.sh  # 指定输出路径
  python3 generate_ticktick_urls.py --input 某文件.md --dry-run           # 仅预览
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote


def strip_wikilinks(text: str) -> str:
    """去掉 [[...]] 双方括号，保留内部文本"""
    return re.sub(r'\[\[(.+?)\]\]', r'\1', text)


def parse_articles(md_path: Path) -> list[dict]:
    articles = []
    current_h2 = None
    current_h3 = None
    current_article = None

    def flush():
        nonlocal current_article
        if current_article and current_article.get('title'):
            articles.append(dict(current_article))
        current_article = None

    with open(md_path, encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.rstrip('\n')

            # H2 → list
            m = re.match(r'^## (.+)', line)
            if m:
                flush()
                current_h2 = m.group(1).strip()
                current_h3 = None
                continue

            # H3 → tags
            m = re.match(r'^### (.+)', line)
            if m:
                flush()
                current_h3 = m.group(1).strip()
                continue

            # 文章标题行：**[title](url)**
            m = re.match(r'^\*\*(\[.+?\]\(.+?\))\*\*\s*$', line)
            if m:
                flush()
                current_article = {
                    'title': m.group(1),
                    'content_parts': [],
                    'list': current_h2 or '',
                    'tags': current_h3,
                }
                continue

            # bullet 正文行
            if current_article is not None and line.startswith('- '):
                text = strip_wikilinks(line[2:].strip())
                current_article['content_parts'].append(text)

    flush()
    return articles


def build_url(article: dict) -> str:
    title = article['title']
    today = date.today().strftime('%Y-%m-%d')
    content = f"{today}，" + '，'.join(article['content_parts'])
    list_name = article['list']
    tags = article['tags']

    params = (
        f"title={quote(title, safe='')}"
        f"&content={quote(content, safe='')}"
        f"&list={quote(list_name, safe='')}"
    )
    if tags:
        params += f"&tags={quote(tags, safe='')}"
    return f"ticktick://x-callback-url/v1/add_task?{params}"


def main():
    parser = argparse.ArgumentParser(description='生成 TickTick URL Scheme 批量脚本')
    parser.add_argument('--input', type=Path, required=True,
                        help='输入 markdown 文件路径')
    parser.add_argument('--output', type=Path,
                        help='输出 .sh 文件路径（默认：输入文件同目录的 run_ticktick.sh）')
    parser.add_argument('--dry-run', action='store_true',
                        help='仅预览解析结果，不生成 .sh 文件')
    args = parser.parse_args()

    if not args.input.exists():
        print(f"错误：文件不存在：{args.input}", file=sys.stderr)
        sys.exit(1)

    articles = parse_articles(args.input)
    if not articles:
        print("未解析到任何文章，请检查输入文件格式", file=sys.stderr)
        sys.exit(1)

    urls = [build_url(a) for a in articles]
    print(f"共解析到 {len(urls)} 篇文章\n")

    if args.dry_run:
        for i, (a, url) in enumerate(zip(articles, urls), 1):
            content_preview = '，'.join(a['content_parts'])
            print(f"[{i:02d}] {a['title']}")
            print(f"      list : {a['list']}")
            print(f"      tags : {a['tags'] or '（无）'}")
            print(f"      content: {content_preview[:70]}{'...' if len(content_preview) > 70 else ''}")
            print(f"      url  : {url[:100]}...")
            print()
        return

    # 生成 run_ticktick.sh
    sh_path = args.output or args.input.parent / 'run_ticktick.sh'
    with open(sh_path, 'w', encoding='utf-8') as f:
        f.write('#!/bin/bash\n')
        f.write(f'# 自动生成，共 {len(urls)} 条任务\n')
        f.write('# 运行前请确保 TickTick 应用已启动并置于前台\n\n')
        f.write(f'TOTAL={len(urls)}\n')
        f.write('COUNT=0\n\n')
        for url in urls:
            safe_url = url.replace("'", "'\\''")
            f.write('COUNT=$((COUNT + 1))\n')
            f.write('echo "[$COUNT/$TOTAL] 正在添加..."\n')
            f.write(f"open '{safe_url}'\n")
            f.write('sleep 0.5\n\n')
        f.write('echo "✓ 全部添加完成"\n')

    sh_path.chmod(0o755)
    print(f"已生成：{sh_path}")
    print(f"执行方式：bash '{sh_path}'")


if __name__ == '__main__':
    main()
