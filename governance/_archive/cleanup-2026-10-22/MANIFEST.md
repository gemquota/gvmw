# Cleanup archive manifest, 22 Oct 2026

Written 2026-10-22 22:54:18 AEST (UTC+10), before any move, by Grok Bot. Gem's approval, 10:53pm AEST, word for word: "Yes, archive the 19 safe items (moved, not deleted)". Source list: group A of `master/redundancy-phase-cleanup-2026-10-22.md`. Everything is MOVED to `_archive/cleanup-2026-10-22/<original relative path>`; nothing is deleted.

## Items to move

| Item | Original path | Files | Bytes |
|---|---|---|---|
| A0 | `codex/_shared/handoff-phase1` | 2 | 5515 |
| A1 | `proposals/handoff-phase1-v001.md` | 1 | 8828 |
| A1 | `proposals/phase1-interim-bundle-v001.md` | 1 | 9843 |
| A2 | `schedule.md.bak-p1` | 1 | 4548 |
| A4 | `proposals/2026-10-09-retire-merge` | 3 | 56527 |
| A5 | `proposals/merge-F-unretire-assembler-2026-10-04.md` | 1 | 5223 |
| A6 | `proposals/2026-10-22-redundancy` | 18 | 154366 |
| A7 | `proposals/2026-10-22-redesign` | 73 | 694220 |
| A8 | `proposals/2026-10-22-r044-veto` | 29 | 203618 |
| A8 | `proposals/2026-10-22-gvmw` | 37 | 680775 |
| A9 | `proposals/2026-10-05` | 13 | 75144 |
| A9 | `proposals/2026-10-09` | 9 | 53769 |
| A9 | `proposals/2026-10-15` | 11 | 114594 |
| A9 | `proposals/2026-10-16` | 16 | 144749 |
| A9 | `proposals/2026-10-16-rr028` | 10 | 81037 |
| A9 | `proposals/2026-10-16-deploy` | 5 | 40344 |
| A9 | `proposals/2026-10-16-investigator` | 3 | 11137 |
| A9 | `proposals/2026-10-16-connectors2` | 11 | 191853 |
| A9 | `proposals/imitator-approver-2026-10-04` | 5 | 16176 |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04` | 8 | 28523 |
| A10 | `proposals/clone-accuracy-validator-v002.md` | 1 | 3667 |
| A10 | `proposals/comms-concierge-v002.md` | 1 | 3146 |
| A10 | `proposals/cost-budget-sentinel-v002.md` | 1 | 3660 |
| A10 | `proposals/genesis-gang-god-v002.md` | 1 | 5218 |
| A10 | `proposals/governance-continuity-deputy-v002.md` | 1 | 4973 |
| A10 | `proposals/orchestration-conductor-v002.md` | 1 | 3908 |
| A10 | `proposals/connector-steward-v002.md` | 1 | 3447 |
| A10 | `proposals/secrets-credentials-custodian-v002.md` | 1 | 4324 |
| A10 | `proposals/auditor-v002.md` | 1 | 1688 |
| A10 | `proposals/compliance-risk-officer-v002.md` | 1 | 4619 |
| A10 | `proposals/codex-keeper-v002.md` | 1 | 6215 |
| A10 | `proposals/archivist-brief-v002.md` | 1 | 7611 |
| A10 | `proposals/codey.md` | 1 | 6873 |
| A10 | `proposals/grok-bot.md` | 1 | 5933 |
| A10 | `proposals/scraper.md` | 1 | 8619 |
| A10 | `proposals/APPROVED-for-archivist-2026-10-04.md` | 1 | 7858 |
| A10 | `proposals/agent-message-verification-rule-v001.md` | 1 | 7940 |
| A10 | `proposals/collaboration-map.png` | 1 | 206575 |
| A11 | `proposals/2026-10-22-adversarial-response` | 8 | 105710 |
| A12 | `proposals/2026-10-10-backlog-triage.md` | 1 | 15052 |
| A13 | `codex/PENDING-FOR-ARBITER.md` | 1 | 21020 |
| A13 | `codex/PENDING-FOR-ASSEMBLER.md` | 1 | 3538 |
| A15 | `risk/2026-10-22-liveness-watchdog-plan.md` | 1 | 1614 |
| A16 | `risk/2026-10-22-destructive-ops-gate.md` | 1 | 3795 |
| A17 | `archive/rulings-2026-10-22-pre-consolidation.md` | 1 | 76196 |
| A17 | `directory.md.bak-0909` | 1 | 3809 |
| A17 | `directory.md.bak-1504` | 1 | 6696 |
| A17 | `schedule.md.bak-20261016` | 1 | 8401 |
| A17 | `schedule.md.bak-20261016-1107` | 1 | 10945 |
| A17 | `schedule.md.bak-20261016-1148` | 1 | 11346 |
| A17 | `schedule.md.bak-20261022-1845` | 1 | 12042 |
| A17 | `risk/register.md.bak-20261016` | 1 | 28650 |

**Total:** 296 files, 3185877 bytes.

## Not moved

- A3: the public-repo phase sections live in my compiled editions on gemquota/swarm. That needs a rebuild and a push, not a move.
- A14: New Bot's empty folder is an agent folder outside /workspace/governance. Gem removes the bot from the sidebar.
- A18: role-map versions v1–v21 are skipped as Archivist's call; Archivist keeps them on purpose.
- A1's `proposals/final-2026-10-04/handoff-phase1-final.md` moves as part of A9's `final-2026-10-04/` folder.
- A8 `proposals/2026-10-16-github`: skipped, referenced by shared:github, shared:message-verification-rule
- A9 `proposals/2026-10-06`: skipped, referenced by shared:confirm-deployment
- A9 `proposals/final-2026-10-04`: skipped, referenced by shared:handoff-phase1, shared:collaboration-map
- A10 `proposals/collaboration-map.md`: skipped, referenced by shared:collaboration-map

## Per-file sha256

| Item | File (original path) | Bytes | sha256 |
|---|---|---|---|
| A0 | `codex/_shared/handoff-phase1/CHANGELOG.md` | 420 | `d8970b7005dac5caf9b68280ce63211359b426d06ba16aafdfafe7d1fd15d59c` |
| A0 | `codex/_shared/handoff-phase1/v001.md` | 5095 | `225e241fe29a9df2818df38f7dfa6aabdd6bfd29aaa9c603d78d5f5a1b411535` |
| A1 | `proposals/handoff-phase1-v001.md` | 8828 | `45a209eb7e8b2c97a2aa6b49b78ce67ec1571de5e0f07b69440acc6c66df5315` |
| A1 | `proposals/phase1-interim-bundle-v001.md` | 9843 | `6902c1ea06c4a1c9c8b36d957af78cc7473eb00945dfbe8f830356d979df35db` |
| A2 | `schedule.md.bak-p1` | 4548 | `ac2dce6773e1dba3f1fc540ecd30dfeca7211a2fd32ee089f8c6c70d4b5048e2` |
| A4 | `proposals/2026-10-09-retire-merge/README.md` | 9448 | `7d3222bbcb692fbe6757b0b0d497ff85f0bc90cfb18c11d5fda3cd82ac3087ad` |
| A4 | `proposals/2026-10-09-retire-merge/_build.py` | 14975 | `c73a4eeff0a2be129fdd4f3a4280c8a6e756408a80e4e26712a6755457e5349c` |
| A4 | `proposals/2026-10-09-retire-merge/apply.json` | 32104 | `ceb6eeea89b6999f5c5305006ebef2def4a5c7a29f02cb5e3287c9cc9fcab6d6` |
| A5 | `proposals/merge-F-unretire-assembler-2026-10-04.md` | 5223 | `1f7e865cb3784452fddf7f8b80bff78daa26bfa10ef0c01fad96250b02b43c7f` |
| A6 | `proposals/2026-10-22-redundancy/README.md` | 9079 | `770c604b8a2129431fc939eb427454bbedaa9311f09c44b365d218462fca959f` |
| A6 | `proposals/2026-10-22-redundancy/_tools/__pycache__/split.cpython-313.pyc` | 653 | `ac3df182180f45ae2e233f0f18018dc49c4d255e579dcafd6dc09092e9402d64` |
| A6 | `proposals/2026-10-22-redundancy/_tools/build-rev1.py.bak` | 27959 | `3ddb5feda69f4a3d4da088d03ec13911177becdd4f2b33af441123ce785b55bf` |
| A6 | `proposals/2026-10-22-redundancy/_tools/build.py` | 29854 | `2b2b3bb1067fe2511f41d11bb033c5cf61d3e92dac988674bf2fe9040fe67ac5` |
| A6 | `proposals/2026-10-22-redundancy/_tools/split.py` | 309 | `5efb42c49e4d62b377f4705f720545032b0f1457015560b9ea637e9fd6e0911c` |
| A6 | `proposals/2026-10-22-redundancy/arbiter-v006.md` | 3344 | `848371ff1d497aa920dd2407b5be0f85bcf0046493142466d1c70a7f134f4bae` |
| A6 | `proposals/2026-10-22-redundancy/architect-v005.md` | 4705 | `19a60a5f578fd178209425ed319d8eb2890e636888ade29ba3551ffecd6d1557` |
| A6 | `proposals/2026-10-22-redundancy/archivist-v009.md` | 9942 | `6e17f41bafe3555c585a450a15b213d348521e3d3a5d1b5ebf43ee9f146b663a` |
| A6 | `proposals/2026-10-22-redundancy/emissary-v007.md` | 8164 | `9b2b7acf61195f171eac8308c0f1f0d35ab6e713e08693a10ed29575addff807` |
| A6 | `proposals/2026-10-22-redundancy/explorer-v006.md` | 10186 | `3877021e4870496c23295729b0a45ab32354258d88444a02bc87dbdb3ab2a864` |
| A6 | `proposals/2026-10-22-redundancy/extractor-fold-proposal.md` | 3101 | `1a77a4daa10f0cae6dc4ecacdc021c9bcef69b4e54a2b099030466f8b9e5a5e5` |
| A6 | `proposals/2026-10-22-redundancy/extractor-v006.md` | 9134 | `f1849e752e35dd360620800d4a1f486199d6d1c8f86ae3bee5bdb5a1971c6e67` |
| A6 | `proposals/2026-10-22-redundancy/imitator-v007.md` | 7501 | `0c94628980f2b4626dc887073bdede1c5c9f760a983acef8233b8eb6930412e2` |
| A6 | `proposals/2026-10-22-redundancy/inferer-v006.md` | 9224 | `7798ada968612823126ae7e4bc67fe9a716c70141a0706b0e270d9c98ba9917f` |
| A6 | `proposals/2026-10-22-redundancy/investigator-v005.md` | 6153 | `f9969494895ffbb38c031834fe1f534c3c5a1d593bfd0ec3c09e4f094df03a31` |
| A6 | `proposals/2026-10-22-redundancy/safeguard-v007.md` | 6865 | `dbec26ac5af4494b3921722543f360efc46283a3ced5dc3629ed7307494bee00` |
| A6 | `proposals/2026-10-22-redundancy/scorer-v005.md` | 4006 | `91ae6fb6fa65f92f2111615c51ee3a9cab4c6160a8942489903d7368880dbd21` |
| A6 | `proposals/2026-10-22-redundancy/scrutineer-v005.md` | 4187 | `ff6381c41407263766b4d8157927771ff8b3c3b32d5ff3ed770bc40e37a2bec1` |
| A7 | `proposals/2026-10-22-redesign/README-pre-status.md.bak` | 10298 | `f7b2389bad2cb25947ba05c74b2c83e390fb19a22c83b724f3d14073b72de6a3` |
| A7 | `proposals/2026-10-22-redesign/README.md` | 10850 | `e151d46140d4420b9be6981292732c8e78363b444b3079cfab2fd19fff77d27a` |
| A7 | `proposals/2026-10-22-redesign/_pre832/README.md` | 9455 | `4fd414a087c2096bf98ae434e3290d086eb7a51a1190bdeec1d600f4082b7818` |
| A7 | `proposals/2026-10-22-redesign/_pre832/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/_pre832/archivist-v011.md` | 10524 | `fde284ba8a23e54deee845d6d2c5b5f3540f61f47ac0c389bc90edc0b23c03a4` |
| A7 | `proposals/2026-10-22-redesign/_pre832/deterministic-checks-v001.md` | 4261 | `a53190532dedbcb535bed1b9d9500306e41893d6d238a536a3d2133b8bb14b2a` |
| A7 | `proposals/2026-10-22-redesign/_pre832/emissary-v010.md` | 16241 | `bb494f09eaea0211a21d4b3d2b82f98fe1581bc36ec4f5d9cc158d07052d1711` |
| A7 | `proposals/2026-10-22-redesign/_pre832/inferer-v008.md` | 13493 | `739eb17049b8ee338d4d8177fe28229fa5116d095a76c2eb790500dd9dab1465` |
| A7 | `proposals/2026-10-22-redesign/_pre832/investigator-v007.md` | 5816 | `87086101a7f3a596f5c69cf58ab930a48065a3c21727307c501fc6b7c71b3224` |
| A7 | `proposals/2026-10-22-redesign/_pre832/mender-v007.md` | 13306 | `df9b5864e1046f4b46c6d8f0fa6c48ed879ff041f77050d350e296634858aa58` |
| A7 | `proposals/2026-10-22-redesign/_pre832/resilience-v001.md` | 2776 | `d71dea9b44bf5f2e18c855eb3d39809a292debd9062d652098d820e449ea81cb` |
| A7 | `proposals/2026-10-22-redesign/_pre832/safeguard-v009.md` | 15188 | `d6f6a9a517c6b53e530b503f22c29fc60f261fe3839350fa95ddd7e4eedc202a` |
| A7 | `proposals/2026-10-22-redesign/_pre832/scrutineer-v007.md` | 8007 | `4d5561aa90aaccd4d01902ec60db5634b38802db94fd58271decc12c80005340` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/README.md` | 10038 | `bda48b427ab1d596f948272b6eb5e6db52f9374ae4a88a0b36400b086ed2643b` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/archivist-v011.md` | 10524 | `fde284ba8a23e54deee845d6d2c5b5f3540f61f47ac0c389bc90edc0b23c03a4` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/deterministic-checks-v001.md` | 4455 | `c6584c15ecdfe6ed26b031de39eba4605ce267425e8c848f2d0630914239f374` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/emissary-v010.md` | 16241 | `bb494f09eaea0211a21d4b3d2b82f98fe1581bc36ec4f5d9cc158d07052d1711` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/inferer-v008.md` | 13493 | `739eb17049b8ee338d4d8177fe28229fa5116d095a76c2eb790500dd9dab1465` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/investigator-v007.md` | 5816 | `87086101a7f3a596f5c69cf58ab930a48065a3c21727307c501fc6b7c71b3224` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/mender-v007.md` | 13306 | `df9b5864e1046f4b46c6d8f0fa6c48ed879ff041f77050d350e296634858aa58` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/resilience-v001.md` | 2776 | `d71dea9b44bf5f2e18c855eb3d39809a292debd9062d652098d820e449ea81cb` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/safeguard-v009.md` | 15341 | `9834679c225873388fe56f4424fd5cbc29cc8730a63f6c41aa5b99947de07301` |
| A7 | `proposals/2026-10-22-redesign/_prefinal/scrutineer-v007.md` | 8007 | `4d5561aa90aaccd4d01902ec60db5634b38802db94fd58271decc12c80005340` |
| A7 | `proposals/2026-10-22-redesign/_r1/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/_r1/archivist-v009.md` | 9017 | `b9db7c02432d99d2290962252776ea647c4f559065fefad735b11c88037aaae4` |
| A7 | `proposals/2026-10-22-redesign/_r1/deterministic-checks-v001.md` | 3421 | `adf6bc1f97111f8ff9bc78d2262f6dad967d25b976819e78637b44f5af6952ac` |
| A7 | `proposals/2026-10-22-redesign/_r1/emissary-v008.md` | 14595 | `7801f1bab0b1827911dd158318cfa65488912f48fd075360f926235bd5f66851` |
| A7 | `proposals/2026-10-22-redesign/_r1/inferer-v007.md` | 12431 | `c435bbfdbc53263fede373c89d3e9bd5f7efec311f76a100addb423eb8ae3cfe` |
| A7 | `proposals/2026-10-22-redesign/_r1/investigator-v005.md` | 4319 | `70da1f1f099770495197e68a282f631cc333a6ab2ba4b3d74d0a010466f11b9e` |
| A7 | `proposals/2026-10-22-redesign/_r1/mender-v006.md` | 11225 | `afee7ae4ed3d53f0f2381123b347daa4a6a74f19004d54541c60038fb4a2c250` |
| A7 | `proposals/2026-10-22-redesign/_r1/resilience-v001.md` | 2536 | `22c8fb385bd5c6c6a6b475f8663bd92090f608d2225c03bcd2f8fddcdeb7a97e` |
| A7 | `proposals/2026-10-22-redesign/_r1/safeguard-v008.md` | 10449 | `adec785c621310e077cb984a0d8150e92a358c187026e745d2868398a3d781af` |
| A7 | `proposals/2026-10-22-redesign/_r1/scrutineer-v005.md` | 6205 | `5ae819ef51091bbe479dd445eebaf23a575c4936fcd925772452d0c1462d02d1` |
| A7 | `proposals/2026-10-22-redesign/_r2/README.md` | 5928 | `83e345d946889f795811863afd6746086a77f6a71045957734bc62ba67e2eb3f` |
| A7 | `proposals/2026-10-22-redesign/_r2/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/_r2/archivist-v011.md` | 9644 | `153daec69a29b1c32990d324e1d419d8944493deed5dd8b0699eb55090b05678` |
| A7 | `proposals/2026-10-22-redesign/_r2/deterministic-checks-v001.md` | 3421 | `adf6bc1f97111f8ff9bc78d2262f6dad967d25b976819e78637b44f5af6952ac` |
| A7 | `proposals/2026-10-22-redesign/_r2/emissary-v010.md` | 15887 | `68634fd44e51647f08d28755d8eff93d8f4cca6894b47cb60ed61c7fcc7a41c6` |
| A7 | `proposals/2026-10-22-redesign/_r2/inferer-v008.md` | 13147 | `94388979611c176de06c06259f69c48708b3914e56ff0c686978f730be97da92` |
| A7 | `proposals/2026-10-22-redesign/_r2/investigator-v007.md` | 5282 | `920c8b23c9581fb9d363624186d6f955053064c98194cb38ece509e2d897220e` |
| A7 | `proposals/2026-10-22-redesign/_r2/mender-v007.md` | 12840 | `d5ef004502bd6662170230faf69792782315bf3c9b5a496e71c23609eb7cbecb` |
| A7 | `proposals/2026-10-22-redesign/_r2/resilience-v001.md` | 2535 | `059fe27b555c0697fea3758ad6bfb501f6ea4a297ca32e1e7da22f39ef34e675` |
| A7 | `proposals/2026-10-22-redesign/_r2/safeguard-v009.md` | 14652 | `997c22f035e4c9dc845407931d3dba77d3a789b7ff952de7da721daac8b291f3` |
| A7 | `proposals/2026-10-22-redesign/_r2/scrutineer-v007.md` | 7328 | `26055e39f217c6d7d16b53dc3e83088c34b5ab166b69ab10e2f97ac2e3641162` |
| A7 | `proposals/2026-10-22-redesign/_r3/README.md` | 7942 | `72f6a39e11595f3014105149c08e43b74e7307a5a3fd1ae0bf5a89bc407aae76` |
| A7 | `proposals/2026-10-22-redesign/_r3/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/_r3/archivist-v011.md` | 9844 | `197ef75c954fb7d1c341456bab0fc5638fd3fd7c3d4e2d9a528649ea32d0e1fe` |
| A7 | `proposals/2026-10-22-redesign/_r3/deterministic-checks-v001.md` | 3711 | `e4cea617fa6e757bd800becae39b978a67c4b7f645ce6b23b5e844a65d2a1125` |
| A7 | `proposals/2026-10-22-redesign/_r3/emissary-v010.md` | 16087 | `e3d0e805a87a4fa714f0a4c3b602c7793066cfa0ba875892d895a2564ef2e692` |
| A7 | `proposals/2026-10-22-redesign/_r3/inferer-v008.md` | 13347 | `25f47e6067b740b815126209720d3f4caaf09320c5801f8b9b3d14ac39d22ee3` |
| A7 | `proposals/2026-10-22-redesign/_r3/investigator-v007.md` | 5482 | `109a2ec0721404ed68ed912fafbe9e5ca28a7b94465dfa3eabff5844631c127f` |
| A7 | `proposals/2026-10-22-redesign/_r3/mender-v007.md` | 13168 | `c81642f2c919403ef28f2227f23060bfa000771f4919579f795b07b27f2b1019` |
| A7 | `proposals/2026-10-22-redesign/_r3/resilience-v001.md` | 2535 | `059fe27b555c0697fea3758ad6bfb501f6ea4a297ca32e1e7da22f39ef34e675` |
| A7 | `proposals/2026-10-22-redesign/_r3/safeguard-v009.md` | 14852 | `6e1ac4c573565b739d4d78725551db020bd2d7347c201c60ca9aef85e0499e77` |
| A7 | `proposals/2026-10-22-redesign/_r3/scrutineer-v007.md` | 7850 | `ac6d38914be3e9f88dc28626ec99be805798d0c9f76ec1b294e40bf9f58e6342` |
| A7 | `proposals/2026-10-22-redesign/_tools/build-pre832.py.bak` | 20307 | `0b4373dbf8734dfc78a1866c23f3bfc4b2b920693db6db4e163a2464a4925e0f` |
| A7 | `proposals/2026-10-22-redesign/_tools/build-prefinal.py.bak` | 20624 | `f04698d93c28e889dfcffafd622ffe5e7720f5b60b13847b16a2d977e5fce861` |
| A7 | `proposals/2026-10-22-redesign/_tools/build-r1.py.bak` | 15750 | `82a423d509884b96d329ddfb270c7a948564441b78009423434fd4e1037e442d` |
| A7 | `proposals/2026-10-22-redesign/_tools/build-r2.py.bak` | 16327 | `1b299bd9c55d857ba38d9053287227c0000067abe49d1f68b3cf79a21d7d8902` |
| A7 | `proposals/2026-10-22-redesign/_tools/build-r3.py.bak` | 18769 | `24b4e6c8b9bbd9b10f74c6b9cc4c443aa932c047941867a6bba579b2d832c8e1` |
| A7 | `proposals/2026-10-22-redesign/_tools/build.py` | 20620 | `555805902a6ba6f0a583f3d4327fa07a99474ba2165a0c6cb66cc9b50af3bfca` |
| A7 | `proposals/2026-10-22-redesign/_tools/hashes.txt` | 457 | `e4a4a7e5817de98a66fe4e48b48b7d5b3883faa608ecf793af92131d93f7c24b` |
| A7 | `proposals/2026-10-22-redesign/approval-objects-v001.md` | 1918 | `aa9a7fdcb4d2412051402e8f343912a18cd123d8c200311149c800862abfc585` |
| A7 | `proposals/2026-10-22-redesign/archivist-v011.md` | 10524 | `fde284ba8a23e54deee845d6d2c5b5f3540f61f47ac0c389bc90edc0b23c03a4` |
| A7 | `proposals/2026-10-22-redesign/deterministic-checks-v001.md` | 4455 | `c6584c15ecdfe6ed26b031de39eba4605ce267425e8c848f2d0630914239f374` |
| A7 | `proposals/2026-10-22-redesign/emissary-v010.md` | 16241 | `bb494f09eaea0211a21d4b3d2b82f98fe1581bc36ec4f5d9cc158d07052d1711` |
| A7 | `proposals/2026-10-22-redesign/inferer-v008.md` | 13493 | `739eb17049b8ee338d4d8177fe28229fa5116d095a76c2eb790500dd9dab1465` |
| A7 | `proposals/2026-10-22-redesign/investigator-v007.md` | 5816 | `87086101a7f3a596f5c69cf58ab930a48065a3c21727307c501fc6b7c71b3224` |
| A7 | `proposals/2026-10-22-redesign/mender-v007.md` | 13306 | `df9b5864e1046f4b46c6d8f0fa6c48ed879ff041f77050d350e296634858aa58` |
| A7 | `proposals/2026-10-22-redesign/resilience-v001.md` | 2772 | `4d18854f685cc12123f67b02ef36025ec22b9da7b7eba433c608a5b07e40820b` |
| A7 | `proposals/2026-10-22-redesign/safeguard-v009.md` | 15352 | `256d0464f5bd7628c63cf23b27079145976677e1f1aa62481ce39f09ccc28f0d` |
| A7 | `proposals/2026-10-22-redesign/scrutineer-v007.md` | 8007 | `4d5561aa90aaccd4d01902ec60db5634b38802db94fd58271decc12c80005340` |
| A8 | `proposals/2026-10-22-r044-veto/README.md` | 5929 | `1ebb6b9239cb3ac8898240261f4be59a75e84f7cfe0aee90a27b85baf226e19f` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/README.md.r1.bak` | 2309 | `c70b00259cdbda6d19326af65b22018e972ae9b265364d0ae772442a15860b6f` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/arbiter-v007.md.r1.bak` | 3902 | `569828054cc4ee4850a69fd4033c9b832c556f6d85fb38746b197d2119a2d30b` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build-r1.py.bak` | 4396 | `7bb16ff8552fe448f10b7afedf956d57b1477bba4cec0573a8b924b25d42933f` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build-r2.py.bak` | 5282 | `85c813ec64b3885116363094ba8208631286e1e0b5b88ad96c61bd31b6ae8ba5` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build-r3.py.bak` | 9375 | `5bfae52342e88af6f5563b74ccacf02a30e4943e1efef249f862608bd5b54acb` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build-r4.py.bak` | 10163 | `4d42a12b9643a3d03b31d84e5eec6721d085acccc36b252837c66ed65f864d90` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build-r5.py.bak` | 10738 | `0deabe566dd22dfe81b58347d86148d96382271172ccb8e8dc5f9170fd4d28f5` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/build.py` | 10776 | `680fb35760b2b7ac68417eb1eea08dea1725ab75463fbae6a8cf4407d5721092` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/imitator-v008.md.r1.bak` | 6853 | `9e59235880ee83423d5ae47414b7470f75a561b73b05277cdaae2bb0c2dffc6c` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/prefinal/README.md` | 5814 | `1203c08bb941d96bc9cd392319bc5b28ba2318703eb2fb7f1496b775930834bf` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r2/README.md` | 2967 | `0d05cae9c84a60190c3715dd74a3a24ba40a23d7ba08374efecddb37de31e795` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r2/arbiter-v007.md` | 4454 | `38ae56219e67e53ccf84f518f98deae4731a81b2969c95271f1fcf736169d697` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r2/imitator-v008.md` | 7573 | `842c9148c347048f4f56790bbf1b866f9a4410edd0e2f1f4d26e082471ead107` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r3/README.md` | 4139 | `a9a78c6dd61c4385662ea9ff1d2c60385fec4c603d8015cad9e6e4c3a955e470` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r3/arbiter-v007.md` | 4745 | `fc80f5f4911ed99f4ed54aa6644899aadf9bdbd7619c14d54c3cb90ae7d09ddc` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r3/emissary-v008.md` | 8938 | `4a4e9a40520d7471eefb870f9e549b86bb74d04e572dc426f2e04e7025f55751` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r3/imitator-v008.md` | 9388 | `af00634358d045b714165f23b66f3acab685c7b6f19fd3dee24d4648b6ebfbe0` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r4/README.md` | 4913 | `00ec39ed2e380ce6e02f2d735e250987dacd04c16ecf158bdd81d6076daf5aa3` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r4/arbiter-v007.md` | 4745 | `fc80f5f4911ed99f4ed54aa6644899aadf9bdbd7619c14d54c3cb90ae7d09ddc` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r4/emissary-v008.md` | 9243 | `efbd507860eadabc18ee7b29f8f610dbe35314313ced913b4c516d09e292e224` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r4/imitator-v008.md` | 10353 | `4e2a2293e12c990be2804596dbf0cd39aa3c09c3e69dae86c3fcd758d8957462` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r5/README.md` | 5581 | `5452917858889a2122305fd4c287ba37abde96edf920ee4ae0ab71170b1b9bef` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r5/arbiter-v007.md` | 4745 | `fc80f5f4911ed99f4ed54aa6644899aadf9bdbd7619c14d54c3cb90ae7d09ddc` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r5/emissary-v008.md` | 9243 | `efbd507860eadabc18ee7b29f8f610dbe35314313ced913b4c516d09e292e224` |
| A8 | `proposals/2026-10-22-r044-veto/_tools/r5/imitator-v008.md` | 11495 | `40f0f3d4a3c7d8dadd17641cdb9e6cfca8c33faa87d6586033a02f9d2bcf4b56` |
| A8 | `proposals/2026-10-22-r044-veto/arbiter-v007.md` | 4745 | `fc80f5f4911ed99f4ed54aa6644899aadf9bdbd7619c14d54c3cb90ae7d09ddc` |
| A8 | `proposals/2026-10-22-r044-veto/emissary-v008.md` | 9243 | `efbd507860eadabc18ee7b29f8f610dbe35314313ced913b4c516d09e292e224` |
| A8 | `proposals/2026-10-22-r044-veto/imitator-v008.md` | 11571 | `654852de7f2a430e74d37c65e3f1d2253b1c6d2804a8c0af15ce3f1c39ec7cea` |
| A8 | `proposals/2026-10-22-gvmw/README-rev6.md.bak` | 18184 | `945d845dbccf29926a00cac663e9246ad9ea914d1a482b5e0045cfbe1f860cca` |
| A8 | `proposals/2026-10-22-gvmw/README.md` | 21804 | `680de7dc7ce49814cc5a233789d69fecf31809191231fdafe69ce3b096d0abed` |
| A8 | `proposals/2026-10-22-gvmw/_pre832/README.md` | 21078 | `f25f223f5f7ac211d2bc492762846d5185025989d08730621f5e943569fa38c3` |
| A8 | `proposals/2026-10-22-gvmw/_pre832/connector-limits-v003-variant-b.md` | 28645 | `65c26a0005ac462139792107e0b0a4708227794a425745208a541b6ac57ce3e0` |
| A8 | `proposals/2026-10-22-gvmw/_pre832/connector-limits-v003-variant-c.md` | 28492 | `d8351340e089b85896e5a01c71e8eb2b47623fb9d6034fb46e655b80396ab54a` |
| A8 | `proposals/2026-10-22-gvmw/_pre832/connector-limits-v003.md` | 27835 | `4de9ca4031a31467ffeebf9a362c6abf0fec1a810496846279c70bbcbb6a17ea` |
| A8 | `proposals/2026-10-22-gvmw/_pre832/input-safeguard.md` | 1639 | `bbc76cccbfc8cc026a8a981a7597a55b43148bf09f3ee835a80986cbb5f95fd2` |
| A8 | `proposals/2026-10-22-gvmw/_rev6/README.md` | 18184 | `945d845dbccf29926a00cac663e9246ad9ea914d1a482b5e0045cfbe1f860cca` |
| A8 | `proposals/2026-10-22-gvmw/_rev6/connector-limits-v003-variant-b.md` | 27448 | `7d004d4a21dc615a08a8ac08ebd3e4450a72b944939e7bdfd77fdd24b20e8492` |
| A8 | `proposals/2026-10-22-gvmw/_rev6/connector-limits-v003-variant-c.md` | 27295 | `04330e3747556df49bcac963f5a54e7c02551c128fe8bf85b5ffdeb889b1e582` |
| A8 | `proposals/2026-10-22-gvmw/_rev6/connector-limits-v003.md` | 26638 | `d748aac166126e866a640265931090d5d16ea4485d2f59ea213e2e194a06c2ca` |
| A8 | `proposals/2026-10-22-gvmw/_rev6/input-safeguard.md` | 1639 | `bbc76cccbfc8cc026a8a981a7597a55b43148bf09f3ee835a80986cbb5f95fd2` |
| A8 | `proposals/2026-10-22-gvmw/_rev7/README.md` | 19746 | `1c2c40e1bba94a9dc88e021ff0efe8657990480ec0ce76d17cf2e5fc6a66959d` |
| A8 | `proposals/2026-10-22-gvmw/_rev7/connector-limits-v003-variant-b.md` | 27569 | `478f6a2f108c969dfb90d750d20405ccf88cd3f91f59a9742c68579906cc5fee` |
| A8 | `proposals/2026-10-22-gvmw/_rev7/connector-limits-v003-variant-c.md` | 27416 | `638322dad20fef5ea6e39fcc39d125deb1e0e31c757e2480e6d205540b0e4c43` |
| A8 | `proposals/2026-10-22-gvmw/_rev7/connector-limits-v003.md` | 26759 | `c32b0514b05a634970cdf5def4f22bee223f75519d7d9da75594ebef5c8a6379` |
| A8 | `proposals/2026-10-22-gvmw/_rev7/input-safeguard.md` | 1639 | `bbc76cccbfc8cc026a8a981a7597a55b43148bf09f3ee835a80986cbb5f95fd2` |
| A8 | `proposals/2026-10-22-gvmw/_rev8/README.md` | 20651 | `84be57fb27f3bec3d4465030a83a031aa4d6a7108f22bfaa1317d1986b533e19` |
| A8 | `proposals/2026-10-22-gvmw/_rev8/connector-limits-v003-variant-b.md` | 28149 | `8fb3f3bcb805e664ee1773a0e3334feea6a283c10c3458d8b8311c840423a104` |
| A8 | `proposals/2026-10-22-gvmw/_rev8/connector-limits-v003-variant-c.md` | 27996 | `afcfd78f0c53867a72cedf84917da81d310da8f8227c11bbc1d967d8ebb78285` |
| A8 | `proposals/2026-10-22-gvmw/_rev8/connector-limits-v003.md` | 27339 | `6083fc741a8956a4d16aa6cb6c6ddfd3f8b69978b75f5d26fef26dc17a3b74ee` |
| A8 | `proposals/2026-10-22-gvmw/_rev8/input-safeguard.md` | 1639 | `bbc76cccbfc8cc026a8a981a7597a55b43148bf09f3ee835a80986cbb5f95fd2` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-pre832.py.bak` | 16170 | `698db042b163b344f6f2c2e6a7fd24adb41172b5a8f6d65ff3ecbbebd8ed6d19` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-r1.py.bak` | 6145 | `c4b0bbfa454cde5c8ef303c98e55b6a0595df11b681561824917357caa0aa340` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-r2.py.bak` | 8366 | `55d3bc1f16fc65e5dd67a8afa2d1e5cf4490f50bbd4992022715f78efb22abff` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev2.py.bak` | 9084 | `ed49981bfbad2431fc3b2a2e3146b4a0b39b5ff30580f8049d252d6b41ad69f4` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev3.py.bak` | 10549 | `9c8d3f7b9f2c5ff7da9eeeb5b728bdef4d5cf69ac05f24d667f70e5daec40d18` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev4.py.bak` | 12324 | `45e384bc5fb214971299a2effe0b6fc8b60399cb22da83884e2a15638403d6b3` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev5.py.bak` | 13536 | `c265c960f590b81e92be320ed29d329d976555c4393db8d7e9bb3affeedf2100` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev6.py.bak` | 14283 | `fb501cd62ddcc3e0fe1b250c5a750490a64304af877f10f332ced74a05f82e09` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev7.py.bak` | 14406 | `0fd99f4964705e7d365314c5d2282a8fbd71590cba69e091886f53addfd487e0` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build-rev8.py.bak` | 15467 | `fafd39d1a403dde9f9b02f8b90db2cdd923f2195d5262acd3a615e4be9f3b1d1` |
| A8 | `proposals/2026-10-22-gvmw/_tools/build.py` | 16140 | `9089a908a7d169ac2d9a3c3f5ffcd6d725327daa6962cc16cef184592ca0d365` |
| A8 | `proposals/2026-10-22-gvmw/connector-limits-v003-variant-b.md` | 28615 | `9f0acf635543ef5b7f66af332be4adfc118d88b7aa91558b66ede23e37537170` |
| A8 | `proposals/2026-10-22-gvmw/connector-limits-v003-variant-c.md` | 28462 | `474d865effe5fe6c9cbf2d1e569fb41df0deffcf30d0b5639804e232ed802da9` |
| A8 | `proposals/2026-10-22-gvmw/connector-limits-v003.md` | 27805 | `5c61d0a314796198c7c5201f6bb29218c653b5da0e55c9c71b53424ef29fd8bb` |
| A8 | `proposals/2026-10-22-gvmw/input-safeguard.md` | 1639 | `bbc76cccbfc8cc026a8a981a7597a55b43148bf09f3ee835a80986cbb5f95fd2` |
| A9 | `proposals/2026-10-05/README.md` | 14952 | `d47bdbf8c9cb2ad4fecc99dc98033615b08eace09032d5599dcce5048bb49b20` |
| A9 | `proposals/2026-10-05/arbiter-v004.md` | 2456 | `fb7852b6418221267514c7117b9e83c852005953fab307affe49b555b937d45f` |
| A9 | `proposals/2026-10-05/archivist-v004.md` | 6330 | `906983ae347429545838fa41139b38f3132a41f1496b371cec640680e9d9a2aa` |
| A9 | `proposals/2026-10-05/emissary-v004.md` | 6372 | `1e78221d746e0d85cc7ccfbdb87da39f47f1fe4e2358849666fe0b0f185d367a` |
| A9 | `proposals/2026-10-05/engineer-v005.md` | 6539 | `bf080fe0935a76738eb2c4fdab883147fdbb6a752efb339cab434e6cbb1e11fd` |
| A9 | `proposals/2026-10-05/explorer-v004.md` | 6404 | `086f700dc578d7a607439a4dab7cffbb039431e36594ce60570bdbde331dee69` |
| A9 | `proposals/2026-10-05/extractor-v003.md` | 7178 | `980c36d2d451f787d797ddd08b74cbef2b5994df2e112e030073eedf6938ed6e` |
| A9 | `proposals/2026-10-05/inferer-v002.md` | 4908 | `02259cbcd695500100d97828debc61037653c7816fafe94af76a8eb0e9121a69` |
| A9 | `proposals/2026-10-05/inquirer-v002.md` | 4450 | `b3571d7cd1332aef513e40089ecd0546776803665784b67d4c7334d1b58e339a` |
| A9 | `proposals/2026-10-05/marshal-v004.md` | 3433 | `04efe702a163436e95a0488047c4a9325ab9883f4900fbc384dc27a8406036ce` |
| A9 | `proposals/2026-10-05/safeguard-v004.md` | 4364 | `30c47a32ca91a28ae9687a6b6685a59cc8b1e9bd08de90613fdce75ca4ba00c1` |
| A9 | `proposals/2026-10-05/safekeeper-v004.md` | 4728 | `9c669612113f7d2689e4385a337f5b8109bf546852b2f1898df8c3dd5313399b` |
| A9 | `proposals/2026-10-05/scorer-v003.md` | 3030 | `3170ceabcdc4a263a979065ac4c4a1919c9f70cbde392fe1ac6250c88dbcc810` |
| A9 | `proposals/2026-10-09/README.md` | 4716 | `484d3402876e4cf04d455982e556a493c1a03a0e749a220500e2c79fad947750` |
| A9 | `proposals/2026-10-09/arbiter-v005.md` | 3289 | `d14c4bd98db7f71aaf2764ff7627da1d474cc84a428e97d129b3722019b3075e` |
| A9 | `proposals/2026-10-09/architect-v004.md` | 3977 | `5aef95829a33a9cf393c9122c46eddeee951f62f192e919cba22c91651679eab` |
| A9 | `proposals/2026-10-09/emissary-v005.md` | 5377 | `94e5702a6f22229b3b66210df2158f4f209ccc6b1bc7fd034e6f07c0cebc6490` |
| A9 | `proposals/2026-10-09/engineer-v006.md` | 4802 | `cb513afd4bfaace3caaf54cc392f43074c5327ca9e6823cda102cbe0f4141584` |
| A9 | `proposals/2026-10-09/explorer-v002.md` | 8966 | `549cfaedeaece7d068466d30f5c38e1962011d2c2eb00046dee0d0c8e46fbac5` |
| A9 | `proposals/2026-10-09/inferer-v003.md` | 8126 | `6d7f7fdb576fd5fb9c17721c18841da9b7337875d9f2883f132bf0f9af71554a` |
| A9 | `proposals/2026-10-09/inquirer-v003.md` | 9346 | `253975df990b4bce69adac41a9464355d5a0fdead2e08e92b8cc9f6b45b1e1aa` |
| A9 | `proposals/2026-10-09/scrutineer-v004.md` | 5170 | `fbbbda2e3256ece2fd2001dfd447d4f6fe18c9fddee035caee0e59361ebbd8db` |
| A9 | `proposals/2026-10-15/README.md` | 20620 | `3beef495e4c3813863583dfa117de5ec3efee56af5f399859adfe43f0f486b99` |
| A9 | `proposals/2026-10-15/_tools/build.py` | 28464 | `20e178a0e80202ef7b252a94434ae04f321ba09fc7039f27eafbf2bab5556f3e` |
| A9 | `proposals/2026-10-15/archivist-v006.md` | 9249 | `d74dd98b533fb5c48bc9a4d733326b977b50270cae78d45eb15ca0bcb2e5f2c8` |
| A9 | `proposals/2026-10-15/emissary-v005.md` | 7149 | `5e77af7382eb2eb4fbb2af2b993a51d8c466860e7d80c85d0881d6dff281c457` |
| A9 | `proposals/2026-10-15/explorer-v002.md` | 9332 | `3a925dc74770882282a4c3a3b08c6c218d95dc0a15a49c3d1f866c77e3405b38` |
| A9 | `proposals/2026-10-15/extractor-v004.md` | 7223 | `a916231ecbb2c1793aaf64e5379745f06e86736c407855335d3936d20ba2bf9f` |
| A9 | `proposals/2026-10-15/imitator-v005.md` | 7888 | `92601dbd8f3a9c99a0b3ec07a83845c772b6a272a181e08e97a4b8419579f780` |
| A9 | `proposals/2026-10-15/inferer-v004.md` | 6678 | `865a6855e46b124dfe2e862af8137e5f8b051f99832afd2f16921baea7efdb8d` |
| A9 | `proposals/2026-10-15/investigator-v003.md` | 5756 | `19dc1bccdc77e57928f1b494456a87aa76071ce6b983618758664db61df3b32d` |
| A9 | `proposals/2026-10-15/message-verification-rule-v002.md` | 7208 | `2e1b06eee1d34af6c9f996d76fc3c82343a639fd842ec09ee9bb42b128abc218` |
| A9 | `proposals/2026-10-15/safeguard-v005.md` | 5027 | `8b8b95bd77d8287ea3de3a318f7975866ff50f16398f9887b7a51dfeb95add92` |
| A9 | `proposals/2026-10-16/README.md` | 29293 | `a1427c252947dc386092b87516f4361c496ffba7f009b207b266ed2c9184cf02` |
| A9 | `proposals/2026-10-16/_tools/build.py` | 32889 | `07d9f3b24f925fd258fd9dd0974ac8b7ad0ca701069df762063e76091bfa98a6` |
| A9 | `proposals/2026-10-16/arbiter-v005.md` | 3894 | `47bcfb1929c77e41ea74ff760aad5cd66c43374be47d74ae5267e70b7038a6f7` |
| A9 | `proposals/2026-10-16/architect-v004.md` | 6374 | `278506086d634e66aa174954bd2e92cd8884b2e138645a92dcc280d71a2d9415` |
| A9 | `proposals/2026-10-16/archivist-v007.md` | 8936 | `5e3dc343bde3de0654e5614dab9921820196c75ed0b165824264a5f606969216` |
| A9 | `proposals/2026-10-16/engineer-v006.md` | 5742 | `6a1b9a6d689e787cb910f641d7f245a82b60333cf5e11d514e338942ccd745c1` |
| A9 | `proposals/2026-10-16/explorer-v003.md` | 8555 | `b27fc4cf9726c584efc338b2c93625da3368c63ead6951a06c528c69d71971a3` |
| A9 | `proposals/2026-10-16/imitator-v006.md` | 5786 | `01775c06964e72195becc2ab27741f37ca8ebad1b3d15816c2cbc6e8dd7d8acd` |
| A9 | `proposals/2026-10-16/inferer-v005.md` | 6922 | `8b0d0c026d7d9d5974449f4312787f87f17a99226ff2cfd3d954ffcac3735ddd` |
| A9 | `proposals/2026-10-16/inquirer-v004.md` | 6112 | `d8ac34989517dc5725c2acc4aba88fefd4d515ae31836781732091a7daff89e9` |
| A9 | `proposals/2026-10-16/mediator-v005.md` | 4964 | `4cfbb334803295398f6c0ea7963866cddc5420736ce8a732e170d13673025c8f` |
| A9 | `proposals/2026-10-16/mender-v005.md` | 7033 | `e52ebf9e88aa1dc8738f2d6217ef44a3e858c8ce477e6eb9d2dc371c8b94d0e5` |
| A9 | `proposals/2026-10-16/message-verification-rule-v003.md` | 4452 | `99969a87b2b661bb5e2337a8bd6c8124f115588b5487d4228ad5ed5e534a8c2c` |
| A9 | `proposals/2026-10-16/safekeeper-v005.md` | 5704 | `395e82216689784d149beee1c95293a743268afb4e7d94ca5b3922803b041813` |
| A9 | `proposals/2026-10-16/scorer-v004.md` | 3630 | `1ba3ef7b9152b341117f4a2fe849cee266486447327f127d5e7701b932c30743` |
| A9 | `proposals/2026-10-16/scrutineer-v004.md` | 4463 | `090cb2a3b6a74f70bbd91ac9067a8f373083acb87b6af896d6dee74b5d27ef74` |
| A9 | `proposals/2026-10-16-rr028/README.md` | 9283 | `1a213bc6b6582127ac09c133a43172a330fa28db6029d3af71ebef89c73e1318` |
| A9 | `proposals/2026-10-16-rr028/_tools/build.py` | 16203 | `a8b4ed461ec99447d5f293b737bbe2f7f58945ddb8bfc3562350e90d15c5171e` |
| A9 | `proposals/2026-10-16-rr028/connector-limits-v001.md` | 3972 | `e812e6970cf02f63f21dee5c7d7f01131fa2c2f459bb22bfb64691c61128ef8a` |
| A9 | `proposals/2026-10-16-rr028/emissary-v006.md` | 7780 | `cc9568126dba2056ea90dc66207898d5006e530290f091dc4c73f1ee2c56302a` |
| A9 | `proposals/2026-10-16-rr028/engineer-v007.md` | 6281 | `4b8e0bbd30e6b189edf895b1bfee8e20e062332415cdb9cd292353daf73b8aa4` |
| A9 | `proposals/2026-10-16-rr028/explorer-v003-rr028.md` | 8802 | `e397f168ec7b2ff7fa4634651f68f9ad8e13ab47d10757e74b5a10bb8033d6e3` |
| A9 | `proposals/2026-10-16-rr028/explorer-v004-combined.md` | 9058 | `3b6bee90fd3d3334b41e1f848bb0f7ec01c3100436c6e24bd3106da161a3d43f` |
| A9 | `proposals/2026-10-16-rr028/extractor-v005.md` | 7825 | `59e7922b297f32cbf639f17f9619e0bdcffc4d673173335f08e07bf1592b7152` |
| A9 | `proposals/2026-10-16-rr028/mediator-v006.md` | 5513 | `2d92ed3b15dda29b4360643801f2b3d7f0d6b50525946b69fdc8c9ee700f5cd6` |
| A9 | `proposals/2026-10-16-rr028/safeguard-v006.md` | 6320 | `b7a6aaf78120a30feef08d32cb4c16938a47ea7107380efaeb96f69f8d74b1dc` |
| A9 | `proposals/2026-10-16-deploy/README.md` | 6805 | `96b44f0ace90acd596328bf22b911553ff2cbfd992aab1029c9a82ba77e115cd` |
| A9 | `proposals/2026-10-16-deploy/_tools/build.py` | 7609 | `3d0c9c26b5471295087d5464fd0ace4c196bc07fe0c1a0c6ee46f5e9828c585d` |
| A9 | `proposals/2026-10-16-deploy/archivist-v008.md` | 11320 | `157b3f4ae181c6484a397d530d47ea92dcc751d33ed0257a2841b80e00925f46` |
| A9 | `proposals/2026-10-16-deploy/explorer-v005.md` | 9104 | `f4f80c03aeea58019fc42db453ba7d2b36575d5e1e0818be78c93ed63d51118a` |
| A9 | `proposals/2026-10-16-deploy/message-verification-rule-v004.md` | 5506 | `8bcacc54856da7435108e547965b9d89ff97e2730257f839a155468ab253f1ed` |
| A9 | `proposals/2026-10-16-investigator/README.md` | 4252 | `8b47599d1547ba8928003b177a69208c6d9767538a566d24bd68d759b1733e92` |
| A9 | `proposals/2026-10-16-investigator/_tools/build.py` | 2664 | `7043434fe2cfb649685956e642ac3c3e4a51c696051142153e62add3575bc522` |
| A9 | `proposals/2026-10-16-investigator/investigator-v004.md` | 4221 | `7c05c1a1b33300ad73687cad86715b8ced13390f353f580bc06732e5db6c4314` |
| A9 | `proposals/2026-10-16-connectors2/README.md` | 26930 | `86a7463772fe3384f768e987a4e901da8f840ecbd71dc61d113def32559cb9ea` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r1.py.bak` | 9279 | `3b990302c111ff393a26d7c2b56ab77fc69775531cbcc7cb7df1c5ef9d077d49` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r2.py.bak` | 9528 | `c9767fcbb7e942ad81def7f82757bf6514529fc206bc753276320eb35ee63b5b` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r3.py.bak` | 15598 | `296acfa2dcdbc48752e9286cceb2f59575efa51057820762025f3079b2ac229d` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r4.py.bak` | 19344 | `fdc54eefce73a47ef6707a068227e27a18541d17bfe6546283dd364678be072a` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r5.py.bak` | 20553 | `c6d7fd66d8654dd4cc1ab9d103f5e1fabb8a8a292c6269b490015b9841a13b53` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build-r6.py.bak` | 22457 | `11fd6558613edeb0d67cfd09d28c9f6d42b6bf4083eefe0deb498130000d2eff` |
| A9 | `proposals/2026-10-16-connectors2/_tools/build.py` | 22547 | `69f261de7db931941e33d78d0551537b471aafa7add9377671cde0c4c68bf403` |
| A9 | `proposals/2026-10-16-connectors2/connector-limits-v002-variant-b.md` | 21627 | `601ab830a8252cf69d22b8f7f1f717f8a2afbad96b5d1934d7589af32ca17b14` |
| A9 | `proposals/2026-10-16-connectors2/connector-limits-v002.md` | 21478 | `f4b6da9c15c3c1e6530bc7ebed0ad422de91f95245eab5cf0d8c6661ba371f36` |
| A9 | `proposals/2026-10-16-connectors2/input-safeguard.md` | 2512 | `841efb15db895cb847a0f10a8f2105f69908873fc5efb6f14af85d0132400541` |
| A9 | `proposals/imitator-approver-2026-10-04/README.md` | 3829 | `8fb89cf29748b96f069ec79a710ad6bb1ede849a3fb9873868344360f2b0b3a2` |
| A9 | `proposals/imitator-approver-2026-10-04/architect-v003.md` | 2493 | `c921bac19916c1829e063917aa7397eda60857380f52b1623e33e412b0571e89` |
| A9 | `proposals/imitator-approver-2026-10-04/archivist-v003.md` | 4046 | `94aab9f06b47e98fb486c7436d4cce2abd53511088c38a3d61fbeee2db595712` |
| A9 | `proposals/imitator-approver-2026-10-04/assembler-v004.md` | 2649 | `18847e0c1f06e52758209cf8d93399e8af36b60e926b5ff6ff801ad83757e67e` |
| A9 | `proposals/imitator-approver-2026-10-04/explorer-v003.md` | 3159 | `33c9fc509c240bf61b9b5c42629be454984ffc802def2d25b52d724303a31dd7` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/README.md` | 5016 | `e0c11bf6f25e9de5aa0b1134c5392cade9cbc6eb7d346c56165ce5fa813f61cc` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-01-self-checking.md` | 4292 | `55e124dd008606d3b5e3fefdba4c118c3c682503ad856050c3cacd109d8cbdb3` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-02-overlaps.md` | 4114 | `ed248e839afabfe4077a36874c5be85527a39264608329305f59f7c2ef0e72a8` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-03-stale-references.md` | 4144 | `07726c78d1c21b0eef087b2e28088d8c335ae34f8d9ebb75d17db8d02f2abd4a` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-04-gaps.md` | 2724 | `1b9eb74ecffbc85c1bd712783bb9eade927579377fe71df33b8088e9d9baca27` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-05-imitator-approval.md` | 1830 | `a686f643b062d0fa9e8f85029d684bf34a66bc59f741699a90af6745667de59a` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/fix-06-not-in-codex.md` | 992 | `4fd11d3030e7f5972112f284a3ec4ad3d9ec89625b685bc2048041e156f99d0c` |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04/roles-pipeline.md` | 5411 | `2e4ca8b6a56097eb03f1eadb5ee61e5f28cff2b2588b1e4479c1448003f3705d` |
| A10 | `proposals/clone-accuracy-validator-v002.md` | 3667 | `4642366b64855d13f3db705dc856abba986f5e8e5d09c7417148eaadabe856a1` |
| A10 | `proposals/comms-concierge-v002.md` | 3146 | `917d4e5617cffeab47907b3c0e61c5cb67e46b3c3722223e6994c1b846894a3e` |
| A10 | `proposals/cost-budget-sentinel-v002.md` | 3660 | `81bfeac04077e0ea9ad5b0b7f130e81adfb8cdf1fe1c790f84cab410e468db1d` |
| A10 | `proposals/genesis-gang-god-v002.md` | 5218 | `1eafa60455c7d71e9f98e5c1424bf05457136ae1238be8c3ee7c2fdda6d787b1` |
| A10 | `proposals/governance-continuity-deputy-v002.md` | 4973 | `3613ffc4be055dc76e06a737f2fa22ee39b8711c730c494f0036a28e49abd1ac` |
| A10 | `proposals/orchestration-conductor-v002.md` | 3908 | `8e410953b9af3635af6292fe2160666c3cb3032ca1d3a09f0fde20c214480eb2` |
| A10 | `proposals/connector-steward-v002.md` | 3447 | `a00efe90e281a467ed8e346cd543abb81716384f5a349451f83578ef79859665` |
| A10 | `proposals/secrets-credentials-custodian-v002.md` | 4324 | `0c05a051e5815ae55c03a7de0742b9d61ff5b6dc79e3d90768f73a76863acd6e` |
| A10 | `proposals/auditor-v002.md` | 1688 | `4c2f76e515b795094c8d4a956d33a492b7ef96f85f684883c1f4f377e82a61eb` |
| A10 | `proposals/compliance-risk-officer-v002.md` | 4619 | `78c15a3a5b60959559f115da6e37c0b4e63bf320198b8863c5e4a4b785b605a7` |
| A10 | `proposals/codex-keeper-v002.md` | 6215 | `76bb6ba2e062c19d4b1a2838ddd38360de4b5c947c08b7ca21256caec5733853` |
| A10 | `proposals/archivist-brief-v002.md` | 7611 | `0068eeb3b9bdb902346903b51eb0967d0893c219c884496ecd8baa0f2aae014f` |
| A10 | `proposals/codey.md` | 6873 | `0f3248e66b833f0f9cb6c4f187c3d0b36ced6a175e074ac862b22b1145bb1b59` |
| A10 | `proposals/grok-bot.md` | 5933 | `2f4de5d6f171c9a997f549bd016b0fc7b3cfe8bcf08929861eeb21dac73d5f76` |
| A10 | `proposals/scraper.md` | 8619 | `2013d166448da7257d96d7a12973b4403958851510e596d6af28ab567bbb0f82` |
| A10 | `proposals/APPROVED-for-archivist-2026-10-04.md` | 7858 | `fe59c0fa03d109d98f52db004be077b982880ec1a44368d4d02a30632555a529` |
| A10 | `proposals/agent-message-verification-rule-v001.md` | 7940 | `cc1031e1973baf828ab9c5a144b9a63fb119ebebe80c4958c666ed22112a3d20` |
| A10 | `proposals/collaboration-map.png` | 206575 | `97c72913fc7d02d71d54d0c01fbb2e50db12e8190bbeee4cc459ba276d5ccb24` |
| A11 | `proposals/2026-10-22-adversarial-response/README.md` | 2683 | `345306588257353c10eb7b96bd25a65a87bcd61bc734cbc1fc70d461f5e5d271` |
| A11 | `proposals/2026-10-22-adversarial-response/arbiter-section.md` | 10839 | `2515b855d8cf17cceaa28144c60454086ffcc0f4a133a4bcc32d0b0d31de6a4b` |
| A11 | `proposals/2026-10-22-adversarial-response/gem-answers-inquirer-2026-10-22.md` | 1302 | `e9fcf138b8b1a55469f6948e803b885be44744fd2efcbc01347cf92def87034c` |
| A11 | `proposals/2026-10-22-adversarial-response/p1a-stage1-token-inventory-safekeeper.md` | 14174 | `ee58a1d67ca36cab736c158d3bf7f27246428b6a2a74bd2e025afc21fa4331e6` |
| A11 | `proposals/2026-10-22-adversarial-response/plan.md` | 19255 | `65afa42285c365865fc35d00de76eebc6767db82c3d5963a395d8883b62c819f` |
| A11 | `proposals/2026-10-22-adversarial-response/plan.md.pre-redesign.bak` | 19712 | `f3de797259e3cc9f5af99218f79a4345e5467d2ae126f93371b21f7093318dc3` |
| A11 | `proposals/2026-10-22-adversarial-response/plan.md.pre-scrap-hc.bak` | 18622 | `2fbba1b4004a47a97b0922bc4d8ddce0024b1d40f4b29d3d8890785d7a14a6ae` |
| A11 | `proposals/2026-10-22-adversarial-response/plan.md.pre832.bak` | 19123 | `5429089613e75190bcdc5a41cb679c4e88e803c215b12b5bd63287b711362d92` |
| A12 | `proposals/2026-10-10-backlog-triage.md` | 15052 | `b310de42059000009c61845d966cd9b9a801349e6152753c4a0f6c239b07aea4` |
| A13 | `codex/PENDING-FOR-ARBITER.md` | 21020 | `ce6866eaa20a0fb4467ed32ce956fa3c999966243f8933e3f32ce4ec6be063fb` |
| A13 | `codex/PENDING-FOR-ASSEMBLER.md` | 3538 | `39c2bab3f0cc39af77a974a09ad51fac2534d6dec12e563bc2d34a5ef51c7c33` |
| A15 | `risk/2026-10-22-liveness-watchdog-plan.md` | 1614 | `63b87b0498c4c524fd02640f0d67c7fc9697141ebaf14bb4e1bbf37c55ecde72` |
| A16 | `risk/2026-10-22-destructive-ops-gate.md` | 3795 | `caed923c8906df31dac0959983224795d1c69c21a6117538d7de4d447f6b388d` |
| A17 | `archive/rulings-2026-10-22-pre-consolidation.md` | 76196 | `d430eb70484f9adfbfe080b786e6645f7ff77700996b1f60eaa1d6d00cbd18ca` |
| A17 | `directory.md.bak-0909` | 3809 | `17832744fc27504601bc52cef9eafebd1df103922df75282da608f43c322ceb5` |
| A17 | `directory.md.bak-1504` | 6696 | `e796169c19d91e5c07048a2ebf414874bde5016ff8f28cb9ef79eab484c95db9` |
| A17 | `schedule.md.bak-20261016` | 8401 | `c174b322a305fdb08c38bf6fa70ad05b686b9a2294c75c3993fffa0d6fd9f719` |
| A17 | `schedule.md.bak-20261016-1107` | 10945 | `dfba099e1eb6a85aec93272c7a452fe3cbc7714c7f3c884e2f74bfa7f1105571` |
| A17 | `schedule.md.bak-20261016-1148` | 11346 | `aa43fbaa141dcd5771d8c12a9380f9d1128908a6c475804852da84ab981fa9f3` |
| A17 | `schedule.md.bak-20261022-1845` | 12042 | `4ddd6239f67c6fd87a4fbb00d65118750fc5c0e8a8a71b6b90aec9c74baa427e` |
| A17 | `risk/register.md.bak-20261016` | 28650 | `10fee846edd3258c35ecceec0dea8bb906aafbb217e14ca8764715603adebe71` |

## Execution and verification (2026-10-22 22:54:49 AEST)

Moves used a plain rename only, never copy-and-delete. The first attempt at `proposals/2026-10-22-redundancy` hit a read-only folder. Python's move then fell back to copy-then-remove, and the remove failed, so nothing was deleted. The original's 18 files are intact, each re-hashed against the table above. A **duplicate copy** of that folder was left at `_archive/cleanup-2026-10-22/proposals/2026-10-22-redundancy/`; it isn't the archived original.

| Item | Path | Result |
|---|---|---|
| A0 | `codex/_shared/handoff-phase1` | moved |
| A1 | `proposals/handoff-phase1-v001.md` | moved |
| A1 | `proposals/phase1-interim-bundle-v001.md` | moved |
| A2 | `schedule.md.bak-p1` | moved |
| A4 | `proposals/2026-10-09-retire-merge` | moved |
| A5 | `proposals/merge-F-unretire-assembler-2026-10-04.md` | moved |
| A6 | `proposals/2026-10-22-redundancy` | SKIPPED: folder is read-only (3 read-only dirs; frozen by its owner), not moved |
| A7 | `proposals/2026-10-22-redesign` | SKIPPED: folder is read-only (7 read-only dirs; frozen by its owner), not moved |
| A8 | `proposals/2026-10-22-r044-veto` | SKIPPED: folder is read-only (7 read-only dirs; frozen by its owner), not moved |
| A8 | `proposals/2026-10-22-gvmw` | SKIPPED: folder is read-only (6 read-only dirs; frozen by its owner), not moved |
| A9 | `proposals/2026-10-05` | moved |
| A9 | `proposals/2026-10-09` | moved |
| A9 | `proposals/2026-10-15` | moved |
| A9 | `proposals/2026-10-16` | moved |
| A9 | `proposals/2026-10-16-rr028` | moved |
| A9 | `proposals/2026-10-16-deploy` | moved |
| A9 | `proposals/2026-10-16-investigator` | moved |
| A9 | `proposals/2026-10-16-connectors2` | moved |
| A9 | `proposals/imitator-approver-2026-10-04` | moved |
| A9 | `proposals/rolemap-v3-fixes-2026-10-04` | moved |
| A10 | `proposals/clone-accuracy-validator-v002.md` | moved |
| A10 | `proposals/comms-concierge-v002.md` | moved |
| A10 | `proposals/cost-budget-sentinel-v002.md` | moved |
| A10 | `proposals/genesis-gang-god-v002.md` | moved |
| A10 | `proposals/governance-continuity-deputy-v002.md` | moved |
| A10 | `proposals/orchestration-conductor-v002.md` | moved |
| A10 | `proposals/connector-steward-v002.md` | moved |
| A10 | `proposals/secrets-credentials-custodian-v002.md` | moved |
| A10 | `proposals/auditor-v002.md` | moved |
| A10 | `proposals/compliance-risk-officer-v002.md` | moved |
| A10 | `proposals/codex-keeper-v002.md` | moved |
| A10 | `proposals/archivist-brief-v002.md` | moved |
| A10 | `proposals/codey.md` | moved |
| A10 | `proposals/grok-bot.md` | moved |
| A10 | `proposals/scraper.md` | moved |
| A10 | `proposals/APPROVED-for-archivist-2026-10-04.md` | moved |
| A10 | `proposals/agent-message-verification-rule-v001.md` | moved |
| A10 | `proposals/collaboration-map.png` | moved |
| A11 | `proposals/2026-10-22-adversarial-response` | moved |
| A12 | `proposals/2026-10-10-backlog-triage.md` | moved |
| A13 | `codex/PENDING-FOR-ARBITER.md` | moved |
| A13 | `codex/PENDING-FOR-ASSEMBLER.md` | moved |
| A15 | `risk/2026-10-22-liveness-watchdog-plan.md` | moved |
| A16 | `risk/2026-10-22-destructive-ops-gate.md` | moved |
| A17 | `archive/rulings-2026-10-22-pre-consolidation.md` | moved |
| A17 | `directory.md.bak-0909` | moved |
| A17 | `directory.md.bak-1504` | moved |
| A17 | `schedule.md.bak-20261016` | moved |
| A17 | `schedule.md.bak-20261016-1107` | moved |
| A17 | `schedule.md.bak-20261016-1148` | moved |
| A17 | `schedule.md.bak-20261022-1845` | moved |
| A17 | `risk/register.md.bak-20261016` | moved |

Verified at the new location: 139 files, 1452898 bytes, hash mismatches or missing: 0.
