# Codebase Intake

`codebase-intake.py` generates a read-only Markdown intake report for a repository. The goal is to turn a fresh codebase into an inspection artifact: what stack it uses, where the important files are, how tests are shaped, where churn and size overlap, what passive risk signals exist, and what to inspect first.

The original goal was to replace noisy scanner dumps with a useful first-pass engineering report. The report should not scan its own scanner files, should not let agent/editor tooling pollute app findings, should summarize noisy searches, and should interpret the result in terms a reviewer or coding agent can act on.

## Why This Is Useful

Raw grep output is cheap but hard to use. This script keeps the cheap passive scan, then adds structure:

- It separates repo shape, risk, quality, test surface, architecture surface, and next inspection targets.
- It detects stack-specific context before making recommendations.
- It highlights large files, recently changed files, and large-plus-changed hotspots.
- It explains why a file is worth inspecting, not just that it matched a regex.
- It keeps default mode passive and read-only, so it is safe to run in unfamiliar repos.
- It has `--deep` for slower commands and external scanners once you are ready.

## Files

- `codebase-intake.py` is the main implementation.
- `codebase-shape.py` is a compatibility wrapper that runs `codebase-intake.py`.
- `codebase-extra-scan.sh` is a shell compatibility wrapper that runs `codebase-intake.py`.
- `codebase-shape.md` is the generated report.

When moving this into another repository, copy at least `codebase-intake.py`. Copy the wrapper files only if existing habits or docs refer to them.

## Usage

Default passive report:

```bash
python3 codebase-intake.py
```

Suppress status output:

```bash
python3 codebase-intake.py --quiet
```

Run installed external scanners and detected project commands:

```bash
python3 codebase-intake.py --deep --command-timeout 900
```

Include local agent/editor tooling in scans:

```bash
python3 codebase-intake.py --include-tooling
```

Default output is `codebase-shape.md` in the current working directory.

## Default Behavior

Default mode is passive:

- reads local files
- reads git history for 90-day churn when `.git` exists
- generates Markdown
- does not install anything
- does not run tests
- does not fetch dependencies
- excludes dependency folders, generated folders, test artifacts, local state folders, lockfiles, scanner files, local env files, and local AI/editor tooling folders

Excluded app-adjacent tooling includes `.cursor` and `.claude`. Those paths are listed separately as tooling config unless `--include-tooling` is passed.
Generated/local-state exclusions also include common cruft across JS/TS, Python, Ruby/Rails, Elixir, Go, JVM, PHP/Laravel, mobile, data/ML, and local database tooling: caches, build outputs, generated docs, test artifacts, local service data, binary model/checkpoint files, and package/vendor folders.
Environment example files such as `.env.example`, `.env.sample`, and `.env.template` are kept as source signal; local env files remain excluded.

## Report Sections

The report is organized as:

- Executive Summary
- Detected Stack
- Commands
- Size and Shape
- Hotspots
- Test Surface
- Architecture Surface
- Quality Signals
- Passive Risk Scan
- Stack-Specific Best Practice Audit
- Optional Scanner Results
- Recommended Inspection Order

## Stack-Specific Audit Packs

The script currently has passive audit packs for:

- TypeScript
- React / Next.js
- Tailwind CSS
- Supabase / Postgres
- Prisma
- Drizzle

These packs are intentionally heuristic. They flag inspection targets, not definitive bugs.

Examples:

- TypeScript: missing `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, missing typecheck script, type escape hatches.
- Next.js: suspicious `NEXT_PUBLIC_*` secret names, client-side secret references, missing obvious security headers/CSP, mutating route handlers without obvious auth.
- Tailwind: dynamically constructed utility classes that Tailwind cannot statically detect.
- Supabase/Postgres: public tables without detected RLS, RLS tables without policies, service-role references, destructive SQL, `SECURITY DEFINER` functions without obvious `search_path`.
- Prisma: `prisma db push` in scripts, missing migrations, repeated `new PrismaClient()`.
- Drizzle: missing migration/config surface and raw SQL escape hatches.

## Deep Mode

`--deep` runs external tools only if they are already installed. It can run commands such as:

- `gitleaks`
- `osv-scanner`
- `semgrep`
- `pip-audit`
- `mix format --check-formatted`
- `mix test`
- `mix credo --strict`
- `mix dialyzer`
- detected package scripts like `typecheck`, `lint`, `test`, and `build`
- `supabase db lint --fail-on warning` when Supabase is detected and the CLI exists

Deep mode can be slow and may require local dependencies or services. Default mode avoids that by design.
While each deep command is running, the script keeps command output for the final report and prints periodic status heartbeats so a long test or scanner does not look frozen.

## Implementation Notes

The script is Python on purpose. The job is mostly filesystem walking, text parsing, JSON parsing, regex scanning, git metadata, process execution, and Markdown generation. Python keeps the scanner easy to alter when new stack patterns show up.

Go could be useful later if the scanner needs to be distributed as a single binary, embedded into CI at scale, or parallelized heavily. Right now, Python is the more practical maintenance choice.

The script uses small in-process caches for file text and parsed JSON so repeated risk, architecture, and stack-specific scans do not keep rereading the same files.

## Future Improvements

Good next improvements:

- Add a config file, for example `.codebase-intake.toml`, for custom excludes, stack packs, and deep command policy.
- Add `--output` so the report filename is configurable.
- Add `--json` output for machine-readable findings.
- Add severity totals to the Executive Summary.
- Add confidence levels for heuristic findings.
- Add line-numbered finding tables for stack-specific audits.
- Add framework packs for Rails, Django, Laravel, Go services, Rust services, and Cloudflare Workers.
- Add package-manager-specific audit commands for npm, pnpm, yarn, and bun.
- Add Supabase type freshness checks by comparing latest migration timestamp to generated database type files.
- Add route-to-auth mapping for Next.js and common auth providers.
- Add migration ordering and destructive-change risk scoring for SQL.
- Add optional parallel scanning for very large repositories.
- Add tests for the scanner itself with small fixture repos.
- Split the script into modules if it becomes a maintained internal tool instead of a copyable single-file utility.

The main design rule should stay the same: default output should be safe, fast, interpretive, and immediately useful for deciding where a human or agent should look first.
