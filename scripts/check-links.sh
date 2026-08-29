#!/usr/bin/env bash
set -euo pipefail

rg -No 'https?://[^ )`]+' --glob '*.md' \
  | sed 's/^[^:]*://' \
  | sort -u \
  | while IFS= read -r url; do
      code="$(curl -L -sS -o /dev/null -w '%{http_code}' --max-time 20 "$url" || true)"
      case "$code" in
        200|204|301|302|303|307|308|401|403) ;;
        *) printf '%s %s\n' "$code" "$url"; exit 1 ;;
      esac
    done
