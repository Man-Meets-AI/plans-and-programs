# Codebase Intake Report

Generated: `2026-05-04T12:24:21`

Root: `/Users/bazelrex/Developer/symphony`

## Executive Summary

Detected repo shape: Elixir service with Mix, Phoenix web components, Codex app-server integration, Linear integration, SSH worker support, substantial ExUnit coverage.

- Repo size counted: `90` text files, `23852` lines outside ignored folders.
- Detected stack: `Elixir / Mix / Phoenix-ish, Dockerized runtime`
- Primary implementation folders: `elixir/lib` (9458 lines)
- Test folders: `elixir/test` (9603 lines)
- Test density: `9603` test lines / `9458` source lines = `1.02` test/source ratio.
- Suggested first files to inspect:
  - `elixir/lib/symphony_elixir/orchestrator.ex` - large, recently changed; likely owns concurrency, retry, and state behavior.
  - `elixir/lib/symphony_elixir/codex/app_server.ex` - large, recently changed; likely owns external protocol and session behavior.
  - `elixir/lib/symphony_elixir/status_dashboard.ex` - large, recently changed; likely mixes rendering, formatting, and event humanization.
  - `elixir/lib/symphony_elixir/agent_runner.ex` - recently changed; likely central control path.
  - `elixir/lib/symphony_elixir/config/schema.ex` - medium-large, recently changed; config validation and runtime behavior boundary.
- Test suite note: `4` test files are over 1,000 lines; inspect them for brittle integration coverage.
- Passive risk focus: `5` process candidates, `19` filesystem mutation candidates, and `7` network call candidates. Review process spawning, workspace path containment, SSH worker behavior, Codex app-server protocol handling, Linear API token handling, cleanup behavior around per-issue workspaces.

## Detected Stack

### Languages

| Language | Files | Lines |
| --- | ---: | ---: |
| Elixir | 59 | 19551 |

### Stack Indicators

- Elixir / Mix / Phoenix-ish
- Dockerized runtime

### Package / Dependency Files

- `elixir/mix.exs`
- `elixir/mix.lock`

### Runtime / Deployment Files

- `.github/workflows/make-all.yml`
- `.github/workflows/pr-description-lint.yml`
- `elixir/Makefile`
- `elixir/test/support/live_e2e_docker/Dockerfile`
- `elixir/test/support/live_e2e_docker/docker-compose.yml`

### Stack Signal Files

- `README.md`
- `elixir/.formatter.exs`
- `elixir/AGENTS.md`
- `elixir/Makefile`
- `elixir/README.md`
- `elixir/config/config.exs`
- `elixir/mix.exs`
- `elixir/mix.lock`
- `elixir/test/support/live_e2e_docker/Dockerfile`
- `elixir/test/support/live_e2e_docker/docker-compose.yml`

### Agent / Editor Tooling Config

These paths are listed separately and excluded from passive scans unless `--include-tooling` is used.

- `.codex/`
- `.codex/skills/commit/SKILL.md`
- `.codex/skills/debug/SKILL.md`
- `.codex/skills/land/SKILL.md`
- `.codex/skills/land/land_watch.py`
- `.codex/skills/linear/SKILL.md`
- `.codex/skills/pull/SKILL.md`
- `.codex/skills/push/SKILL.md`
- `.codex/worktree_init.sh`

## Commands

### Make Targets

- `elixir/Makefile`: `setup, deps, build, fmt, fmt-check, lint, test, coverage, ci, dialyzer, e2e`

### Mix Aliases

- `elixir/mix.exs`: `build, lint, setup`

### Likely Commands

| Category | Commands |
| --- | --- |
| Build | `make build`, `mix build` |
| CI | `make ci`, `make all` |
| Dev | `mix phx.server` |
| Format | `make fmt-check`, `make fmt`, `mix format --check-formatted` |
| Install | `make setup`, `make deps`, `mix deps.get` |
| Lint | `make lint`, `make dialyzer`, `mix credo --strict`, `mix dialyzer` |
| Security | `mix deps.audit`, `mix hex.audit`, `mix sobelow` |
| Test | `make test`, `make coverage`, `make e2e`, `mix test` |

## Size and Shape

### Lines by Type

| Type | Files | Lines |
| --- | ---: | ---: |
| .exs | 22 | 10093 |
| .ex | 37 | 9458 |
| .md | 13 | 3292 |
| .css | 1 | 463 |
| [no extension] | 4 | 268 |
| .txt | 5 | 95 |
| .yml | 3 | 91 |
| Makefile | 1 | 47 |
| Dockerfile | 1 | 22 |
| .sh | 1 | 13 |
| .conf | 1 | 7 |
| .toml | 1 | 3 |

### Lines by Top-Level Folder

| Folder | Files | Lines |
| --- | ---: | ---: |
| elixir | 83 | 21335 |
| . | 4 | 2424 |
| .github | 3 | 93 |

### Lines by Main Folder

| Folder | Files | Lines |
| --- | ---: | ---: |
| elixir/test | 33 | 10236 |
| elixir/lib | 37 | 9458 |
| . | 4 | 2424 |
| elixir | 9 | 818 |
| elixir/priv | 1 | 463 |
| elixir/docs | 2 | 344 |
| .github/workflows | 2 | 71 |
| .github | 1 | 22 |
| elixir/config | 1 | 16 |

### Tree

```text
symphony/
|-- .github/
|   |-- media/
|   |-- workflows/
|   |   |-- make-all.yml
|   |   `-- pr-description-lint.yml
|   `-- pull_request_template.md
|-- elixir/
|   |-- config/
|   |   `-- config.exs
|   |-- docs/
|   |   |-- logging.md
|   |   `-- token_accounting.md
|   |-- lib/
|   |   |-- mix/
|   |   |   `-- tasks/
|   |   |       |-- pr_body.check.ex
|   |   |       |-- specs.check.ex
|   |   |       `-- workspace.before_remove.ex
|   |   |-- symphony_elixir/
|   |   |   |-- codex/
|   |   |   |   |-- app_server.ex
|   |   |   |   `-- dynamic_tool.ex
|   |   |   |-- config/
|   |   |   |   `-- schema.ex
|   |   |   |-- linear/
|   |   |   |   |-- adapter.ex
|   |   |   |   |-- client.ex
|   |   |   |   `-- issue.ex
|   |   |   |-- tracker/
|   |   |   |   `-- memory.ex
|   |   |   |-- agent_runner.ex
|   |   |   |-- cli.ex
|   |   |   |-- config.ex
|   |   |   |-- http_server.ex
|   |   |   |-- log_file.ex
|   |   |   |-- orchestrator.ex
|   |   |   |-- path_safety.ex
|   |   |   |-- prompt_builder.ex
|   |   |   |-- specs_check.ex
|   |   |   |-- ssh.ex
|   |   |   |-- status_dashboard.ex
|   |   |   |-- tracker.ex
|   |   |   |-- workflow.ex
|   |   |   |-- workflow_store.ex
|   |   |   `-- workspace.ex
|   |   |-- symphony_elixir_web/
|   |   |   |-- components/
|   |   |   |   `-- layouts.ex
|   |   |   |-- controllers/
|   |   |   |   |-- observability_api_controller.ex
|   |   |   |   `-- static_asset_controller.ex
|   |   |   |-- live/
|   |   |   |   `-- dashboard_live.ex
|   |   |   |-- endpoint.ex
|   |   |   |-- error_html.ex
|   |   |   |-- error_json.ex
|   |   |   |-- observability_pubsub.ex
|   |   |   |-- presenter.ex
|   |   |   |-- router.ex
|   |   |   `-- static_assets.ex
|   |   `-- symphony_elixir.ex
|   |-- priv/
|   |   `-- static/
|   |       `-- dashboard.css
|   |-- test/
|   |   |-- fixtures/
|   |   |   `-- status_dashboard_snapshots/
|   |   |       |-- backoff_queue.evidence.md
|   |   |       |-- backoff_queue.snapshot.txt
|   |   |       |-- credits_unlimited.evidence.md
|   |   |       |-- credits_unlimited.snapshot.txt
|   |   |       |-- idle.evidence.md
|   |   |       |-- idle.snapshot.txt
|   |   |       |-- idle_with_dashboard_url.evidence.md
|   |   |       |-- idle_with_dashboard_url.snapshot.txt
|   |   |       |-- super_busy.evidence.md
|   |   |       `-- super_busy.snapshot.txt
|   |   |-- mix/
|   |   |   `-- tasks/
|   |   |       |-- pr_body_check_test.exs
|   |   |       |-- specs_check_task_test.exs
|   |   |       `-- workspace_before_remove_test.exs
|   |   |-- support/
|   |   |   |-- live_e2e_docker/
|   |   |   |   |-- docker-compose.yml
|   |   |   |   |-- Dockerfile
|   |   |   |   |-- live_worker_entrypoint.sh
|   |   |   |   `-- symphony-live-worker.conf
|   |   |   |-- snapshot_support.exs
|   |   |   `-- test_support.exs
|   |   |-- symphony_elixir/
|   |   |   |-- app_server_test.exs
|   |   |   |-- cli_test.exs
|   |   |   |-- core_test.exs
|   |   |   |-- dynamic_tool_test.exs
|   |   |   |-- extensions_test.exs
|   |   |   |-- live_e2e_test.exs
|   |   |   |-- log_file_test.exs
|   |   |   |-- observability_pubsub_test.exs
|   |   |   |-- orchestrator_status_test.exs
|   |   |   |-- specs_check_test.exs
|   |   |   |-- ssh_test.exs
|   |   |   |-- status_dashboard_snapshot_test.exs
|   |   |   `-- workspace_and_config_test.exs
|   |   `-- test_helper.exs
|   |-- .formatter.exs
|   |-- .gitattributes
|   |-- .gitignore
|   |-- AGENTS.md
|   |-- Makefile
|   |-- mise.toml
|   |-- mix.exs
|   |-- README.md
|   `-- WORKFLOW.md
|-- LICENSE
|-- NOTICE
|-- README.md
`-- SPEC.md
```

## Hotspots

### Largest Source / Config Files

| File | Lines |
| --- | ---: |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 1952 |
| `elixir/test/symphony_elixir/core_test.exs` | 1819 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 1655 |
| `elixir/test/symphony_elixir/orchestrator_status_test.exs` | 1604 |
| `elixir/test/symphony_elixir/app_server_test.exs` | 1410 |
| `elixir/test/symphony_elixir/workspace_and_config_test.exs` | 1306 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 1096 |
| `elixir/test/symphony_elixir/live_e2e_test.exs` | 802 |
| `elixir/test/symphony_elixir/extensions_test.exs` | 750 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 586 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 557 |
| `elixir/lib/symphony_elixir/workspace.ex` | 483 |
| `elixir/priv/static/dashboard.css` | 463 |
| `elixir/test/mix/tasks/workspace_before_remove_test.exs` | 390 |
| `elixir/test/mix/tasks/pr_body_check_test.exs` | 341 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 330 |
| `elixir/test/symphony_elixir/dynamic_tool_test.exs` | 310 |
| `elixir/test/support/test_support.exs` | 290 |
| `elixir/test/symphony_elixir/status_dashboard_snapshot_test.exs` | 288 |
| `elixir/lib/mix/tasks/pr_body.check.ex` | 216 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 209 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 203 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 200 |
| `elixir/test/symphony_elixir/ssh_test.exs` | 199 |
| `elixir/lib/symphony_elixir/cli.ex` | 191 |
| `elixir/lib/symphony_elixir/specs_check.ex` | 175 |
| `elixir/lib/symphony_elixir/config.ex` | 154 |
| `elixir/lib/symphony_elixir/workflow_store.ex` | 153 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 140 |
| `elixir/test/symphony_elixir/cli_test.exs` | 139 |

### Most Changed Source / Config Files: Last 90 Days

| File | 90d Changes |
| --- | ---: |
| `elixir/test/symphony_elixir/core_test.exs` | 6 |
| `elixir/test/symphony_elixir/workspace_and_config_test.exs` | 5 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 5 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 5 |
| `elixir/test/symphony_elixir/app_server_test.exs` | 4 |
| `elixir/Makefile` | 4 |
| `elixir/lib/symphony_elixir/config.ex` | 4 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 4 |
| `elixir/lib/symphony_elixir/workspace.ex` | 4 |
| `elixir/test/symphony_elixir/extensions_test.exs` | 4 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 3 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 3 |
| `elixir/test/support/test_support.exs` | 3 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 3 |
| `elixir/lib/symphony_elixir/http_server.ex` | 3 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 3 |
| `elixir/mix.exs` | 3 |
| `.github/workflows/make-all.yml` | 2 |
| `.github/workflows/pr-description-lint.yml` | 2 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 2 |
| `elixir/test/symphony_elixir/dynamic_tool_test.exs` | 2 |
| `elixir/test/symphony_elixir/live_e2e_test.exs` | 2 |
| `elixir/test/symphony_elixir/orchestrator_status_test.exs` | 2 |
| `elixir/lib/symphony_elixir/tracker.ex` | 2 |
| `elixir/lib/symphony_elixir.ex` | 2 |
| `elixir/lib/symphony_elixir/ssh.ex` | 1 |
| `elixir/test/support/live_e2e_docker/Dockerfile` | 1 |
| `elixir/test/support/live_e2e_docker/docker-compose.yml` | 1 |
| `elixir/test/support/live_e2e_docker/live_worker_entrypoint.sh` | 1 |
| `elixir/test/support/live_e2e_docker/symphony-live-worker.conf` | 1 |

### Size x Recent Churn

| File | Lines | 90d Changes | Hotspot Score |
| --- | ---: | ---: | ---: |
| `elixir/test/symphony_elixir/core_test.exs` | 1819 | 6 | 10914 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 1655 | 4 | 6620 |
| `elixir/test/symphony_elixir/workspace_and_config_test.exs` | 1306 | 5 | 6530 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 1952 | 3 | 5856 |
| `elixir/test/symphony_elixir/app_server_test.exs` | 1410 | 4 | 5640 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 1096 | 5 | 5480 |
| `elixir/test/symphony_elixir/orchestrator_status_test.exs` | 1604 | 2 | 3208 |
| `elixir/test/symphony_elixir/extensions_test.exs` | 750 | 4 | 3000 |
| `elixir/lib/symphony_elixir/workspace.ex` | 483 | 4 | 1932 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 586 | 3 | 1758 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 557 | 3 | 1671 |
| `elixir/test/symphony_elixir/live_e2e_test.exs` | 802 | 2 | 1604 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 203 | 5 | 1015 |
| `elixir/test/support/test_support.exs` | 290 | 3 | 870 |
| `elixir/test/symphony_elixir/dynamic_tool_test.exs` | 310 | 2 | 620 |
| `elixir/lib/symphony_elixir/config.ex` | 154 | 4 | 616 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 200 | 3 | 600 |
| `elixir/priv/static/dashboard.css` | 463 | 1 | 463 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 209 | 2 | 418 |
| `elixir/test/mix/tasks/workspace_before_remove_test.exs` | 390 | 1 | 390 |
| `elixir/test/mix/tasks/pr_body_check_test.exs` | 341 | 1 | 341 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 330 | 1 | 330 |
| `elixir/mix.exs` | 98 | 3 | 294 |
| `elixir/test/symphony_elixir/status_dashboard_snapshot_test.exs` | 288 | 1 | 288 |
| `elixir/lib/symphony_elixir/http_server.ex` | 88 | 3 | 264 |
| `elixir/lib/mix/tasks/pr_body.check.ex` | 216 | 1 | 216 |
| `elixir/test/symphony_elixir/ssh_test.exs` | 199 | 1 | 199 |
| `elixir/lib/symphony_elixir/cli.ex` | 191 | 1 | 191 |
| `elixir/Makefile` | 47 | 4 | 188 |
| `elixir/lib/symphony_elixir/specs_check.ex` | 175 | 1 | 175 |

### Large Elixir Module Warnings

High attention, over 1,000 lines:

- `elixir/lib/symphony_elixir/orchestrator.ex`: `1655` lines - large; likely owns concurrency, retry, and state behavior.
- `elixir/lib/symphony_elixir/status_dashboard.ex`: `1952` lines - large; likely mixes rendering, formatting, and event humanization.
- `elixir/lib/symphony_elixir/codex/app_server.ex`: `1096` lines - large; likely owns external protocol and session behavior.

Likely refactor candidates, over 500 lines:

- `elixir/lib/symphony_elixir/config/schema.ex`: `557` lines - medium-large; config validation and runtime behavior boundary.
- `elixir/lib/symphony_elixir/linear/client.ex`: `586` lines - medium-large; external API and token-handling boundary.

## Test Surface

### Source / Test Ratio

| Metric | Value |
| --- | --- |
| Source files | 37 |
| Source lines | 9458 |
| Test files | 16 |
| Test lines | 9603 |
| Test/source ratio | 1.02 |

### Largest Test Files

| File | Lines |
| --- | ---: |
| `elixir/test/symphony_elixir/core_test.exs` | 1819 |
| `elixir/test/symphony_elixir/orchestrator_status_test.exs` | 1604 |
| `elixir/test/symphony_elixir/app_server_test.exs` | 1410 |
| `elixir/test/symphony_elixir/workspace_and_config_test.exs` | 1306 |
| `elixir/test/symphony_elixir/live_e2e_test.exs` | 802 |
| `elixir/test/symphony_elixir/extensions_test.exs` | 750 |
| `elixir/test/mix/tasks/workspace_before_remove_test.exs` | 390 |
| `elixir/test/mix/tasks/pr_body_check_test.exs` | 341 |
| `elixir/test/symphony_elixir/dynamic_tool_test.exs` | 310 |
| `elixir/test/symphony_elixir/status_dashboard_snapshot_test.exs` | 288 |
| `elixir/test/symphony_elixir/ssh_test.exs` | 199 |
| `elixir/test/symphony_elixir/cli_test.exs` | 139 |
| `elixir/test/mix/tasks/specs_check_task_test.exs` | 112 |
| `elixir/test/symphony_elixir/specs_check_test.exs` | 92 |
| `elixir/test/symphony_elixir/observability_pubsub_test.exs` | 28 |
| `elixir/test/symphony_elixir/log_file_test.exs` | 13 |

### Largest Source Files Without Obvious Matching Tests

| Source File | Lines |
| --- | ---: |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 1952 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 1655 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 1096 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 586 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 557 |
| `elixir/lib/symphony_elixir/workspace.ex` | 483 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 330 |
| `elixir/lib/mix/tasks/pr_body.check.ex` | 216 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 209 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 203 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 200 |
| `elixir/lib/symphony_elixir/config.ex` | 154 |
| `elixir/lib/symphony_elixir/workflow_store.ex` | 153 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 140 |
| `elixir/lib/symphony_elixir/workflow.ex` | 123 |
| `elixir/lib/symphony_elixir/linear/adapter.ex` | 91 |
| `elixir/lib/symphony_elixir/http_server.ex` | 88 |
| `elixir/lib/symphony_elixir/tracker/memory.ex` | 72 |
| `elixir/lib/symphony_elixir/prompt_builder.ex` | 64 |
| `elixir/lib/symphony_elixir_web/controllers/observability_api_controller.ex` | 63 |
| `elixir/lib/symphony_elixir_web/components/layouts.ex` | 56 |
| `elixir/lib/mix/tasks/specs.check.ex` | 53 |
| `elixir/lib/symphony_elixir/path_safety.ex` | 50 |
| `elixir/lib/symphony_elixir.ex` | 47 |
| `elixir/lib/symphony_elixir/tracker.ex` | 46 |
| `elixir/lib/symphony_elixir/linear/issue.ex` | 43 |
| `elixir/lib/symphony_elixir_web/router.ex` | 41 |
| `elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex` | 35 |
| `elixir/lib/symphony_elixir_web/static_assets.ex` | 33 |
| `elixir/lib/symphony_elixir_web/endpoint.ex` | 32 |

### Detected Test Files

- `elixir/test/symphony_elixir/core_test.exs`
- `elixir/test/symphony_elixir/orchestrator_status_test.exs`
- `elixir/test/symphony_elixir/app_server_test.exs`
- `elixir/test/symphony_elixir/workspace_and_config_test.exs`
- `elixir/test/symphony_elixir/live_e2e_test.exs`
- `elixir/test/symphony_elixir/extensions_test.exs`
- `elixir/test/mix/tasks/workspace_before_remove_test.exs`
- `elixir/test/mix/tasks/pr_body_check_test.exs`
- `elixir/test/symphony_elixir/dynamic_tool_test.exs`
- `elixir/test/symphony_elixir/status_dashboard_snapshot_test.exs`
- `elixir/test/symphony_elixir/ssh_test.exs`
- `elixir/test/symphony_elixir/cli_test.exs`
- `elixir/test/mix/tasks/specs_check_task_test.exs`
- `elixir/test/symphony_elixir/specs_check_test.exs`
- `elixir/test/symphony_elixir/observability_pubsub_test.exs`
- `elixir/test/symphony_elixir/log_file_test.exs`

## Architecture Surface

### Elixir Module / Function Surface

| File | Modules | Public defs | Private defs | Callbacks-ish | Lines |
| --- | ---: | ---: | ---: | ---: | ---: |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 2 | 25 | 143 | 15 | 1655 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 11 | 25 | 38 | 0 | 557 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 1 | 23 | 223 | 8 | 1952 |
| `elixir/lib/symphony_elixir/workspace.ex` | 1 | 10 | 28 | 0 | 483 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 1 | 9 | 48 | 0 | 586 |
| `elixir/lib/symphony_elixir/config.ex` | 1 | 9 | 2 | 0 | 154 |
| `elixir/lib/symphony_elixir/workflow_store.ex` | 2 | 7 | 7 | 5 | 153 |
| `elixir/lib/symphony_elixir/workflow.ex` | 1 | 6 | 4 | 0 | 123 |
| `elixir/lib/symphony_elixir/tracker.ex` | 1 | 6 | 0 | 0 | 46 |
| `elixir/lib/symphony_elixir/linear/adapter.ex` | 1 | 5 | 2 | 0 | 91 |
| `elixir/lib/symphony_elixir/tracker/memory.ex` | 1 | 5 | 5 | 0 | 72 |
| `elixir/lib/symphony_elixir_web/controllers/observability_api_controller.ex` | 1 | 5 | 3 | 1 | 63 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 1 | 4 | 70 | 0 | 1096 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 1 | 4 | 17 | 3 | 330 |
| `elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex` | 1 | 4 | 1 | 1 | 35 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 1 | 3 | 21 | 0 | 200 |
| `elixir/lib/symphony_elixir/cli.ex` | 1 | 3 | 9 | 0 | 191 |
| `elixir/lib/symphony_elixir/ssh.ex` | 1 | 3 | 11 | 0 | 100 |
| `elixir/lib/symphony_elixir/http_server.ex` | 1 | 3 | 7 | 0 | 88 |
| `elixir/lib/symphony_elixir/log_file.ex` | 1 | 3 | 4 | 0 | 80 |
| `elixir/lib/symphony_elixir.ex` | 2 | 3 | 0 | 0 | 47 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 1 | 2 | 19 | 0 | 209 |
| `elixir/lib/symphony_elixir/specs_check.ex` | 1 | 2 | 24 | 0 | 175 |
| `elixir/mix.exs` | 1 | 2 | 3 | 0 | 98 |
| `elixir/lib/symphony_elixir_web/components/layouts.ex` | 1 | 2 | 0 | 1 | 56 |
| `elixir/lib/symphony_elixir_web/observability_pubsub.ex` | 1 | 2 | 0 | 0 | 25 |
| `elixir/lib/mix/tasks/pr_body.check.ex` | 1 | 1 | 18 | 0 | 216 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 1 | 1 | 20 | 0 | 203 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 1 | 1 | 11 | 0 | 140 |
| `elixir/lib/symphony_elixir/prompt_builder.ex` | 1 | 1 | 13 | 0 | 64 |
| `elixir/lib/mix/tasks/specs.check.ex` | 1 | 1 | 1 | 0 | 53 |
| `elixir/lib/symphony_elixir/path_safety.ex` | 1 | 1 | 4 | 0 | 50 |
| `elixir/lib/symphony_elixir/linear/issue.ex` | 1 | 1 | 0 | 0 | 43 |
| `elixir/lib/symphony_elixir_web/static_assets.ex` | 1 | 1 | 0 | 0 | 33 |
| `elixir/lib/symphony_elixir_web/error_html.ex` | 1 | 1 | 0 | 0 | 8 |
| `elixir/lib/symphony_elixir_web/error_json.ex` | 1 | 1 | 0 | 0 | 8 |
| `elixir/lib/symphony_elixir_web/router.ex` | 1 | 0 | 0 | 0 | 41 |
| `elixir/lib/symphony_elixir_web/endpoint.ex` | 1 | 0 | 0 | 0 | 32 |

High public function count can signal a module carrying too many responsibilities.

### Routes / Controllers / Live Views

Total matches: `11`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir_web/router.ex` | 5 |
| `elixir/lib/symphony_elixir_web/controllers/observability_api_controller.ex` | 2 |
| `elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex` | 2 |
| `elixir/lib/symphony_elixir_web/components/layouts.ex` | 1 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 1 |

```text
elixir/lib/symphony_elixir_web/router.ex:6: use Phoenix.Router
elixir/lib/symphony_elixir_web/router.ex:17: scope "/", SymphonyElixirWeb do
elixir/lib/symphony_elixir_web/router.ex:24: scope "/", SymphonyElixirWeb do
elixir/lib/symphony_elixir_web/router.ex:25: pipe_through(:browser)
elixir/lib/symphony_elixir_web/router.ex:30: scope "/", SymphonyElixirWeb do
elixir/lib/symphony_elixir_web/components/layouts.ex:6: use Phoenix.Component
elixir/lib/symphony_elixir_web/controllers/observability_api_controller.ex:1: defmodule SymphonyElixirWeb.ObservabilityApiController do
elixir/lib/symphony_elixir_web/controllers/observability_api_controller.ex:6: use Phoenix.Controller, formats: [:json]
elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex:1: defmodule SymphonyElixirWeb.StaticAssetController do
elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex:6: use Phoenix.Controller, formats: []
elixir/lib/symphony_elixir_web/live/dashboard_live.ex:6: use Phoenix.LiveView, layout: {SymphonyElixirWeb.Layouts, :app}
```

### Workers / Jobs / Cron / Processes

Total matches: `63`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 23 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 11 |
| `elixir/lib/symphony_elixir/workspace.ex` | 7 |
| `elixir/lib/symphony_elixir/workflow_store.ex` | 5 |
| `elixir/lib/symphony_elixir.ex` | 4 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 3 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 3 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 3 |
| `elixir/lib/symphony_elixir/cli.ex` | 2 |
| `elixir/lib/symphony_elixir/http_server.ex` | 1 |

```text
elixir/lib/symphony_elixir.ex:17: OTP application entrypoint that starts core supervisors and workers.
elixir/lib/symphony_elixir.ex:28: {Task.Supervisor, name: SymphonyElixir.TaskSupervisor},
elixir/lib/symphony_elixir.ex:35: Supervisor.start_link(
elixir/lib/symphony_elixir.ex:38: name: SymphonyElixir.Supervisor
elixir/lib/symphony_elixir/agent_runner.ex:14: # The orchestrator owns host retries so one worker lifetime never hops machines.
elixir/lib/symphony_elixir/agent_runner.ex:15: worker_host = selected_worker_host(Keyword.get(opts, :worker_host), Config.settings!().worker.ssh_hosts)
elixir/lib/symphony_elixir/agent_runner.ex:30: Logger.info("Starting worker attempt for #{issue_context(issue)} worker_host=#{worker_host_for_log(worker_host)}")
elixir/lib/symphony_elixir/cli.ex:174: case Process.whereis(SymphonyElixir.Supervisor) do
elixir/lib/symphony_elixir/cli.ex:176: IO.puts(:stderr, "Symphony supervisor is not running")
elixir/lib/symphony_elixir/http_server.ex:11: @spec child_spec(keyword()) :: Supervisor.child_spec()
elixir/lib/symphony_elixir/orchestrator.ex:6: use GenServer
elixir/lib/symphony_elixir/orchestrator.ex:74: def handle_info({:tick, tick_token}, %{tick_token: tick_token} = state)
elixir/lib/symphony_elixir/orchestrator.ex:91: def handle_info({:tick, _tick_token}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/orchestrator.ex:93: def handle_info(:tick, state) do
elixir/lib/symphony_elixir/orchestrator.ex:109: def handle_info(:run_poll_cycle, state) do
elixir/lib/symphony_elixir/orchestrator.ex:119: def handle_info(
elixir/lib/symphony_elixir/orchestrator.ex:166: def handle_info({:worker_runtime_info, issue_id, runtime_info}, %{running: running} = state)
elixir/lib/symphony_elixir/orchestrator.ex:183: def handle_info(
elixir/lib/symphony_elixir/orchestrator.ex:204: def handle_info({:codex_worker_update, _issue_id, _update}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/orchestrator.ex:206: def handle_info({:retry_issue, issue_id, retry_token}, state) do
elixir/lib/symphony_elixir/orchestrator.ex:217: def handle_info({:retry_issue, _issue_id}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/orchestrator.ex:219: def handle_info(msg, state) do
elixir/lib/symphony_elixir/orchestrator.ex:355: Logger.info("Issue no longer routed to this worker: #{issue_context(issue)} assignee=#{inspect(issue.assignee_id)}; stopping active agent")
elixir/lib/symphony_elixir/orchestrator.ex:508: case Task.Supervisor.terminate_child(SymphonyElixir.TaskSupervisor, pid) do
elixir/lib/symphony_elixir/orchestrator.ex:685: Logger.debug("No SSH worker slots available for #{issue_context(issue)} preferred_worker_host=#{inspect(preferred_worker_host)}")
elixir/lib/symphony_elixir/orchestrator.ex:694: case Task.Supervisor.start_child(SymphonyElixir.TaskSupervisor, fn ->
elixir/lib/symphony_elixir/orchestrator.ex:790: timer_ref = Process.send_after(self(), {:retry_issue, issue_id, retry_token}, delay_ms)
elixir/lib/symphony_elixir/orchestrator.ex:974: case Config.settings!().worker.ssh_hosts do
elixir/lib/symphony_elixir/orchestrator.ex:1026: case Config.settings!().worker.max_concurrent_agents_per_host do
elixir/lib/symphony_elixir/orchestrator.ex:1101: def handle_call(:snapshot, _from, state) do
elixir/lib/symphony_elixir/orchestrator.ex:1157: def handle_call(:request_refresh, _from, state) do
elixir/lib/symphony_elixir/orchestrator.ex:1252: timer_ref = Process.send_after(self(), {:tick, tick_token}, delay_ms)
elixir/lib/symphony_elixir/orchestrator.ex:1263: :timer.send_after(@poll_transition_render_delay_ms, self(), :run_poll_cycle)
elixir/lib/symphony_elixir/ssh.ex:72: # here so worker config can use "localhost:2222" without requiring ssh:// URIs.
elixir/lib/symphony_elixir/status_dashboard.ex:3: Renders a status snapshot for orchestrator and worker activity as a terminal UI.
elixir/lib/symphony_elixir/status_dashboard.ex:6: use GenServer
elixir/lib/symphony_elixir/status_dashboard.ex:147: @spec handle_info(term(), t()) :: {:noreply, t()}
elixir/lib/symphony_elixir/status_dashboard.ex:148: def handle_info(:tick, %{enabled: true} = state) do
elixir/lib/symphony_elixir/status_dashboard.ex:155: def handle_info(:refresh, %{enabled: true} = state), do: {:noreply, maybe_render(refresh_runtime_config(state))}
elixir/lib/symphony_elixir/status_dashboard.ex:156: def handle_info(:refresh, state), do: {:noreply, state}
elixir/lib/symphony_elixir/status_dashboard.ex:158: def handle_info({:flush_render, timer_ref}, %{enabled: true, flush_timer_ref: timer_ref} = state) do
elixir/lib/symphony_elixir/status_dashboard.ex:176: def handle_info({:flush_render, _timer_ref}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/status_dashboard.ex:177: def handle_info(:tick, state), do: {:noreply, state}
elixir/lib/symphony_elixir/status_dashboard.ex:190: defp schedule_tick(refresh_ms, true), do: Process.send_after(self(), :tick, refresh_ms)
elixir/lib/symphony_elixir/status_dashboard.ex:278: Process.send_after(self(), {:flush_render, timer_ref}, delay_ms)
elixir/lib/symphony_elixir/workflow_store.ex:6: use GenServer
elixir/lib/symphony_elixir/workflow_store.ex:62: def handle_call(:current, _from, %State{} = state) do
elixir/lib/symphony_elixir/workflow_store.ex:72: def handle_call(:force_reload, _from, %State{} = state) do
elixir/lib/symphony_elixir/workflow_store.ex:83: def handle_info(:poll, %State{} = state) do
elixir/lib/symphony_elixir/workflow_store.ex:93: Process.send_after(self(), :poll, @poll_interval_ms)
elixir/lib/symphony_elixir/workspace.ex:148: case Config.settings!().worker.ssh_hosts do
elixir/lib/symphony_elixir/workspace.ex:300: Task.async(fn ->
elixir/lib/symphony_elixir/workspace.ex:304: case Task.yield(task, timeout_ms) do
elixir/lib/symphony_elixir/workspace.ex:309: Task.shutdown(task, :brutal_kill)
elixir/lib/symphony_elixir/workspace.ex:438: Task.async(fn ->
elixir/lib/symphony_elixir/workspace.ex:442: case Task.yield(task, timeout_ms) do
elixir/lib/symphony_elixir/workspace.ex:447: Task.shutdown(task, :brutal_kill)
elixir/lib/symphony_elixir/config/schema.ex:103: defmodule Worker do
elixir/lib/symphony_elixir/config/schema.ex:268: embeds_one(:worker, Worker, on_replace: :update, defaults_to_struct: true)
elixir/lib/symphony_elixir/config/schema.ex:360: |> cast_embed(:worker, with: &Worker.changeset/2)
elixir/lib/symphony_elixir_web/live/dashboard_live.ex:27: def handle_info(:runtime_tick, socket) do
elixir/lib/symphony_elixir_web/live/dashboard_live.ex:33: def handle_info(:observability_updated, socket) do
elixir/lib/symphony_elixir_web/live/dashboard_live.ex:325: Process.send_after(self(), :runtime_tick, @runtime_tick_ms)
```

### DB / Persistence

Total matches: `284`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/workspace.ex` | 113 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 46 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 46 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 25 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 19 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 12 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 6 |
| `elixir/lib/symphony_elixir/config.ex` | 4 |
| `elixir/lib/symphony_elixir_web/static_assets.ex` | 4 |
| `elixir/lib/mix/tasks/pr_body.check.ex` | 2 |

```text
elixir/mix.exs:28: SymphonyElixir.Workspace,
elixir/lib/mix/tasks/pr_body.check.ex:57: case File.read(path) do
elixir/lib/mix/tasks/pr_body.check.ex:71: case File.read(path) do
elixir/lib/mix/tasks/specs.check.ex:44: |> File.read!()
elixir/lib/mix/tasks/workspace.before_remove.ex:1: defmodule Mix.Tasks.Workspace.BeforeRemove do
elixir/lib/mix/tasks/workspace.before_remove.ex:4: @shortdoc "Close open GitHub PRs for the current branch before workspace removal"
elixir/lib/mix/tasks/workspace.before_remove.ex:9: This task is intended for use from the `before_remove` workspace hook.
elixir/lib/mix/tasks/workspace.before_remove.ex:13: mix workspace.before_remove
elixir/lib/mix/tasks/workspace.before_remove.ex:14: mix workspace.before_remove --branch feature/my-branch
elixir/lib/mix/tasks/workspace.before_remove.ex:15: mix workspace.before_remove --repo openai/symphony
elixir/lib/symphony_elixir/agent_runner.ex:3: Executes a single Linear issue in its workspace with Codex.
elixir/lib/symphony_elixir/agent_runner.ex:8: alias SymphonyElixir.{Config, Linear.Issue, PromptBuilder, Tracker, Workspace}
elixir/lib/symphony_elixir/agent_runner.ex:32: case Workspace.create_for_issue(issue, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:33: {:ok, workspace} ->
elixir/lib/symphony_elixir/agent_runner.ex:34: send_worker_runtime_info(codex_update_recipient, issue, worker_host, workspace)
elixir/lib/symphony_elixir/agent_runner.ex:37: with :ok <- Workspace.run_before_run_hook(workspace, issue, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:38: run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host)
elixir/lib/symphony_elixir/agent_runner.ex:41: Workspace.run_after_run_hook(workspace, issue, worker_host)
elixir/lib/symphony_elixir/agent_runner.ex:63: defp send_worker_runtime_info(recipient, %Issue{id: issue_id}, worker_host, workspace)
elixir/lib/symphony_elixir/agent_runner.ex:64: when is_binary(issue_id) and is_pid(recipient) and is_binary(workspace) do
elixir/lib/symphony_elixir/agent_runner.ex:70: workspace_path: workspace
elixir/lib/symphony_elixir/agent_runner.ex:77: defp send_worker_runtime_info(_recipient, _issue, _worker_host, _workspace), do: :ok
elixir/lib/symphony_elixir/agent_runner.ex:79: defp run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:83: with {:ok, session} <- AppServer.start_session(workspace, worker_host: worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:85: do_run_codex_turns(session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, 1, max_turns)
elixir/lib/symphony_elixir/agent_runner.ex:92: defp do_run_codex_turns(app_session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, turn_number, max_turns) do
elixir/lib/symphony_elixir/agent_runner.ex:102: Logger.info("Completed agent run for #{issue_context(issue)} session_id=#{turn_session[:session_id]} workspace=#{workspace} turn=#{turn_number}/#{max_turns}")
elixir/lib/symphony_elixir/agent_runner.ex:110: workspace,
elixir/lib/symphony_elixir/agent_runner.ex:141: - Resume from the current workspace and workpad state instead of restarting from scratch.
elixir/lib/symphony_elixir/config.ex:65: def codex_turn_sandbox_policy(workspace \\ nil) do
elixir/lib/symphony_elixir/config.ex:66: case Schema.resolve_runtime_turn_sandbox_policy(settings!(), workspace) do
elixir/lib/symphony_elixir/config.ex:103: def codex_runtime_settings(workspace \\ nil, opts \\ []) do
elixir/lib/symphony_elixir/config.ex:106: Schema.resolve_runtime_turn_sandbox_policy(settings, workspace, opts) do
elixir/lib/symphony_elixir/log_file.ex:34: :ok = File.mkdir_p(Path.dirname(expanded_path))
elixir/lib/symphony_elixir/orchestrator.ex:10: alias SymphonyElixir.{AgentRunner, Config, StatusDashboard, Tracker, Workspace}
elixir/lib/symphony_elixir/orchestrator.ex:67: run_terminal_workspace_cleanup()
elixir/lib/symphony_elixir/orchestrator.ex:143: workspace_path: Map.get(running_entry, :workspace_path)
elixir/lib/symphony_elixir/orchestrator.ex:155: workspace_path: Map.get(running_entry, :workspace_path)
elixir/lib/symphony_elixir/orchestrator.ex:176: |> maybe_put_runtime_value(:workspace_path, runtime_info[:workspace_path])
elixir/lib/symphony_elixir/orchestrator.ex:415: defp terminate_running_issue(%State{} = state, issue_id, cleanup_workspace) do
elixir/lib/symphony_elixir/orchestrator.ex:424: if cleanup_workspace do
elixir/lib/symphony_elixir/orchestrator.ex:425: cleanup_issue_workspace(identifier, worker_host)
elixir/lib/symphony_elixir/orchestrator.ex:709: workspace_path: nil,
elixir/lib/symphony_elixir/orchestrator.ex:784: workspace_path = pick_retry_workspace_path(previous_retry, metadata)
elixir/lib/symphony_elixir/orchestrator.ex:807: workspace_path: workspace_path
elixir/lib/symphony_elixir/orchestrator.ex:819: workspace_path: Map.get(retry_entry, :workspace_path)
elixir/lib/symphony_elixir/orchestrator.ex:854: Logger.info("Issue state is terminal: issue_id=#{issue_id} issue_identifier=#{issue.identifier} state=#{issue.state}; removing associated workspace")
elixir/lib/symphony_elixir/orchestrator.ex:856: cleanup_issue_workspace(issue.identifier, metadata[:worker_host])
elixir/lib/symphony_elixir/orchestrator.ex:874: defp cleanup_issue_workspace(identifier, worker_host \\ nil)
elixir/lib/symphony_elixir/orchestrator.ex:876: defp cleanup_issue_workspace(identifier, worker_host) when is_binary(identifier) do
elixir/lib/symphony_elixir/orchestrator.ex:877: Workspace.remove_issue_workspaces(identifier, worker_host)
elixir/lib/symphony_elixir/orchestrator.ex:880: defp cleanup_issue_workspace(_identifier, _worker_host), do: :ok
elixir/lib/symphony_elixir/orchestrator.ex:882: defp run_terminal_workspace_cleanup do
elixir/lib/symphony_elixir/orchestrator.ex:888: cleanup_issue_workspace(identifier)
elixir/lib/symphony_elixir/orchestrator.ex:895: Logger.warning("Skipping startup terminal workspace cleanup; failed to fetch terminal issues: #{inspect(reason)}")
elixir/lib/symphony_elixir/orchestrator.ex:963: defp pick_retry_workspace_path(previous_retry, metadata) do
elixir/lib/symphony_elixir/orchestrator.ex:964: metadata[:workspace_path] || Map.get(previous_retry, :workspace_path)
elixir/lib/symphony_elixir/orchestrator.ex:1114: workspace_path: Map.get(metadata, :workspace_path),
elixir/lib/symphony_elixir/orchestrator.ex:1139: workspace_path: Map.get(retry, :workspace_path)
elixir/lib/symphony_elixir/path_safety.ex:30: with {:ok, target} <- :file.read_link_all(String.to_charlist(candidate_path)) do
elixir/lib/symphony_elixir/specs_check.ex:44: with {:ok, source} <- File.read(file),
elixir/lib/symphony_elixir/workflow.ex:54: case File.read(path) do
elixir/lib/symphony_elixir/workflow_store.ex:143: {:ok, content} <- File.read(path) do
elixir/lib/symphony_elixir/workspace.ex:1: defmodule SymphonyElixir.Workspace do
elixir/lib/symphony_elixir/workspace.ex:3: Creates isolated per-issue workspaces for parallel Codex agents.
elixir/lib/symphony_elixir/workspace.ex:9: @remote_workspace_marker "__SYMPHONY_WORKSPACE__"
elixir/lib/symphony_elixir/workspace.ex:21: with {:ok, workspace} <- workspace_path_for_issue(safe_id, worker_host),
elixir/lib/symphony_elixir/workspace.ex:22: :ok <- validate_workspace_path(workspace, worker_host),
elixir/lib/symphony_elixir/workspace.ex:23: {:ok, workspace, created?} <- ensure_workspace(workspace, worker_host),
elixir/lib/symphony_elixir/workspace.ex:24: :ok <- maybe_run_after_create_hook(workspace, issue_context, created?, worker_host) do
elixir/lib/symphony_elixir/workspace.ex:25: {:ok, workspace}
elixir/lib/symphony_elixir/workspace.ex:29: Logger.error("Workspace creation failed #{issue_log_context(issue_context)} worker_host=#{worker_host_for_log(worker_host)} error=#{Exception.message(error)}")
elixir/lib/symphony_elixir/workspace.ex:34: defp ensure_workspace(workspace, nil) do
elixir/lib/symphony_elixir/workspace.ex:36: File.dir?(workspace) ->
elixir/lib/symphony_elixir/workspace.ex:37: {:ok, workspace, false}
elixir/lib/symphony_elixir/workspace.ex:39: File.exists?(workspace) ->
elixir/lib/symphony_elixir/workspace.ex:40: File.rm_rf!(workspace)
elixir/lib/symphony_elixir/workspace.ex:41: create_workspace(workspace)
elixir/lib/symphony_elixir/workspace.ex:44: create_workspace(workspace)
elixir/lib/symphony_elixir/workspace.ex:48: defp ensure_workspace(workspace, worker_host) when is_binary(worker_host) do
```

... truncated after 80 matches

### External API Clients

Total matches: `368`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 110 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 80 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 31 |
| `elixir/lib/symphony_elixir/codex/dynamic_tool.ex` | 30 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 20 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 18 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 17 |
| `elixir/lib/symphony_elixir/config.ex` | 15 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 14 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 5 |

```text
.github/workflows/pr-description-lint.yml:27: PR_BODY_JSON: ${{ toJson(github.event.pull_request.body) }}
elixir/mix.exs:17: SymphonyElixir.Linear.Client,
elixir/mix.exs:23: SymphonyElixir.Codex.AppServer,
elixir/mix.exs:24: SymphonyElixir.Codex.DynamicTool,
elixir/lib/mix/tasks/pr_body.check.ex:16: ".github/pull_request_template.md",
elixir/lib/mix/tasks/pr_body.check.ex:17: "../.github/pull_request_template.md"
elixir/lib/mix/tasks/workspace.before_remove.ex:4: @shortdoc "Close open GitHub PRs for the current branch before workspace removal"
elixir/lib/mix/tasks/workspace.before_remove.ex:15: mix workspace.before_remove --repo openai/symphony
elixir/lib/mix/tasks/workspace.before_remove.ex:18: @default_repo "openai/symphony"
elixir/lib/mix/tasks/workspace.before_remove.ex:109: "Closing because the Linear issue for branch #{branch} entered a terminal state without merge."
elixir/lib/symphony_elixir/agent_runner.ex:3: Executes a single Linear issue in its workspace with Codex.
elixir/lib/symphony_elixir/agent_runner.ex:7: alias SymphonyElixir.Codex.AppServer
elixir/lib/symphony_elixir/agent_runner.ex:8: alias SymphonyElixir.{Config, Linear.Issue, PromptBuilder, Tracker, Workspace}
elixir/lib/symphony_elixir/agent_runner.ex:13: def run(issue, codex_update_recipient \\ nil, opts \\ []) do
elixir/lib/symphony_elixir/agent_runner.ex:19: case run_on_worker_host(issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:29: defp run_on_worker_host(issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:34: send_worker_runtime_info(codex_update_recipient, issue, worker_host, workspace)
elixir/lib/symphony_elixir/agent_runner.ex:38: run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host)
elixir/lib/symphony_elixir/agent_runner.ex:49: defp codex_message_handler(recipient, issue) do
elixir/lib/symphony_elixir/agent_runner.ex:51: send_codex_update(recipient, issue, message)
elixir/lib/symphony_elixir/agent_runner.ex:55: defp send_codex_update(recipient, %Issue{id: issue_id}, message)
elixir/lib/symphony_elixir/agent_runner.ex:57: send(recipient, {:codex_worker_update, issue_id, message})
elixir/lib/symphony_elixir/agent_runner.ex:61: defp send_codex_update(_recipient, _issue, _message), do: :ok
elixir/lib/symphony_elixir/agent_runner.ex:79: defp run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:85: do_run_codex_turns(session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, 1, max_turns)
elixir/lib/symphony_elixir/agent_runner.ex:92: defp do_run_codex_turns(app_session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, turn_number, max_turns) do
elixir/lib/symphony_elixir/agent_runner.ex:100: on_message: codex_message_handler(codex_update_recipient, issue)
elixir/lib/symphony_elixir/agent_runner.ex:108: do_run_codex_turns(
elixir/lib/symphony_elixir/agent_runner.ex:112: codex_update_recipient,
elixir/lib/symphony_elixir/agent_runner.ex:139: - The previous Codex turn completed normally, but the Linear issue is still in an active state.
elixir/lib/symphony_elixir/cli.ex:117: "Codex will run without any guardrails.",
elixir/lib/symphony_elixir/config.ex:10: You are working on a Linear issue.
elixir/lib/symphony_elixir/config.ex:23: @type codex_runtime_settings :: %{
elixir/lib/symphony_elixir/config.ex:64: @spec codex_turn_sandbox_policy(Path.t() | nil) :: map()
elixir/lib/symphony_elixir/config.ex:65: def codex_turn_sandbox_policy(workspace \\ nil) do
elixir/lib/symphony_elixir/config.ex:71: raise ArgumentError, message: "Invalid codex turn sandbox policy: #{inspect(reason)}"
elixir/lib/symphony_elixir/config.ex:101: @spec codex_runtime_settings(Path.t() | nil, keyword()) ::
elixir/lib/symphony_elixir/config.ex:102: {:ok, codex_runtime_settings()} | {:error, term()}
elixir/lib/symphony_elixir/config.ex:103: def codex_runtime_settings(workspace \\ nil, opts \\ []) do
elixir/lib/symphony_elixir/config.ex:109: approval_policy: settings.codex.approval_policy,
elixir/lib/symphony_elixir/config.ex:110: thread_sandbox: settings.codex.thread_sandbox,
elixir/lib/symphony_elixir/config.ex:122: settings.tracker.kind not in ["linear", "memory"] ->
elixir/lib/symphony_elixir/config.ex:125: settings.tracker.kind == "linear" and not is_binary(settings.tracker.api_key) ->
elixir/lib/symphony_elixir/config.ex:126: {:error, :missing_linear_api_token}
elixir/lib/symphony_elixir/config.ex:128: settings.tracker.kind == "linear" and not is_binary(settings.tracker.project_slug) ->
elixir/lib/symphony_elixir/config.ex:129: {:error, :missing_linear_project_slug}
elixir/lib/symphony_elixir/orchestrator.ex:3: Polls Linear and dispatches repository copies to Codex-backed workers.
elixir/lib/symphony_elixir/orchestrator.ex:11: alias SymphonyElixir.Linear.Issue
elixir/lib/symphony_elixir/orchestrator.ex:17: @empty_codex_totals %{
elixir/lib/symphony_elixir/orchestrator.ex:40: codex_totals: nil,
elixir/lib/symphony_elixir/orchestrator.ex:41: codex_rate_limits: nil
elixir/lib/symphony_elixir/orchestrator.ex:63: codex_totals: @empty_codex_totals,
elixir/lib/symphony_elixir/orchestrator.ex:64: codex_rate_limits: nil
elixir/lib/symphony_elixir/orchestrator.ex:184: {:codex_worker_update, issue_id, %{event: _, timestamp: _} = update},
elixir/lib/symphony_elixir/orchestrator.ex:192: {updated_running_entry, token_delta} = integrate_codex_update(running_entry, update)
elixir/lib/symphony_elixir/orchestrator.ex:196: |> apply_codex_token_delta(token_delta)
elixir/lib/symphony_elixir/orchestrator.ex:197: |> apply_codex_rate_limits(update)
elixir/lib/symphony_elixir/orchestrator.ex:204: def handle_info({:codex_worker_update, _issue_id, _update}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/orchestrator.ex:232: {:error, :missing_linear_api_token} ->
elixir/lib/symphony_elixir/orchestrator.ex:233: Logger.error("Linear API token missing in WORKFLOW.md")
elixir/lib/symphony_elixir/orchestrator.ex:236: {:error, :missing_linear_project_slug} ->
elixir/lib/symphony_elixir/orchestrator.ex:237: Logger.error("Linear project slug missing in WORKFLOW.md")
elixir/lib/symphony_elixir/orchestrator.ex:267: Logger.error("Failed to fetch from Linear: #{inspect(reason)}")
elixir/lib/symphony_elixir/orchestrator.ex:449: timeout_ms = Config.settings!().codex.stall_timeout_ms
elixir/lib/symphony_elixir/orchestrator.ex:482: error: "stalled for #{elapsed_ms}ms without codex activity"
elixir/lib/symphony_elixir/orchestrator.ex:502: Map.get(running_entry, :last_codex_timestamp) || Map.get(running_entry, :started_at)
elixir/lib/symphony_elixir/orchestrator.ex:711: last_codex_message: nil,
elixir/lib/symphony_elixir/orchestrator.ex:712: last_codex_timestamp: nil,
elixir/lib/symphony_elixir/orchestrator.ex:713: last_codex_event: nil,
elixir/lib/symphony_elixir/orchestrator.ex:714: codex_app_server_pid: nil,
elixir/lib/symphony_elixir/orchestrator.ex:715: codex_input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:716: codex_output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:717: codex_total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:718: codex_last_reported_input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:719: codex_last_reported_output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:720: codex_last_reported_total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:1116: codex_app_server_pid: metadata.codex_app_server_pid,
elixir/lib/symphony_elixir/orchestrator.ex:1117: codex_input_tokens: metadata.codex_input_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1118: codex_output_tokens: metadata.codex_output_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1119: codex_total_tokens: metadata.codex_total_tokens,
```

... truncated after 80 matches

### Auth / Security

Total matches: `301`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 138 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 90 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 13 |
| `elixir/lib/symphony_elixir/ssh.ex` | 12 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 9 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 8 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 5 |
| `elixir/lib/symphony_elixir_web/components/layouts.ex` | 5 |
| `elixir/lib/symphony_elixir/http_server.ex` | 4 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 3 |

```text
elixir/config/config.exs:14: secret_key_base: String.duplicate("s", 64),
elixir/lib/mix/tasks/workspace.before_remove.ex:46: if gh_available?() and gh_authenticated?() do
elixir/lib/mix/tasks/workspace.before_remove.ex:59: defp gh_authenticated? do
elixir/lib/mix/tasks/workspace.before_remove.ex:60: match?({:ok, _output}, run_command("gh", ["auth", "status"]))
elixir/lib/symphony_elixir/agent_runner.ex:15: worker_host = selected_worker_host(Keyword.get(opts, :worker_host), Config.settings!().worker.ssh_hosts)
elixir/lib/symphony_elixir/config.ex:126: {:error, :missing_linear_api_token}
elixir/lib/symphony_elixir/http_server.ex:9: @secret_key_bytes 48
elixir/lib/symphony_elixir/http_server.ex:34: secret_key_base: secret_key_base()
elixir/lib/symphony_elixir/http_server.ex:85: defp secret_key_base do
elixir/lib/symphony_elixir/http_server.ex:86: Base.encode64(:crypto.strong_rand_bytes(@secret_key_bytes), padding: false)
elixir/lib/symphony_elixir/orchestrator.ex:18: input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:19: output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:20: total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:35: :tick_token,
elixir/lib/symphony_elixir/orchestrator.ex:62: tick_token: nil,
elixir/lib/symphony_elixir/orchestrator.ex:74: def handle_info({:tick, tick_token}, %{tick_token: tick_token} = state)
elixir/lib/symphony_elixir/orchestrator.ex:75: when is_reference(tick_token) do
elixir/lib/symphony_elixir/orchestrator.ex:83: tick_token: nil
elixir/lib/symphony_elixir/orchestrator.ex:91: def handle_info({:tick, _tick_token}, state), do: {:noreply, state}
elixir/lib/symphony_elixir/orchestrator.ex:101: tick_token: nil
elixir/lib/symphony_elixir/orchestrator.ex:192: {updated_running_entry, token_delta} = integrate_codex_update(running_entry, update)
elixir/lib/symphony_elixir/orchestrator.ex:196: |> apply_codex_token_delta(token_delta)
elixir/lib/symphony_elixir/orchestrator.ex:206: def handle_info({:retry_issue, issue_id, retry_token}, state) do
elixir/lib/symphony_elixir/orchestrator.ex:208: case pop_retry_attempt_state(state, issue_id, retry_token) do
elixir/lib/symphony_elixir/orchestrator.ex:232: {:error, :missing_linear_api_token} ->
elixir/lib/symphony_elixir/orchestrator.ex:233: Logger.error("Linear API token missing in WORKFLOW.md")
elixir/lib/symphony_elixir/orchestrator.ex:685: Logger.debug("No SSH worker slots available for #{issue_context(issue)} preferred_worker_host=#{inspect(preferred_worker_host)}")
elixir/lib/symphony_elixir/orchestrator.ex:715: codex_input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:716: codex_output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:717: codex_total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:718: codex_last_reported_input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:719: codex_last_reported_output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:720: codex_last_reported_total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:779: retry_token = make_ref()
elixir/lib/symphony_elixir/orchestrator.ex:790: timer_ref = Process.send_after(self(), {:retry_issue, issue_id, retry_token}, delay_ms)
elixir/lib/symphony_elixir/orchestrator.ex:802: retry_token: retry_token,
elixir/lib/symphony_elixir/orchestrator.ex:812: defp pop_retry_attempt_state(%State{} = state, issue_id, retry_token) when is_reference(retry_token) do
elixir/lib/symphony_elixir/orchestrator.ex:814: %{attempt: attempt, retry_token: ^retry_token} = retry_entry ->
elixir/lib/symphony_elixir/orchestrator.ex:974: case Config.settings!().worker.ssh_hosts do
elixir/lib/symphony_elixir/orchestrator.ex:1117: codex_input_tokens: metadata.codex_input_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1118: codex_output_tokens: metadata.codex_output_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1119: codex_total_tokens: metadata.codex_total_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1173: token_delta = extract_token_delta(running_entry, update)
elixir/lib/symphony_elixir/orchestrator.ex:1174: codex_input_tokens = Map.get(running_entry, :codex_input_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1175: codex_output_tokens = Map.get(running_entry, :codex_output_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1176: codex_total_tokens = Map.get(running_entry, :codex_total_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1178: last_reported_input = Map.get(running_entry, :codex_last_reported_input_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1179: last_reported_output = Map.get(running_entry, :codex_last_reported_output_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1180: last_reported_total = Map.get(running_entry, :codex_last_reported_total_tokens, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1190: codex_input_tokens: codex_input_tokens + token_delta.input_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1191: codex_output_tokens: codex_output_tokens + token_delta.output_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1192: codex_total_tokens: codex_total_tokens + token_delta.total_tokens,
elixir/lib/symphony_elixir/orchestrator.ex:1193: codex_last_reported_input_tokens: max(last_reported_input, token_delta.input_reported),
elixir/lib/symphony_elixir/orchestrator.ex:1194: codex_last_reported_output_tokens: max(last_reported_output, token_delta.output_reported),
elixir/lib/symphony_elixir/orchestrator.ex:1195: codex_last_reported_total_tokens: max(last_reported_total, token_delta.total_reported),
elixir/lib/symphony_elixir/orchestrator.ex:1198: token_delta
elixir/lib/symphony_elixir/orchestrator.ex:1251: tick_token = make_ref()
elixir/lib/symphony_elixir/orchestrator.ex:1252: timer_ref = Process.send_after(self(), {:tick, tick_token}, delay_ms)
elixir/lib/symphony_elixir/orchestrator.ex:1257: tick_token: tick_token,
elixir/lib/symphony_elixir/orchestrator.ex:1281: apply_token_delta(
elixir/lib/symphony_elixir/orchestrator.ex:1284: input_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:1285: output_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:1286: total_tokens: 0,
elixir/lib/symphony_elixir/orchestrator.ex:1315: defp apply_codex_token_delta(
elixir/lib/symphony_elixir/orchestrator.ex:1317: %{input_tokens: input, output_tokens: output, total_tokens: total} = token_delta
elixir/lib/symphony_elixir/orchestrator.ex:1320: %{state | codex_totals: apply_token_delta(codex_totals, token_delta)}
elixir/lib/symphony_elixir/orchestrator.ex:1323: defp apply_codex_token_delta(state, _token_delta), do: state
elixir/lib/symphony_elixir/orchestrator.ex:1337: defp apply_token_delta(codex_totals, token_delta) do
elixir/lib/symphony_elixir/orchestrator.ex:1338: input_tokens = Map.get(codex_totals, :input_tokens, 0) + token_delta.input_tokens
elixir/lib/symphony_elixir/orchestrator.ex:1339: output_tokens = Map.get(codex_totals, :output_tokens, 0) + token_delta.output_tokens
elixir/lib/symphony_elixir/orchestrator.ex:1340: total_tokens = Map.get(codex_totals, :total_tokens, 0) + token_delta.total_tokens
elixir/lib/symphony_elixir/orchestrator.ex:1343: Map.get(codex_totals, :seconds_running, 0) + Map.get(token_delta, :seconds_running, 0)
elixir/lib/symphony_elixir/orchestrator.ex:1346: input_tokens: max(0, input_tokens),
elixir/lib/symphony_elixir/orchestrator.ex:1347: output_tokens: max(0, output_tokens),
elixir/lib/symphony_elixir/orchestrator.ex:1348: total_tokens: max(0, total_tokens),
elixir/lib/symphony_elixir/orchestrator.ex:1353: defp extract_token_delta(running_entry, %{event: _, timestamp: _} = update) do
elixir/lib/symphony_elixir/orchestrator.ex:1355: usage = extract_token_usage(update)
elixir/lib/symphony_elixir/orchestrator.ex:1358: compute_token_delta(
elixir/lib/symphony_elixir/orchestrator.ex:1362: :codex_last_reported_input_tokens
elixir/lib/symphony_elixir/orchestrator.ex:1364: compute_token_delta(
```

... truncated after 80 matches

### Billing / Payments

Total matches: `0`

No matches found.

### AI / LLM / Agent Code

Total matches: `405`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 128 |
| `elixir/lib/symphony_elixir/orchestrator.ex` | 116 |
| `elixir/lib/symphony_elixir/agent_runner.ex` | 33 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 25 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 23 |
| `elixir/lib/symphony_elixir/config.ex` | 20 |
| `elixir/lib/symphony_elixir_web/presenter.ex` | 18 |
| `elixir/lib/symphony_elixir/prompt_builder.ex` | 14 |
| `elixir/lib/symphony_elixir/workflow.ex` | 8 |
| `elixir/lib/symphony_elixir_web/live/dashboard_live.ex` | 6 |

```text
elixir/Makefile:1: .PHONY: help all setup deps build fmt fmt-check lint test coverage ci dialyzer e2e
elixir/Makefile:6: @echo "Targets: setup, deps, fmt, fmt-check, lint, test, coverage, dialyzer, e2e, ci"
elixir/Makefile:26: coverage:
elixir/Makefile:44: $(MAKE) coverage
elixir/mix.exs:11: test_coverage: [
elixir/mix.exs:21: SymphonyElixir.AgentRunner,
elixir/mix.exs:23: SymphonyElixir.Codex.AppServer,
elixir/mix.exs:24: SymphonyElixir.Codex.DynamicTool,
elixir/lib/mix/tasks/workspace.before_remove.ex:15: mix workspace.before_remove --repo openai/symphony
elixir/lib/mix/tasks/workspace.before_remove.ex:18: @default_repo "openai/symphony"
elixir/lib/symphony_elixir/agent_runner.ex:1: defmodule SymphonyElixir.AgentRunner do
elixir/lib/symphony_elixir/agent_runner.ex:3: Executes a single Linear issue in its workspace with Codex.
elixir/lib/symphony_elixir/agent_runner.ex:7: alias SymphonyElixir.Codex.AppServer
elixir/lib/symphony_elixir/agent_runner.ex:8: alias SymphonyElixir.{Config, Linear.Issue, PromptBuilder, Tracker, Workspace}
elixir/lib/symphony_elixir/agent_runner.ex:13: def run(issue, codex_update_recipient \\ nil, opts \\ []) do
elixir/lib/symphony_elixir/agent_runner.ex:17: Logger.info("Starting agent run for #{issue_context(issue)} worker_host=#{worker_host_for_log(worker_host)}")
elixir/lib/symphony_elixir/agent_runner.ex:19: case run_on_worker_host(issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:24: Logger.error("Agent run failed for #{issue_context(issue)}: #{inspect(reason)}")
elixir/lib/symphony_elixir/agent_runner.ex:25: raise RuntimeError, "Agent run failed for #{issue_context(issue)}: #{inspect(reason)}"
elixir/lib/symphony_elixir/agent_runner.ex:29: defp run_on_worker_host(issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:34: send_worker_runtime_info(codex_update_recipient, issue, worker_host, workspace)
elixir/lib/symphony_elixir/agent_runner.ex:38: run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host)
elixir/lib/symphony_elixir/agent_runner.ex:49: defp codex_message_handler(recipient, issue) do
elixir/lib/symphony_elixir/agent_runner.ex:51: send_codex_update(recipient, issue, message)
elixir/lib/symphony_elixir/agent_runner.ex:55: defp send_codex_update(recipient, %Issue{id: issue_id}, message)
elixir/lib/symphony_elixir/agent_runner.ex:57: send(recipient, {:codex_worker_update, issue_id, message})
elixir/lib/symphony_elixir/agent_runner.ex:61: defp send_codex_update(_recipient, _issue, _message), do: :ok
elixir/lib/symphony_elixir/agent_runner.ex:79: defp run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host) do
elixir/lib/symphony_elixir/agent_runner.ex:80: max_turns = Keyword.get(opts, :max_turns, Config.settings!().agent.max_turns)
elixir/lib/symphony_elixir/agent_runner.ex:85: do_run_codex_turns(session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, 1, max_turns)
elixir/lib/symphony_elixir/agent_runner.ex:92: defp do_run_codex_turns(app_session, workspace, issue, codex_update_recipient, opts, issue_state_fetcher, turn_number, max_turns) do
elixir/lib/symphony_elixir/agent_runner.ex:93: prompt = build_turn_prompt(issue, opts, turn_number, max_turns)
elixir/lib/symphony_elixir/agent_runner.ex:98: prompt,
elixir/lib/symphony_elixir/agent_runner.ex:100: on_message: codex_message_handler(codex_update_recipient, issue)
elixir/lib/symphony_elixir/agent_runner.ex:102: Logger.info("Completed agent run for #{issue_context(issue)} session_id=#{turn_session[:session_id]} workspace=#{workspace} turn=#{turn_number}/#{max_turns}")
elixir/lib/symphony_elixir/agent_runner.ex:106: Logger.info("Continuing agent run for #{issue_context(refreshed_issue)} after normal turn completion turn=#{turn_number}/#{max_turns}")
elixir/lib/symphony_elixir/agent_runner.ex:108: do_run_codex_turns(
elixir/lib/symphony_elixir/agent_runner.ex:112: codex_update_recipient,
elixir/lib/symphony_elixir/agent_runner.ex:120: Logger.info("Reached agent.max_turns for #{issue_context(refreshed_issue)} with issue still active; returning control to orchestrator")
elixir/lib/symphony_elixir/agent_runner.ex:133: defp build_turn_prompt(issue, opts, 1, _max_turns), do: PromptBuilder.build_prompt(issue, opts)
elixir/lib/symphony_elixir/agent_runner.ex:135: defp build_turn_prompt(_issue, _opts, turn_number, max_turns) do
elixir/lib/symphony_elixir/agent_runner.ex:139: - The previous Codex turn completed normally, but the Linear issue is still in an active state.
elixir/lib/symphony_elixir/agent_runner.ex:140: - This is continuation turn ##{turn_number} of #{max_turns} for the current agent run.
elixir/lib/symphony_elixir/cli.ex:117: "Codex will run without any guardrails.",
elixir/lib/symphony_elixir/config.ex:9: @default_prompt_template """
elixir/lib/symphony_elixir/config.ex:23: @type codex_runtime_settings :: %{
elixir/lib/symphony_elixir/config.ex:51: @spec max_concurrent_agents_for_state(term()) :: pos_integer()
elixir/lib/symphony_elixir/config.ex:52: def max_concurrent_agents_for_state(state_name) when is_binary(state_name) do
elixir/lib/symphony_elixir/config.ex:56: config.agent.max_concurrent_agents_by_state,
elixir/lib/symphony_elixir/config.ex:58: config.agent.max_concurrent_agents
elixir/lib/symphony_elixir/config.ex:62: def max_concurrent_agents_for_state(_state_name), do: settings!().agent.max_concurrent_agents
elixir/lib/symphony_elixir/config.ex:64: @spec codex_turn_sandbox_policy(Path.t() | nil) :: map()
elixir/lib/symphony_elixir/config.ex:65: def codex_turn_sandbox_policy(workspace \\ nil) do
elixir/lib/symphony_elixir/config.ex:71: raise ArgumentError, message: "Invalid codex turn sandbox policy: #{inspect(reason)}"
elixir/lib/symphony_elixir/config.ex:75: @spec workflow_prompt() :: String.t()
elixir/lib/symphony_elixir/config.ex:76: def workflow_prompt do
elixir/lib/symphony_elixir/config.ex:78: {:ok, %{prompt_template: prompt}} ->
elixir/lib/symphony_elixir/config.ex:79: if String.trim(prompt) == "", do: @default_prompt_template, else: prompt
elixir/lib/symphony_elixir/config.ex:82: @default_prompt_template
elixir/lib/symphony_elixir/config.ex:101: @spec codex_runtime_settings(Path.t() | nil, keyword()) ::
elixir/lib/symphony_elixir/config.ex:102: {:ok, codex_runtime_settings()} | {:error, term()}
elixir/lib/symphony_elixir/config.ex:103: def codex_runtime_settings(workspace \\ nil, opts \\ []) do
elixir/lib/symphony_elixir/config.ex:109: approval_policy: settings.codex.approval_policy,
elixir/lib/symphony_elixir/config.ex:110: thread_sandbox: settings.codex.thread_sandbox,
elixir/lib/symphony_elixir/orchestrator.ex:3: Polls Linear and dispatches repository copies to Codex-backed workers.
elixir/lib/symphony_elixir/orchestrator.ex:10: alias SymphonyElixir.{AgentRunner, Config, StatusDashboard, Tracker, Workspace}
elixir/lib/symphony_elixir/orchestrator.ex:17: @empty_codex_totals %{
elixir/lib/symphony_elixir/orchestrator.ex:31: :max_concurrent_agents,
elixir/lib/symphony_elixir/orchestrator.ex:40: codex_totals: nil,
elixir/lib/symphony_elixir/orchestrator.ex:41: codex_rate_limits: nil
elixir/lib/symphony_elixir/orchestrator.ex:58: max_concurrent_agents: config.agent.max_concurrent_agents,
elixir/lib/symphony_elixir/orchestrator.ex:63: codex_totals: @empty_codex_totals,
elixir/lib/symphony_elixir/orchestrator.ex:64: codex_rate_limits: nil
elixir/lib/symphony_elixir/orchestrator.ex:129: state = record_session_completion_totals(state, running_entry)
elixir/lib/symphony_elixir/orchestrator.ex:135: Logger.info("Agent task completed for issue_id=#{issue_id} session_id=#{session_id}; scheduling active-state continuation check")
elixir/lib/symphony_elixir/orchestrator.ex:147: Logger.warning("Agent task exited for issue_id=#{issue_id} session_id=#{session_id} reason=#{inspect(reason)}; scheduling retry")
elixir/lib/symphony_elixir/orchestrator.ex:153: error: "agent exited: #{inspect(reason)}",
elixir/lib/symphony_elixir/orchestrator.ex:159: Logger.info("Agent task finished for issue_id=#{issue_id} session_id=#{session_id} reason=#{inspect(reason)}")
elixir/lib/symphony_elixir/orchestrator.ex:184: {:codex_worker_update, issue_id, %{event: _, timestamp: _} = update},
elixir/lib/symphony_elixir/orchestrator.ex:192: {updated_running_entry, token_delta} = integrate_codex_update(running_entry, update)
```

... truncated after 80 matches

## Quality Signals

These scans cover source/config files, including tests, but exclude docs, lockfiles, intake scripts, generated folders, and agent/editor tooling by default.

### Work markers: TODO / FIXME / HACK / XXX

Total matches: `0`

No matches found.

### TypeScript and lint escape hatches

Total matches: `0`

No matches found.

### Debug leftovers

Total matches: `5`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/config/schema.ex` | 3 |
| `elixir/test/symphony_elixir/workspace_and_config_test.exs` | 2 |

```text
elixir/lib/symphony_elixir/config/schema.ex:35: @spec dump(term()) :: {:ok, String.t() | map()} | :error
elixir/lib/symphony_elixir/config/schema.ex:36: def dump(value) when is_binary(value) or is_map(value), do: {:ok, value}
elixir/lib/symphony_elixir/config/schema.ex:37: def dump(_value), do: :error
elixir/test/symphony_elixir/workspace_and_config_test.exs:986: assert {:ok, %{"a" => 1}} = StringOrMap.dump(%{"a" => 1})
elixir/test/symphony_elixir/workspace_and_config_test.exs:987: assert :error = StringOrMap.dump(123)
```

## Passive Risk Scan

These scans cover production source/config files only. Tests, docs, lockfiles, intake scripts, generated folders, and agent/editor tooling are excluded by default.

### Secrets-shaped strings, redacted

Total matches: `1`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/config/schema.ex` | 1 |

```text
elixir/lib/symphony_elixir/config/schema.ex:371: | api_key: [REDACTED] System.get_env("LINEAR_API_KEY")),
```

### Unsafe code patterns

Total matches: `0`

No matches found.

### Auth bypass terms

Total matches: `0`

No matches found.

### Environment variable usage

Total matches: `15`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/config/schema.ex` | 4 |
| `elixir/lib/symphony_elixir/log_file.ex` | 3 |
| `elixir/lib/symphony_elixir/tracker/memory.ex` | 2 |
| `elixir/lib/symphony_elixir/config.ex` | 1 |
| `elixir/lib/symphony_elixir/http_server.ex` | 1 |
| `elixir/lib/symphony_elixir/ssh.ex` | 1 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 1 |
| `elixir/lib/symphony_elixir/workflow.ex` | 1 |
| `elixir/lib/symphony_elixir/linear/adapter.ex` | 1 |

```text
elixir/lib/symphony_elixir/config.ex:88: case Application.get_env(:symphony_elixir, :server_port_override) do
elixir/lib/symphony_elixir/http_server.ex:39: |> Application.get_env(Endpoint, [])
elixir/lib/symphony_elixir/log_file.ex:25: log_file = Application.get_env(:symphony_elixir, :log_file, default_log_file())
elixir/lib/symphony_elixir/log_file.ex:26: max_bytes = Application.get_env(:symphony_elixir, :log_file_max_bytes, @default_max_bytes)
elixir/lib/symphony_elixir/log_file.ex:27: max_files = Application.get_env(:symphony_elixir, :log_file_max_files, @default_max_files)
elixir/lib/symphony_elixir/ssh.ex:55: case System.get_env("SYMPHONY_SSH_CONFIG") do
elixir/lib/symphony_elixir/status_dashboard.ex:797: case System.get_env("COLUMNS") do
elixir/lib/symphony_elixir/workflow.ex:12: Application.get_env(:symphony_elixir, :workflow_file_path) ||
elixir/lib/symphony_elixir/config/schema.ex:371: | api_key: resolve_secret_setting(settings.tracker.api_key, System.get_env("LINEAR_API_KEY")),
elixir/lib/symphony_elixir/config/schema.ex:372: assignee: resolve_secret_setting(settings.tracker.assignee, System.get_env("LINEAR_ASSIGNEE"))
elixir/lib/symphony_elixir/config/schema.ex:441: case System.get_env(env_name) do
elixir/lib/symphony_elixir/config/schema.ex:470: case System.get_env(env_name) do
elixir/lib/symphony_elixir/linear/adapter.ex:77: Application.get_env(:symphony_elixir, :linear_client_module, Client)
elixir/lib/symphony_elixir/tracker/memory.ex:51: Application.get_env(:symphony_elixir, :memory_tracker_issues, [])
elixir/lib/symphony_elixir/tracker/memory.ex:59: case Application.get_env(:symphony_elixir, :memory_tracker_recipient) do
```

### Raw shell / process execution

Total matches: `5`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/ssh.ex` | 2 |
| `elixir/lib/mix/tasks/workspace.before_remove.ex` | 1 |
| `elixir/lib/symphony_elixir/workspace.ex` | 1 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 1 |

```text
elixir/lib/mix/tasks/workspace.before_remove.ex:134: case System.cmd(path, args, stderr_to_stdout: true) do
elixir/lib/symphony_elixir/ssh.ex:7: {:ok, System.cmd(executable, ssh_args(host, command), opts)}
elixir/lib/symphony_elixir/ssh.ex:25: {:ok, Port.open({:spawn_executable, String.to_charlist(executable)}, port_opts)}
elixir/lib/symphony_elixir/workspace.ex:301: System.cmd("sh", ["-lc", command], cd: workspace, stderr_to_stdout: true)
elixir/lib/symphony_elixir/codex/app_server.ex:196: Port.open(
```

### Network calls

Total matches: `7`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir_web/static_assets.ex` | 3 |
| `elixir/lib/symphony_elixir/status_dashboard.ex` | 2 |
| `elixir/lib/symphony_elixir/linear/client.ex` | 1 |
| `elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex` | 1 |

```text
elixir/lib/symphony_elixir/status_dashboard.ex:1904: case Map.fetch(map, key) do
elixir/lib/symphony_elixir/status_dashboard.ex:1914: Map.fetch(map, alternate)
elixir/lib/symphony_elixir/linear/client.ex:398: Req.post(Config.settings!().tracker.endpoint,
elixir/lib/symphony_elixir_web/static_assets.ex:26: @spec fetch(String.t()) :: {:ok, String.t(), binary()} | :error
elixir/lib/symphony_elixir_web/static_assets.ex:27: def fetch(path) when is_binary(path) do
elixir/lib/symphony_elixir_web/static_assets.ex:28: case Map.fetch(@assets, path) do
elixir/lib/symphony_elixir_web/controllers/static_asset_controller.ex:24: case StaticAssets.fetch(path) do
```

### Filesystem writes / deletes

Total matches: `19`

| File | Matches |
| --- | ---: |
| `elixir/lib/symphony_elixir/workspace.ex` | 7 |
| `elixir/lib/symphony_elixir/cli.ex` | 3 |
| `elixir/lib/symphony_elixir/log_file.ex` | 2 |
| `elixir/lib/symphony_elixir/path_safety.ex` | 2 |
| `elixir/lib/symphony_elixir/codex/app_server.ex` | 2 |
| `elixir/lib/symphony_elixir/config/schema.ex` | 2 |
| `elixir/lib/symphony_elixir_web/static_assets.ex` | 1 |

```text
elixir/lib/symphony_elixir/cli.ex:39: run(Path.expand("WORKFLOW.md"), deps)
elixir/lib/symphony_elixir/cli.ex:56: expanded_path = Path.expand(workflow_path)
elixir/lib/symphony_elixir/cli.ex:100: :ok = deps.set_logs_root.(Path.expand(logs_root))
elixir/lib/symphony_elixir/log_file.ex:33: expanded_path = Path.expand(log_file)
elixir/lib/symphony_elixir/log_file.ex:34: :ok = File.mkdir_p(Path.dirname(expanded_path))
elixir/lib/symphony_elixir/path_safety.ex:6: expanded_path = Path.expand(path)
elixir/lib/symphony_elixir/path_safety.ex:31: resolved_target = Path.expand(IO.chardata_to_string(target), join_path(root, resolved_segments))
elixir/lib/symphony_elixir/workspace.ex:40: File.rm_rf!(workspace)
elixir/lib/symphony_elixir/workspace.ex:82: File.rm_rf!(workspace)
elixir/lib/symphony_elixir/workspace.ex:83: File.mkdir_p!(workspace)
elixir/lib/symphony_elixir/workspace.ex:97: File.rm_rf(workspace)
elixir/lib/symphony_elixir/workspace.ex:104: File.rm_rf(workspace)
elixir/lib/symphony_elixir/workspace.ex:359: expanded_workspace = Path.expand(workspace)
elixir/lib/symphony_elixir/workspace.ex:360: expanded_root = Path.expand(Config.settings!().workspace.root)
elixir/lib/symphony_elixir/codex/app_server.ex:148: expanded_workspace = Path.expand(workspace)
elixir/lib/symphony_elixir/codex/app_server.ex:149: expanded_root = Path.expand(Config.settings!().workspace.root)
elixir/lib/symphony_elixir/config/schema.ex:517: Path.expand(workspace_root)
elixir/lib/symphony_elixir/config/schema.ex:521: Path.expand(Path.join(System.tmp_dir!(), "symphony_workspaces"))
elixir/lib/symphony_elixir_web/static_assets.ex:4: @dashboard_css_path Path.expand("../../priv/static/dashboard.css", __DIR__)
```

## Stack-Specific Best Practice Audit

No TypeScript, React/Next.js, Tailwind, Supabase/Postgres, Prisma, or Drizzle-specific packs were detected.

## Optional Scanner Results

Deep scanners were not run. Re-run with `python3 codebase-intake.py --deep` to run installed scanners and language-specific commands.

| Tool | Status |
| --- | --- |
| gitleaks | available |
| osv-scanner | available |
| semgrep | available |
| pip-audit | available |
| mix | available |
| supabase | not installed |
| npm | available |
| pnpm | not installed |
| yarn | not installed |
| bun | available |

## Recommended Inspection Order

1. `elixir/lib/symphony_elixir/orchestrator.ex` - large, recently changed; likely owns concurrency, retry, and state behavior.
2. `elixir/lib/symphony_elixir/codex/app_server.ex` - large, recently changed; likely owns external protocol and session behavior.
3. `elixir/lib/symphony_elixir/status_dashboard.ex` - large, recently changed; likely mixes rendering, formatting, and event humanization.
4. `elixir/lib/symphony_elixir/agent_runner.ex` - recently changed; likely central control path.
5. `elixir/lib/symphony_elixir/config/schema.ex` - medium-large, recently changed; config validation and runtime behavior boundary.
6. `elixir/lib/symphony_elixir/workspace.ex` - recently changed; workspace path containment and filesystem boundary.
7. `elixir/lib/symphony_elixir/linear/client.ex` - medium-large, recently changed; external API and token-handling boundary.
8. `elixir/lib/symphony_elixir/ssh.ex` - recently changed; remote worker and process boundary.

9. Inspect large source files over 1,000 lines, especially modules that mix rendering, orchestration, external I/O, and state transitions.
10. Inspect external-boundary files: auth, webhooks, API clients, process execution, filesystem mutation, SSH, workspace cleanup, and token handling.
11. Inspect test files over 1,000 lines for brittle integration coverage and slow setup paths.
12. Run `python3 codebase-intake.py --deep` before production or security-sensitive work.
