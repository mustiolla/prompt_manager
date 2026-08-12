# prompt_manager/main.py

# 기본 카테고리 정의
CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 초기 데이터 (이전 미션에서 만든 AI 홈트 브랜드 관련 프롬프트 3개)
prompts = [
    {
        "title": "트루폼(TrueForm) 브랜드 페르소나",
        "content": "당신은 실시간 자세 교정 AI 홈트 브랜드 '트루폼'의 전략가입니다. 신뢰감 있고 전문적인 톤으로 브랜드를 소개해주세요.",
        "category": "페르소나",
        "favorite": True
    },
    {
        "title": "키네틱스 로고 생성 프롬프트",
        "content": "미래지향적이고 역동적인 운동학적 에너지가 느껴지는 미니멀한 로고를 그려줘. 파란색과 은색을 주로 사용해.",
        "category": "이미지 생성",
        "favorite": False
    },
    {
        "title": "엑시스 서비스 홍보 문구",
        "content": "몸의 중심축을 잡아주는 AI 홈트 '엑시스'. 바쁜 직장인을 위한 15분 루틴 홍보 카피를 3개 작성해줘.",
        "category": "텍스트 생성",
        "favorite": False
    }
]

def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리 (추가/해제)")
    print("7. 즐겨찾기 목록")
    print("0. 종료")
    return input("선택: ")

def add_prompt():
    print("\n=== 프롬프트 추가 ===")
    title = input("제목: ").strip()
    content = input("내용: ").strip()
    if not title or not content:
        print("⚠️ 제목과 내용은 비어있을 수 없습니다.")
        return

    print("\n카테고리 선택:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}) {cat}")
    
    try:
        choice = int(input("선택: "))
        category = CATEGORIES[choice-1]
    except:
        category = "기타"

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    })
    print("✅ 프롬프트가 추가되었습니다!")

def list_prompts(target_list=None, title="프롬프트 목록"):
    display_list = target_list if target_list is not None else prompts
    print(f"\n=== {title} ===")
    if not display_list:
        print("데이터가 없습니다.")
        return

    for i, p in enumerate(display_list, 1):
        fav = "⭐" if p['favorite'] else ""
        print(f"{i}. [{p['category']}] {p['title']} {fav}")
    print(f"\n총 {len(display_list)}개의 프롬프트")

def filter_by_category():
    print("\n=== 카테고리별 조회 ===")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}) {cat}")
    
    try:
        choice = int(input("선택: "))
        selected_cat = CATEGORIES[choice-1]
        filtered = [p for p in prompts if p['category'] == selected_cat]
        list_prompts(filtered, f"{selected_cat} 조회 결과")
    except:
        print("잘못된 선택입니다.")

def search_prompts():
    keyword = input("\n검색어 입력: ").lower()
    result = [p for p in prompts if keyword in p['title'].lower() or keyword in p['content'].lower()]
    list_prompts(result, f"'{keyword}' 검색 결과")

def view_detail():
    list_prompts()
    try:
        idx = int(input("\n상세 보기 할 번호 입력: ")) - 1
        p = prompts[idx]
        print("\n" + "─"*30)
        print(f"제목: {p['title']}")
        print(f"카테고리: {p['category']}")
        print(f"즐겨찾기: {'⭐' if p['favorite'] else 'X'}")
        print("─"*30)
        print(f"내용:\n{p['content']}")
        print("─"*30)
    except:
        print("잘못된 번호입니다.")

def toggle_favorite():
    list_prompts()
    try:
        idx = int(input("\n즐겨찾기 설정/해제 할 번호 입력: ")) - 1
        prompts[idx]['favorite'] = not prompts[idx]['favorite']
        status = "추가" if prompts[idx]['favorite'] else "해제"
        print(f"✅ '{prompts[idx]['title']}'이(가) 즐겨찾기 {status}되었습니다.")
    except:
        print("잘못된 번호입니다.")

def main():
    while True:
        choice = show_menu()
        if choice == '1': add_prompt()
        elif choice == '2': list_prompts()
        elif choice == '3': filter_by_category()
        elif choice == '4': search_prompts()
        elif choice == '5': view_detail()
        elif choice == '6': toggle_favorite()
        elif choice == '7': 
            favs = [p for p in prompts if p['favorite']]
            list_prompts(favs, "즐겨찾기 목록")
        elif choice == '0':
            print("프로그램을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("❌ 잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()