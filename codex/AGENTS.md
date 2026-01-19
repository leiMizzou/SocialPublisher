## Codex Runbook (isolated from Claude Skill)

This repo includes a Claude Code Skill under `.claude/`. Codex must not modify
or depend on that skill. All Codex-specific docs and scripts live in `codex/`.

### Scope and isolation
- Do not edit or execute anything under `.claude/`.
- Do not rely on Playwright MCP or Claude-specific commands.
- Use the shared Python helper scripts in `scripts/` only.
- Read/write `.social_publisher/` only via the helper scripts or `codex/login.py`.
- Keep Codex automation in `codex/`.

### What Codex can do today
- Run login status checks via `scripts/check_login.py`.
- Track and verify sessions via `scripts/content_tracker.py`.
- Use wrappers: `codex/run.sh` (preferred) or `scripts/publish.sh`.
- Launch manual logins and save cookies via `codex/login.py`.

### Setup
```bash
pip install -r requirements.txt
python3 -m playwright install chromium
chmod +x codex/run.sh
```

### Minimal Codex workflow (manual inputs)
1) Check login status:
```bash
./codex/run.sh status --json
```

2) Manual login if needed:
```bash
./codex/run.sh login --platform wechat
./codex/run.sh login --platform xiaohongshu
```

3) Start a session:
```bash
./codex/run.sh init --topic "Your Topic"
```

4) Record search results (posts must be supplied by the user or another tool):
```bash
./codex/run.sh search \
  --query "Your Topic" \
  --time-range "24h" \
  --posts '[{"id":"1","author":"@user","content":"...","likes":1}]'
```

5) Record engagement, distilled points, generated content, publish status:
```bash
./codex/run.sh engage --action like --post-id "1"
./codex/run.sh distill --trends '["t1"]' --points '["p1"]'
./codex/run.sh generate --platform twitter --thread '["1/ ..."]'
./codex/run.sh publish --platform twitter --status published --count 1
```

6) Verify:
```bash
./codex/run.sh verify
```

### Notes
- Full browser automation is not implemented for Codex in this repo.
- If automation is requested, create new Codex-specific scripts under `codex/`
  and keep them independent of `.claude/`.
