# 🚀 나만의 프롬프트 관리 프로그램

AI 프롬프트를 효율적으로 관리하고 저장하는 파이썬 도구입니다. 
이 프로젝트는 Git과 GitHub을 활용한 버전 관리 학습을 위해 제작되었습니다.

## 1. 프로그램 흐름도
```mermaid
flowchart TD
    Start([시작]) --> Load[데이터 로드]
    Load --> Menu{메인 메뉴 선택}

    Menu --> Op1[1. 프롬프트 추가]
    Menu --> Op2[2. 목록 보기]
    Menu --> Op3[3. 카테고리별 조회]
    Menu --> Op4[4. 검색 및 상세 보기]
    Menu --> Op5[5. 즐겨찾기 관리]
    Menu --> Op0[0. 프로그램 종료]

    Op1 --> Menu
    Op2 --> Menu
    Op3 --> Menu
    Op4 --> Menu
    Op5 --> Menu

    style Start fill:#fff4dd,stroke:#d4a017,stroke-width:2px
    style Menu fill:#f9f,stroke:#333,stroke-width:2px