#!/bin/bash
cd /tmp
PY=/workspace/bie/.venv/bin/python; D=/workspace/bie_tools/discover.py
echo "=== $(date +%T) urlscan resume"; $PY $D testharvest urlscan
echo "=== $(date +%T) au listing pages"; TAG=au_pages $PY $D pages https://pokiesmate.bet/bonus https://truebluepokies.win/bonus https://auspokieslist.com https://audplay.online https://gday77-australia.co
echo "=== $(date +%T) websearch file"; TAG=au_websearch $PY $D file /workspace/bie_tools/au/search_au.txt
echo "=== $(date +%T) websearch pages"; TAG=au_webpages $PY $D pages https://audplay.tech/partnership/ https://toponlinepokiesaus.com/partnership/ https://pokiesaus.online/ https://heylink.me/audplaypartnership/ https://igaustralia.live/ https://ausonlinepokies.link/ https://mrpokies.co/partnership/ https://aa7au.com/partnership88 https://audplay.co/australian-online-pokies-casino-trend https://tgadsspy.com/channels/freeauspokies2u/advertisers https://tgadsspy.com/channels/auspokiesstation https://tgadsspy.com/bots/pokies33_bot
echo "=== $(date +%T) telegram AU"; $PY $D telegram cloud9aus auspokiesstation pokies2u aud22aud freeauspokies2u wildpokiesofficialchannel cimperioaus_channel
echo "=== RESUME DONE $(date +%T)"
