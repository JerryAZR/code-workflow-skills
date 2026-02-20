#!/usr/bin/env python3
"""
Security Scanner for All Skills
Runs security scans on all skills under the skills/ directory.

USAGE:
  uv run scripts/security_scan_all.py              # Scan all skills
  uv run scripts/security_scan_all.py --verbose   # Detailed scan with pattern checks

EXIT CODES:
  0 - All skills passed
  1 - Some skills failed
  2 - Critical issues found
  3 - gitleaks not installed
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List

# ANSI color codes
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILLS_DIR = SCRIPT_DIR.parent / "skills"

# Use security_scan.py from skill-creator if available, else use local
SECURITY_SCAN_PATHS = [
    Path(__file__).parent / "security_scan.py",
    Path.home() / ".claude" / "plugins" / "cache" / "daymade-skills" / "skill-creator" / "1.4.0" / "skill-creator" / "scripts" / "security_scan.py",
]

# Use uv to run python scripts
PYTHON_CMD = "uv"


def find_security_scan_script() -> Path:
    """Find the security scan script"""
    for script_path in SECURITY_SCAN_PATHS:
        if script_path.exists():
            return script_path
    raise FileNotFoundError("security_scan.py not found")


@dataclass
class ScanResult:
    skill_name: str
    skill_path: Path
    exit_code: int
    stdout: str
    stderr: str


# Folders to exclude from scanning (not actual skills)
EXCLUDED_FOLDERS = {"deprecated"}


def get_skills() -> List[Path]:
    """Get all skill directories"""
    if not SKILLS_DIR.exists():
        print(f"{RED}[ERROR] Skills directory not found: {SKILLS_DIR}{RESET}")
        sys.exit(1)

    skills = []
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name not in EXCLUDED_FOLDERS:
            skills.append(item)
    return skills


def scan_skill(skill_path: Path, verbose: bool = False) -> ScanResult:
    """Run security scan on a single skill"""
    script_path = find_security_scan_script()

    cmd = [PYTHON_CMD, "run", str(script_path), str(skill_path)]
    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return ScanResult(
            skill_name=skill_path.name,
            skill_path=skill_path,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr
        )
    except subprocess.TimeoutExpired:
        return ScanResult(
            skill_name=skill_path.name,
            skill_path=skill_path,
            exit_code=4,
            stdout="",
            stderr="Scan timed out"
        )
    except Exception as e:
        return ScanResult(
            skill_name=skill_name,
            skill_path=skill_path,
            exit_code=4,
            stdout="",
            stderr=str(e)
        )


def get_exit_code_description(code: int) -> str:
    """Get description for exit code"""
    descriptions = {
        0: "PASS",
        1: "HIGH severity",
        2: "CRITICAL",
        3: "gitleaks not installed",
        4: "Scan error"
    }
    return descriptions.get(code, f"Code {code}")


def main():
    parser = argparse.ArgumentParser(
        description="Security scanner for all skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/security_scan_all.py              # Scan all skills
  uv run scripts/security_scan_all.py --verbose   # Detailed scan with pattern checks
        """
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed educational review with pattern-based checks")

    args = parser.parse_args()

    # Find security scan script
    try:
        script_path = find_security_scan_script()
        print(f"{BLUE}[INFO] Using security scan: {script_path}{RESET}\n")
    except FileNotFoundError as e:
        print(f"{RED}[ERROR] {e}{RESET}")
        sys.exit(1)

    # Get all skills
    skills = get_skills()
    print(f"{BLUE}[INFO] Found {len(skills)} skills to scan{RESET}\n")

    # Scan each skill
    results: List[ScanResult] = []
    for skill_path in skills:
        print(f"{BLUE}[SCAN] {skill_path.name}{RESET}")
        result = scan_skill(skill_path, args.verbose)
        results.append(result)

        if result.exit_code == 0:
            print(f"  {GREEN}[PASS]{RESET} {get_exit_code_description(result.exit_code)}")
        elif result.exit_code == 3:
            print(f"  {RED}[ERROR]{RESET} {get_exit_code_description(result.exit_code)}")
        else:
            print(f"  {RED}[FAIL]{RESET} {get_exit_code_description(result.exit_code)}")

        # Print summary of issues if verbose
        if args.verbose and result.exit_code != 0 and result.stdout:
            # Print just the summary lines from the scan
            for line in result.stdout.split('\n'):
                if any(marker in line for marker in ['[CRIT]', '[HIGH]', '[FAIL]', '[PASS]']):
                    print(f"    {line}")

        print()

    # Summary
    passed = sum(1 for r in results if r.exit_code == 0)
    failed = sum(1 for r in results if r.exit_code in (1, 2))
    errors = sum(1 for r in results if r.exit_code in (3, 4))
    critical = sum(1 for r in results if r.exit_code == 2)

    print(f"{'=' * 60}")
    print(f"{BLUE}[SUMMARY]{RESET}")
    print(f"  Total skills scanned: {len(results)}")
    print(f"  {GREEN}Passed: {passed}{RESET}")
    print(f"  {RED}Failed: {failed}{RESET}")
    if errors > 0:
        print(f"  {YELLOW}Errors: {errors}{RESET}")
    if critical > 0:
        print(f"  {RED}Critical issues: {critical}{RESET}")
    print(f"{'=' * 60}\n")

    # Exit code
    if critical > 0:
        sys.exit(2)
    elif failed > 0:
        sys.exit(1)
    elif errors > 0:
        sys.exit(3)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
