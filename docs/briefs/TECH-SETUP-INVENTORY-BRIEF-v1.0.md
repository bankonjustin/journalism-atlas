# TECH-SETUP-INVENTORY-BRIEF v1.0

From: Cowork session in the "Building the Database/Atlas" Project (planning, rulings, briefs)
To: Claude Code, started in `~/Documents/GitHub` (the parent folder; this brief covers several repos)
Date: Fri Nov 6, 2026
Changelog: v1.0, first version.

## Purpose

This is Step 1 of organizing Justin's technical setup: a **read-only inventory** of how the Atlas work runs on this Mac. The output is one map that later sessions start from. **Change nothing.** No commits, no fetch, no deletes, no moves, no config edits, no lock removal. Stop when the report is written.

## Standing rules

- Read-only. The single file you may write is the report (see Output).
- Don't run `git fetch`, `git gc`, `git maintenance`, or anything else that writes to `.git/`.
- Don't print the contents of secrets: tokens, keys, `.env` values, keychain items. Report each one's path, its purpose if it's obvious, and whether git ignores it. Nothing else.
- Facts only, each with its path or the command that produced it. Mark anything you infer as "inferred".
- If something looks broken or risky, list it under Findings. Don't fix it.

## Established facts (Cowork, Nov 6 at 9:30 ET)

- Global git `user.email` and `user.name` are empty, and neither Atlas repo sets a local value. Justin's commits arrive as `justin@bettermedia.studio`, probably through GitHub Desktop. Ryan commits to `journalism-atlas-private` as `ryan.kellett@gmail.com`.
- Remotes are `github.com/bankonjustin/journalism-atlas` and `github.com/bankonjustin/journalism-atlas-private`.
- `journalism-atlas`:
  - The checkout is on branch `nn/asu-preview-fixes`, which has no upstream. Its commits are already in `main`.
  - Two files under `preview/nn-launch-kit/figures/` (`map`, `timeline`) have uncommitted changes.
  - `main` = `origin/main` at `b0283a5` (Nov 5, 15:27).
  - Lock files: `.git/refs/remotes/origin/HEAD.lock` (Oct 6) and `.git/stale-maintenance.lock`.
  - 16 local branches.
- `journalism-atlas-private`:
  - `main` = `origin/main`.
  - `LEAVE-OFF-LOG.md` is modified and uncommitted.
  - Untracked: `data/snapshots/CLEANUP-2026-11-04.md` and its folder.
  - Branches: `round4-medill-watershed` (ahead 1), `round5`, `round7`, `chore/vertical-natives-housekeeping`.
- Other folders in `~/Documents/GitHub/`:
  - `DMV-switchboard-OLD`
  - `Media Industry Research`
  - `atlas-list-claude`
  - `bankonjustin.com`
  - `journalism-atlas-private-round7`
  - `journalism-atlas-watershed-go`
  - `nodes-networks-v5` (not in git)
  - `paper-one-band-dataset`
  - `nov5-flip.patch`
  - `atlas-directory-audit-2026-07-20.md`
- Home folder: `~/nn5-backup-2026-10-23/`, `~/nn5-backup-2026-11-01/`, `~/migration-backup-2026-10-05/`, `~/Switchboard-handoff/`, `~/Developer/` (`DMV-switchboard`, `team-dmv-research`).

## Assumptions to verify

- Which GitHub account GitHub Desktop is signed in to, and which email it commits with. Read Desktop's config files; don't open the app.
- Whether `gh` is installed and authenticated, and as whom (`gh auth status` is read-only).
- Whether any launchd agents, cron jobs or Claude Routines run Atlas work on this machine.

## Inventory (report each section as a table)

1. **Folders.** Every folder under `~/Documents/GitHub/`, `~/Developer/`, and the backup and handoff folders in `~`. For each one:
   - is it a git repo;
   - remote URL;
   - current branch;
   - clean or dirty;
   - ahead/behind, using local refs only;
   - last commit date;
   - size;
   - what it is for, if a README or `CLAUDE.md` says.

   Flag duplicates and forks: for example `journalism-atlas-private-round7` vs `journalism-atlas-private`, `journalism-atlas-watershed-go` vs `journalism-atlas`, and `DMV-switchboard-OLD` vs `~/Developer/DMV-switchboard`.
2. **Branches.** For every branch in the two Atlas repos: last commit, upstream state, whether it's merged into `main`, and the one-line purpose from its commit subjects. Don't recommend deletions. Just mark each one "merged", "unmerged" or "gone upstream".
3. **Identities.** Git config at every level (system, global, each repo's local), GitHub Desktop accounts, `gh auth status`, SSH keys (file names only), and the credential helper. Also list the author emails on the last 30 days of commits in each Atlas repo, with counts.
4. **Scheduled and background work.**
   - `crontab -l`.
   - User LaunchAgents (`~/Library/LaunchAgents`) that mention atlas, pulse or claude.
   - Claude Code config: `~/.claude/` settings, allow rules and agents. List keys and names, not values.
   - Any Routine or scheduled-task folders, including the orphan ones named in `ops/DECISIONS-QUEUE.md` W5.
5. **Secrets and config files.** `~/.atlas_pulse_secrets`, any `.env` files, and API-key files referenced by scripts (grep for `ANTHROPIC_API_KEY`, `BSKY`, `TOKEN`, `SECRET` and print only file paths). Note whether each one is gitignored.
6. **Pipelines and entry points.** For Pulse, `convert.js`, `build-dist.sh`, `nn/build.py` and the spidering core: where each lives, how it's run (script or command), and when it last ran, judged from output file times.
7. **Cloudflare and deploy.** What `build-dist.sh` publishes, the `_headers` and `_redirects` sizes, and any `wrangler` config. Read-only.
8. **Non-git work at risk.** Folders with real work and no git and no backup: `nodes-networks-v5`, parts of `paper-one-band-dataset`, `~/Downloads` items referenced in docs. Give sizes and the newest file dates.

## Findings

A short numbered list of risks and inconsistencies, each with evidence. Examples of the kind:

- the repo is checked out on a branch with no upstream;
- lock files;
- the same work in two folders;
- secrets inside a repo;
- a Routine pointing at an old path.

## Output

Write `journalism-atlas-private/ops/TECH-INVENTORY-2026-11-06.md`. That's the only file you write. Then print a 10-line summary and stop.

## Out of scope

Fixing anything. Repo privacy, the TIJA LLC org, CODEOWNERS, branch cleanup, the Pulse Routine and identity changes are all Step 3. Each will get its own brief after Justin reviews the map.
