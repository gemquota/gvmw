#!/bin/bash
cd /tmp
PY=/workspace/bie/.venv/bin/python; D=/workspace/bie_tools/discover.py
while pgrep -f au_discover.sh >/dev/null; do sleep 15; done
echo "=== $(date +%T) websearch file"; TAG=au_websearch $PY $D file /workspace/bie_tools/au/search_au.txt
echo "=== $(date +%T) websearch pages"; TAG=au_webpages $PY $D pages https://audplay.tech/partnership/ https://toponlinepokiesaus.com/partnership/ https://pokiesaus.online/ https://heylink.me/audplaypartnership/ https://igaustralia.live/ https://ausonlinepokies.link/ https://mrpokies.co/partnership/ https://aa7au.com/partnership88 https://audplay.co/australian-online-pokies-casino-trend https://tgadsspy.com/channels/freeauspokies2u/advertisers https://tgadsspy.com/channels/auspokiesstation https://tgadsspy.com/bots/pokies33_bot
echo "=== $(date +%T) telegram AU"; $PY $D telegram cloud9aus auspokiesstation pokies2u aud22aud freeauspokies2u wildpokiesofficialchannel cimperioaus_channel
echo "=== ALL2 DONE $(date +%T)"
