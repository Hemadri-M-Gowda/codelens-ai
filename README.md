
# CodeLens AI 🔍

A Python codebase analyzer that uses Python's Abstract Syntax Tree (AST)
to inspect source files and generate structured reports.

## Features

- Finds functions and classes in Python files.
- Extracts function arguments and import statements.
- Detects syntax errors.
- Warns when functions are missing docstrings.
- Generates JSON analysis reports.
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

- Python 3.9 or newer
- No external Python packages required

## Usage

Run the analyzer from the project directory:

```bash
python main.py sample_project --output report.json
```

The program prints a summary and saves the detailed analysis
to `report.json`.

## Run Tests

```bash
python -m unittest -v test_analyzer
```

## How It Works

Python's `ast` module parses source code into a structured tree.
CodeLens AI traverses this tree to extract information about
functions, classes, and imports.

## Future Improvements

- Dependency mapping between project files.
- More code-quality checks.
- A visual dashboard.
- Retrieval-augmented code explanations.

## Author

Created as a learning project for Python and AI engineering.
