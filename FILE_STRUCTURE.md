# 📂 프로젝트 구조 (File Structure)

```text
prompt_manager/
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI 자동화 파이프라인
├── Screenshots/              # 프로그램 실행 화면 및 Git 이력 캡처 이미지
├── .gitignore                # Git 제외 대상 설정 파일
├── FILE_STRUCTURE.md         # 프로젝트 구조 설명 문서 (현재 파일)
├── README.md                 # 프로젝트 개요, 사용법 및 아키텍처 상세 안내
├── A1-1_Summary.md           # 미션 결과 요약, 평가문항 및 추가 기능 기술 답변서
├── test_prompt_manager.py    # 단위 테스트 및 회귀 테스트 스위트
├── prompts.json              # [추가 기능] 프롬프트 데이터 영속화 저장소 (JSON)
├── prompts.json.bak          # [추가 기능] 데이터 손상 대비 자동 백업본
├── prompts_export.md         # [추가 기능] 카테고리별 마크다운 내보내기 결과 파일
└── main.py                   # 프로그램 메인 실행 파일 (전체 기능 구현)
```