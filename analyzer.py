
import ast
import json
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".venv", "venv",
    "__pycache__", "node_modules"
}


def analyze_file(file_path):
    result = {
        "file": str(file_path),
        "functions": [],
        "classes": [],
        "imports": [],
        "errors": [],
        "warnings": []
    }

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except (OSError, UnicodeError) as error:
        result["errors"].append(str(error))
        return result
    except SyntaxError as error:
        result["errors"].append(
            f"Syntax error at line {error.lineno}: {error.msg}"
        )
        return result

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_docstring = ast.get_docstring(node) is not None

            result["functions"].append({
                "name": node.name,
                "line": node.lineno,
                "arguments": [
                    arg.arg for arg in node.args.args
                ],
                "has_docstring": has_docstring
            })

            if not has_docstring:
                result["warnings"].append(
                    f"Function '{node.name}' has no docstring"
                )

        elif isinstance(node, ast.ClassDef):
            result["classes"].append({
                "name": node.name,
                "line": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None
            })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            result["imports"].append(node.module or "")

    return result


def analyze_project(root_dir):
    root = Path(root_dir).resolve()

    if not root.is_dir():
        raise ValueError(f"Not a directory: {root_dir}")

    results = []

    for file_path in root.rglob("*.py"):
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        results.append(analyze_file(file_path))

    return {
        "project": root.name,
        "files_analyzed": len(results),
        "functions_found": sum(
            len(item["functions"]) for item in results
        ),
        "classes_found": sum(
            len(item["classes"]) for item in results
        ),
        "files": results
    }


def save_report(report, output_file):
    Path(output_file).write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )
