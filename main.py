# Project: Prompt Manager
# Version: 1.4.0 (Bonus Features Included)
# Last Updated: 2026.10.19
# ==========================================
# 나만의 프롬프트 관리 프로그램 (main.py)
# ==========================================

import os
import sys
import json
from datetime import datetime

# 콘솔 환경(특히 Windows)에서 한글 및 이모지 출력 시 인코딩 오류 방지
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# 파일 경로 상수 정의
DATA_FILE = "prompts.json"
EXPORT_FILE = "prompts_export.md"

# 기본 카테고리 목록 정의
DEFAULT_CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "개발", "기타"]
CATEGORIES = list(DEFAULT_CATEGORIES)

# 기본 프롬프트 데이터셋 (초기 파일이 없을 때 사용)
DEFAULT_PROMPTS = [
    {
        "title": "LLM 기반 회의록 자동화",
        "content": "회의 녹취록을 입력하면 안건, 결정사항, 실행 과제로 요약해줘.",
        "category": "자동화",
        "date": "2026-08-12 09:15:00",
        "favorite": True,
        "views": 0
    },
    {
        "title": "날으는 자동차 영상 제작",
        "content": "미래 도시를 배경으로 날으는 자동차가 질주하는 16초 영상을 위한 프롬프트.",
        "category": "영상 생성",
        "date": "2026-08-12 09:20:00",
        "favorite": False,
        "views": 0
    },
    {
        "title": "최신 논문 요약 메일 발송",
        "content": "Make를 활용해 매일 아침 최신 AI 논문을 요약해서 메일로 보내줘.",
        "category": "자동화",
        "date": "2026-08-12 09:30:00",
        "favorite": True,
        "views": 0
    },
    {
        "title": "블로그 포스팅 생성기",
        "content": "특정 주제를 주면 서론-본론-결론 구조의 블로그 글을 써줘.",
        "category": "텍스트 생성",
        "date": "2026-08-12 09:45:00",
        "favorite": False,
        "views": 0
    },
    {
        "title": "제품 홍보용 썸네일 이미지",
        "content": "세련된 느낌의 IT 기기 홍보용 썸네일 이미지를 생성해줘.",
        "category": "이미지 생성",
        "date": "2026-08-12 10:00:00",
        "favorite": False,
        "views": 0
    },
    {
        "title": "파이썬 코드 리뷰",
        "content": "작성한 파이썬 코드를 분석해서 가독성을 높일 수 있는 방법을 알려줘.",
        "category": "개발",
        "date": "2026-08-12 10:15:00",
        "favorite": False,
        "views": 0
    }    
]

# [전역 변수] 프로그램 전체에서 사용할 데이터 저장소
prompts = [dict(p) for p in DEFAULT_PROMPTS]


# ------------------------------------------
# [보너스 1-a] JSON 파일 영속화 (Load / Save)
# ------------------------------------------
def load_prompts():
    """JSON 파일에서 프롬프트 및 카테고리 데이터를 불러옵니다."""
    global prompts, CATEGORIES
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    loaded_prompts = data.get("prompts", DEFAULT_PROMPTS)
                    loaded_cats = data.get("categories", DEFAULT_CATEGORIES)
                    for cat in loaded_cats:
                        if cat not in CATEGORIES:
                            CATEGORIES.append(cat)
                    prompts = loaded_prompts
                elif isinstance(data, list):
                    prompts = data
                
                # 각 프롬프트에 views 속성 보장
                for p in prompts:
                    if "views" not in p:
                        p["views"] = 0
            return
        except Exception as e:
            print(f"⚠️ 데이터 파일 로드 중 오류 발생: {e}")
            prompts = [dict(p) for p in DEFAULT_PROMPTS]
    else:
        prompts = [dict(p) for p in DEFAULT_PROMPTS]
        save_prompts()


def save_prompts():
    """현재 프롬프트 및 카테고리 데이터를 JSON 파일로 저장합니다."""
    try:
        data = {
            "categories": CATEGORIES,
            "prompts": prompts
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"⚠️ 데이터 파일 저장 중 오류 발생: {e}")


# ------------------------------------------
# 1. 메인 실행 함수 (Top)
# ------------------------------------------
def main():
    """프로그램의 시작점이며 전체 흐름을 제어합니다."""
    # 데이터 영속화: 시작 시 자동 로드
    load_prompts()
    
    while True:
        display_menu()
        choice = input("\n선택: ").strip()
        
        if choice == "1":
            show_list()
        elif choice == "2":
            add_prompt()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            modify_prompt()
        elif choice == "9":
            delete_prompt()
        elif choice == "10":
            show_top_prompts()
        elif choice == "11":
            export_to_markdown()
        elif choice == "0":
            save_prompts()
            print("프로그램을 종료합니다. 즐거운 하루 되세요!")
            break
        else:
            print("⚠️ 잘못된 번호입니다. 다시 입력해주세요.")


# ------------------------------------------
# 2. 메뉴 출력 함수
# ------------------------------------------
def display_menu():
    """사용자에게 보여줄 메뉴 화면을 출력합니다."""
    print("\n" + "="*38)
    print("        나만의 프롬프트 관리자")
    print("-" * 45)
    print("[1]  프롬프트 목록")   
    print("[2]  프롬프트 추가")   
    print("[3]  카테고리별 조회")
    print("[4]  프롬프트 검색")
    print("[5]  프롬프트 상세 보기 (조회수 +1)")
    print("[6]  즐겨찾기 관리")
    print("[7]  즐겨찾기 목록")
    print("[8]  프롬프트 수정")
    print("[9]  프롬프트 삭제")
    print("[10] 인기 프롬프트 (조회수 Top 순위)")
    print("[11] 마크다운(.md)으로 내보내기")
    print("[0]  종료 (자동 저장)")
    print("-" * 45)


# ------------------------------------------
# 3. 공통: 카테고리 선택 및 추가 함수
# ------------------------------------------
def select_category(default_cat=None):
    """카테고리를 선택하거나 0번을 눌러 새 카테고리를 추가합니다."""
    print("\n[카테고리 목록]")
    print("0. 직접 입력 (새 카테고리 추가)")
    for i, cat in enumerate(CATEGORIES):
        print(f"{i+1}. {cat}")
    
    if default_cat:
        print(f"* 엔터(Enter) 키를 누르면 기존 카테고리 '{default_cat}'(을)를 유지합니다.")
        
    choice_input = input("\n카테고리 번호 선택: ").strip()
    
    # 기본값이 주어졌을 때 그냥 엔터를 치면 기본값 유지
    if not choice_input and default_cat:
        return default_cat
        
    try:
        cat_idx = int(choice_input)
        if cat_idx == 0:
            new_cat = input("새로운 카테고리명을 입력하세요: ").strip()
            if new_cat:
                if new_cat not in CATEGORIES:
                    CATEGORIES.append(new_cat)
                    save_prompts()
                return new_cat
            else:
                print(f"⚠️ 입력값이 없어 '{default_cat or '기타'}'(으)로 설정합니다.")
                return default_cat or "기타"
        elif 1 <= cat_idx <= len(CATEGORIES):
            return CATEGORIES[cat_idx - 1]
        else:
            print(f"⚠️ 잘못된 선택입니다. '{default_cat or '기타'}'(으)로 설정합니다.")
            return default_cat or "기타"
    except ValueError:
        print(f"⚠️ 잘못된 선택입니다. '{default_cat or '기타'}'(으)로 설정합니다.")
        return default_cat or "기타"


# ------------------------------------------
# 4. 프롬프트 추가 함수 (Create)
# ------------------------------------------
def add_prompt():
    """새로운 프롬프트를 입력받아 저장합니다."""
    print("\n--- 새 프롬프트 등록 ---")
    title = input("제목을 입력하세요: ").strip()
    if not title:
        print("⚠️ 제목은 비어 있을 수 없습니다.")
        return

    content = input("내용을 입력하세요: ").strip()
    if not content:
        print("⚠️ 내용은 비어 있을 수 없습니다.")
        return
    
    category = select_category()

    # 타임스탬프 생성
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    new_item = {
        "title": title,
        "content": content,
        "category": category,
        "date": current_time,
        "favorite": False,
        "views": 0
    }
    
    prompts.append(new_item)
    save_prompts()
    print(f"\n✅ '{title}' 등록 완료! (시간: {current_time})")


# ------------------------------------------
# 5. 프롬프트 수정 함수 (Update)
# ------------------------------------------
def modify_prompt():
    """기존 프롬프트를 선택하여 제목, 내용, 카테고리를 수정합니다."""
    if not prompts:
        print("\n⚠️ 등록된 프롬프트가 없습니다.")
        return

    try:
        idx = int(input("\n수정할 프롬프트 번호: ")) - 1
        
        if 0 <= idx < len(prompts):
            p = prompts[idx]
            print(f"\n--- '{p['title']}' 수정 ---")
            print("* 수정하지 않을 항목은 그대로 엔터(Enter)를 누르세요.")
            
            new_title = input(f"새 제목 ({p['title']}): ").strip()
            if new_title:
                p['title'] = new_title
                
            new_content = input(f"새 내용 ({p['content']}): ").strip()
            if new_content:
                p['content'] = new_content
                
            p['category'] = select_category(p['category'])
            
            # 수정된 시간 반영
            p['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_prompts()
            
            print(f"\n✅ 프롬프트 수정이 완료되었습니다.")
        else:
            print("⚠️ 해당 번호의 프롬프트가 없습니다.")
            
    except ValueError:
        print("⚠️ 숫자만 입력해주세요.")


# ------------------------------------------
# 6. 프롬프트 삭제 함수 (Delete)
# ------------------------------------------
def delete_prompt():
    """기존 프롬프트를 번호로 선택하여 삭제합니다."""
    if not prompts:
        print("\n⚠️ 등록된 프롬프트가 없습니다.")
        return

    try:
        idx = int(input("\n삭제할 프롬프트 번호: ")) - 1
        
        if 0 <= idx < len(prompts):
            deleted = prompts.pop(idx)
            save_prompts()
            print(f"\n✅ '{deleted['title']}' 프롬프트가 삭제되었습니다.")
        else:
            print("⚠️ 해당 번호의 프롬프트가 없습니다.")
            
    except ValueError:
        print("⚠️ 숫자만 입력해주세요.")


# ------------------------------------------
# 7. 목록 보기 함수 (Read)
# ------------------------------------------
def show_list():
    """저장된 모든 프롬프트의 목록을 출력합니다."""
    print(f"\n{'No':<3} | {'카테고리':<10} | {'제목':<20} | {'조회수':<6} | {'등록/수정일'}")
    print("-" * 75)
    
    for i, p in enumerate(prompts):
        # 즐겨찾기 표시 (True면 ★, False면 빈칸)
        fav = "★" if p.get("favorite") else "  "
        date = p.get("date", "기존 데이터")
        views = f"{p.get('views', 0)}회"
        
        print(f"{i+1:<3} | {p['category']:<10} | {p['title']:<20} | {views:<6} | {date} {fav}")


# ------------------------------------------
# 8. 카테고리별 조회 함수 (Read)
# ------------------------------------------
def show_by_category():
    """특정 카테고리의 프롬프트만 선택해서 보여줍니다."""
    print("\n--- 카테고리별 조회 ---")
    for i, cat in enumerate(CATEGORIES):
        print(f"{i+1}. {cat}")
        
    try:
        choice = int(input("\n조회할 카테고리 번호: ")) - 1
        if not (0 <= choice < len(CATEGORIES)):
            print("⚠️ 올바른 번호를 선택해주세요.")
            return
        target_cat = CATEGORIES[choice]
        
        print(f"\n[{target_cat}] 카테고리 검색 결과:")
        print("-" * 50)
        
        found = False
        for p in prompts:
            if p["category"] == target_cat:
                views = f"({p.get('views', 0)}회)"
                fav = "★" if p.get("favorite") else ""
                print(f"- {p['title']} {views} {fav}")
                found = True
        
        if not found:
            print("해당 카테고리에 등록된 프롬프트가 없습니다.")
            
    except (ValueError, IndexError):
        print("⚠️ 올바른 번호를 선택해주세요.")


# ------------------------------------------
# 9. 검색 함수 (Read)
# ------------------------------------------
def search_prompt():
    """키워드를 입력받아 제목이나 내용에서 검색합니다."""
    keyword = input("\n검색할 키워드를 입력하세요: ").strip()
    
    if not keyword:
        print("⚠️ 검색어를 입력해야 합니다.")
        return

    print(f"\n'{keyword}' 검색 결과:")
    print("-" * 50)
    
    found = False
    for p in prompts:
        # 제목이나 내용에 키워드가 포함되어 있는지 확인
        if keyword.lower() in p["title"].lower() or keyword.lower() in p["content"].lower():
            views = f"({p.get('views', 0)}회)"
            fav = "★" if p.get("favorite") else ""
            print(f"[{p['category']}] {p['title']} {views} {fav}")
            found = True
            
    if not found:
        print("검색 결과가 없습니다.")


# ------------------------------------------
# 10. 상세 보기 함수 (보너스 2-b: 조회수 기록)
# ------------------------------------------
def show_detail():
    """번호를 입력받아 해당 프롬프트의 상세 내용을 보여주고 조회수를 1 증가시킵니다."""
    if not prompts:
        print("\n⚠️ 등록된 프롬프트가 없습니다.")
        return

    try:
        idx = int(input("\n상세히 볼 프롬프트 번호: ")) - 1
        
        if 0 <= idx < len(prompts):
            p = prompts[idx]
            # 사용 횟수(조회수) 1 증가 및 저장
            p["views"] = p.get("views", 0) + 1
            save_prompts()
            
            print(f"\n--- 상세 정보 ---")
            print(f"제목: {p['title']}")
            print(f"카테고리: {p['category']}")
            print(f"등록/수정일: {p.get('date', '기존 데이터')}")
            print(f"조회수: {p['views']}회")
            print(f"즐겨찾기: {'★' if p.get('favorite') else '☆'}")
            print("-" * 25)
            print(f"내용:\n{p['content']}")
            print("-" * 25)
        else:
            print("⚠️ 해당 번호의 프롬프트가 없습니다.")
            
    except ValueError:
        print("⚠️ 숫자만 입력해주세요.")


# ------------------------------------------
# 11. 즐겨찾기 관리 함수 (Update)
# ------------------------------------------
def toggle_favorite():
    """프롬프트의 즐겨찾기 상태를 반전(On/Off)시킵니다."""
    if not prompts:
        print("\n⚠️ 등록된 프롬프트가 없습니다.")
        return

    try:
        idx = int(input("\n즐겨찾기 설정/해제할 번호: ")) - 1
        
        if 0 <= idx < len(prompts):
            current_status = prompts[idx].get("favorite", False)
            prompts[idx]["favorite"] = not current_status
            save_prompts()
            
            status_str = "등록" if prompts[idx]["favorite"] else "해제"
            print(f"✅ '{prompts[idx]['title']}'이(가) 즐겨찾기 {status_str}되었습니다.")
        else:
            print("⚠️ 해당 번호의 프롬프트가 없습니다.")
            
    except ValueError:
        print("⚠️ 숫자만 입력해주세요.")


# ------------------------------------------
# 12. 즐겨찾기 목록 함수 (Read)
# ------------------------------------------
def show_favorites():
    """즐겨찾기에 등록된 프롬프트만 보여줍니다."""
    print("\n--- ★ 즐겨찾기 목록 ---")
    print("-" * 55)
    
    found = False
    for i, p in enumerate(prompts):
        if p.get("favorite"):
            views = f"({p.get('views', 0)}회)"
            print(f"{i+1}. [{p['category']}] {p['title']} {views}")
            found = True
            
    if not found:
        print("즐겨찾기에 등록된 프롬프트가 없습니다.")
    print("-" * 55)


# ------------------------------------------
# [보너스 2-c] 인기 프롬프트 (조회수 기준 Top 목록)
# ------------------------------------------
def show_top_prompts():
    """조회수(사용 횟수) 기준 내림차순 정렬된 Top 프롬프트 목록을 출력합니다."""
    if not prompts:
        print("\n⚠️ 등록된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(prompts, key=lambda x: x.get("views", 0), reverse=True)

    print("\n--- 🏆 인기 프롬프트 Top 목록 (조회수 기준) ---")
    print(f"{'순위':<4} | {'조회수':<6} | {'카테고리':<10} | {'제목':<22} | {'즐겨찾기'}")
    print("-" * 65)

    for rank, p in enumerate(sorted_prompts, 1):
        fav = "★" if p.get("favorite") else " "
        views = f"{p.get('views', 0)}회"
        print(f"{rank:<4} | {views:<6} | {p['category']:<10} | {p['title']:<22} | {fav}")
    print("-" * 65)


# ------------------------------------------
# [보너스 1-b] 카테고리별 Markdown 파일 내보내기
# ------------------------------------------
def export_to_markdown(filepath=EXPORT_FILE):
    """전체 프롬프트를 카테고리별로 분류하여 Markdown 파일로 내보냅니다."""
    if not prompts:
        print("\n⚠️ 내보낼 프롬프트가 없습니다.")
        return

    # 카테고리별 그룹화
    cat_map = {}
    for p in prompts:
        cat = p.get("category", "기타")
        if cat not in cat_map:
            cat_map[cat] = []
        cat_map[cat].append(p)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    md_lines = [
        "# 📚 나만의 프롬프트 모음집 (카테고리별 내보내기)",
        f"> **내보낸 일시:** {now_str}  ",
        f"> **총 프롬프트 수:** {len(prompts)}개  \n",
        "---",
        ""
    ]

    # 카테고리 정렬 순서
    ordered_cats = [c for c in CATEGORIES if c in cat_map]
    for c in cat_map:
        if c not in ordered_cats:
            ordered_cats.append(c)

    for cat in ordered_cats:
        items = cat_map[cat]
        md_lines.append(f"## 📂 {cat} ({len(items)}개)")
        md_lines.append("")
        for idx, item in enumerate(items, 1):
            fav_str = "⭐ 즐겨찾기" if item.get("favorite") else "일반"
            views = item.get("views", 0)
            date_str = item.get("date", "기존 데이터")
            md_lines.append(f"### {idx}. {item['title']}")
            md_lines.append(f"- **등록/수정일:** {date_str}")
            md_lines.append(f"- **상태:** {fav_str} | **조회수:** {views}회")
            md_lines.append("- **프롬프트 내용:**")
            md_lines.append("```text")
            md_lines.append(item.get("content", "").strip())
            md_lines.append("```")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"\n✅ 전체 프롬프트가 '{filepath}'(으)로 성공적으로 내보내졌습니다!")
    except Exception as e:
        print(f"\n⚠️ 마크다운 내보내기 중 오류 발생: {e}")


# 프로그램 실행
if __name__ == "__main__":
    main()
    print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")