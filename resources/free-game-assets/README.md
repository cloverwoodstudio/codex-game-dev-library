# Cloverwood Free Game Assets & Tools

**Reviewed:** 2026-10-10 · **Owner:** Cloverwood Studio · **Scope:** commercial iPhone games, Blender/Godot workflows, 2D games.

Vyhľadateľná knižnica bezplatných **zdrojov**, nie úložisko cudzích súborov. Je súčasťou [Codex Game Development Library](../../README.md) a môže ju čítať ChatGPT, Codex aj ďalší autorizovaní agenti.

## Začni tu

- [Katalóg (odkazy overiteľné v CI; blokované weby označené manuálne)](INDEX.md) — všetky odkazy rozdelené podľa kategórie.
- [JSON katalóg](catalog.json) — strojové vyhľadávanie, výber pre projekt a agentov.
- [Licenčné pravidlá pre App Store](LICENSE_POLICY.md) — povolené, podmienené a zakázané zdroje.
- [Výber pre naše hry](PROJECT_RECIPES.md) — BB, Hotel Panic, Starfall Rescue, Split, Neluvo a PAUSEPORT.
- [Karta pôvodu stiahnutého assetu](DOWNLOAD_LEDGER.template.csv) — pred použitím v hre.
- [Ako rozširovať katalóg](CONTRIBUTING.md).

## Kategórie

3D modely a celé sady; postavy a animácie; PBR textúry a HDRI; zvukové efekty; hudba; 2D/UI; VFX/shadery; výrobné nástroje; všeobecné trhoviská.

### Komerčná bezpečnosť

| `commercial_game_use` | Význam | Rozhodnutie |
| --- | --- | --- |
| `yes` | Primárny zdroj povoľuje použitie v komerčnej hre za uvedených podmienok. | Vždy prečítať podmienky konkrétneho stiahnutia, uchovať dôkaz. |
| `verify-item` | Portál ponúka rôzne licencie alebo je potrebné preveriť konkrétny balík. | **Bez schválenia nepoužívať v hre.** |
| `no` | Použitie v komerčnej videohre nie je povolené. | **Nepoužívať.** |

Pri `commercial_game_use: yes` nejde o univerzálne povolenie na ľubovoľný súbor z danej stránky. Katalóg je len predbežná klasifikácia. `verify-item` znamená, že výber je **zablokovaný pre produkčnú integráciu**, kým agent nezdokumentuje konkrétny súbor, licenciu a schválenie.

`free-tier` znamená, že **iba bezplatná časť** katalógu je dostupná bez zaplatenia. Plné balíky, editovateľné .blend zdroje a rozšírenia bývajú platené.

**Dôležité:** Mixkit **sound effects** povoľuje vo videohrách, ale Mixkit **stock music** ich výslovne zakazuje. Quaternius QAL zakazuje samostatné šírenie modelov ako asset balíkov. Pri starších packoch skontroluj priloženú licenciu.

## Použitie agentom / Codex

1. Otvor `resources/free-game-assets/catalog.json`.
2. Filtruj podľa `category`, `projects` a `commercial_game_use`.
3. Over licenciu **konkrétneho** modelu/zvuku/skladby vrátane aktuálneho znenia.
4. Pred stiahnutím a zaradením vyplň `DOWNLOAD_LEDGER.template.csv` vo vlastnom projekte.
5. Vyrob samostatný optimizovaný GAME derivát, otestuj GLB, animácie, fyziku a pamäťové nároky.
6. Vykonaj OWNER REVIEW v Game Lab Vieweri; technické PASS **nie je** schválenie do hry.
7. Nenahrávaj originálne stiahnuté súbory do tejto knižnice a nepridávaj ich do hry bez povolenia.

Príklad filtrácie:

```sh
python3 - <<'PY'
import json
d = json.load(open('resources/free-game-assets/catalog.json'))
for r in d['resources']:
    if 'BB' in r['projects'] and r['commercial_game_use'] == 'yes':
        print(f"{r['category']:20s} {r['name']}: {r['url']}")
PY
```

Validácia katalógu a synchronizácie indexu:

```sh
python3 scripts/check_free_game_assets.py --check
```

Na autorizovanom Macu spusti testy cez `bash scripts/cloverwood-local-run.sh -- ...` podľa koreňového `AGENTS.md`.

## Hranice

Žiadne automatické sťahovanie, import do hier, platený nákup, použitie API, licenčné udelenie, merge, release ani nasadenie nie je týmto katalógom autorizované. **Všetky výsledné hry majú vlastnú autoritu.** Katalóg je kurátorovaný prehľad zdrojov, nie záruka, že každá položka zostane bezplatná navždy.

Písaný obsah tejto knižnice spadá pod [licenciu repozitára](../../LICENSE); **odkazované assety majú vlastné licencie**.
