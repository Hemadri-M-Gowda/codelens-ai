
import argparse
import json
from analyzer import analyze_project, save_report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a Python codebase using AST."
    )
    parser.add_argument(
        "directory",
        help="Path to the Python project directory"
    )
    parser.add_argument(
        "--output",
        default="report.json",
        help="Output JSON report filename"
    )

    args = parser.parse_args()

    try:
        report = analyze_project(args.directory)
        save_report(report, args.output)

        print("Analysis completed!")
        print(f"Project: {report['project']}")
        print(f"Files analyzed: {report['files_analyzed']}")
        print(f"Functions found: {report['functions_found']}")
        print(f"Classes found: {report['classes_found']}")
        print(f"Report saved to: {args.output}")

    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
