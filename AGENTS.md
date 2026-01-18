# AGENTS.md

Baekjoon Online Judge problem viewer and controller tool. A CLI utility for viewing Baekjoon problems in terminal, creating solution templates, and testing solutions against sample I/O.

## Project Overview

- **Purpose**: View Baekjoon problems without browser, generate solution templates, and test solutions
- **Language**: Python 3
- **Key Dependencies**: `requests`, `beautifulsoup4`, `rich`

## Build and Test Commands

### Running the Tool

```bash
# View problem
python3 boj_ctrl.py <problem_id>

# Show only sample I/O
python3 boj_ctrl.py <problem_id> --sample

# Create solution file with template
python3 boj_ctrl.py <problem_id> --init

# Create and test solution (run --init first, then test)
python3 boj_ctrl.py <problem_id> --test

# Recommend random problem by tier
python3 boj_ctrl.py --random <tier>  # tiers: b1-b4, s1-s4, g1-g4, p1-p4, d, r
```

### Running Solution Files

```bash
# Direct execution of solution file
python3 <problem_id>.py

# Example:
python3 1015.py
```

### No Build/Install Required

This is a standalone Python script. Just ensure dependencies are installed:

```bash
pip install requests beautifulsoup4 rich
```

No automated testing framework, linting, or build system is configured. Testing is done manually via the `--test` flag.

## Code Style Guidelines

### File Structure

```python
"""
Module docstring describing purpose.
"""

# Standard library imports
import sys
import os

# Third-party imports
import requests
from bs4 import BeautifulSoup
from rich.console import Console

# Constants
HEADERS = {...}
BOJ_PROBLEM_URL = "..."

def main():
    pass

if __name__ == "__main__":
    main()
```

### Import Pattern

1. Standard library imports first
2. Third-party imports after
3. Each import on its own line
4. Group imports logically
5. **Fast I/O pattern**: `import sys` followed by `input = sys.stdin.readline`

### Naming Conventions

- **Functions**: snake_case (`fetch_problem_page`, `parse_problem`, `display_problem`)
- **Variables**: snake_case (`problem_id`, `sample_only`, `filename`, `all_passed`)
- **Constants**: UPPER_SNAKE_CASE (`HEADERS`, `BOJ_PROBLEM_URL`, `SOLVEDAC_API_URL`)
- **Parameters**: snake_case, descriptive names
- **Files**: lowercase_with_underscores (or single word like `boj_ctrl.py`)

### Type Hints

**Mandatory** on all function signatures. Use standard Python type hints:

```python
def fetch_problem_page(problem_id: int) -> str:
    """Docstring here."""
    pass

def parse_problem(html: str, sample_only: bool = False):
    """Docstring here."""
    pass

def recommend_random(tier: str):
    """Docstring here."""
    pass
```

Common types: `int`, `str`, `bool`, `dict`, `list`, `Path`

### Docstrings

Every function must have a docstring. Keep it concise (one line preferred):

```python
def fetch_problem_page(problem_id: int) -> str:
    """Fetch problem page HTML from Baekjoon."""
    pass

def parse_sample_pairs(samples: list) -> list:
    """Parse sample I/O pairs from flat list."""
    pass
```

### Indentation and Formatting

- **4 spaces** for indentation (no tabs)
- **Blank line** between functions
- **Blank line** after docstring before code
- **Trailing whitespace**: avoid
- **Line length**: reasonable, not strictly enforced

### Error Handling

```python
# HTTP requests - use raise_for_status()
response = requests.get(url, headers=HEADERS, timeout=10)
response.raise_for_status()

# File operations - check existence
if filepath.exists() and not force:
    raise FileExistsError(f"File '{filename}' already exists.")

# Try-except for specific exceptions
try:
    # code
except requests.exceptions.RequestException as e:
    print(f"[Error] Failed to fetch problem: {e}", file=sys.stderr)
    sys.exit(1)
except FileExistsError as e:
    print(f"[Error] {e}", file=sys.stderr)
    sys.exit(1)
except KeyboardInterrupt:
    print("\nCancelled.", file=sys.stderr)
    sys.exit(0)
```

**Rules**:
- Print errors to `sys.stderr`
- Exit with non-zero status on errors
- Handle specific exceptions, not broad `Exception`
- Use descriptive error messages

### Constants and Global Variables

Define at module level, after imports, before functions:

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
}

BOJ_PROBLEM_URL = "https://www.acmicpc.net/problem/"
SOLVEDAC_API_URL = "https://solved.ac/api/v3"
```

### Function Structure

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """Concise one-line description."""
    # Variable declarations

    # Main logic

    return value
```

### CLI Argument Parsing

Use `argparse` for command-line interfaces:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("problem_id", type=int, help="Problem ID")
    parser.add_argument("--sample", action="store_true", help="Show only sample I/O")
    parser.add_argument("--init", action="store_true", help="Create solution file")

    args = parser.parse_args()

    if args.problem_id is None:
        parser.print_help()
        return

    # Use args.problem_id, args.sample, args.init, etc.
```

### Rich Output

Use `rich` library for formatted terminal output:

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Colored text
console.print("[bold green]All tests passed![/bold green]")
console.print(f"[cyan]Tier: {tier}[/cyan]")

# Panels
console.print(Panel(content, border_style="green"))
```

### File Operations

```python
from pathlib import Path

filename = f"{problem_id}.py"
filepath = Path(filename)

# Check existence
if filepath.exists():
    # handle

# Write with UTF-8 encoding
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
```

### Subprocess for Testing

Use `subprocess.run` with `capture_output`:

```python
result = subprocess.run(
    ["python3", filename],
    stdin=open(tmp_file, "r"),
    capture_output=True,
    text=True,
    timeout=5
)

actual_output = result.stdout.rstrip()
```

### Testing Solutions

Solution files are tested by:
1. Creating temporary file with sample input
2. Running solution with subprocess
3. Comparing stdout to expected output
4. Timeout of 5 seconds per test case

Template includes embedded sample I/O as comments for reference.

## Best Practices

1. **Fast I/O**: Always use `input = sys.stdin.readline` for reading input
2. **Type safety**: Use type hints on all function signatures
3. **Documentation**: Every function needs a docstring
4. **Error messages**: Print to `sys.stderr`, exit with non-zero on errors
5. **Timeouts**: Always set timeout on network requests (10s recommended)
6. **UTF-8**: Use `encoding="utf-8"` for file operations
7. **Clean exit**: Handle `KeyboardInterrupt` gracefully
8. **Module guard**: Always use `if __name__ == "__main__":` for main execution
