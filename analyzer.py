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

    # Collect names referenced in the source code.
    used_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
    }

    # Analyze functions, classes, and imports.
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

                imported_name = (
                    alias.asname or alias.name.split(".")[0]
                )

                if imported_name not in used_names:
                    result["warnings"].append(
                        f"Unused import: {imported_name}"
                    )

        elif isinstance(node, ast.ImportFrom):
            result["imports"].append(node.module or "")

            for alias in node.names:
                if alias.name == "*":
                    continue

                imported_name = alias.asname or alias.name

                if imported_name not in used_names:
                    result["warnings"].append(
                        f"Unused import: {imported_name}"
                    )

    return result


def analyze_project(root_dir):
    root = Path(root_dir).resolve()

    if not root.is_dir():
        raise ValueError(f"Not a directory: {root_dir}")

    results = []

    for file_path in sorted(root.rglob("*.py")):
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue

        results.append(analyze_file(file_path))

    # Map module names to project-relative file paths.
    module_to_file = {}

    for file_path in sorted(root.rglob("*.py")):
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue

        relative = file_path.relative_to(root)
        module_relative = relative.with_suffix("")
        parts = list(module_relative.parts)

        if parts[-1] == "__init__":
            parts.pop()

        if parts:
            module_name = ".".join(parts)
            module_to_file[module_name] = relative.as_posix()

    # Match project imports to files within the project.
    dependencies = []

    for item in results:
        source_path = Path(item["file"])

        try:
            source_relative = source_path.resolve().relative_to(root)
        except ValueError:
            continue

        for imported_module in item["imports"]:
            if not imported_module:
                continue

            matched_paths = set()

            for module_name, target_path in module_to_file.items():
                if (
                    imported_module == module_name
                    or imported_module.startswith(module_name + ".")
                    or module_name.startswith(imported_module + ".")
                ):
                    if target_path != source_relative.as_posix():
                        matched_paths.add(target_path)

            for target_path in sorted(matched_paths):
                dependencies.append({
                    "source": source_relative.as_posix(),
                    "target": target_path,
                    "import": imported_module
                })

    return {
        "project": root.name,
        "files_analyzed": len(results),
        "functions_found": sum(
            len(item["functions"]) for item in results
        ),
        "classes_found": sum(
            len(item["classes"]) for item in results
        ),
        "dependencies": dependencies,
        "files": results
    }


def save_report(report, output_file):
    Path(output_file).write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )
