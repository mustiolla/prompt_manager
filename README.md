# 🚀 나만의 프롬프트 관리 프로그램

AI 프롬프트를 효율적으로 관리하는 파이썬 도구입니다.

## 1. 프로그램 흐름도
```mermaid
flowchart TD
    %% 스타일 정의
    classDef main fill:#f9f,stroke:#333,stroke-width:2px;
    classDef box fill:#ffffff,stroke:#333,stroke-width:1px;
    classDef point fill:#fff4dd,stroke:#d4a017,stroke-width:2px;

    Start([Start]) --> Load[데이터 로드]
    Load --> Menu{메인 메뉴 선택}

    Menu --> Op1[1. 프롬프트 추가]
    Menu --> Op2[2. 목록 보기]
    Menu --> Op3[3. 카테고리별 조회]
    Menu --> Op4[4. 검색 및 상세 보기]
    Menu --> Op5[6. 즐겨찾기 관리]
    Menu --> Op0([0. 프로그램 종료])

    Op1 --> Menu
    Op2 --> Menu
    Op3 --> Menu
    Op4 --> Menu
    Op5 --> Menu

    class Menu main;
    class Op1,Op2,Op3,Op4,Op5 box;
    class Start,Op0 point;
    ```