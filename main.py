# ==========================================
# 나만의 프롬프트 관리 프로그램 (main.py)
# 작성자: mustiolla
# 작성일: 2026-08-12
# ==========================================

# [전역 변수] 프로그램 전체에서 사용할 데이터 저장소
# 리스트 안에 딕셔너리 형태로 데이터를 저장합니다.
prompts = [
    {
        "title": "LLM 기반 회의록 자동화",
        "content": "회의 녹취록을 입력하면 안건, 결정사항, 실행 과제로 요약해줘.",
        "category": "자동화",
        "favorite": True
    },
    {
        "title": "날으는 자동차 영상 제작",
        "content": "미래 도시를 배경으로 날으는 자동차가 질주하는 16초 영상을 위한 프롬프트.",
        "category": "영상 생성",
        "favorite": False
    },
    {
        "title": "최신 논문 요약 메일 발송",
        "content": "Make를 활용해 매일 아침 최신 AI 논문을 요약해서 메일로 보내줘.",
        "category": "자동화",
        "favorite": True
    },
    {
        "title": "블로그 포스팅 생성기",
        "content": "특정 주제를 주면 서론-본론-결론 구조의 블로그 글을 써줘.",
        "category": "텍스트 생성",
        "favorite": False
    },
    {
        "title": "제품 홍보용 썸네일 이미지",
        "content": "세련된 느낌의 IT 기기 홍보용 썸네일 이미지를 생성해줘.",
        "category": "이미지 생성",
        "favorite": False
    }
    {
        "title": "파이썬 코드 리뷰",
        "content": "작성한 파이썬 코드를 분석해서 가독성을 높일 수 있는 방법을 알려줘.",
        "category": "개발",
        "favorite": False
    }    
]

# 카테고리 목록 정의
CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# ------------------------------------------
# 1. 메인 실행 함수 (Top)
# ------------------------------------------
def main():
    """프로그램의 시작점이며 전체 흐름을 제어합니다."""
    while True:
        display_menu()
        choice = input("\n선택: ").strip()
        
        if choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            manage_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "0":
            print("프로그램을 종료합니다. 즐거운 하루 되세요!")
            break
        else:
            print("⚠️ 잘못된 번호입니다. 다시 입력해주세요.")

# ------------------------------------------
# 2. 메뉴 출력 함수
# ------------------------------------------
def display_menu():
    """사용자에게 보여줄 메뉴 화면을 출력합니다."""
    print("\n" + "="*30)
    print("   나만의 프롬프트 관리자")
    print("-" * 40)
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")
    print("-" * 40)

# ------------------------------------------
# 3. 프롬프트 추가 함수
# ------------------------------------------
def add_prompt():
    """새로운 프롬프트를 입력받아 저장합니다."""
    print("\n[프롬프트 추가]")
    title = input("제목: ").strip()
    content = input("내용: ").strip()
    
    if not title or not content:
        print("⚠️ 제목과 내용은 비어있을 수 없습니다.")
        return

    print("\n카테고리 선택:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}) {cat}")
    
    cat_choice = input("선택: ").strip()
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(CATEGORIES):
        category = CATEGORIES[int(cat_choice)-1]
    else:
        category = "기타"

    new_item = {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    }
    prompts.append(new_item)
    print(f"✅ '{title}' 추가 완료!")

# ------------------------------------------
# 4. 목록 보기 함수
# ------------------------------------------
def show_list():
    """저장된 모든 프롬프트를 요약해서 보여줍니다."""
    print("\n[프롬프트 목록]")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    
    for i, p in enumerate(prompts, 1):
        fav = "⭐" if p["favorite"] else "  "
        print(f"{i}. [{p['category']}] {p['title']} {fav}")

# ------------------------------------------
# 5. 카테고리별 조회 함수
# ------------------------------------------
def show_by_category():
    """특정 카테고리의 프롬프트만 필터링해서 보여줍니다."""
    print("\n조회할 카테고리 선택:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}) {cat}")
    
    choice = input("선택: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        target_cat = CATEGORIES[int(choice)-1]
        print(f"\n[{target_cat}] 검색 결과:")
        found = False
        for i, p in enumerate(prompts, 1):
            if p["category"] == target_cat:
                print(f"{i}. {p['title']}")
                found = True
        if not found:
            print("해당 카테고리에 프롬프트가 없습니다.")
    else:
        print("⚠️ 잘못된 선택입니다.")

# ------------------------------------------
# 6. 검색 함수
# ------------------------------------------
def search_prompt():
    """키워드로 제목이나 내용을 검색합니다."""
     # 사용자의 입력값에서 양쪽 공백을 제거(.strip)하고, 대소문자 구분 없이 검색하기 위해 소문자로 변환(.lower)합니다.
    keyword = input("\n검색어 입력: ").strip().lower()
    print(f"\n'{keyword}' 검색 결과:")
    found = False
    for i, p in enumerate(prompts, 1):
        if keyword in p["title"].lower() or keyword in p["content"].lower():
            print(f"{i}. [{p['category']}] {p['title']}")
            found = True
    if not found:
        print("검색 결과가 없습니다.")

# ------------------------------------------
# 7. 상세 보기 함수
# ------------------------------------------
def show_detail():
    """번호를 입력받아 프롬프트의 전체 내용을 보여줍니다."""
    show_list()
    idx_str = input("\n상세히 볼 번호 입력: ").strip()
    if idx_str.isdigit():
        idx = int(idx_str) - 1
        if 0 <= idx < len(prompts):
            p = prompts[idx]
            print("\n" + "-"*40)
            print(f"제목: {p['title']}")
            print(f"카테고리: {p['category']}")
            print(f"즐겨찾기: {'⭐' if p['favorite'] else 'X'}")
            print("-"*40)
            print(f"내용:\n{p['content']}")
            print("-"*40)
        else:
            print("⚠️ 해당 번호가 없습니다.")
    else:
        print("⚠️ 숫자만 입력해주세요.")

# ------------------------------------------
# 8. 즐겨찾기 관리 함수
# ------------------------------------------
def manage_favorite():
    """즐겨찾기를 추가하거나 해제합니다."""
    show_list()
    idx_str = input("\n즐겨찾기 설정/해제할 번호 입력: ").strip()
    if idx_str.isdigit():
        idx = int(idx_str) - 1
        if 0 <= idx < len(prompts):
            prompts[idx]["favorite"] = not prompts[idx]["favorite"]
            status = "설정" if prompts[idx]["favorite"] else "해제"
            print(f"✅ '{prompts[idx]['title']}' 즐겨찾기 {status} 완료!")
        else:
            print("⚠️ 해당 번호가 없습니다.")

# ------------------------------------------
# 9. 즐겨찾기 목록 함수
# ------------------------------------------
def show_favorites():
    """즐겨찾기된 프롬프트만 모아서 보여줍니다."""
    print("\n[⭐ 즐겨찾기 목록]")
    found = False
    for i, p in enumerate(prompts, 1):
        if p["favorite"]:
            print(f"{i}. [{p['category']}] {p['title']}")
            found = True
    if not found:
        print("즐겨찾기된 항목이 없습니다.")

# 프로그램 실행
if __name__ == "__main__":
    main()

