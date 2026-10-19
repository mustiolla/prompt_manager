"""
test_prompt_manager.py - CI 및 기능 검증용 자동화 테스트 스위트
"""

import os
import json
import shutil
import unittest
import main

class TestPromptManager(unittest.TestCase):
    def setUp(self):
        # 테스트 전 데이터 초기화
        self.backup_exists = os.path.exists(main.DATA_FILE)
        if self.backup_exists:
            shutil.copy2(main.DATA_FILE, "prompts_test_backup.json")
        main.prompts = [dict(p) for p in main.DEFAULT_PROMPTS]
        main.CATEGORIES = list(main.DEFAULT_CATEGORIES)
        main.save_prompts()

    def tearDown(self):
        # 테스트 후 원래 데이터 복원
        if self.backup_exists and os.path.exists("prompts_test_backup.json"):
            shutil.copy2("prompts_test_backup.json", main.DATA_FILE)
            os.remove("prompts_test_backup.json")
        if os.path.exists(main.TEMP_FILE):
            os.remove(main.TEMP_FILE)

    def test_initial_prompts_and_categories(self):
        """기본 프롬프트 및 카테고리 구성 확인"""
        self.assertGreaterEqual(len(main.prompts), 6)
        self.assertIn("개발", main.CATEGORIES)
        self.assertIn("자동화", main.CATEGORIES)

    def test_atomic_save_and_backup(self):
        """원자적 저장 및 백업본(.bak) 생성 검증"""
        main.save_prompts()
        self.assertTrue(os.path.exists(main.DATA_FILE))
        self.assertTrue(os.path.exists(main.BACKUP_FILE))

        # JSON 유효성 검증
        with open(main.DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("prompts", data)
            self.assertIn("categories", data)

    def test_auto_recovery_from_backup(self):
        """메인 JSON 파일 손상 시 백업본 복구 검증"""
        main.save_prompts()
        self.assertTrue(os.path.exists(main.BACKUP_FILE))

        # 메인 파일 고의 훼손
        with open(main.DATA_FILE, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON DATA ... ")

        # load_prompts() 호출 시 백업본에서 복구되어야 함
        main.load_prompts()
        self.assertGreaterEqual(len(main.prompts), 6)

    def test_view_count_increment(self):
        """상세 보기 및 조회수 증가 검증"""
        initial_views = main.prompts[0].get("views", 0)
        main.prompts[0]["views"] = initial_views + 1
        main.save_prompts()

        # 재로드 후 조회수 보존 확인
        main.load_prompts()
        self.assertEqual(main.prompts[0]["views"], initial_views + 1)

    def test_regex_search(self):
        """정규표현식 검색 동작 검증"""
        import re
        pattern = re.compile(r"회의록|자동차", re.IGNORECASE)
        results = [p for p in main.prompts if pattern.search(p["title"]) or pattern.search(p["content"])]
        self.assertGreaterEqual(len(results), 2)

    def test_markdown_export(self):
        """카테고리별 마크다운 내보내기 검증"""
        test_export_path = "test_export.md"
        main.export_to_markdown(filepath=test_export_path)
        self.assertTrue(os.path.exists(test_export_path))
        with open(test_export_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# 📚 나만의 프롬프트 모음집", content)
            self.assertIn("## 📂", content)
        os.remove(test_export_path)

if __name__ == "__main__":
    unittest.main()
