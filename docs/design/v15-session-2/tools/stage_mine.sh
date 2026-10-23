cd ~/Documents/GitHub/journalism-atlas
# stage only files this session edits: public pages, shared css/js, CLAUDE.md, session docs. Never nn5 / edition / _headers / CURRENT_STATE.
git diff --name-only | grep -E '^([a-z0-9_-]+\.html|partners/[a-z0-9_-]+\.html|assets/css/[a-z]+\.css|assets/js/(header|footer|main|components)\.js|CLAUDE\.md|build-dist\.sh|docs/design/v15-session-2/.*)$' | tr '\n' '\0' | xargs -0 git add --
git diff --cached --stat | tail -1
