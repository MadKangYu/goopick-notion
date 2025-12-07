#!/usr/bin/env python3
"""
Notion 마크다운 내보내기 스크립트
- 페이지를 마크다운으로 변환
- Obsidian 호환 형식
"""

import os
import json
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests 패키지 필요: pip install requests")
    exit(1)

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"
EXPORT_DIR = Path(__file__).parent.parent / "exports"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


def block_to_markdown(block: dict) -> str:
    """블록을 마크다운으로 변환"""
    block_type = block.get("type", "")
    content = block.get(block_type, {})

    if block_type == "paragraph":
        texts = content.get("rich_text", [])
        return "".join([t.get("plain_text", "") for t in texts]) + "\n"

    elif block_type == "heading_1":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"# {text}\n"

    elif block_type == "heading_2":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"## {text}\n"

    elif block_type == "heading_3":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"### {text}\n"

    elif block_type == "bulleted_list_item":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"- {text}\n"

    elif block_type == "numbered_list_item":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"1. {text}\n"

    elif block_type == "to_do":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        checked = "x" if content.get("checked", False) else " "
        return f"- [{checked}] {text}\n"

    elif block_type == "code":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        lang = content.get("language", "")
        return f"```{lang}\n{text}\n```\n"

    elif block_type == "quote":
        texts = content.get("rich_text", [])
        text = "".join([t.get("plain_text", "") for t in texts])
        return f"> {text}\n"

    elif block_type == "divider":
        return "---\n"

    return ""


def export_page(page_id: str, title: str) -> str:
    """페이지를 마크다운으로 내보내기"""
    # 블록 가져오기
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    blocks = data.get("results", [])

    # 마크다운 생성
    md_content = f"# {title}\n\n"
    for block in blocks:
        md_content += block_to_markdown(block)

    return md_content


def export_all():
    """모든 페이지 내보내기"""
    print("📤 Notion 내보내기 시작...")
    print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY가 설정되지 않았습니다.")
        return

    # 내보내기 폴더 생성
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # 페이지 검색
    url = "https://api.notion.com/v1/search"
    payload = {"filter": {"property": "object", "value": "page"}, "page_size": 100}
    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()

    pages = data.get("results", [])
    print(f"   페이지: {len(pages)} 개")
    print()

    exported = 0
    for page in pages:
        page_id = page["id"]

        # 제목 추출
        title = "Untitled"
        props = page.get("properties", {})
        for key, val in props.items():
            if val.get("type") == "title":
                title_arr = val.get("title", [])
                if title_arr:
                    title = title_arr[0].get("plain_text", "Untitled")
                break

        try:
            md_content = export_page(page_id, title)

            # 파일명 안전하게
            safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
            if not safe_title:
                safe_title = page_id[:8]

            filepath = EXPORT_DIR / f"{safe_title}.md"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)

            exported += 1
            print(f"   ✓ {safe_title}.md")

        except Exception as e:
            print(f"   ✗ {title}: {e}")

    print()
    print(f"✅ 내보내기 완료! ({exported}/{len(pages)})")
    print(f"   위치: {EXPORT_DIR}")


if __name__ == "__main__":
    export_all()
