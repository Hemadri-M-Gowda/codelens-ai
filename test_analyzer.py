
import tempfile
import unittest
from pathlib import Path

from analyzer import analyze_file, analyze_project


class TestAnalyzer(unittest.TestCase):

    def test_detects_function_and_class(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"
            file_path.write_text(
                'def greet(name):\n'
                '    return name\n\n'
                'class Calculator:\n'
                '    """A calculator."""\n'
                '    pass\n',
                encoding="utf-8"
            )

            result = analyze_file(file_path)

            self.assertEqual(len(result["functions"]), 1)
            self.assertEqual(len(result["classes"]), 1)
            self.assertEqual(
                result["functions"][0]["name"], "greet"
            )

    def test_detects_missing_docstring(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.py"
            file_path.write_text(
                "def greet(name):\n"
                "    return name\n",
                encoding="utf-8"
            )

            result = analyze_file(file_path)

            self.assertTrue(
                any("no docstring" in warning
                    for warning in result["warnings"])
            )

    def test_reports_syntax_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "broken.py"
            file_path.write_text(
                "def greet(:\n    pass\n",
                encoding="utf-8"
            )

            result = analyze_file(file_path)

            self.assertTrue(result["errors"])

    def test_analyzes_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_file = Path(temp_dir) / "app.py"
            project_file.write_text(
                'def add(a, b):\n'
                '    """Add numbers."""\n'
                '    return a + b\n',
                encoding="utf-8"
            )

            report = analyze_project(temp_dir)

            self.assertEqual(report["files_analyzed"], 1)
            self.assertEqual(report["functions_found"], 1)


if __name__ == "__main__":
    unittest.main()
