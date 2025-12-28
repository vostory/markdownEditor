#!/usr/bin/env python3
"""
微信公众号内容提取（极简版）
职责：获取 HTML，提取 js_content 和标题
AI 负责：样式分析、主题生成、写入配置
"""

import sys
import re
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("用法: python3 extract.py <微信文章URL>")
        sys.exit(1)

    url = sys.argv[1]

    print("📥 获取微信文章...")

    # 1. 获取 HTML
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    result = subprocess.run(
        ['curl', '-s', '-A', user_agent, url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0 or not result.stdout:
        print("❌ 获取失败")
        sys.exit(1)

    html = result.stdout
    print(f"✓ 获取成功 ({len(html):,} 字符)")

    # 2. 提取标题
    title_match = re.search(r'<h1[^>]*class="[^"]*rich_media_title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else "未知标题"
    print(f"📝 标题: {title}")

    # 3. 提取 js_content
    print("✂️  提取内容区域...")
    content_match = re.search(
        r'id="js_content"[^>]*>(.*?)</div>\s*</div>\s*<script',
        html,
        re.DOTALL
    )

    if not content_match:
        print("❌ 未找到 js_content")
        sys.exit(1)

    content = content_match.group(1)
    print(f"✓ 提取完成 ({len(content):,} 字符)")

    # 4. 保存到文件（带标题和 URL 信息）
    skill_dir = Path(__file__).parent
    output_file = skill_dir / '.extracted_content.html'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"<!-- 标题: {title} -->\n")
        f.write(f"<!-- URL: {url} -->\n")
        f.write(content)

    print(f"💾 已保存到: {output_file}")
    print()
    print("✅ 提取完成！交给 AI 分析...")

if __name__ == "__main__":
    main()
