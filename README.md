# CodeLens AI 🔍

A lightweight Python codebase analyzer that uses Python's Abstract Syntax Tree (AST) to inspect source files and generate structured JSON reports.

## Features

- Finds functions and classes in Python files.
- Extracts function arguments and import statements.
- Detects syntax errors.
- Warns about missing function docstrings.
- Flags potentially unused imports.
- Maps dependencies between Python files in a project.
- Generates structured JSON analysis reports.
- Includes automated unit tests.

## Project Structure

```text
codelens-ai/
├── analyzer.py
├── main.py
├── test_analyzer.py
├── sample_project/
│   └── app.py
└── README.md
```

## Requirements

- Python 3.10 or newer recommended.
- No external Python packages required.

## Usage

Run the analyzer from the project directory:

```bash
python main.py sample_project --output report.json
```

The program prints a summary and saves the detailed analysis to `report.json`.

## Run Tests

```bash
python -m unittest -v test_analyzer
```

## How It Works

Python's built-in `ast` module parses source code into a structured tree without executing the analyzed code. CodeLens AI traverses this tree to extract information about functions, classes, and imports, detect selected code-quality issues, and identify project dependencies.

## Limitations

- Unused-import detection uses simple name-reference checks and may produce false positives or miss some cases.
- Dependency mapping focuses on recognizable Python imports within the project.
- The current version does not include an LLM or RAG integration.

## Future Improvements

- More accurate scope-aware code analysis.
- A visual dependency dashboard.
- AI-assisted code explanations.
- Retrieval-augmented code explanations.

## Author

Created as a learning project focused on Python, static analysis, and AI engineering.
