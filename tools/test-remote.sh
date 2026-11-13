#!/bin/sh
# Presses a safe set of keys through a running TV Remote Air server and reports each result.
# Skips power, so the TV stays on. Usage: sh tools/test-remote.sh [http://server:8080] [device] [token]
URL=${1:-http://localhost:8080}; DEV=${2:-tv}; TOKEN=${3:-}
ok=0; fail=0
call() {  # method path body
  r=$(curl -s -m 8 -o /tmp/tra.$$ -w '%{http_code}' -X "$1" -H "Content-Type: application/json" -H "X-Token: $TOKEN" ${3:+-d "$3"} "$URL$2")
  if [ "$r" = 200 ]; then ok=$((ok+1)); echo "ok    $1 $2 $3"; else fail=$((fail+1)); echo "FAIL  $1 $2 $3 -> $r $(cat /tmp/tra.$$)"; fi
  sleep 0.4
}
call GET /api/config
call GET /api/$DEV/status
for k in home down up right left ok back volup voldown mute mute playpause playpause; do call POST /api/$DEV/key "{\"key\":\"$k\"}"; done
call GET /api/$DEV/apps
call GET /api/$DEV/inputs
call POST /api/$DEV/key '{"key":"home"}'
rm -f /tmp/tra.$$
echo; echo "$ok ok, $fail failed"
[ "$fail" = 0 ]
