#!/usr/bin/env bash
# Usage: channel/send.sh <message-file>   (or: echo "..." | channel/send.sh -)
# Sends to Argon's live conversation, logs BOTH directions into channel/ and INDEX.md.
set -euo pipefail
cd ~/projects/Vault
CONV="$(cat channel/.argon-conversation 2>/dev/null || echo 7523344b-84d9-4527-9037-a76f4dcae2b7)"
SRC="${1:?usage: send.sh <message-file|->}"
[ "$SRC" = "-" ] && SRC=/dev/stdin
BODY="$(cat "$SRC")"
N=$(printf '%03d' $(( $(ls channel/to-argon channel/to-claude 2>/dev/null | grep -cE '^[0-9]{3}-') + 1 )))
TS=$(date '+%Y%m%d-%H%M')
OUT="channel/to-argon/${N}-${TS}-claude.md"
printf -- '---\nfrom: claude\nto: argon\ndate: %s\n---\n\n%s\n' "$(date '+%F %H:%M')" "$BODY" > "$OUT"
echo "sent -> $OUT"
{ printf '\n%s\n## CLAUDE -> ARGON  —  %s\n%s\n\n' "$(printf '=%.0s' {1..78})" "$(basename $OUT)" "$(printf '=%.0s' {1..78})"; cat "$OUT"; } >> channel/TRANSCRIPT.md
agy -p "$BODY" --conversation="$CONV" --output-format json --dangerously-skip-permissions \
  | .venv/bin/python -c "
import json,sys,pathlib
d=json.load(sys.stdin); r=d.get('response','')
p=pathlib.Path('channel/to-claude/${N}r-${TS}-argon.md'); p.write_text(r or '(empty response)')
print('reply ->',p,'| chars',len(r),'| denied:',d.get('denied_actions'))
print(); print(r[:7000])
open('channel/TRANSCRIPT.md','a').write('\n'+'='*78+'\n## ARGON -> CLAUDE  —  '+p.name+'\n'+'='*78+'\n\n'+(r or '(empty)')+'\n')
"
printf '| %s | %s | claude -> argon | see file | sent |\n' "$N" "$(date '+%F')" >> channel/INDEX.md
