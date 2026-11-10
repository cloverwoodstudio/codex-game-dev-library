# Quixel Megascans na Fab — zdroj a mobilný workflow

**Reviewed:** 2026-11-10 · **Status:** verify-item / REVIEW HOLD · **Scope:** zdrojové odkazy, bez akvizície alebo importu.

## Oficiálne zdroje a dostupnosť

- [Quixel Megascans na Fab](https://www.fab.com/sellers/Quixel%20Megascans?lang=en) — fotogrametrické statické modely, PBR povrchy a decals.
- [Oznámenie Quixel z 2026-11-05](https://quixel.com/news/update-megascans-are-going-free-again) — prechod celej knižnice na bezplatný prístup; oznámené aj rozšírenie práv na AI tréning.
- [Fab Standard License](https://www.fab.com/eula) — súhrn a záväzné podmienky; konkrétne oprávnenie overiť pri akvizícii.
- [Akvizícia a staršie licencie](https://dev.epicgames.com/documentation/en-us/fab/purchasing-and-downloading-assets-in-fab).
- [Export z Fab v Launcheri](https://dev.epicgames.com/documentation/fab/exporting-assets-from-fab-in-launcher) — formáty, podporované verzie a pluginy.

K 2026-11-10 je prechod cien oznámený; verejná stránka predajcu sama nedokazuje nulovú cenu každého listingu. Preto je katalóg dočasne `free-tier`, nie blanket free. Pred výberom skontrolovať presnú položku, cenu, licenciu a dostupnosť zdrojových súborov. Fab v Launcheri vyžaduje Epic účet aj pre bezplatný obsah; žiadne prihlasovanie, Add to Library, prijatie podmienok, nákup ani download nie je autorizované touto dokumentáciou.

## Licencia a evidencia

Fab Standard typicky povoľuje komerčné hry, úpravy, distribúciu integrovaného obsahu a kompatibilné nástroje mimo Unreal. Samostatná redistribúcia alebo predaj assetu je zakázaný. Zdieľanie s projektovými spolupracovníkmi podlieha podmienkam; verejný GitHub nesmie mirrorovať modely, textúry ani samostatne použiteľné deriváty. Standard spravidla nevyžaduje kredit, ale staršie alebo iné podmienky over osobitne. Staršie Bridge/Quixel entitlementy posudzuj podľa podmienok, za ktorých vznikli; nepredpokladaj automatické práva mimo Unreal. Štúdiové zmluvy majú vlastné podmienky. Megaplants a Unreal-native balíky nie sú automaticky Unity zdrojmi.

Pred osobitne autorizovanou akvizíciou zaznamenaj listing URL/ID, autora, verziu, cenu, typ licencie, práva na komerčnú iOS hru a úpravy, kredit, redistribúciu a dostupné formáty. Zachovaj dôkaz o akvizícii a účinných podmienkach; po stiahnutí vypočítaj SHA-256 skutočných pôvodných bajtov a zaznamenaj lokálnu cestu, dátum a verziu podľa [DOWNLOAD_LEDGER.template.csv](DOWNLOAD_LEDGER.template.csv). Nejasné práva = BLOCKED_LICENSE_REVIEW. Registrácia nie je právne stanovisko. Oznámené AI práva nie sú autorizáciou tréningu; vyžadujú samostatnú kontrolu účinných podmienok a súhlas.

## Výber pre hry (iba návrhy)

| Projekt | Potenciálne použitie | Podmienka |
| --- | --- | --- |
| Country Road | Asfalt, štrk, zem, skaly, les, rekvizity zastávok | Nenarušiť jazdu, kolízie ani čitateľnosť trasy. |
| BLACKOUT | Betón, hrdza, potrubia, sutiny, industriálne povrchy | Zachovať art direction, čitateľnosť a výkon. |
| HOTEL PANIC | Drevo, dlažba, steny, dekoratívne rekvizity | Zhodný vizuálny štýl a herné mierky. |

Country Road a BLACKOUT nie sú aktuálne ID v schéme katalógu; `GENERAL` umožňuje discovery bez zmeny schémy.

## Mobilný Unity / Blender workflow — budúci pilot

1. Zvoliť jeden konkrétny bezplatný listing podľa art direction, mierky a výkonového rozpočtu; overiť licenčnú bránu a získať osobitný súhlas s downloadom.
2. Na schválenom externom úložisku zachovať originálny archív nemenný (MASTER), SHA-256 a ledger. Fab v Launcheri podporuje výber download priečinka; nesťahovať na interný disk ani neinštalovať plugin bez samostatného súhlasu. Ak export nevie garantovať schválené úložisko, zastaviť.
3. Zvoliť dostupný FBX (Epic ho odporúča pre Megascans v Unity a DCC) alebo glTF/GLB podľa listingu a verzie nástroja. Unreal-only súbory nie sú priamy Unity/Blender zdroj. Oficiálny export podporuje macOS, Unity 2022/2023/6+ a Blender 3.6/4 podľa dokumentácie; overiť reálne nainštalované verzie.
4. Blender: samostatný GAME derivát; overiť jednotky, orientáciu, pivot, normály, UV a materiály. Znížiť zložitosť geometrie, odstrániť zbytočné plochy, vytvoriť LOD podľa vzdialenosti, prípadne bake normal/AO z MASTER. Použiť jednoduché samostatné collidery. Originál neprepísať.
5. Unity: import FBX alebo overený glTF/GLB pipeline do izolovanej QA scény; nastaviť PBR pre existujúci render pipeline (napr. URP). Overiť sRGB pre base color, lineárne normal/roughness/metallic/AO mapy, roughness/smoothness a kanály. Mipmapy, instancing podľa potreby, ASTC pre iOS; začať 1K–2K textúrami (malé dekorácie 512–1K), nie 8K/Nanite. Limity určí meranie.
6. QA: porovnať MASTER/GAME vizuál, tris, textúry, draw calls, GPU/CPU frame time, FPS, peak memory, veľkosť buildu, kolízie, loading a tepelnú stabilitu na cieľovom fyzickom iPhone; zachovať baseline a výsledok. Na Macu použiť povinný repo wrapper, izolované výstupy, cleanup receipt a heavy-job lock podľa AGENTS.md. Žiadne tvrdenie PASS bez merania.
7. Publikovať iba autorizovanú projektovú QA evidenciu v existujúcom Asset Viewer owner workflow; OWNER REVIEW presnej revízie pred samostatne schválenou integráciou. Technické PASS nie je owner schválenie ani povolenie na release.

## Hranice

Dokument registruje zdroj, nie assety. Žiadne binárne súbory, automatické sťahovanie, API, prijatie podmienok, nákupy, AI tréning, inštalácie, game import, merge, nasadenie ani release. Pilot vyžaduje samostatnú autorizáciu. Pozri [licenčnú politiku](LICENSE_POLICY.md) a [pravidlá katalógu](CONTRIBUTING.md).
