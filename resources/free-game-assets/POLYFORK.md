# Polyfork — low-poly 3D modely, tematické kity a agent API

**Reviewed:** 2026-11-09 · **Katalógový status:** `commercial_game_use: yes` iba pre bezplatné low-poly **mesh súbory**, pri podmienkach konkrétnej licenčnej vetvy; **nie** automatický produkčný import.

## Primárne zdroje

- Modely a kity: https://polyfork.dev/
- **Oficiálna licencia**: https://polyfork.dev/licensing
- Návod pre agentov / MCP: https://polyfork.dev/agents
- Samopopisné REST API: https://polyfork.dev/api
- Aktuálny pracovný prompt: https://polyfork.dev/prompt.txt
- MCP endpoint: `https://polyfork.dev/mcp` (HTTP; na prehliadanie katalógu bez kľúča)

## Čo je bezplatné

Poskytovateľ od 25. 10. 2026 deklaruje všetky **low-poly** modely a tematické kity ako bezplatné. Bez účtu sú dostupné bežné mesh exporty (napr. GLB, FBX, OBJ; na stránke uvádzajú aj USD). Zdrojové parametrické programy `.mjs` a balené kity môžu potrebovať bezplatný účet; detail účtu alebo limity treba pri potrebe znova overiť. **HD/PBR verzie sú platené.** Počet modelov sa mení, preto ho nezamykáme do katalógu.

Modely sú určené pre Three.js, Blender, Godot, Unity a iné nástroje podporujúce príslušné formáty. Kompatibilita konkrétneho skeletonu, animácií, materiálov a výkon na iPhone/iPade **nie sú testom tejto evidencie potvrdené**.

## Licenčné rozdelenie — nezamieňať

| Typ súborov | Právny režim | Čo smieme |
| --- | --- | --- |
| **Bezplatné low-poly mesh** (`.glb`, `.fbx`, `.obj`, `.usd`), baked varianty a kit scény | **CC BY 4.0** *alebo* vlastná licencia Polyfork, podľa našej voľby | CC BY: komerčná hra, úpravy aj redistribúcia samostatného mesh s uvedením Polyfork, odkazom a uvedením zmien. Polyfork licencia: komerčná hra bez kreditu, ale **nie** samostatná redistribúcia súborov. |
| Parametrické zdrojové súbory `.mjs` | **Vlastná licencia Polyfork** | Použitie vo vlastnom projekte je dovolené; samostatné šírenie, mirror alebo predaj zdrojových programov **nie**. |
| HD/PBR verzie, oficiálne náhľady, render obrázky, katalógový text | **Vlastná licencia Polyfork** a obmedzenia konkrétnej služby | Nepovažovať za CC BY, nekopírovať do verejnej knižnice. HD vyžaduje platený prístup. |

**Pre knižnicu Cloverwood:** evidujeme iba odkazy + vlastnú stručnú dokumentáciu. Tento zápis **nesťahuje ani nemirroruje** cudzie 3D modely. Pri výbere konkrétneho modelu uchovať URL, verziu/dátum, SHA-256 mesh súboru a zvolenú licenčnú vetvu. Pri CC BY 4.0 zachovať napr. `Model by Polyfork (URL na konkrétny model), CC BY 4.0; modified: [zmeny]` a preveriť presnú kreditnú vetu na stránke modelu.

Dôležitá výnimka: Polyfork vlastná licencia obmedzuje komerčné generátory 3D assetov trénované alebo postavené na týchto podkladoch. Všetky použitia na trénovanie/benchmarking oddeľte od bežného model importu; stránka výslovne upozorňuje, že obmedzenie **neprenáša** na súbory použité pod CC BY 4.0.

## AI agenti: bezpečný discovery workflow

1. Pred prácou prečítať aktuálnu dokumentáciu `https://polyfork.dev/agents` alebo `https://polyfork.dev/prompt.txt`. Nie je to automatická inštalácia nástroja.
2. Vyhľadávať metadáta podľa témy a limitu trianglov (napr. `GET https://polyfork.dev/api/assets?q=windmill&free=1&max_triangles=2000`); následne použiť detail `GET /api/assets/{id}`, nájsť kompatibilné kity a údaje o rozmeroch, origin, materiáloch, rigoch a klipoch.
3. Zvoliť konkrétne modely ručne alebo agentovým návrhom a stiahnuť **iba modely potrebné pre projekt**, nie celý katalóg. Pri použití API/hotlinkingu uviesť User-Agent identifikujúci produkt, rešpektovať `429` s backoff a odkazy CDN ponechať nezmenené.
4. Import `.glb` do Blender/Godot, resp. `.fbx` podľa Unity nástroja; pre každý model overiť materiály, osy, pivoty, typ fyziky, animácie, rozpočet trianglov/draw call a výkon na cieľovom zariadení.
5. Zaznamenať výsledok do projektového asset ledgeru. OWNER REVIEW a game-specific QA sú osobitné brány; samotný odkaz, CC BY alebo bezplatná cena **nie sú** schválením do App Store.

**MCP pre vlastnú autorizovanú integráciu:** `https://polyfork.dev/mcp` (prehliadanie bez API kľúča). Pripojenie servera do Codex/Claude vyžaduje samostatný vedomý krok používateľa/administrátora. Kľúče sú tajné — vždy v prostredí alebo bezpečnom úložisku, nikdy v Git histórii, dokumentácii ani logoch.

## Potenciálne využitie v našich hrách

- **HOTEL PANIC:** nábytok, vybavenie interiéru, postavy (najskôr preveriť skeletony, animačné klipy a štýl).
- **STARFALL RESCUE:** vesmírne rekvizity, moduly a roboty (iba ak sú v súlade s existujúcou hrou).
- **BLOCK BOUNCER:** prototypy technických propov; záväzný kartónový výtvarný štýl sa nesmie rozbiť.
- **Nové 3D projekty:** tematické kity s kompatibilnou paletou a reálnou mierkou, hlavne Godot/Unity.

**Neurobené:** žiadny download modelu, test GLB/FBX, Blender import, agent MCP inštalácia, UAT ani import do herného repa.

**Vždy si over aktuálne podmienky na** https://polyfork.dev/licensing **pred samotným použitím.**
