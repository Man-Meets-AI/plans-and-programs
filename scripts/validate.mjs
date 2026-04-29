import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

const root = process.cwd();
const args = new Set(process.argv.slice(2));

const requiredFiles = [
  "README.md",
  "AGENTS.md",
  "assets/plans-and-programs.png",
  "package.json",
  ".markdownlint.json",
  ".vscode/extensions.json",
  ".vscode/settings.json",
  "schemas/program-frontmatter.schema.json",
  "schemas/exec-plan-frontmatter.schema.json",
  "docs/index.md",
  "docs/adoption.md",
  "docs/programs/README.md",
  "docs/programs/PROGRAMS.md",
  "docs/programs/active/index.md",
  "docs/programs/completed/index.md",
  "docs/programs/templates/program.md",
  "docs/exec-plans/README.md",
  "docs/exec-plans/PLANS.md",
  "docs/exec-plans/active/index.md",
  "docs/exec-plans/completed/index.md",
  "docs/exec-plans/templates/exec-plan.md",
  "docs/prompts/README.md",
  "docs/prompts/exec-plan-writer.md",
  "docs/prompts/exec-plan-grill.md",
  "docs/prompts/exec-plan-execute.md",
  "docs/prompts/exec-plan-validate.md",
  "docs/prompts/program-planning-refresh.md",
  ".agents/skills/shared/exec-plan-writer/SKILL.md",
  ".agents/skills/shared/exec-plan-griller/SKILL.md",
  ".agents/skills/shared/exec-plan-execute/SKILL.md",
  ".agents/skills/shared/exec-plan-validate/SKILL.md",
  ".agents/skills/shared/program-planning-refresh/SKILL.md",
  ".agents/skills/README.md",
  ".gitignore",
];

const requiredProgramFiles = [
  "program.md",
  "research-pass-teaching-starter.md",
  "normalized-pass-teaching-starter.md",
  "converged-decision-packet.md",
  "dependency-graph.md",
  "plan-split-recommendation.md",
  "cross-repo-review.md",
  "planning-brief-1.md",
  "current-planning-brief.txt",
];

const programRequiredSections = [
  "## Purpose / Big Picture",
  "## Program Inputs",
  "## Current State",
  "## Progress",
  "## Decision Log",
  "## Slice Ledger",
  "## Next Slice",
  "## Risks and Watchpoints",
  "## Outcomes & Retrospective",
  "## Validation and Acceptance",
  "## Artifacts and Notes",
  "## Interfaces and Dependencies",
];

const planRequiredSections = [
  "## Purpose / Big Picture",
  "## Progress",
  "## Surprises & Discoveries",
  "## Decision Log",
  "## Outcomes & Retrospective",
  "## Context and Orientation",
  "### In Scope",
  "### Out Of Scope",
  "## Plan of Work",
  "## Milestones",
  "## Concrete Steps",
  "## Validation and Acceptance",
  "### Test Commands",
  "## Idempotence and Recovery",
  "## Artifacts and Notes",
  "## Interfaces and Dependencies",
];

const failures = [];

function fail(message) {
  failures.push(message);
}

function repoPath(relativePath) {
  return path.join(root, relativePath);
}

function read(relativePath) {
  return readFileSync(repoPath(relativePath), "utf8");
}

function assertExists(relativePath) {
  if (!existsSync(repoPath(relativePath))) {
    fail(`Missing required file: ${relativePath}`);
  }
}

function assertContains(relativePath, expected) {
  if (!existsSync(repoPath(relativePath))) {
    fail(`Cannot inspect missing file: ${relativePath}`);
    return;
  }

  const contents = read(relativePath);
  if (!contents.includes(expected)) {
    fail(`${relativePath} is missing required text: ${expected}`);
  }
}

function markdownFiles(directory) {
  if (!existsSync(repoPath(directory))) return [];

  const results = [];
  const stack = [repoPath(directory)];
  while (stack.length > 0) {
    const current = stack.pop();
    for (const entry of readdirSync(current)) {
      const absolute = path.join(current, entry);
      const stat = statSync(absolute);
      if (stat.isDirectory()) {
        stack.push(absolute);
      } else if (entry.endsWith(".md")) {
        results.push(path.relative(root, absolute));
      }
    }
  }
  return results.sort();
}

function assertFrontmatter(relativePath, keys) {
  const contents = read(relativePath);
  if (!contents.startsWith("---\n")) {
    fail(`${relativePath} must start with YAML frontmatter`);
    return;
  }

  const end = contents.indexOf("\n---", 4);
  if (end === -1) {
    fail(`${relativePath} frontmatter is not closed`);
    return;
  }

  const frontmatter = contents.slice(4, end);
  for (const key of keys) {
    if (!frontmatter.includes(`${key}:`)) {
      fail(`${relativePath} frontmatter missing key: ${key}`);
    }
  }
}

function assertSections(relativePath, sections) {
  const contents = read(relativePath);
  let lastIndex = -1;
  for (const section of sections) {
    const index = contents.indexOf(section);
    if (index === -1) {
      fail(`${relativePath} missing section: ${section}`);
      continue;
    }
    if (index < lastIndex) {
      fail(`${relativePath} section is out of order: ${section}`);
    }
    lastIndex = index;
  }
}

function validatePrograms() {
  const programRoot = "docs/programs/completed/2026-04-29-teaching-starter-seed";
  for (const file of requiredProgramFiles) {
    assertExists(`${programRoot}/${file}`);
  }

  const pointer = read(`${programRoot}/current-planning-brief.txt`).trim();
  if (pointer !== "planning-brief-1.md") {
    fail(`${programRoot}/current-planning-brief.txt must contain exactly planning-brief-1.md`);
  }

  const programPath = `${programRoot}/program.md`;
  assertFrontmatter(programPath, [
    "program_id",
    "title",
    "status",
    "created_at",
    "completed_at",
    "summary",
    "post_build_recap",
    "read_when",
  ]);
  assertSections(programPath, programRequiredSections);
  assertContains(programPath, "status: complete");
  assertContains(programPath, "No required next slice remains");
}

function validatePlans() {
  const planPath = "docs/exec-plans/completed/2026-04-29-seed-program-execplan-starter.md";
  assertExists(planPath);
  assertFrontmatter(planPath, [
    "title",
    "status",
    "created_at",
    "completed_at",
    "summary",
    "post_build_recap",
    "read_when",
  ]);
  assertSections(planPath, planRequiredSections);
  assertContains(planPath, "status: complete");
  assertContains(planPath, "program_id: teaching-starter-seed");
  assertContains(planPath, "planning_brief: docs/programs/completed/2026-04-29-teaching-starter-seed/planning-brief-1.md");
}

function validateMarkdownBasics() {
  for (const file of markdownFiles(".")) {
    const contents = read(file);
    if (contents.includes("\t")) {
      fail(`${file} contains a tab character`);
    }
    if (contents.includes("\r")) {
      fail(`${file} contains CRLF line endings`);
    }
  }
}

if (!args.has("--programs") && !args.has("--plans")) {
  for (const file of requiredFiles) {
    assertExists(file);
  }
  validateMarkdownBasics();
}

if (!args.has("--plans")) {
  validatePrograms();
}

if (!args.has("--programs")) {
  validatePlans();
}

if (failures.length > 0) {
  console.error("Validation failed:");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Validation passed.");
