#!/usr/bin/env bash
# Usage: grok/send.sh <message-file>
# Sends an audit/consult request to Grok Build CLI. No tool access and no
# auto-approval: everything Grok sees is embedded in the message by us, so the
# exchange is reproducible and Grok cannot touch the repository.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
SRC="${1:?usage: send.sh <message-file>}"
N=$(printf '%03d' $(( $(ls grok/to-grok grok/from-grok 2>/dev/null | grep -cE '^[0-9]{3}-') + 1 )))
TS=$(date '+%Y%m%d-%H%M')
OUT="grok/to-grok/${N}-${TS}-claude.md"
printf -- '---\nfrom: claude\nto: grok\ndate: %s\n---\n\n%s\n' "$(date '+%F %H:%M')" "$(cat "$SRC")" > "$OUT"
echo "sent -> $OUT"
REPLY="grok/from-grok/${N}r-${TS}-grok.md"
# strip the YAML frontmatter: a leading '---' is parsed as a CLI flag
BODY="$(sed '1{/^---$/!q};1,/^---$/d' "$OUT")"
grok -p "$BODY" \
     --model grok-4.7 \
     --reasoning-effort high \
     --disable-web-search \
     --no-subagents \
     --max-turns 4 \
     --tools "" \
     --system-prompt-override "You are an adversarial scientific reviewer. You have NO tools and NO file access in this session: every number you need is in the prompt, so answer from the prompt alone and never attempt to read a file. Do not restate the prompt back. Be specific and quantitative, attack rather than summarise, and say plainly when a claim survives. Output the five numbered deliverables requested, nothing else." \
     > "$REPLY" 2>&1 || true
echo "reply -> $REPLY ($(wc -c < "$REPLY") bytes)"
{ printf '\n%s\n## CLAUDE -> GROK  —  %s\n%s\n\n' "$(printf '=%.0s' {1..78})" "$(basename "$OUT")" "$(printf '=%.0s' {1..78})"; cat "$OUT";
  printf '\n%s\n## GROK -> CLAUDE  —  %s\n%s\n\n' "$(printf '=%.0s' {1..78})" "$(basename "$REPLY")" "$(printf '=%.0s' {1..78})"; cat "$REPLY"; } >> grok/TRANSCRIPT.md
