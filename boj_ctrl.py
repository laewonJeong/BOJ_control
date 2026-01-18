"""
Baekjoon Online Judge Problem Viewer
View Baekjoon problems in terminal without opening browser.

Usage:
    python boj_ctrl.py <problem_id>
    python boj_ctrl.py <problem_id> --sample    # Show only sample I/O
    python boj_ctrl.py <problem_id> --init      # Create solution file with template
    python boj_ctrl.py <problem_id> --init --test  # Create and test solution
    python boj_ctrl.py <problem_id> --random <tier>    # Recommend random problem by tier (b1, s2, s3, s4, g1, g2, g3, g4, p1, p2, p3, p4, d, r)
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BOJ_PROBLEM_URL = "https://www.acmicpc.net/problem/"
SOLVEDAC_API_URL = "https://solved.ac/api/v3"


def fetch_problem_page(problem_id: int) -> str:
    """Fetch problem page HTML from Baekjoon."""
    url = f"{BOJ_PROBLEM_URL}{problem_id}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def parse_problem(html: str, sample_only: bool = False):
    """Parse problem information from HTML."""
    soup = BeautifulSoup(html, "lxml")

    result = {
        "id": None,
        "title": None,
        "description": None,
        "input": None,
        "output": None,
        "samples": [],
        "limit": None,
        "tags": [],
    }

    title_elem = soup.find("span", id="problem_title")
    if title_elem:
        result["title"] = title_elem.get_text(strip=True)

    desc_elem = soup.find("div", id="problem_description")
    if desc_elem:
        result["description"] = desc_elem.get_text(separator="\n", strip=True)

    input_elem = soup.find("div", id="problem_input")
    if input_elem:
        result["input"] = input_elem.get_text(separator="\n", strip=True)

    output_elem = soup.find("div", id="problem_output")
    if output_elem:
        result["output"] = output_elem.get_text(separator="\n", strip=True)

    sample_elems = soup.find_all("pre", class_="sampledata")
    for elem in sample_elems:
        result["samples"].append(elem.get_text(strip=True))

    limit_elem = soup.find("div", id="problem_limit")
    if limit_elem:
        result["limit"] = limit_elem.get_text(separator="\n", strip=True)

    return result


def display_problem(problem: dict, sample_only: bool = False):
    """Display problem information using Rich."""
    console = Console()

    if problem["title"]:
        title_text = Text(f"#{problem.get('id', '?')} {problem['title']}", style="bold cyan")
        console.print(Panel(title_text, style="bold"))

    if sample_only:
        if not problem["samples"]:
            console.print("[yellow]No sample I/O found[/yellow]")
            return

        for i in range(0, len(problem["samples"]), 2):
            if i < len(problem["samples"]):
                console.print(f"\n[bold green]Sample Input {i//2 + 1}:[/bold green]")
                console.print(Panel(problem["samples"][i], border_style="green"))

            if i + 1 < len(problem["samples"]):
                console.print(f"\n[bold blue]Sample Output {i//2 + 1}:[/bold blue]")
                console.print(Panel(problem["samples"][i + 1], border_style="blue"))

        return

    if problem["description"]:
        console.print("\n[bold yellow]Problem Description:[/bold yellow]")
        console.print(Panel(problem["description"], border_style="yellow"))

    if problem["input"]:
        console.print("\n[bold green]Input:[/bold green]")
        console.print(Panel(problem["input"], border_style="green"))

    if problem["output"]:
        console.print("\n[bold blue]Output:[/bold blue]")
        console.print(Panel(problem["output"], border_style="blue"))

    if problem["limit"]:
        console.print("\n[bold magenta]Limit:[/bold magenta]")
        console.print(Panel(problem["limit"], border_style="magenta"))

    if problem["samples"]:
        console.print("\n[bold white]Sample I/O:[/bold white]")
        for i in range(0, len(problem["samples"]), 2):
            if i < len(problem["samples"]):
                console.print(f"\n[bold green]Sample Input {i//2 + 1}:[/bold green]")
                console.print(Panel(problem["samples"][i], border_style="green"))

            if i + 1 < len(problem["samples"]):
                console.print(f"\n[bold blue]Sample Output {i//2 + 1}:[/bold blue]")
                console.print(Panel(problem["samples"][i + 1], border_style="blue"))

    console.print(f"\n[dim]URL: {BOJ_PROBLEM_URL}{problem.get('id', '?')}[/dim]")


def generate_template(problem: dict) -> str:
    """Generate solution file template with embedded sample I/O."""
    template_lines = []

    if problem["title"]:
        template_lines.append(f"# {problem['title']}")

    template_lines.append("import sys")
    template_lines.append("input = sys.stdin.readline")
    template_lines.append("")

    template_lines.append("def main():")
    template_lines.append("    # Write your solution here")
    template_lines.append("    pass")
    template_lines.append("")

    template_lines.append("if __name__ == \"__main__\":")
    template_lines.append("    main()")
    template_lines.append("")

    if problem["samples"]:
        template_lines.append("# Sample Input/Output for testing:")
        for i in range(0, len(problem["samples"]), 2):
            sample_num = i // 2 + 1
            template_lines.append(f"# Sample {sample_num}:")
            template_lines.append("# Input:")
            if i < len(problem["samples"]):
                sample_input = problem["samples"][i]
                for line in sample_input.split("\n"):
                    template_lines.append(f"# {line}")
            template_lines.append("# Output:")
            if i + 1 < len(problem["samples"]):
                sample_output = problem["samples"][i + 1]
                template_lines.append(f"# {sample_output}")
            template_lines.append("")

    return "\n".join(template_lines)


def create_solution_file(problem_id: int, problem: dict, force: bool = False):
    """Create solution file with template."""
    filename = f"{problem_id}.py"
    filepath = Path(filename)

    if filepath.exists() and not force:
        raise FileExistsError(f"File '{filename}' already exists. Use --force to overwrite.")

    template = generate_template(problem)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template)

    return filename


def parse_sample_pairs(samples: list) -> list:
    """Parse sample I/O pairs from flat list."""
    sample_pairs = []
    num_samples = len(samples)

    for i in range(0, num_samples, 2):
        sample_input = samples[i] if i < num_samples else ""
        sample_output = samples[i + 1] if i + 1 < num_samples else ""
        sample_pairs.append((sample_input, sample_output))

    return sample_pairs


def test_solution_file(problem_id: int, samples: list) -> bool:
    """Test solution file against sample I/O."""
    import subprocess
    import tempfile

    filename = f"{problem_id}.py"
    filepath = Path(filename)

    if not filepath.exists():
        print(f"[Error] File '{filename}' does not exist.", file=sys.stderr)
        return False

    sample_pairs = parse_sample_pairs(samples)
    all_passed = True
    tmp_file = None
    console = Console()

    for i, (sample_input, expected_output) in enumerate(sample_pairs, 1):
        if not sample_input:
            continue

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp:
            tmp.write(sample_input)
            tmp.flush()
            tmp_file = tmp.name

        try:
            result = subprocess.run(
                ["python3", filename],
                stdin=open(tmp_file, "r"),
                capture_output=True,
                text=True,
                timeout=5
            )

            actual_output = result.stdout.rstrip()
            expected_output = expected_output.rstrip()

            if actual_output == expected_output:
                console.print(f"[bold green]Sample {i}: PASSED")
            else:
                console.print(f"[bold red]Sample {i}: FAILED")
                panel_expected = Panel(f"Expected:\n{expected_output}", border_style="yellow")
                panel_actual = Panel(f"Actual:\n{actual_output}", border_style="red")
                console.print(panel_expected)
                console.print(panel_actual)
                all_passed = False

        except subprocess.TimeoutExpired:
            console.print(f"[bold red]Sample {i}: TIMEOUT")
            all_passed = False
        except Exception as e:
            console.print(f"[bold red]Sample {i}: ERROR - {e}")
            all_passed = False
        finally:
            if tmp_file:
                try:
                    os.unlink(tmp_file)
                except:
                    pass

    console.print()
    if all_passed:
        console.print("[bold green]All tests passed![/bold green]")
    else:
        console.print("[bold red]Some tests failed.[/bold red]")

    return all_passed


def recommend_random(tier: str):
    """Recommend random problem by tier using solved.ac API."""
    console = Console()

    console.print(f"[cyan]Fetching random problem from tier {tier}...[/cyan]")

    tier_codes = {
        "b1": "5",
        "b2": "4",
        "b3": "3",
        "b4": "2",
        "s1": "10",
        "s2": "9",
        "s3": "8",
        "s4": "7",
        "g1": "15",
        "g2": "14",
        "g3": "13",
        "g4": "12",
        "p1": "20",
        "p2": "19",
        "p3": "18",
        "p4": "17",
        "d": "21",
        "r": "22",
    }

    if tier not in tier_codes:
        console.print(f"[red]Invalid tier: {tier}[/red]")
        console.print(f"[yellow]Valid tiers: bronze(b1-b4), silver(s1-s4), gold(g1-g4), platinum(p1-p4), diamond(d), ruby(r), undefined[/yellow]")
        return

    tier_code = tier_codes[tier]

    response = requests.get(
        f"{SOLVEDAC_API_URL}/search/problem?query=*%20tier:{tier_code}",
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    if not data or "items" not in data:
        console.print("[red]No problems found for this tier[/red]")
        return

    problems = data["items"]

    if problems:
        import random
        problem = random.choice(problems)
        console.print(f"\n[bold green]Recommended problem: #{problem['problemId']} {problem['titleKo']}[/bold green]")
        console.print(f"[cyan]Difficulty: {tier}[/cyan]")
        console.print(f"[dim]URL: https://www.acmicpc.net/problem/{problem['problemId']}[/dim]")
    else:
        console.print("[red]No problems found for this tier[/red]")


def main():
    parser = argparse.ArgumentParser(description="View Baekjoon Online Judge problems in terminal")
    parser.add_argument("problem_id", type=int, nargs="?", help="Problem ID (e.g., 1015)")
    parser.add_argument("--sample", action="store_true", help="Show only sample I/O")
    parser.add_argument("--init", action="store_true", help="Create solution file with template")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file when using --init")
    parser.add_argument("--test", action="store_true", help="Test solution file with sample I/O")
    parser.add_argument("--random", metavar="<tier>", help="Recommend random problem by tier")

    args = parser.parse_args()

    if args.random:
        recommend_random(args.random)
        return

    if args.problem_id is None:
        parser.print_help()
        return

    try:
        html = fetch_problem_page(args.problem_id)
        problem = parse_problem(html, sample_only=args.sample)
        problem["id"] = args.problem_id

        if args.init:
            if args.test:
                print("don't use --init and --test together. use only --init and retry again.")
                return

            filename = create_solution_file(args.problem_id, problem, force=args.force)
            console = Console()
            console.print(f"Created: {filename}")
            return

        if args.test:
            test_solution_file(args.problem_id, problem["samples"])
            return

        display_problem(problem, sample_only=args.sample)

    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch problem: {e}", file=sys.stderr)
        sys.exit(1)
    except FileExistsError as e:
        print(f"[Error] {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
