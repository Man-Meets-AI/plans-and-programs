#!/usr/bin/env python3
"""Generate an interpretive codebase intake report."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


ROOT = Path.cwd().resolve()
REPORT_NAME = "codebase-shape.md"
MAX_STACK_FILE_CHARS = 20_000
MAX_COMMAND_OUTPUT_CHARS = 40_000
MAX_SCAN_SAMPLES = 80
COMMAND_HEARTBEAT_SECONDS = 15
START_TIME = time.monotonic()
STATUS_ENABLED = True

TEXT_CACHE: dict[Path, str] = {}
JSON_CACHE: dict[Path, object | None] = {}

TOOLING_DIR_NAMES = {
    ".cursor",
    ".claude",
}

EXCLUDE_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".codex",
    ".sandcastle",
    "node_modules",
    "bower_components",
    "jspm_packages",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".expo",
    "dist",
    "build",
    "out",
    "coverage",
    ".nyc_output",
    ".cache",
    ".turbo",
    ".parcel-cache",
    ".vite",
    ".vercel",
    ".netlify",
    "playwright-report",
    "test-results",
    "venv",
    ".venv",
    "env",
    ".env",
    "virtualenv",
    "site-packages",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "vendor",
    "target",
    "bin",
    "obj",
    ".gradle",
    "Pods",
    "DerivedData",
    "_build",
    "deps",
    ".elixir_ls",
    ".serverless",
    ".webpack",
    "tmp",
    "temp",
    "logs",
    "log",
    ".idea",
    ".vscode",
}

EXCLUDE_DIR_RELPATHS = {
    ".ai/current",
    ".claude/worktrees",
    "packages/db/dist",
    "supabase/backups",
}

INTAKE_FILE_NAMES = {
    "codebase-intake.py",
    "codebase-intake.README.md",
    "codebase-shape.py",
    "codebase-extra-scan.sh",
    REPORT_NAME,
}

LOCKFILE_NAMES = {
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "Cargo.lock",
    "Gemfile.lock",
    "Pipfile.lock",
    "poetry.lock",
    "composer.lock",
    "mix.lock",
}

BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".icns",
    ".svgz",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".bz2",
    ".7z",
    ".rar",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".eot",
    ".pyc",
    ".pyo",
    ".class",
    ".o",
    ".so",
    ".dll",
    ".dylib",
    ".exe",
    ".map",
    ".log",
}

DOCUMENTATION_SUFFIXES = {
    ".md",
    ".mdx",
    ".rst",
    ".txt",
    ".adoc",
}

CODE_SUFFIXES = {
    ".ex",
    ".exs",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".py",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".swift",
    ".cs",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".m",
    ".mm",
    ".php",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".sql",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".vue",
    ".svelte",
    ".astro",
}

CONFIG_SUFFIXES = {
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".ini",
    ".cfg",
    ".conf",
    ".env.example",
}

SPECIAL_CODE_FILE_NAMES = {
    "Dockerfile",
    "Makefile",
    "Procfile",
    "Rakefile",
    "Gemfile",
    "Pipfile",
}

STACK_SIGNAL_NAMES = {
    "package.json",
    "tsconfig.json",
    "jsconfig.json",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "vite.config.js",
    "vite.config.ts",
    "vitest.config.js",
    "vitest.config.ts",
    "playwright.config.js",
    "playwright.config.ts",
    "tailwind.config.js",
    "tailwind.config.mjs",
    "tailwind.config.ts",
    "postcss.config.js",
    "postcss.config.mjs",
    "eslint.config.js",
    "eslint.config.mjs",
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.json",
    "biome.json",
    "components.json",
    "convex.json",
    "drizzle.config.js",
    "drizzle.config.mjs",
    "drizzle.config.ts",
    "wrangler.toml",
    "vercel.json",
    "turbo.json",
    "nx.json",
    "netlify.toml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "prisma.schema",
    "schema.prisma",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    "Gemfile",
    "mix.exs",
    "mix.lock",
    ".formatter.exs",
    "config.exs",
    "runtime.exs",
    "prod.exs",
    "dev.exs",
    "test.exs",
    "Makefile",
    "AGENTS.md",
    "README.md",
}

LANGUAGE_BY_SUFFIX = {
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".py": "Python",
    ".rb": "Ruby",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".swift": "Swift",
    ".cs": "C#",
    ".c": "C/C++",
    ".h": "C/C++",
    ".cpp": "C/C++",
    ".hpp": "C/C++",
    ".php": "PHP",
}


@dataclass(frozen=True)
class FileInfo:
    path: Path
    relpath: str
    name: str
    suffix: str
    lines: int
    top_folder: str


@dataclass
class ScanResult:
    title: str
    total: int
    by_file: Counter[str]
    samples: list[str]
    truncated: bool


@dataclass
class CommandResult:
    title: str
    command: str
    cwd: str
    returncode: int | None
    output: str
    timed_out: bool = False


@dataclass(frozen=True)
class AuditFinding:
    severity: str
    area: str
    finding: str
    why: str
    target: str


@dataclass(frozen=True)
class AuditPackReport:
    name: str
    summary: str
    findings: list[AuditFinding]
    recommended_commands: list[str]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace(os.sep, "/")


def path_parts(relpath: str) -> tuple[str, ...]:
    return Path(relpath).parts


def status(message: str) -> None:
    if not STATUS_ENABLED:
        return
    elapsed = time.monotonic() - START_TIME
    print(f"[{elapsed:6.1f}s] {message}", file=sys.stderr, flush=True)


def is_tooling_dir_name(name: str) -> bool:
    return name in TOOLING_DIR_NAMES


def is_excluded_dir(path: Path, include_tooling: bool) -> bool:
    if path.name in EXCLUDE_DIR_NAMES:
        return True
    if is_excluded_dir_relpath(path):
        return True
    if not include_tooling and is_tooling_dir_name(path.name):
        return True
    return False


def normalized_relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace(os.sep, "/")
    except ValueError:
        return path.name


def is_excluded_dir_relpath(path: Path) -> bool:
    return normalized_relpath(path) in EXCLUDE_DIR_RELPATHS


def is_under_excluded_dir_relpath(path: Path) -> bool:
    relpath = normalized_relpath(path)
    return any(relpath == excluded or relpath.startswith(f"{excluded}/") for excluded in EXCLUDE_DIR_RELPATHS)


def is_lockfile(path: Path) -> bool:
    return path.name in LOCKFILE_NAMES or path.name.endswith(".lock")


def is_intake_file(path: Path) -> bool:
    return path.name in INTAKE_FILE_NAMES


def is_excluded_file(path: Path, include_lockfiles: bool) -> bool:
    if is_intake_file(path):
        return True
    if path.name == ".DS_Store" or path.name == "Thumbs.db":
        return True
    if path.name.startswith(".env"):
        return True
    if not include_lockfiles and is_lockfile(path):
        return True
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    if path.name.endswith(".min.js") or path.name.endswith(".min.css"):
        return True
    return False


def iter_paths(
    *,
    include_tooling: bool = False,
    include_lockfiles: bool = False,
) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        current = Path(dirpath)
        dirnames[:] = [
            dirname
            for dirname in sorted(dirnames)
            if not is_excluded_dir(current / dirname, include_tooling)
            and not (current / dirname).is_symlink()
        ]

        for filename in sorted(filenames):
            path = current / filename
            if path.is_symlink():
                continue
            if is_excluded_file(path, include_lockfiles):
                continue
            yield path


def looks_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return True

    if b"\0" in chunk:
        return True

    try:
        chunk.decode("utf-8")
        return False
    except UnicodeDecodeError:
        try:
            chunk.decode("latin-1")
            return False
        except UnicodeDecodeError:
            return True


def count_lines(path: Path) -> int:
    try:
        with path.open("rb") as file:
            return sum(1 for _ in file)
    except OSError:
        return 0


def file_type(path: Path) -> str:
    if path.name in SPECIAL_CODE_FILE_NAMES:
        return path.name
    if path.suffix:
        return path.suffix.lower()
    return "[no extension]"


def build_file_infos(include_tooling: bool) -> list[FileInfo]:
    infos: list[FileInfo] = []
    for path in iter_paths(include_tooling=include_tooling, include_lockfiles=False):
        if looks_binary(path):
            continue

        relpath = rel(path)
        parts = path_parts(relpath)
        top_folder = parts[0] if len(parts) > 1 else "."
        infos.append(
            FileInfo(
                path=path,
                relpath=relpath,
                name=path.name,
                suffix=path.suffix.lower(),
                lines=count_lines(path),
                top_folder=top_folder,
            )
        )
    return infos


def read_text(path: Path, max_chars: int | None = None) -> str:
    if path not in TEXT_CACHE:
        try:
            TEXT_CACHE[path] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            TEXT_CACHE[path] = path.read_text(encoding="latin-1")
        except OSError as exc:
            TEXT_CACHE[path] = f"Could not read file: {exc}"

    text = TEXT_CACHE[path]

    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n\n...[truncated]"
    return text


def iter_text_lines(path: Path) -> Iterable[tuple[int, str]]:
    for line_number, line in enumerate(read_text(path).splitlines(), 1):
        yield line_number, line


def markdown_cell(value: object) -> str:
    text = str(value)
    text = text.replace("|", "\\|")
    text = text.replace("\n", "<br>")
    return text


def md_table(
    rows: Sequence[Sequence[object]],
    headers: Sequence[str],
    numeric_columns: set[int] | None = None,
) -> str:
    numeric_columns = numeric_columns or set()
    separator = ["---:" if index in numeric_columns else "---" for index in range(len(headers))]
    lines = [
        "| " + " | ".join(markdown_cell(header) for header in headers) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(value) for value in row) + " |")
    return "\n".join(lines)


def fenced(text: str, language: str = "text") -> str:
    return f"```{language}\n{text.rstrip()}\n```"


def truncate_line(line: str, max_chars: int = 240) -> str:
    stripped = line.strip()
    if len(stripped) <= max_chars:
        return stripped
    return stripped[: max_chars - 15].rstrip() + " ...[truncated]"


def is_code_or_config(info: FileInfo) -> bool:
    if info.name in SPECIAL_CODE_FILE_NAMES:
        return True
    if info.relpath.startswith(".github/workflows/"):
        return True
    if info.suffix in CODE_SUFFIXES or info.suffix in CONFIG_SUFFIXES:
        return True
    return False


def is_documentation(info: FileInfo) -> bool:
    return info.suffix in DOCUMENTATION_SUFFIXES


def is_test_file(info: FileInfo) -> bool:
    parts = set(path_parts(info.relpath))
    if "__tests__" in parts or "test" in parts or "tests" in parts:
        return True
    return bool(
        re.search(r"\.(test|spec)\.", info.name)
        or info.name.endswith("_test.exs")
        or info.name.endswith("_test.py")
        or info.name.endswith("_test.go")
    )


def is_production_scan_file(info: FileInfo) -> bool:
    return is_code_or_config(info) and not is_documentation(info) and not is_test_file(info)


def is_test_scan_file(info: FileInfo) -> bool:
    return is_code_or_config(info) and is_test_file(info)


def language_rows(file_infos: Sequence[FileInfo]) -> list[tuple[str, int, int]]:
    by_language: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for info in file_infos:
        language = LANGUAGE_BY_SUFFIX.get(info.suffix)
        if language is None:
            continue
        by_language[language][0] += 1
        by_language[language][1] += info.lines

    return [
        (language, counts[0], counts[1])
        for language, counts in sorted(
            by_language.items(),
            key=lambda item: item[1][1],
            reverse=True,
        )
    ]


def type_rows(file_infos: Sequence[FileInfo]) -> list[tuple[str, int, int]]:
    files_by_type: Counter[str] = Counter()
    lines_by_type: Counter[str] = Counter()
    for info in file_infos:
        typ = file_type(info.path)
        files_by_type[typ] += 1
        lines_by_type[typ] += info.lines

    return [
        (typ, files_by_type[typ], lines_by_type[typ])
        for typ in sorted(lines_by_type, key=lambda key: lines_by_type[key], reverse=True)
    ]


def folder_rows(file_infos: Sequence[FileInfo]) -> list[tuple[str, int, int]]:
    files_by_folder: Counter[str] = Counter()
    lines_by_folder: Counter[str] = Counter()
    for info in file_infos:
        files_by_folder[info.top_folder] += 1
        lines_by_folder[info.top_folder] += info.lines

    return [
        (folder, files_by_folder[folder], lines_by_folder[folder])
        for folder in sorted(lines_by_folder, key=lambda key: lines_by_folder[key], reverse=True)
    ]


def two_level_folder_rows(file_infos: Sequence[FileInfo]) -> list[tuple[str, int, int]]:
    files_by_folder: Counter[str] = Counter()
    lines_by_folder: Counter[str] = Counter()
    for info in file_infos:
        parts = path_parts(info.relpath)
        if len(parts) >= 3:
            folder = "/".join(parts[:2])
        elif len(parts) >= 2:
            folder = parts[0]
        else:
            folder = "."
        files_by_folder[folder] += 1
        lines_by_folder[folder] += info.lines

    return [
        (folder, files_by_folder[folder], lines_by_folder[folder])
        for folder in sorted(lines_by_folder, key=lambda key: lines_by_folder[key], reverse=True)
    ]


def build_tree(include_tooling: bool, max_entries: int = 800) -> str:
    lines = [ROOT.name + "/"]
    emitted = 0
    truncated = False

    def allowed(child: Path) -> bool:
        if child.is_symlink():
            return False
        if child.is_dir():
            return not is_excluded_dir(child, include_tooling)
        return not is_excluded_file(child, include_lockfiles=False)

    def walk_dir(directory: Path, prefix: str = "") -> None:
        nonlocal emitted, truncated
        if emitted >= max_entries:
            truncated = True
            return

        try:
            entries = [child for child in directory.iterdir() if allowed(child)]
        except OSError:
            return

        entries.sort(key=lambda item: (item.is_file(), item.name.lower()))
        for index, child in enumerate(entries):
            if emitted >= max_entries:
                truncated = True
                return

            is_last = index == len(entries) - 1
            connector = "`-- " if is_last else "|-- "
            lines.append(prefix + connector + child.name + ("/" if child.is_dir() else ""))
            emitted += 1

            if child.is_dir():
                walk_dir(child, prefix + ("    " if is_last else "|   "))

    walk_dir(ROOT)
    if truncated:
        lines.append("... tree truncated after %d entries" % max_entries)
    return "\n".join(lines)


def find_signal_files(include_tooling: bool) -> list[Path]:
    found: list[Path] = []
    for path in iter_paths(include_tooling=include_tooling, include_lockfiles=True):
        relpath = rel(path)
        if (
            path.name in STACK_SIGNAL_NAMES
            or relpath.endswith("/schema.prisma")
            or relpath.endswith("supabase/config.toml")
            or relpath.startswith("supabase/migrations/")
            or relpath.endswith("/supabase/config.toml")
            or "/supabase/migrations/" in relpath
            or re.match(r"(^|.*/)tsconfig[^/]*\.json$", relpath)
        ):
            found.append(path)
    return sorted(set(found), key=rel)


def find_tooling_files() -> list[str]:
    entries: list[str] = []
    for dirname in sorted(TOOLING_DIR_NAMES):
        path = ROOT / dirname
        if not path.exists():
            continue
        if path.is_dir():
            entries.append(dirname + "/")
            listed_children = 0
            for child in sorted(path.rglob("*")):
                if is_under_excluded_dir_relpath(child):
                    continue
                if child.is_file() and not child.is_symlink():
                    entries.append(rel(child))
                    listed_children += 1
                if listed_children >= 60:
                    break
        elif path.is_file():
            entries.append(dirname)

    copilot = ROOT / ".github" / "copilot-instructions.md"
    if copilot.exists():
        entries.append(rel(copilot))

    return sorted(set(entries))


def detect_mix_roots(signal_files: Sequence[Path]) -> list[Path]:
    return sorted({path.parent for path in signal_files if path.name == "mix.exs"})


def detect_package_files(signal_files: Sequence[Path]) -> list[str]:
    dependency_names = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "Cargo.toml",
        "go.mod",
        "composer.json",
        "Gemfile",
        "mix.exs",
        "mix.lock",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "bun.lock",
        "Cargo.lock",
        "Gemfile.lock",
        "poetry.lock",
    }
    return [rel(path) for path in signal_files if path.name in dependency_names]


def detect_runtime_files(signal_files: Sequence[Path]) -> list[str]:
    runtime_names = {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "vercel.json",
        "netlify.toml",
        "wrangler.toml",
        "fly.toml",
        "railway.json",
        "Makefile",
    }
    runtime = [rel(path) for path in signal_files if path.name in runtime_names]
    workflows = []
    github_workflows = ROOT / ".github" / "workflows"
    if github_workflows.exists():
        workflows = [
            rel(path)
            for path in sorted(github_workflows.rglob("*"))
            if path.is_file() and not path.is_symlink()
        ]
    return sorted(set(runtime + workflows))


def has_phoenix(signal_files: Sequence[Path], file_infos: Sequence[FileInfo]) -> bool:
    for path in signal_files:
        if path.name == "mix.exs" and "phoenix" in read_text(path, 120_000).lower():
            return True
    for info in file_infos:
        relpath = info.relpath.lower()
        if relpath.endswith("router.ex") or relpath.endswith("endpoint.ex"):
            return True
        if "_web/" in relpath or "phoenix" in relpath:
            return True
    return False


def detect_stack_descriptors(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
) -> list[str]:
    descriptors: list[str] = []
    names = {path.name for path in signal_files}
    relpaths = {rel(path) for path in signal_files}
    dependencies = all_package_dependencies(signal_files)
    mix_roots = detect_mix_roots(signal_files)

    if mix_roots:
        descriptor = "Elixir / Mix"
        if has_phoenix(signal_files, file_infos):
            descriptor += " / Phoenix-ish"
        descriptors.append(descriptor)
    if "package.json" in names:
        descriptor = "JavaScript/TypeScript package"
        if "next" in dependencies or any(name.startswith("next.config.") for name in names):
            descriptor += " / Next.js"
        elif "vite" in dependencies or any(name.startswith("vite.config.") for name in names):
            descriptor += " / Vite"
        descriptors.append(descriptor)
    if any(info.suffix in {".ts", ".tsx"} for info in file_infos) or any(path.name.startswith("tsconfig") for path in signal_files):
        descriptors.append("TypeScript")
    if "tailwindcss" in dependencies or any(path.name.startswith("tailwind.config.") for path in signal_files):
        descriptors.append("Tailwind CSS")
    if (
        "@supabase/supabase-js" in dependencies
        or "supabase/config.toml" in relpaths
        or any(relpath.startswith("supabase/migrations/") or "/supabase/migrations/" in relpath for relpath in relpaths)
    ):
        descriptors.append("Supabase / Postgres")
    if "prisma" in dependencies or "@prisma/client" in dependencies or "schema.prisma" in names:
        descriptors.append("Prisma")
    if "drizzle-orm" in dependencies or "drizzle-kit" in dependencies or any(path.name.startswith("drizzle.config.") for path in signal_files):
        descriptors.append("Drizzle")
    if "pyproject.toml" in names or "requirements.txt" in names:
        descriptors.append("Python")
    if "Cargo.toml" in names:
        descriptors.append("Rust")
    if "go.mod" in names:
        descriptors.append("Go")
    if "Dockerfile" in names or "docker-compose.yml" in names or "docker-compose.yaml" in names:
        descriptors.append("Dockerized runtime")

    if not descriptors:
        descriptors.append("Undetermined from common stack signal files")
    return descriptors


def describe_repo_shape(
    stack_descriptors: Sequence[str],
    file_infos: Sequence[FileInfo],
    test_ratio: float | None,
) -> str:
    relpaths = [info.relpath.lower() for info in file_infos]
    if any(descriptor.startswith("Elixir / Mix") for descriptor in stack_descriptors):
        parts = ["Elixir service with Mix"]
        if any("Phoenix-ish" in descriptor for descriptor in stack_descriptors):
            parts.append("Phoenix web components")
        if any("codex" in relpath for relpath in relpaths):
            parts.append("Codex app-server integration")
        if any("linear" in relpath for relpath in relpaths):
            parts.append("Linear integration")
        if any("ssh" in relpath for relpath in relpaths):
            parts.append("SSH worker support")
        if test_ratio is not None and test_ratio >= 0.6:
            parts.append("substantial ExUnit coverage")
        return ", ".join(parts) + "."

    if any("JavaScript/TypeScript" in descriptor for descriptor in stack_descriptors):
        parts = ["JavaScript/TypeScript application"]
        if any("Next.js" in descriptor for descriptor in stack_descriptors):
            parts.append("Next.js web surface")
        elif any("Vite" in descriptor for descriptor in stack_descriptors):
            parts.append("Vite frontend")
        if "Tailwind CSS" in stack_descriptors:
            parts.append("Tailwind styling")
        if "Supabase / Postgres" in stack_descriptors:
            parts.append("Supabase/Postgres data boundary")
        if "Prisma" in stack_descriptors:
            parts.append("Prisma ORM")
        if "Drizzle" in stack_descriptors:
            parts.append("Drizzle ORM")
        return ", ".join(parts) + "."

    return ", ".join(stack_descriptors) + "."


def parse_make_targets(path: Path) -> list[str]:
    text = read_text(path)
    phony_match = re.search(r"^\.PHONY:\s*(.+)$", text, flags=re.MULTILINE)
    targets: list[str] = []
    if phony_match:
        targets.extend(phony_match.group(1).split())

    for match in re.finditer(r"^([A-Za-z0-9_.-]+)\s*:(?![=])", text, flags=re.MULTILINE):
        target = match.group(1)
        if target.startswith("."):
            continue
        if target not in targets:
            targets.append(target)

    return targets


def parse_package_scripts(path: Path) -> list[str]:
    data = load_json_config(path)
    if not isinstance(data, dict):
        return []
    scripts = data.get("scripts") or {}
    if not isinstance(scripts, dict):
        return []
    return sorted(scripts)


def strip_json_comments(text: str) -> str:
    output: list[str] = []
    in_string = False
    string_quote = ""
    escaped = False
    index = 0

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == string_quote:
                in_string = False
            index += 1
            continue

        if char in {"'", '"'}:
            in_string = True
            string_quote = char
            output.append(char)
            index += 1
            continue

        if char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue

        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue

        output.append(char)
        index += 1

    uncommented = "".join(output)
    return re.sub(r",\s*([}\]])", r"\1", uncommented)


def load_json_config(path: Path) -> object | None:
    if path in JSON_CACHE:
        return JSON_CACHE[path]

    text = read_text(path)
    try:
        JSON_CACHE[path] = json.loads(text)
    except json.JSONDecodeError:
        try:
            JSON_CACHE[path] = json.loads(strip_json_comments(text))
        except json.JSONDecodeError:
            JSON_CACHE[path] = None

    return JSON_CACHE[path]


def package_json_paths(signal_files: Sequence[Path]) -> list[Path]:
    return sorted({path for path in signal_files if path.name == "package.json"}, key=rel)


def package_json_data(path: Path) -> dict[str, object]:
    data = load_json_config(path)
    return data if isinstance(data, dict) else {}


def package_dependencies(package_json: dict[str, object]) -> set[str]:
    names: set[str] = set()
    for key in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        deps = package_json.get(key) or {}
        if isinstance(deps, dict):
            names.update(str(name) for name in deps)
    return names


def package_scripts(package_json: dict[str, object]) -> dict[str, str]:
    scripts = package_json.get("scripts") or {}
    if not isinstance(scripts, dict):
        return {}
    return {str(name): str(command) for name, command in scripts.items()}


def package_manager_for_root(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lock").exists() or (root / "bun.lockb").exists():
        return "bun"
    return "npm"


def package_run_command(root: Path, script: str) -> list[str]:
    manager = package_manager_for_root(root)
    if manager == "pnpm":
        return ["pnpm", "run", script]
    if manager == "yarn":
        return ["yarn", "run", script]
    if manager == "bun":
        return ["bun", "run", script]
    return ["npm", "run", script]


def package_script_display(root: Path, script: str) -> str:
    return " ".join(package_run_command(root, script))


def all_package_dependencies(signal_files: Sequence[Path]) -> set[str]:
    dependencies: set[str] = set()
    for path in package_json_paths(signal_files):
        dependencies.update(package_dependencies(package_json_data(path)))
    return dependencies


def parse_mix_aliases(path: Path) -> list[str]:
    text = read_text(path, 120_000)
    match = re.search(r"defp\s+aliases\s+do\s*(.*?)\n\s*end", text, flags=re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    return sorted(set(re.findall(r"^\s*([a-zA-Z_][\w]*)\s*:\s*\[", block, flags=re.MULTILINE)))


def discover_commands(signal_files: Sequence[Path], phoenix: bool) -> dict[str, object]:
    make_targets: dict[str, list[str]] = {}
    package_scripts: dict[str, list[str]] = {}
    mix_aliases: dict[str, list[str]] = {}
    likely: dict[str, list[str]] = defaultdict(list)

    for path in signal_files:
        if path.name == "Makefile":
            targets = parse_make_targets(path)
            target_set = set(targets)
            main_targets = [target for target in targets if target not in {"help", "all"}]
            make_targets[rel(path)] = main_targets

            categories = {
                "Install": ["setup", "deps", "install", "bootstrap"],
                "Dev": ["dev", "serve", "server", "start"],
                "Test": ["test", "coverage", "e2e"],
                "Lint": ["lint", "dialyzer", "credo"],
                "Format": ["fmt-check", "format-check", "fmt", "format"],
                "Build": ["build", "compile"],
                "CI": ["ci", "all"],
            }
            for category, names in categories.items():
                for name in names:
                    if name in target_set:
                        likely[category].append(f"make {name}")

        elif path.name == "package.json":
            scripts = parse_package_scripts(path)
            package_scripts[rel(path)] = scripts
            package_root = path.parent
            for script in scripts:
                command = package_script_display(package_root, script)
                lower = script.lower()
                if lower in {"dev", "start", "serve"}:
                    likely["Dev"].append(command)
                elif "test" in lower:
                    likely["Test"].append(command)
                elif lower in {"typecheck", "type-check", "check-types"} or "typecheck" in lower:
                    likely["Typecheck"].append(command)
                elif "lint" in lower:
                    likely["Lint"].append(command)
                elif "format" in lower or lower == "fmt":
                    likely["Format"].append(command)
                elif "build" in lower:
                    likely["Build"].append(command)

        elif path.name == "mix.exs":
            aliases = parse_mix_aliases(path)
            mix_aliases[rel(path)] = aliases
            likely["Install"].append("mix deps.get")
            if phoenix:
                likely["Dev"].append("mix phx.server")
            likely["Test"].append("mix test")
            likely["Format"].append("mix format --check-formatted")
            likely["Lint"].append("mix credo --strict")
            likely["Lint"].append("mix dialyzer")
            if "build" in aliases:
                likely["Build"].append("mix build")
            else:
                likely["Build"].append("mix compile")
            likely["Security"].append("mix deps.audit")
            likely["Security"].append("mix hex.audit")
            likely["Security"].append("mix sobelow")

        elif path.name == "Cargo.toml":
            likely["Test"].append("cargo test")
            likely["Lint"].append("cargo clippy")
            likely["Format"].append("cargo fmt --check")
            likely["Build"].append("cargo build")

        elif path.name == "go.mod":
            likely["Test"].append("go test ./...")
            likely["Format"].append("gofmt -w .")
            likely["Build"].append("go build ./...")

        elif path.name == "pyproject.toml":
            likely["Test"].append("pytest")
            likely["Lint"].append("ruff check .")
            likely["Format"].append("ruff format --check .")

    deduped_likely = {
        category: list(dict.fromkeys(commands))
        for category, commands in sorted(likely.items())
        if commands
    }
    return {
        "make_targets": make_targets,
        "package_scripts": package_scripts,
        "mix_aliases": mix_aliases,
        "likely": deduped_likely,
    }


def elixir_source_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [
        info
        for info in file_infos
        if info.suffix == ".ex" and "/lib/" in f"/{info.relpath}" and not is_test_file(info)
    ]


def elixir_test_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [
        info
        for info in file_infos
        if info.name.endswith("_test.exs") and "/test/" in f"/{info.relpath}"
    ]


def expected_elixir_test_path(source: FileInfo, mix_roots: Sequence[Path]) -> Path | None:
    for root in sorted(mix_roots, key=lambda candidate: len(rel(candidate))):
        lib_root = root / "lib"
        try:
            rel_under_lib = source.path.relative_to(lib_root)
        except ValueError:
            continue
        return root / "test" / rel_under_lib.parent / f"{rel_under_lib.stem}_test.exs"
    return None


def test_metrics(file_infos: Sequence[FileInfo], mix_roots: Sequence[Path]) -> dict[str, object]:
    source_infos = elixir_source_infos(file_infos)
    test_infos = elixir_test_infos(file_infos)
    if not source_infos and not test_infos:
        source_infos = [info for info in file_infos if is_code_or_config(info) and not is_test_file(info)]
        test_infos = [info for info in file_infos if is_test_scan_file(info)]

    source_lines = sum(info.lines for info in source_infos)
    test_lines = sum(info.lines for info in test_infos)
    ratio = (test_lines / source_lines) if source_lines else None

    unpaired: list[FileInfo] = []
    if mix_roots:
        for source in source_infos:
            expected = expected_elixir_test_path(source, mix_roots)
            if expected is not None and not expected.exists():
                unpaired.append(source)

    return {
        "source_infos": sorted(source_infos, key=lambda info: info.lines, reverse=True),
        "test_infos": sorted(test_infos, key=lambda info: info.lines, reverse=True),
        "source_lines": source_lines,
        "test_lines": test_lines,
        "ratio": ratio,
        "unpaired": sorted(unpaired, key=lambda info: info.lines, reverse=True),
    }


def git_recent_changes(file_infos: Sequence[FileInfo]) -> Counter[str]:
    if not (ROOT / ".git").exists() or shutil.which("git") is None:
        return Counter()

    info_by_relpath = {info.relpath for info in file_infos if is_code_or_config(info)}
    try:
        result = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:", "--since=90 days ago"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return Counter()

    changes: Counter[str] = Counter()
    for line in result.stdout.splitlines():
        relpath = line.strip()
        if relpath and relpath in info_by_relpath:
            changes[relpath] += 1
    return changes


def hotspot_rows(file_infos: Sequence[FileInfo], changes: Counter[str]) -> list[tuple[int, str, int, int]]:
    info_by_relpath = {info.relpath: info for info in file_infos if is_code_or_config(info)}
    rows: list[tuple[int, str, int, int]] = []
    for relpath, change_count in changes.items():
        info = info_by_relpath.get(relpath)
        if info is None:
            continue
        score = info.lines * change_count
        rows.append((score, relpath, info.lines, change_count))
    return sorted(rows, reverse=True)


def elixir_api_surface(file_infos: Sequence[FileInfo]) -> list[tuple[str, int, int, int, int, int]]:
    rows: list[tuple[str, int, int, int, int, int]] = []
    module_pattern = re.compile(r"^\s*defmodule\s+")
    public_pattern = re.compile(r"^\s*def\s+")
    private_pattern = re.compile(r"^\s*defp\s+")
    callback_pattern = re.compile(
        r"^\s*(use\s+(GenServer|Phoenix\.LiveView|Phoenix\.Controller|Phoenix\.Component)|"
        r"def\s+(init|handle_call|handle_cast|handle_info|terminate|code_change)\b)"
    )

    for info in file_infos:
        if info.suffix not in {".ex", ".exs"}:
            continue

        modules = public_defs = private_defs = callbacks = 0
        for _, line in iter_text_lines(info.path):
            if module_pattern.search(line):
                modules += 1
            if public_pattern.search(line):
                public_defs += 1
            if private_pattern.search(line):
                private_defs += 1
            if callback_pattern.search(line):
                callbacks += 1

        if modules or public_defs or private_defs or callbacks:
            rows.append((info.relpath, modules, public_defs, private_defs, callbacks, info.lines))

    return sorted(rows, key=lambda row: (row[2], row[5]), reverse=True)


def scan_regex(
    title: str,
    file_infos: Sequence[FileInfo],
    pattern: str,
    *,
    flags: int = 0,
    redact: Callable[[str], str] | None = None,
    max_samples: int = MAX_SCAN_SAMPLES,
) -> ScanResult:
    compiled = re.compile(pattern, flags)
    total = 0
    by_file: Counter[str] = Counter()
    samples: list[str] = []

    for info in file_infos:
        for line_number, line in iter_text_lines(info.path):
            if not compiled.search(line):
                continue
            total += 1
            by_file[info.relpath] += 1
            if len(samples) < max_samples:
                display = truncate_line(line)
                if redact is not None:
                    display = redact(display)
                samples.append(f"{info.relpath}:{line_number}: {display}")

    return ScanResult(
        title=title,
        total=total,
        by_file=by_file,
        samples=samples,
        truncated=total > len(samples),
    )


def redact_secret_line(line: str) -> str:
    return re.sub(
        r"([:=]\s*[\"']?)[^\"'\s]{8,}",
        r"\1[REDACTED]",
        line,
    )


def write_scan_result(file, result: ScanResult) -> None:
    file.write(f"### {result.title}\n\n")
    file.write(f"Total matches: `{result.total}`\n\n")
    if result.by_file:
        rows = [
            (f"`{relpath}`", count)
            for relpath, count in result.by_file.most_common(10)
        ]
        file.write(md_table(rows, ["File", "Matches"], numeric_columns={1}) + "\n\n")
    if result.samples:
        file.write(fenced("\n".join(result.samples)) + "\n\n")
        if result.truncated:
            file.write(f"... truncated after {len(result.samples)} matches\n\n")
    else:
        file.write("No matches found.\n\n")


def architecture_patterns() -> list[tuple[str, str, int]]:
    return [
        (
            "Routes / Controllers / Live Views",
            r"(Phoenix\.Router|scope\s+[\"']|pipe_through|live\s+[\"']|"
            r"\b(get|post|put|patch|delete)\s+[\"']|defmodule\s+.*Controller|"
            r"use\s+Phoenix\.(Controller|LiveView|Component))",
            0,
        ),
        (
            "Workers / Jobs / Cron / Processes",
            r"(Oban|Quantum|use\s+GenServer|Task\.|DynamicSupervisor|Supervisor|"
            r"Process\.send_after|send_after|handle_info|handle_call|handle_cast|"
            r"\bworker\b|\bjob\b|\bcron\b)",
            re.IGNORECASE,
        ),
        (
            "DB / Persistence",
            r"(Repo\.|Ecto\.Schema|schema\s+[\"']|use\s+Ecto\.Schema|postgres|sqlite|redis|"
            r"File\.(write|read|mkdir|mkdir_p|rm|rm_rf)|Workspace)",
            re.IGNORECASE,
        ),
        (
            "External API Clients",
            r"(Req\.|HTTPoison|Tesla|Finch|Mint|:httpc|fetch\(|axios\.|Linear|GitHub|"
            r"OpenAI|Anthropic|Codex)",
            re.IGNORECASE,
        ),
        (
            "Auth / Security",
            r"(auth|authorize|permission|token|secret|password|Bearer|SSH|private_key|"
            r"Plug\.Crypto|basic_auth)",
            re.IGNORECASE,
        ),
        (
            "Billing / Payments",
            r"(stripe|checkout\.sessions|payment_intent|webhook|customer\.created|"
            r"invoice\.|subscription)",
            re.IGNORECASE,
        ),
        (
            "AI / LLM / Agent Code",
            r"(openai|anthropic|claude|gpt-|chat\.completions|responses\.create|"
            r"embeddings|vector|rag|prompt|completion|agent|codex)",
            re.IGNORECASE,
        ),
    ]


def quality_patterns() -> list[tuple[str, str, int, Callable[[str], str] | None]]:
    return [
        ("Work markers: TODO / FIXME / HACK / XXX", r"\b(TODO|FIXME|HACK|XXX)\b", 0, None),
        (
            "TypeScript and lint escape hatches",
            r"(@ts-ignore|@ts-expect-error|eslint-disable|biome-ignore|as any|:\s*any\b)",
            0,
            None,
        ),
        (
            "Debug leftovers",
            r"\b(console\.log|debugger|print\(|println\(|dump\(|var_dump\()",
            0,
            None,
        ),
    ]


def risk_patterns() -> list[tuple[str, str, int, Callable[[str], str] | None]]:
    return [
        (
            "Secrets-shaped strings, redacted",
            r"\b(api[_-]?key|secret|password|passwd|token|private[_-]?key|"
            r"client[_-]?secret|access[_-]?token)\b\s*[:=]\s*[\"']?[^\"'\s]{8,}",
            re.IGNORECASE,
            redact_secret_line,
        ),
        (
            "Unsafe code patterns",
            r"(eval\s*\(|new Function\s*\(|dangerouslySetInnerHTML|innerHTML\s*=|"
            r"document\.write\s*\(|rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED|"
            r"jwt\.decode\s*\(|alg\s*:\s*[\"']none[\"']|\$queryRawUnsafe|executeRawUnsafe|"
            r"csrf\s*:\s*false|origin\s*:\s*[\"']\*[\"']|Code\.eval|:os\.cmd)",
            re.IGNORECASE,
            None,
        ),
        (
            "Auth bypass terms",
            r"(skip[_-]?auth|disable[_-]?auth|bypass[_-]?auth|TODO.*auth|FIXME.*auth|"
            r"is_admin\s*=\s*true|isAdmin\s*=\s*true|admin_override|adminOverride|"
            r"temporary.*auth|no[_-]?auth)",
            re.IGNORECASE,
            None,
        ),
        (
            "Environment variable usage",
            r"(process\.env|import\.meta\.env|Deno\.env|getenv\(|os\.environ|"
            r"System\.get_env|Application\.fetch_env|Application\.get_env|ENV\[)",
            0,
            None,
        ),
        (
            "Raw shell / process execution",
            r"(System\.cmd|Port\.open|:os\.cmd|child_process|subprocess\.|os\.system|"
            r"\bexec\(|\bspawn\()",
            0,
            None,
        ),
        (
            "Network calls",
            r"(Req\.|HTTPoison|Tesla|Finch|Mint|:httpc|fetch\(|axios\.|Faraday|"
            r"Net::HTTP|requests\.|urllib|http\.Client|http\.Get|\bcurl\s+)",
            0,
            None,
        ),
        (
            "Filesystem writes / deletes",
            r"(File\.(rm|rm_rf|write|cp|mkdir|mkdir_p|rename|chmod|touch)|Path\.expand|"
            r"File\.open\([^,\n]+,\s*\[.*(:write|:append)|fs\.(write|unlink|rm|mkdir|rename)|"
            r"shutil\.rmtree|os\.remove|os\.unlink)",
            0,
            None,
        ),
    ]


def run_scan_groups(
    file_infos: Sequence[FileInfo],
    patterns: Sequence[tuple[str, str, int, Callable[[str], str] | None]],
) -> list[ScanResult]:
    return [
        scan_regex(title, file_infos, pattern, flags=flags, redact=redact)
        for title, pattern, flags, redact in patterns
    ]


def run_architecture_scans(file_infos: Sequence[FileInfo]) -> list[ScanResult]:
    return [
        scan_regex(title, file_infos, pattern, flags=flags)
        for title, pattern, flags in architecture_patterns()
    ]


def top_scan_targets(result: ScanResult, limit: int = 3) -> str:
    if not result.by_file:
        return "n/a"
    return ", ".join(f"`{relpath}` ({count})" for relpath, count in result.by_file.most_common(limit))


def audit_finding(
    severity: str,
    area: str,
    finding: str,
    why: str,
    target: str,
) -> AuditFinding:
    return AuditFinding(severity=severity, area=area, finding=finding, why=why, target=target)


def js_like_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [info for info in file_infos if info.suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}]


def ts_like_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [info for info in file_infos if info.suffix in {".ts", ".tsx"}]


def jsx_like_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [info for info in file_infos if info.suffix in {".jsx", ".tsx", ".vue", ".svelte", ".astro"}]


def sql_infos(file_infos: Sequence[FileInfo]) -> list[FileInfo]:
    return [info for info in file_infos if info.suffix == ".sql"]


def find_file_infos(file_infos: Sequence[FileInfo], predicate: Callable[[FileInfo], bool]) -> list[FileInfo]:
    return sorted([info for info in file_infos if predicate(info)], key=lambda info: info.relpath)


def package_script_lookup(signal_files: Sequence[Path]) -> dict[Path, dict[str, str]]:
    return {
        path: package_scripts(package_json_data(path))
        for path in package_json_paths(signal_files)
    }


def audit_typescript_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    ts_files = ts_like_infos(file_infos)
    tsconfig_files = find_file_infos(file_infos, lambda info: re.match(r"tsconfig[^/]*\.json$", info.name) is not None)
    if not ts_files and not tsconfig_files:
        return None

    findings: list[AuditFinding] = []
    commands: list[str] = []
    scripts_by_package = package_script_lookup(signal_files)

    for package_path, scripts in scripts_by_package.items():
        for script in scripts:
            lower = script.lower()
            if lower in {"typecheck", "type-check", "check-types"} or "typecheck" in lower:
                commands.append(package_script_display(package_path.parent, script))

    if not commands:
        findings.append(
            audit_finding(
                "Medium",
                "TypeScript",
                "No package script that clearly runs type checking was detected.",
                "A dedicated typecheck command lets review and CI separate type safety from bundling.",
                "package.json scripts",
            )
        )

    if not tsconfig_files:
        findings.append(
            audit_finding(
                "High",
                "TypeScript",
                "TypeScript files are present but no tsconfig was detected.",
                "Without an explicit compiler configuration, strictness and module boundaries are ambiguous.",
                "tsconfig.json",
            )
        )

    for info in tsconfig_files:
        data = load_json_config(info.path)
        config = data if isinstance(data, dict) else {}
        compiler_options = config.get("compilerOptions") if isinstance(config.get("compilerOptions"), dict) else {}
        if compiler_options.get("strict") is not True:
            findings.append(
                audit_finding(
                    "High",
                    "TypeScript",
                    "`strict` is not enabled.",
                    "The strict flag turns on core type-checking behavior that catches common correctness bugs.",
                    info.relpath,
                )
            )
        if compiler_options.get("noUncheckedIndexedAccess") is not True:
            findings.append(
                audit_finding(
                    "Medium",
                    "TypeScript",
                    "`noUncheckedIndexedAccess` is not enabled.",
                    "Indexed array/object reads otherwise hide possible `undefined` values.",
                    info.relpath,
                )
            )
        if compiler_options.get("exactOptionalPropertyTypes") is not True:
            findings.append(
                audit_finding(
                    "Medium",
                    "TypeScript",
                    "`exactOptionalPropertyTypes` is not enabled.",
                    "Optional properties otherwise conflate omitted values and explicit `undefined`.",
                    info.relpath,
                )
            )
        if compiler_options.get("noImplicitOverride") is not True:
            findings.append(
                audit_finding(
                    "Info",
                    "TypeScript",
                    "`noImplicitOverride` is not enabled.",
                    "Explicit overrides make class inheritance changes easier to audit.",
                    info.relpath,
                )
            )

    escape_scan = scan_regex(
        "Type escape hatches",
        ts_like_infos(production_infos),
        r"(@ts-ignore|@ts-expect-error|as\s+any\b|:\s*any\b|unknown\s+as|JSON\.parse\()",
    )
    if escape_scan.total:
        findings.append(
            audit_finding(
                "Medium",
                "TypeScript",
                f"`{escape_scan.total}` type escape hatch candidates found.",
                "These are valid sometimes, but they are the first places where static guarantees usually leak.",
                top_scan_targets(escape_scan),
            )
        )

    eslint_files = find_file_infos(
        file_infos,
        lambda info: info.name.startswith("eslint.config.") or info.name.startswith(".eslintrc"),
    )
    if eslint_files:
        eslint_text = "\n".join(read_text(info.path, 120_000) for info in eslint_files)
        has_type_checked_config = bool(
            re.search(
                r"(recommendedTypeChecked|strictTypeChecked|recommended-type-checked|strict-type-checked)",
                eslint_text,
            )
        )
        if "@typescript-eslint" in eslint_text or "typescript-eslint" in eslint_text:
            if not has_type_checked_config:
                findings.append(
                    audit_finding(
                        "Medium",
                        "TypeScript ESLint",
                        "ESLint uses TypeScript support but no type-checked shared config was detected.",
                        "Type-aware linting catches unsafe promises, member access, and other bugs the syntax-only pass misses.",
                        ", ".join(info.relpath for info in eslint_files[:3]),
                    )
                )
        else:
            findings.append(
                audit_finding(
                    "Info",
                    "TypeScript ESLint",
                    "ESLint config exists but TypeScript-specific rules were not detected.",
                    "TypeScript projects usually need TypeScript-aware lint rules in addition to base JavaScript linting.",
                    ", ".join(info.relpath for info in eslint_files[:3]),
                )
            )
    else:
        findings.append(
            audit_finding(
                "Medium",
                "TypeScript ESLint",
                "No ESLint config was detected.",
                "Linting is the cheapest way to catch unsafe TypeScript and React patterns before runtime.",
                "eslint.config.* / .eslintrc*",
            )
        )

    return AuditPackReport(
        name="TypeScript",
        summary=f"Detected `{len(ts_files)}` TypeScript files and `{len(tsconfig_files)}` tsconfig files.",
        findings=findings,
        recommended_commands=list(dict.fromkeys(commands)),
    )


def audit_react_next_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    dependencies = all_package_dependencies(signal_files)
    next_files = find_file_infos(file_infos, lambda info: info.name.startswith("next.config."))
    has_next = "next" in dependencies or bool(next_files)
    has_react = "react" in dependencies or any(info.suffix in {".jsx", ".tsx"} for info in file_infos)
    if not has_next and not has_react:
        return None

    findings: list[AuditFinding] = []
    commands: list[str] = []
    scripts_by_package = package_script_lookup(signal_files)
    for package_path, scripts in scripts_by_package.items():
        for script in scripts:
            lower = script.lower()
            if "lint" in lower or "build" in lower or "test" in lower:
                commands.append(package_script_display(package_path.parent, script))

    if has_next:
        if not next_files:
            findings.append(
                audit_finding(
                    "Info",
                    "Next.js",
                    "Next.js dependency detected but no `next.config.*` file was found.",
                    "The config is where production controls such as headers, redirects, and `poweredByHeader` usually live.",
                    "next.config.*",
                )
            )
        else:
            config_text = "\n".join(read_text(info.path, 120_000) for info in next_files)
            if not re.search(r"poweredByHeader\s*:\s*false", config_text):
                findings.append(
                    audit_finding(
                        "Info",
                        "Next.js Security",
                        "`poweredByHeader: false` was not detected.",
                        "Disabling framework disclosure is a low-cost hardening step for public apps.",
                        ", ".join(info.relpath for info in next_files),
                    )
                )
            if not re.search(r"(Content-Security-Policy|headers\s*\()", config_text):
                findings.append(
                    audit_finding(
                        "Medium",
                        "Next.js Security",
                        "No obvious security headers or CSP configuration was detected.",
                        "A CSP and security headers reduce XSS, clickjacking, and injection blast radius.",
                        ", ".join(info.relpath for info in next_files),
                    )
                )

    public_env_scan = scan_regex(
        "Suspicious public env names",
        production_infos,
        r"NEXT_PUBLIC_[A-Z0-9_]*(SECRET|TOKEN|PRIVATE|SERVICE|DATABASE|PASSWORD|KEY)[A-Z0-9_]*",
    )
    if public_env_scan.total:
        findings.append(
            audit_finding(
                "High",
                "Next.js Environment",
                f"`{public_env_scan.total}` suspicious `NEXT_PUBLIC_*` env references found.",
                "`NEXT_PUBLIC_*` values are bundled for browser use; secrets and service keys must stay server-side.",
                top_scan_targets(public_env_scan),
            )
        )

    client_secret_scan = scan_regex(
        "Client-side secret/service role references",
        jsx_like_infos(production_infos),
        r"(SERVICE_ROLE|service[_-]?role|SUPABASE_SERVICE_ROLE|DATABASE_URL|PRIVATE_KEY|SECRET)",
        flags=re.IGNORECASE,
    )
    if client_secret_scan.total:
        findings.append(
            audit_finding(
                "High",
                "React / Next.js Boundary",
                f"`{client_secret_scan.total}` secret-shaped references appear in component-like files.",
                "Client-rendered modules can be bundled to the browser, so server secrets must be isolated.",
                top_scan_targets(client_secret_scan),
            )
        )

    use_client_scan = scan_regex(
        "Client component boundaries",
        jsx_like_infos(production_infos),
        r"^\s*[\"']use client[\"']",
    )
    if has_next and use_client_scan.total >= 20:
        findings.append(
            audit_finding(
                "Info",
                "Next.js App Router",
                f"`{use_client_scan.total}` client component boundaries found.",
                "A broad client surface increases bundle size and can pull code across server/client boundaries.",
                top_scan_targets(use_client_scan),
            )
        )

    mutation_without_auth: Counter[str] = Counter()
    for info in production_infos:
        relpath = info.relpath
        is_route = (
            re.search(r"(^|/)app/.*/route\.(ts|tsx|js|jsx)$", relpath)
            or re.search(r"(^|/)pages/api/.*\.(ts|tsx|js|jsx)$", relpath)
        )
        if not is_route:
            continue
        text = read_text(info.path, 120_000)
        has_mutation = re.search(r"\b(insert|update|delete|upsert|create|patch|mutate)\b", text, re.IGNORECASE)
        has_auth = re.search(r"(auth\(|getServerSession|getUser\(|requireUser|requireAuth|currentUser|verify)", text)
        if has_mutation and not has_auth:
            mutation_without_auth[info.relpath] += 1
    if mutation_without_auth:
        findings.append(
            audit_finding(
                "Medium",
                "API Authorization",
                f"`{sum(mutation_without_auth.values())}` mutating route handlers without obvious auth checks.",
                "Mutating HTTP handlers should make authorization explicit at the boundary.",
                ", ".join(f"`{relpath}`" for relpath, _ in mutation_without_auth.most_common(5)),
            )
        )

    return AuditPackReport(
        name="React / Next.js",
        summary="Detected React/Next.js UI surface." if has_next else "Detected React-style UI surface.",
        findings=findings,
        recommended_commands=list(dict.fromkeys(commands)),
    )


def audit_tailwind_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    dependencies = all_package_dependencies(signal_files)
    tailwind_files = find_file_infos(file_infos, lambda info: "tailwind" in info.name)
    css_tailwind_scan = scan_regex(
        "Tailwind CSS imports",
        [info for info in file_infos if info.suffix in {".css", ".scss", ".sass"}],
        r"(@import\s+[\"']tailwindcss[\"']|@tailwind\s+(base|components|utilities))",
    )
    if "tailwindcss" not in dependencies and not tailwind_files and css_tailwind_scan.total == 0:
        return None

    findings: list[AuditFinding] = []
    dynamic_class_scan = scan_regex(
        "Dynamic Tailwind class construction",
        jsx_like_infos(production_infos) + [info for info in production_infos if info.suffix in {".html", ".js", ".ts"}],
        r"((bg|text|border|ring|from|via|to|grid-cols|col-span|row-span|w|h|p|m)-\$\{|\$\{[^}\n]+\}-(50|100|200|300|400|500|600|700|800|900|950))",
    )
    if dynamic_class_scan.total:
        findings.append(
            audit_finding(
                "High",
                "Tailwind CSS",
                f"`{dynamic_class_scan.total}` dynamically constructed utility class candidates found.",
                "Tailwind scans source text and cannot generate classes that only exist after string interpolation.",
                top_scan_targets(dynamic_class_scan),
            )
        )

    broad_content_targets: list[str] = []
    for info in tailwind_files:
        text = read_text(info.path, 120_000)
        if re.search(r"content\s*:\s*\[[^\]]*['\"](\./)?\*\*/\*[^'\"]*['\"]", text, re.DOTALL):
            broad_content_targets.append(info.relpath)
    if broad_content_targets:
        findings.append(
            audit_finding(
                "Medium",
                "Tailwind CSS",
                "Broad content globs were detected.",
                "Overly broad scanning can slow builds and accidentally include classes from generated or unrelated files.",
                ", ".join(f"`{target}`" for target in broad_content_targets[:5]),
            )
        )

    if "class-variance-authority" in dependencies or "tailwind-variants" in dependencies:
        findings.append(
            audit_finding(
                "Info",
                "Tailwind CSS",
                "Variant helper dependency detected.",
                "Inspect variant maps for complete static class names and avoid interpolated utility fragments.",
                "package.json dependencies",
            )
        )

    commands: list[str] = []
    for package_path, scripts in package_script_lookup(signal_files).items():
        for script in scripts:
            lower = script.lower()
            if "build" in lower or "lint" in lower:
                commands.append(package_script_display(package_path.parent, script))

    return AuditPackReport(
        name="Tailwind CSS",
        summary=f"Detected Tailwind via `{len(tailwind_files)}` config-like files and `{css_tailwind_scan.total}` CSS import/directive matches.",
        findings=findings,
        recommended_commands=list(dict.fromkeys(commands)),
    )


def normalize_sql_identifier(identifier: str) -> str:
    return identifier.strip().strip('"').lower()


def extract_sql_table_name(match: re.Match[str]) -> str:
    schema = match.group("schema")
    table = match.group("table")
    if schema:
        return f"{normalize_sql_identifier(schema)}.{normalize_sql_identifier(table)}"
    return f"public.{normalize_sql_identifier(table)}"


def audit_supabase_postgres_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    dependencies = all_package_dependencies(signal_files)
    relpaths = {info.relpath for info in file_infos}
    has_supabase = (
        "@supabase/supabase-js" in dependencies
        or any(relpath.endswith("supabase/config.toml") for relpath in relpaths)
        or any("/supabase/migrations/" in f"/{relpath}" for relpath in relpaths)
    )
    if not has_supabase:
        return None

    findings: list[AuditFinding] = []
    commands = ["supabase db lint --fail-on warning"]
    if any("/supabase/tests/" in f"/{relpath}" for relpath in relpaths):
        commands.append("supabase test db")
    commands.append("supabase gen types --lang typescript --local")

    sql_files = sql_infos(file_infos)
    sql_text_by_file = {info.relpath: read_text(info.path, 300_000) for info in sql_files}
    all_sql = "\n".join(sql_text_by_file.values())

    table_pattern = re.compile(
        r"create\s+table\s+(if\s+not\s+exists\s+)?(?:(?P<schema>\"?[\w]+\"?)\.)?(?P<table>\"?[\w]+\"?)",
        re.IGNORECASE,
    )
    rls_pattern = re.compile(
        r"alter\s+table\s+(?:(?P<schema>\"?[\w]+\"?)\.)?(?P<table>\"?[\w]+\"?)\s+enable\s+row\s+level\s+security",
        re.IGNORECASE,
    )
    policy_pattern = re.compile(
        r"create\s+policy\b.*?\bon\s+(?:(?P<schema>\"?[\w]+\"?)\.)?(?P<table>\"?[\w]+\"?)",
        re.IGNORECASE | re.DOTALL,
    )

    created_public_tables: dict[str, str] = {}
    rls_tables: set[str] = set()
    policy_tables: set[str] = set()
    for relpath, text in sql_text_by_file.items():
        for match in table_pattern.finditer(text):
            table = extract_sql_table_name(match)
            if table.startswith("public."):
                created_public_tables.setdefault(table, relpath)
        for match in rls_pattern.finditer(text):
            rls_tables.add(extract_sql_table_name(match))
        for match in policy_pattern.finditer(text):
            policy_tables.add(extract_sql_table_name(match))

    missing_rls = [(table, relpath) for table, relpath in created_public_tables.items() if table not in rls_tables]
    if missing_rls:
        target = ", ".join(f"`{table}` in `{relpath}`" for table, relpath in missing_rls[:8])
        findings.append(
            audit_finding(
                "High",
                "Supabase RLS",
                f"`{len(missing_rls)}` public tables are created without detected RLS enablement.",
                "Supabase exposes public schema tables through APIs; RLS should be enabled for exposed tables.",
                target,
            )
        )

    rls_without_policy = sorted(table for table in rls_tables if table.startswith("public.") and table not in policy_tables)
    if rls_without_policy:
        findings.append(
            audit_finding(
                "Medium",
                "Supabase RLS",
                f"`{len(rls_without_policy)}` RLS-enabled public tables have no detected policies.",
                "This may be intentional lockdown, but it is an important authorization behavior to inspect.",
                ", ".join(f"`{table}`" for table in rls_without_policy[:10]),
            )
        )

    policy_without_check: list[str] = []
    for relpath, text in sql_text_by_file.items():
        for statement in re.split(r";\s*(?:\n|$)", text):
            if not re.search(r"create\s+policy\b", statement, re.IGNORECASE):
                continue
            if re.search(r"\bfor\s+(insert|update|all)\b", statement, re.IGNORECASE) and not re.search(r"\bwith\s+check\b", statement, re.IGNORECASE):
                policy_without_check.append(relpath)
    if policy_without_check:
        findings.append(
            audit_finding(
                "Medium",
                "Supabase RLS",
                f"`{len(policy_without_check)}` insert/update policy statements lack an obvious `WITH CHECK` clause.",
                "`WITH CHECK` constrains new row values and prevents policies from only protecting reads.",
                ", ".join(f"`{relpath}`" for relpath in sorted(set(policy_without_check))[:5]),
            )
        )

    security_definer_without_search_path: list[str] = []
    for relpath, text in sql_text_by_file.items():
        for statement in re.split(r";\s*(?:\n|$)", text):
            if re.search(r"\bsecurity\s+definer\b", statement, re.IGNORECASE) and not re.search(r"\bset\s+search_path\b", statement, re.IGNORECASE):
                security_definer_without_search_path.append(relpath)
    if security_definer_without_search_path:
        findings.append(
            audit_finding(
                "High",
                "Postgres Functions",
                f"`{len(security_definer_without_search_path)}` `SECURITY DEFINER` functions lack an obvious `search_path` setting.",
                "Unpinned search paths can make privileged functions resolve attacker-controlled objects.",
                ", ".join(f"`{relpath}`" for relpath in sorted(set(security_definer_without_search_path))[:5]),
            )
        )

    service_role_scan = scan_regex(
        "Supabase service role references",
        js_like_infos(production_infos) + jsx_like_infos(production_infos),
        r"(SUPABASE_SERVICE_ROLE|service[_-]?role|serviceRole)",
        flags=re.IGNORECASE,
    )
    if service_role_scan.total:
        findings.append(
            audit_finding(
                "High",
                "Supabase Boundary",
                f"`{service_role_scan.total}` service-role references found in app code.",
                "Service role keys bypass RLS and must never be available to browser/client bundles.",
                top_scan_targets(service_role_scan),
            )
        )

    destructive_scan = scan_regex(
        "Destructive migration statements",
        sql_files,
        r"\b(drop\s+(table|column|schema|policy|function)|truncate\s+table|delete\s+from)\b",
        flags=re.IGNORECASE,
    )
    if destructive_scan.total:
        findings.append(
            audit_finding(
                "Medium",
                "Postgres Migrations",
                f"`{destructive_scan.total}` destructive SQL statements found.",
                "Drops, truncates, and broad deletes need explicit rollout and backup review.",
                top_scan_targets(destructive_scan),
            )
        )

    if "auth.uid()" in all_sql and "(select auth.uid())" not in all_sql:
        findings.append(
            audit_finding(
                "Info",
                "Supabase RLS Performance",
                "`auth.uid()` appears in policies without detected `(select auth.uid())` wrapping.",
                "Wrapping helper calls can avoid repeated function evaluation in row policies.",
                "supabase migrations",
            )
        )

    return AuditPackReport(
        name="Supabase / Postgres",
        summary=f"Detected Supabase/Postgres surface with `{len(sql_files)}` SQL files and `{len(created_public_tables)}` created public tables.",
        findings=findings,
        recommended_commands=commands,
    )


def audit_prisma_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    dependencies = all_package_dependencies(signal_files)
    prisma_schemas = find_file_infos(file_infos, lambda info: info.name == "schema.prisma")
    if "prisma" not in dependencies and "@prisma/client" not in dependencies and not prisma_schemas:
        return None

    findings: list[AuditFinding] = []
    scripts_text = "\n".join(
        command
        for scripts in package_script_lookup(signal_files).values()
        for command in scripts.values()
    )
    if re.search(r"prisma\s+db\s+push", scripts_text):
        findings.append(
            audit_finding(
                "High",
                "Prisma Migrations",
                "`prisma db push` appears in package scripts.",
                "Production workflows should apply committed migrations, not push schema state directly.",
                "package.json scripts",
            )
        )
    if re.search(r"prisma\s+migrate\s+dev", scripts_text) and re.search(r"(deploy|ci|build|start|prod)", scripts_text, re.IGNORECASE):
        findings.append(
            audit_finding(
                "High",
                "Prisma Migrations",
                "`prisma migrate dev` appears near deployment/CI scripts.",
                "`migrate dev` is an interactive development command; production should use `migrate deploy`.",
                "package.json scripts",
            )
        )
    if prisma_schemas and not any("/prisma/migrations/" in f"/{info.relpath}" for info in file_infos):
        findings.append(
            audit_finding(
                "Medium",
                "Prisma Migrations",
                "Prisma schema detected without a `prisma/migrations` directory.",
                "Missing committed migrations makes production database changes harder to review and reproduce.",
                ", ".join(info.relpath for info in prisma_schemas),
            )
        )

    prisma_client_scan = scan_regex(
        "PrismaClient construction",
        js_like_infos(production_infos),
        r"new\s+PrismaClient\s*\(",
    )
    if prisma_client_scan.total > 1:
        findings.append(
            audit_finding(
                "Medium",
                "Prisma Runtime",
                f"`{prisma_client_scan.total}` `new PrismaClient()` calls found.",
                "Serverless apps should usually reuse a singleton client to avoid exhausting database connections.",
                top_scan_targets(prisma_client_scan),
            )
        )

    commands = []
    for package_path, scripts in package_script_lookup(signal_files).items():
        for script in scripts:
            if "prisma" in scripts[script] or script in {"typecheck", "lint", "build"}:
                commands.append(package_script_display(package_path.parent, script))
    commands.append("prisma validate")

    return AuditPackReport(
        name="Prisma",
        summary=f"Detected Prisma via `{len(prisma_schemas)}` schema files.",
        findings=findings,
        recommended_commands=list(dict.fromkeys(commands)),
    )


def audit_drizzle_pack(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> AuditPackReport | None:
    dependencies = all_package_dependencies(signal_files)
    drizzle_configs = find_file_infos(file_infos, lambda info: info.name.startswith("drizzle.config."))
    if "drizzle-orm" not in dependencies and "drizzle-kit" not in dependencies and not drizzle_configs:
        return None

    findings: list[AuditFinding] = []
    scripts_text = "\n".join(
        command
        for scripts in package_script_lookup(signal_files).values()
        for command in scripts.values()
    )
    if "drizzle-kit" not in scripts_text and not drizzle_configs:
        findings.append(
            audit_finding(
                "Medium",
                "Drizzle Migrations",
                "Drizzle dependency detected without config or migration scripts.",
                "A clear migration workflow is required for reviewable Postgres schema changes.",
                "package.json scripts / drizzle.config.*",
            )
        )

    raw_sql_scan = scan_regex(
        "Drizzle raw SQL escape hatches",
        js_like_infos(production_infos),
        r"(sql\.raw\(|execute\s*\(\s*sql\.raw|unsafe)",
        flags=re.IGNORECASE,
    )
    if raw_sql_scan.total:
        findings.append(
            audit_finding(
                "Medium",
                "Drizzle SQL",
                f"`{raw_sql_scan.total}` raw SQL escape hatch candidates found.",
                "Raw SQL helpers need review for interpolation and tenant/auth constraints.",
                top_scan_targets(raw_sql_scan),
            )
        )

    commands = []
    for package_path, scripts in package_script_lookup(signal_files).items():
        for script, command in scripts.items():
            if "drizzle" in script.lower() or "drizzle" in command.lower():
                commands.append(package_script_display(package_path.parent, script))

    return AuditPackReport(
        name="Drizzle",
        summary=f"Detected Drizzle via `{len(drizzle_configs)}` config files.",
        findings=findings,
        recommended_commands=list(dict.fromkeys(commands)),
    )


def build_stack_audit_reports(
    signal_files: Sequence[Path],
    file_infos: Sequence[FileInfo],
    production_infos: Sequence[FileInfo],
) -> list[AuditPackReport]:
    pack_builders = [
        audit_typescript_pack,
        audit_react_next_pack,
        audit_tailwind_pack,
        audit_supabase_postgres_pack,
        audit_prisma_pack,
        audit_drizzle_pack,
    ]
    reports: list[AuditPackReport] = []
    for builder in pack_builders:
        report = builder(signal_files, file_infos, production_infos)
        if report is not None:
            reports.append(report)
    return reports


def write_stack_audit_report(file, reports: Sequence[AuditPackReport]) -> None:
    file.write("## Stack-Specific Best Practice Audit\n\n")
    if not reports:
        file.write("No TypeScript, React/Next.js, Tailwind, Supabase/Postgres, Prisma, or Drizzle-specific packs were detected.\n\n")
        return

    file.write("Detected packs:\n\n")
    for report in reports:
        file.write(f"- `{report.name}` - {report.summary}\n")
    file.write("\n")

    for report in reports:
        file.write(f"### {report.name}\n\n")
        if report.findings:
            rows = [
                (finding.severity, finding.area, finding.finding, finding.why, finding.target)
                for finding in sorted(report.findings, key=lambda finding: {"High": 0, "Medium": 1, "Info": 2}.get(finding.severity, 3))
            ]
            file.write(md_table(rows, ["Severity", "Area", "Finding", "Why It Matters", "Next Inspection Target"]) + "\n\n")
        else:
            file.write("No passive best-practice findings for this pack.\n\n")

        if report.recommended_commands:
            file.write("Recommended commands:\n\n")
            for command in report.recommended_commands:
                file.write(f"- `{command}`\n")
            file.write("\n")


def file_reason(relpath: str, lines: int | None = None, changes: int | None = None) -> str:
    lower = relpath.lower()
    reasons: list[str] = []
    if lines is not None and lines >= 1000:
        reasons.append("large")
    elif lines is not None and lines >= 500:
        reasons.append("medium-large")
    if changes is not None and changes > 0:
        reasons.append("recently changed")

    if "orchestrator" in lower:
        detail = "likely owns concurrency, retry, and state behavior"
    elif "codex/app_server" in lower or "app_server" in lower:
        detail = "likely owns external protocol and session behavior"
    elif "status_dashboard" in lower:
        detail = "likely mixes rendering, formatting, and event humanization"
    elif "agent_runner" in lower:
        detail = "likely central control path"
    elif "config/schema" in lower or lower.endswith("schema.ex"):
        detail = "config validation and runtime behavior boundary"
    elif "workspace" in lower:
        detail = "workspace path containment and filesystem boundary"
    elif "linear" in lower:
        detail = "external API and token-handling boundary"
    elif "ssh" in lower:
        detail = "remote worker and process boundary"
    elif lower.endswith("package.json"):
        detail = "dependency, script, and package-manager boundary"
    elif lower.endswith("tsconfig.json") or "/tsconfig" in lower:
        detail = "TypeScript compiler strictness boundary"
    elif "supabase/migrations/" in lower or lower.endswith(".sql"):
        detail = "database schema, RLS, and migration behavior boundary"
    elif "app/api/" in lower or lower.endswith("/route.ts") or "/pages/api/" in lower:
        detail = "HTTP mutation and authorization boundary"
    elif lower.endswith("next.config.ts") or lower.endswith("next.config.js") or lower.endswith("next.config.mjs"):
        detail = "Next.js runtime, headers, and deployment config boundary"
    elif "tailwind.config" in lower:
        detail = "Tailwind source scanning and theme config boundary"
    elif lower.endswith("schema.prisma") or "/prisma/" in lower:
        detail = "Prisma schema and migration boundary"
    elif "drizzle.config" in lower:
        detail = "Drizzle migration config boundary"
    elif "router" in lower or "controller" in lower or "live" in lower:
        detail = "web boundary"
    else:
        detail = "high size/churn inspection target"

    prefix = ", ".join(reasons)
    if prefix:
        return f"{prefix}; {detail}"
    return detail


def recommended_targets(
    hotspots: Sequence[tuple[int, str, int, int]],
    largest_source: Sequence[FileInfo],
    risk_results: Sequence[ScanResult],
    max_targets: int = 8,
) -> list[tuple[str, str]]:
    selected: dict[str, str] = {}
    candidate_context: dict[str, tuple[int | None, int | None]] = {}

    for _, relpath, lines, changes in hotspots:
        candidate_context[relpath] = (lines, changes)
    for info in largest_source:
        candidate_context.setdefault(info.relpath, (info.lines, None))

    priority_markers = [
        "orchestrator.ex",
        "codex/app_server.ex",
        "status_dashboard.ex",
        "agent_runner.ex",
        "config/schema.ex",
        "workspace.ex",
        "linear/client.ex",
        "ssh.ex",
    ]
    for marker in priority_markers:
        match = next((relpath for relpath in candidate_context if relpath.endswith(marker)), None)
        if match is None:
            continue
        lines, changes = candidate_context[match]
        selected.setdefault(match, file_reason(match, lines, changes))
        if len(selected) >= max_targets:
            return list(selected.items())

    for score, relpath, lines, changes in hotspots[:10]:
        selected.setdefault(relpath, file_reason(relpath, lines, changes))
        if len(selected) >= max_targets:
            return list(selected.items())

    for info in largest_source:
        selected.setdefault(info.relpath, file_reason(info.relpath, info.lines, None))
        if len(selected) >= max_targets:
            return list(selected.items())

    boundary_counts: Counter[str] = Counter()
    for result in risk_results:
        if result.title in {
            "Raw shell / process execution",
            "Network calls",
            "Filesystem writes / deletes",
            "Environment variable usage",
        }:
            boundary_counts.update(result.by_file)
    for relpath, _ in boundary_counts.most_common(10):
        selected.setdefault(relpath, file_reason(relpath, None, None))
        if len(selected) >= max_targets:
            return list(selected.items())

    return list(selected.items())


def run_command(
    title: str,
    command: Sequence[str],
    cwd: Path,
    timeout_seconds: int,
) -> CommandResult:
    display_cwd = rel(cwd) if cwd != ROOT else "."
    status(f"Running: {title} in {display_cwd}")
    command_start = time.monotonic()
    deadline = command_start + timeout_seconds
    last_heartbeat = command_start

    try:
        with tempfile.TemporaryFile(mode="w+t", encoding="utf-8", errors="replace") as output_file:
            process = subprocess.Popen(
                list(command),
                cwd=cwd,
                stdout=output_file,
                stderr=subprocess.STDOUT,
            )

            while process.poll() is None:
                now = time.monotonic()
                elapsed = int(now - command_start)
                if now >= deadline:
                    process.kill()
                    process.wait()
                    output = command_output(output_file)
                    status(f"Timed out: {title} in {display_cwd} after {elapsed}s")
                    return CommandResult(
                        title=title,
                        command=" ".join(command),
                        cwd=display_cwd,
                        returncode=None,
                        output=output,
                        timed_out=True,
                    )

                if now - last_heartbeat >= COMMAND_HEARTBEAT_SECONDS:
                    remaining = max(0, int(deadline - now))
                    status(f"Still running: {title} in {display_cwd} ({elapsed}s elapsed, {remaining}s until timeout)")
                    last_heartbeat = now

                time.sleep(1)

            elapsed = time.monotonic() - command_start
            output = command_output(output_file)
            status(f"Finished: {title} in {display_cwd} exit={process.returncode} elapsed={elapsed:.1f}s")
            return CommandResult(
                title=title,
                command=" ".join(command),
                cwd=display_cwd,
                returncode=process.returncode,
                output=output,
            )
    except OSError as exc:
        return CommandResult(
            title=title,
            command=" ".join(command),
            cwd=display_cwd,
            returncode=None,
            output=str(exc),
        )


def command_output(output_file) -> str:
    output_file.flush()
    output_file.seek(0)
    output = output_file.read() or ""
    if len(output) > MAX_COMMAND_OUTPUT_CHARS:
        return output[:MAX_COMMAND_OUTPUT_CHARS] + "\n...[truncated]"
    return output


def deep_scanner_results(
    mix_roots: Sequence[Path],
    timeout_seconds: int,
) -> list[CommandResult]:
    results: list[CommandResult] = []

    if shutil.which("gitleaks"):
        results.append(run_command("Gitleaks: current directory secret scan", ["gitleaks", "dir", "--redact", "--no-banner", "."], ROOT, timeout_seconds))
        if (ROOT / ".git").exists():
            results.append(run_command("Gitleaks: git history secret scan", ["gitleaks", "git", "--redact", "--no-banner", "."], ROOT, timeout_seconds))

    if shutil.which("osv-scanner"):
        results.append(run_command("OSV-Scanner: dependency vulnerability scan", ["osv-scanner", "scan", "source", "-r", "."], ROOT, timeout_seconds))

    if shutil.which("semgrep"):
        results.append(
            run_command(
                "Semgrep: static analysis scan",
                [
                    "semgrep",
                    "scan",
                    "--config",
                    "auto",
                    "--metrics=off",
                    "--exclude",
                    "codebase-intake.py",
                    "--exclude",
                    "codebase-shape.py",
                    "--exclude",
                    "codebase-extra-scan.sh",
                    "--exclude",
                    REPORT_NAME,
                    ".",
                ],
                ROOT,
                timeout_seconds,
            )
        )

    if shutil.which("pip-audit"):
        requirements = [
            path
            for path in iter_paths(include_tooling=False, include_lockfiles=True)
            if path.name == "requirements.txt"
        ]
        for path in requirements:
            results.append(run_command(f"pip-audit: {rel(path)}", ["pip-audit", "-r", str(path)], ROOT, timeout_seconds))

    if shutil.which("mix"):
        for mix_root in mix_roots:
            commands = [
                ("Elixir: mix format --check-formatted", ["mix", "format", "--check-formatted"]),
                ("Elixir: mix test", ["mix", "test"]),
                ("Elixir: mix credo --strict", ["mix", "credo", "--strict"]),
                ("Elixir: mix dialyzer", ["mix", "dialyzer"]),
                ("Elixir: mix deps.audit", ["mix", "deps.audit"]),
                ("Elixir: mix hex.audit", ["mix", "hex.audit"]),
                ("Elixir: mix sobelow", ["mix", "sobelow"]),
            ]
            for title, command in commands:
                results.append(run_command(f"{title} ({rel(mix_root)})", command, mix_root, timeout_seconds))

    return results


def stack_deep_command_results(
    signal_files: Sequence[Path],
    audit_reports: Sequence[AuditPackReport],
    timeout_seconds: int,
) -> list[CommandResult]:
    results: list[CommandResult] = []
    report_names = {report.name for report in audit_reports}

    for package_path, scripts in package_script_lookup(signal_files).items():
        package_root = package_path.parent
        selected_scripts: list[str] = []
        for preferred in ["typecheck", "type-check", "check-types", "lint", "test", "build"]:
            if preferred in scripts:
                selected_scripts.append(preferred)
        for script in scripts:
            lower = script.lower()
            if ("typecheck" in lower or "lint" in lower or "test" in lower or "build" in lower) and script not in selected_scripts:
                selected_scripts.append(script)

        for script in selected_scripts:
            command = package_run_command(package_root, script)
            results.append(
                run_command(
                    f"Package script: {script} ({rel(package_root) if package_root != ROOT else '.'})",
                    command,
                    package_root,
                    timeout_seconds,
                )
            )

    if "Supabase / Postgres" in report_names and shutil.which("supabase"):
        supabase_roots = sorted(
            {
                path.parent.parent
                for path in signal_files
                if rel(path).endswith("supabase/config.toml")
            },
            key=rel,
        )
        if not supabase_roots and (ROOT / "supabase").exists():
            supabase_roots = [ROOT]
        for supabase_root in supabase_roots:
            results.append(
                run_command(
                    f"Supabase: db lint ({rel(supabase_root) if supabase_root != ROOT else '.'})",
                    ["supabase", "db", "lint", "--fail-on", "warning"],
                    supabase_root,
                    timeout_seconds,
                )
            )
            if (supabase_root / "supabase" / "tests").exists():
                results.append(
                    run_command(
                        f"Supabase: test db ({rel(supabase_root) if supabase_root != ROOT else '.'})",
                        ["supabase", "test", "db"],
                        supabase_root,
                        timeout_seconds,
                    )
                )

    return results


def write_command_result(file, result: CommandResult) -> None:
    file.write(f"### {result.title}\n\n")
    file.write(f"- Command: `{result.command}`\n")
    file.write(f"- CWD: `{result.cwd}`\n")
    if result.timed_out:
        file.write("- Result: timed out\n\n")
    elif result.returncode is None:
        file.write("- Result: could not run\n\n")
    else:
        file.write(f"- Exit code: `{result.returncode}`\n\n")
    file.write(fenced(result.output or "[no output]") + "\n\n")


def write_list_or_empty(file, items: Sequence[str], empty: str) -> None:
    if not items:
        file.write(empty + "\n\n")
        return
    for item in items:
        file.write(f"- `{item}`\n")
    file.write("\n")


def write_report(args: argparse.Namespace) -> Path:
    report_path = ROOT / REPORT_NAME
    status(f"Starting codebase intake at {ROOT}")
    status("Walking files and counting text lines")
    file_infos = build_file_infos(include_tooling=args.include_tooling)
    code_infos = [info for info in file_infos if is_code_or_config(info) and not is_documentation(info)]
    production_infos = [info for info in file_infos if is_production_scan_file(info)]
    quality_infos = code_infos
    status(f"Counted {len(file_infos)} text files")

    status("Detecting stack, commands, and test surface")
    signal_files = find_signal_files(include_tooling=args.include_tooling)
    mix_roots = detect_mix_roots(signal_files)
    phoenix = has_phoenix(signal_files, file_infos)
    stack_descriptors = detect_stack_descriptors(signal_files, file_infos)
    commands = discover_commands(signal_files, phoenix)
    tests = test_metrics(file_infos, mix_roots)
    status(f"Detected stack: {', '.join(stack_descriptors)}")

    status("Computing git churn and hotspot scores")
    changes = git_recent_changes(code_infos)
    hotspots = hotspot_rows(code_infos, changes)
    production_hotspots = hotspot_rows(production_infos, changes)

    status("Scanning architecture, quality, and passive risk patterns")
    api_surface = elixir_api_surface(production_infos)
    architecture_results = run_architecture_scans(production_infos)
    quality_results = run_scan_groups(quality_infos, quality_patterns())
    risk_results = run_scan_groups(production_infos, risk_patterns())
    largest_code = sorted(code_infos, key=lambda info: info.lines, reverse=True)
    largest_production_code = sorted(production_infos, key=lambda info: info.lines, reverse=True)
    large_elixir = [
        info
        for info in code_infos
        if info.suffix in {".ex", ".exs"} and info.lines >= 500 and not is_test_file(info)
    ]
    status("Running stack-specific passive audit packs")
    stack_audit_reports = build_stack_audit_reports(signal_files, file_infos, production_infos)
    inspection_targets = recommended_targets(production_hotspots, largest_production_code, risk_results)
    scanner_results = []
    if args.deep:
        status("Running deep scanners and detected project commands")
        scanner_results = deep_scanner_results(mix_roots, args.command_timeout)
        scanner_results.extend(stack_deep_command_results(signal_files, stack_audit_reports, args.command_timeout))
    else:
        status("Skipping deep scanners; pass --deep to run them")

    total_lines = sum(info.lines for info in file_infos)
    test_ratio = tests["ratio"]
    repo_shape = describe_repo_shape(stack_descriptors, file_infos, test_ratio)
    source_main_folders = two_level_folder_rows(tests["source_infos"])[:3]
    test_main_folders = two_level_folder_rows(tests["test_infos"])[:2]
    package_files = detect_package_files(signal_files)
    runtime_files = detect_runtime_files(signal_files)
    tooling_files = find_tooling_files()

    status(f"Writing report to {report_path}")
    with report_path.open("w", encoding="utf-8") as file:
        file.write("# Codebase Intake Report\n\n")
        file.write(f"Generated: `{dt.datetime.now().isoformat(timespec='seconds')}`\n\n")
        file.write(f"Root: `{ROOT}`\n\n")

        file.write("## Executive Summary\n\n")
        file.write(f"Detected repo shape: {repo_shape}\n\n")
        file.write(f"- Repo size counted: `{len(file_infos)}` text files, `{total_lines}` lines outside ignored folders.\n")
        file.write(f"- Detected stack: `{', '.join(stack_descriptors)}`\n")
        if stack_audit_reports:
            file.write(f"- Stack-specific audit packs: `{', '.join(report.name for report in stack_audit_reports)}`\n")
        if source_main_folders:
            folders = ", ".join(f"`{folder}` ({lines} lines)" for folder, _, lines in source_main_folders)
            file.write(f"- Primary implementation folders: {folders}\n")
        if test_main_folders:
            folders = ", ".join(f"`{folder}` ({lines} lines)" for folder, _, lines in test_main_folders)
            file.write(f"- Test folders: {folders}\n")
        if test_ratio is None:
            file.write("- Test density: no source/test ratio could be computed from known conventions.\n")
        else:
            file.write(
                f"- Test density: `{tests['test_lines']}` test lines / `{tests['source_lines']}` source lines "
                f"= `{test_ratio:.2f}` test/source ratio.\n"
            )
        if inspection_targets:
            file.write("- Suggested first files to inspect:\n")
            for relpath, reason in inspection_targets[:5]:
                file.write(f"  - `{relpath}` - {reason}.\n")
        else:
            file.write("- Suggested first files to inspect: no hotspot targets found from size/churn data.\n")
        large_tests = [info for info in tests["test_infos"] if info.lines >= 1000]
        if large_tests:
            file.write(
                f"- Test suite note: `{len(large_tests)}` test files are over 1,000 lines; inspect them for brittle integration coverage.\n"
            )
        raw_shell = next((result for result in risk_results if result.title == "Raw shell / process execution"), None)
        fs_mutation = next((result for result in risk_results if result.title == "Filesystem writes / deletes"), None)
        network = next((result for result in risk_results if result.title == "Network calls"), None)
        stack_audit_names = {report.name for report in stack_audit_reports}
        if "Supabase / Postgres" in stack_audit_names:
            security_focus = [
                "RLS coverage",
                "service role key boundaries",
                "public schema tables",
                "mutating route authorization",
                "destructive migrations",
                "generated database types",
            ]
        elif "React / Next.js" in stack_audit_names:
            security_focus = [
                "server/client module boundaries",
                "NEXT_PUBLIC env exposure",
                "mutating route authorization",
                "security headers",
                "database access in route handlers",
            ]
        else:
            security_focus = [
                "process spawning",
                "workspace path containment",
                "SSH worker behavior",
                "Codex app-server protocol handling",
                "Linear API token handling",
                "cleanup behavior around per-issue workspaces",
            ]
        file.write(
            "- Passive risk focus: "
            f"`{raw_shell.total if raw_shell else 0}` process candidates, "
            f"`{fs_mutation.total if fs_mutation else 0}` filesystem mutation candidates, "
            f"and `{network.total if network else 0}` network call candidates. "
            f"Review {', '.join(security_focus)}.\n\n"
        )

        file.write("## Detected Stack\n\n")
        file.write("### Languages\n\n")
        language_summary = language_rows(file_infos)
        if language_summary:
            file.write(md_table(language_summary, ["Language", "Files", "Lines"], numeric_columns={1, 2}) + "\n\n")
        else:
            file.write("No known language files found outside ignored folders.\n\n")

        file.write("### Stack Indicators\n\n")
        for descriptor in stack_descriptors:
            file.write(f"- {descriptor}\n")
        file.write("\n")

        file.write("### Package / Dependency Files\n\n")
        write_list_or_empty(file, package_files, "No package/dependency files found outside ignored folders.")

        file.write("### Runtime / Deployment Files\n\n")
        write_list_or_empty(file, runtime_files, "No runtime/deployment files found outside ignored folders.")

        file.write("### Stack Signal Files\n\n")
        write_list_or_empty(file, [rel(path) for path in signal_files], "No stack signal files found outside ignored folders.")

        file.write("### Agent / Editor Tooling Config\n\n")
        if tooling_files:
            file.write(
                "These paths are listed separately and excluded from passive scans unless `--include-tooling` is used.\n\n"
            )
            write_list_or_empty(file, tooling_files[:80], "No agent/editor tooling config found.")
            if len(tooling_files) > 80:
                file.write(f"... truncated after 80 tooling files from {len(tooling_files)} total.\n\n")
        else:
            file.write("No agent/editor tooling config found.\n\n")

        file.write("## Commands\n\n")
        make_targets = commands["make_targets"]
        if make_targets:
            file.write("### Make Targets\n\n")
            for path, targets in make_targets.items():
                file.write(f"- `{path}`: `{', '.join(targets)}`\n")
            file.write("\n")

        package_scripts = commands["package_scripts"]
        if package_scripts:
            file.write("### package.json Scripts\n\n")
            for path, scripts in package_scripts.items():
                file.write(f"- `{path}`: `{', '.join(scripts)}`\n")
            file.write("\n")

        mix_aliases = commands["mix_aliases"]
        if mix_aliases:
            file.write("### Mix Aliases\n\n")
            for path, aliases in mix_aliases.items():
                file.write(f"- `{path}`: `{', '.join(aliases)}`\n")
            file.write("\n")

        file.write("### Likely Commands\n\n")
        likely = commands["likely"]
        if likely:
            rows = []
            for category, values in likely.items():
                rows.append((category, ", ".join(f"`{value}`" for value in values)))
            file.write(md_table(rows, ["Category", "Commands"]) + "\n\n")
        else:
            file.write("No likely commands discovered from known project files.\n\n")

        file.write("## Size and Shape\n\n")
        file.write("### Lines by Type\n\n")
        file.write(md_table(type_rows(file_infos), ["Type", "Files", "Lines"], numeric_columns={1, 2}) + "\n\n")

        file.write("### Lines by Top-Level Folder\n\n")
        file.write(md_table(folder_rows(file_infos), ["Folder", "Files", "Lines"], numeric_columns={1, 2}) + "\n\n")

        file.write("### Lines by Main Folder\n\n")
        file.write(md_table(two_level_folder_rows(file_infos)[:30], ["Folder", "Files", "Lines"], numeric_columns={1, 2}) + "\n\n")

        file.write("### Tree\n\n")
        file.write(fenced(build_tree(include_tooling=args.include_tooling)) + "\n\n")

        file.write("## Hotspots\n\n")
        file.write("### Largest Source / Config Files\n\n")
        largest_rows = [(f"`{info.relpath}`", info.lines) for info in largest_code[:30]]
        file.write(md_table(largest_rows, ["File", "Lines"], numeric_columns={1}) + "\n\n")

        file.write("### Most Changed Source / Config Files: Last 90 Days\n\n")
        if changes:
            rows = [(f"`{relpath}`", count) for relpath, count in changes.most_common(30)]
            file.write(md_table(rows, ["File", "90d Changes"], numeric_columns={1}) + "\n\n")
        else:
            file.write("No git churn data found for the last 90 days.\n\n")

        file.write("### Size x Recent Churn\n\n")
        if hotspots:
            rows = [
                (f"`{relpath}`", lines, change_count, score)
                for score, relpath, lines, change_count in hotspots[:30]
            ]
            file.write(md_table(rows, ["File", "Lines", "90d Changes", "Hotspot Score"], numeric_columns={1, 2, 3}) + "\n\n")
        else:
            file.write("No size x churn hotspots found.\n\n")

        file.write("### Large Elixir Module Warnings\n\n")
        if large_elixir:
            high = [info for info in large_elixir if info.lines >= 1000]
            medium = [info for info in large_elixir if 500 <= info.lines < 1000]
            if high:
                file.write("High attention, over 1,000 lines:\n\n")
                for info in high:
                    file.write(f"- `{info.relpath}`: `{info.lines}` lines - {file_reason(info.relpath, info.lines, None)}.\n")
                file.write("\n")
            if medium:
                file.write("Likely refactor candidates, over 500 lines:\n\n")
                for info in medium:
                    file.write(f"- `{info.relpath}`: `{info.lines}` lines - {file_reason(info.relpath, info.lines, None)}.\n")
                file.write("\n")
        else:
            file.write("No Elixir source/config files over 500 lines found.\n\n")

        file.write("## Test Surface\n\n")
        file.write("### Source / Test Ratio\n\n")
        ratio_value = "n/a" if test_ratio is None else f"{test_ratio:.2f}"
        ratio_rows = [
            ("Source files", len(tests["source_infos"])),
            ("Source lines", tests["source_lines"]),
            ("Test files", len(tests["test_infos"])),
            ("Test lines", tests["test_lines"]),
            ("Test/source ratio", ratio_value),
        ]
        file.write(md_table(ratio_rows, ["Metric", "Value"]) + "\n\n")

        file.write("### Largest Test Files\n\n")
        if tests["test_infos"]:
            rows = [(f"`{info.relpath}`", info.lines) for info in tests["test_infos"][:30]]
            file.write(md_table(rows, ["File", "Lines"], numeric_columns={1}) + "\n\n")
        else:
            file.write("No test files detected using known conventions.\n\n")

        file.write("### Largest Source Files Without Obvious Matching Tests\n\n")
        unpaired = tests["unpaired"]
        if unpaired:
            rows = [(f"`{info.relpath}`", info.lines) for info in unpaired[:30]]
            file.write(md_table(rows, ["Source File", "Lines"], numeric_columns={1}) + "\n\n")
        else:
            file.write("No unpaired Elixir source files found using the `lib/foo.ex` -> `test/foo_test.exs` convention, or no Elixir project was detected.\n\n")

        file.write("### Detected Test Files\n\n")
        if tests["test_infos"]:
            for info in tests["test_infos"][:200]:
                file.write(f"- `{info.relpath}`\n")
            if len(tests["test_infos"]) > 200:
                file.write(f"- ... truncated after 200 test files from {len(tests['test_infos'])} total\n")
            file.write("\n")
        else:
            file.write("No test files detected.\n\n")

        file.write("## Architecture Surface\n\n")
        file.write("### Elixir Module / Function Surface\n\n")
        if api_surface:
            rows = [
                (f"`{relpath}`", modules, public_defs, private_defs, callbacks, lines)
                for relpath, modules, public_defs, private_defs, callbacks, lines in api_surface[:60]
            ]
            file.write(
                md_table(
                    rows,
                    ["File", "Modules", "Public defs", "Private defs", "Callbacks-ish", "Lines"],
                    numeric_columns={1, 2, 3, 4, 5},
                )
                + "\n\n"
            )
            file.write("High public function count can signal a module carrying too many responsibilities.\n\n")
        else:
            file.write("No Elixir module/function surface detected.\n\n")

        for result in architecture_results:
            write_scan_result(file, result)

        file.write("## Quality Signals\n\n")
        file.write("These scans cover source/config files, including tests, but exclude docs, lockfiles, intake scripts, generated folders, and agent/editor tooling by default.\n\n")
        for result in quality_results:
            write_scan_result(file, result)

        file.write("## Passive Risk Scan\n\n")
        file.write("These scans cover production source/config files only. Tests, docs, lockfiles, intake scripts, generated folders, and agent/editor tooling are excluded by default.\n\n")
        for result in risk_results:
            write_scan_result(file, result)

        write_stack_audit_report(file, stack_audit_reports)

        file.write("## Optional Scanner Results\n\n")
        if not args.deep:
            file.write("Deep scanners were not run. Re-run with `python3 codebase-intake.py --deep` to run installed scanners and language-specific commands.\n\n")
            available = []
            for command in ["gitleaks", "osv-scanner", "semgrep", "pip-audit", "mix", "supabase", "npm", "pnpm", "yarn", "bun"]:
                available.append((command, "available" if shutil.which(command) else "not installed"))
            file.write(md_table(available, ["Tool", "Status"]) + "\n\n")
        elif scanner_results:
            for result in scanner_results:
                write_command_result(file, result)
        else:
            file.write("No optional scanner commands were available to run.\n\n")

        file.write("## Recommended Inspection Order\n\n")
        if inspection_targets:
            for index, (relpath, reason) in enumerate(inspection_targets, 1):
                file.write(f"{index}. `{relpath}` - {reason}.\n")
            file.write("\n")
        file.write(f"{len(inspection_targets) + 1}. Inspect large source files over 1,000 lines, especially modules that mix rendering, orchestration, external I/O, and state transitions.\n")
        file.write(f"{len(inspection_targets) + 2}. Inspect external-boundary files: auth, webhooks, API clients, process execution, filesystem mutation, SSH, workspace cleanup, and token handling.\n")
        file.write(f"{len(inspection_targets) + 3}. Inspect test files over 1,000 lines for brittle integration coverage and slow setup paths.\n")
        file.write(f"{len(inspection_targets) + 4}. Run `python3 codebase-intake.py --deep` before production or security-sensitive work.\n")

    status("Finished codebase intake")
    return report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an interpretive codebase intake report.")
    parser.add_argument("--deep", action="store_true", help="Run installed scanners and language-specific project checks.")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress status output.")
    parser.add_argument(
        "--include-tooling",
        action="store_true",
        help="Include local agent/editor tooling directories in scans instead of listing them separately only.",
    )
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=300,
        help="Timeout in seconds for each --deep command.",
    )
    return parser.parse_args()


def main() -> int:
    global STATUS_ENABLED
    args = parse_args()
    STATUS_ENABLED = not args.quiet
    report_path = write_report(args)
    print(f"Wrote: {report_path}")
    if not args.deep:
        print("Deep scanners skipped. Use --deep to run installed scanners and project checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
