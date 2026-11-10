# Megascans — ponaučenia z Wooden Pallet VISUAL FIX01

**Reviewed:** 2026-11-10 · **Evidence:** historical, bounded physical-device pilot · **Scope:** reusable documentation only.

## Čo sa stalo a prečo je to dôležité

Wooden Pallet (Quixel Megascans, [Fab listing](https://www.fab.com/listings/6622c5d8-691b-4f1b-a29c-80c0e9d54af8?lang=en)) bol získaný po osobitnom OWNER súhlase pod Fab Standard License. Pôvodný RAW má 1 000 000 tris. Prvý GAME s 3 000 tris prešiel technickým iPhone QA, ale OWNER odmietol jeho plastový lesk, mäkké hrany a slabú kresbu dreva. FIX01 pripravil tri samostatné deriváty 3K/10K/20K. Po vizuálnom porovnaní a fyzickom QA OWNER schválil presný nový 3K variant s matným PBR materiálom; ostatné varianty aj odmietnutý kandidát zostali zachované.

Najväčší prínos v tomto prípade bol materiál a normály, nie vyšší počet tris. **Technické PASS nie je vizuálne PASS a ani uzavretý izolovaný pilot nie je povolenie na použitie v hre.** Nepoužívaj tento príklad ako univerzálny polygon budget, predvolenú licenciu alebo automatický súhlas s downloadom.

## Evidencia a hranice reprodukcie

Owner-side záznamy zostávajú mimo verejnej knižnice. Nasledujúce identifikátory umožňujú autorizovanému reviewerovi overiť presnú revíziu; verejný čitateľ nemá zaručený prístup k súborom. Nezverejňujeme originály, samostatné deriváty, textúry, rendery, podpisové údaje, device ID ani súkromné logy.

| Evidencia | SHA-256 |
| --- | --- |
| RAW MASTER ZIP | `9eacb786d5fab8a806e6ee3a7ec84a4d96049116938379516899361a65f99e67` |
| Schválený FIX01 3K FBX | `d0800f4e04799d564b0d459db256c03f1a553da1987bffe60ca13024341f512b` |
| FIX01-RESULT.json | `ef713b311544b0f364763c26ac04ae817512ac347237fe8d6600fc793e479526` |
| OWNER-APPROVAL.json | `fa2d108ebd62c5e6e169748b53708f6fefad99763cf358320291416b9d73e96b` |

Pri uzavretí bolo preverených 153 záznamov SHA-256 (10 pôvodných, 20 iPhone evidence, 35 pôvodný build, 88 FIX01). OWNER záznam viaže 19 súborov vrátane materiálu a import metadata; iba FBX hash by nestačil. Status: CLOSED_OWNER_APPROVED_ISOLATED_PILOT; production_integration: NOT_AUTHORIZED. Manifest pred schválením zostáva historickou evidenciou, nový approval je aditívny.

## Reusable workflow — pred každým ďalším pilotom

1. **License gate:** postupuj podľa [Quixel source guide](QUIXEL-MEGASCANS.md) a [license policy](LICENSE_POLICY.md). Over presný listing, cenu, entitlement, komerčné práva, formát a samostatné povolenie akvizície. Ulož ledger a SHA-256 nemenného MASTER na autorizovanom úložisku. Každý FIX vytvor v samostatnej revízii, nič neprepisuj.
2. **Geometry gate:** importuj v správnej mierke a orientácii; spočítaj skutočné tris, over topológiu, UV švy, otvory a siluetu. Decimate je kandidát, nie automatický PASS. Pri tvrdých plochách označ ostré hrany podľa skutočnej konštrukcie (FIX01 skúšal 35°), použij weighted normals s Keep Sharp a over export/import normál a tangentov. Skontroluj UV presah, deformáciu, normálové švy a tangent-space kompatibilitu; podľa potreby retopológia alebo bake z MASTER. Jedna zachovaná UV vrstva sama nedokazuje bezchybný unwrap. Porovnaj viac rozumných budgetov, nie vždy 3K/10K/20K.
3. **Material gate:** použi originálny BaseColor v sRGB, dátové mapy Normal/Roughness/Metallic/AO lineárne, Normal ako normal map s korektnou orientáciou a tangentmi. Pri neznámej konvencii normal map over smer na osvetlenom teste, neinvertuj kanál naslepo. Pre drevo metallic=0; ak shader očakáva smoothness, prevod z lineárnej roughness je 1 - roughness, uložený do kanála predpísaného shaderom. FIX01 použil floor roughness 0.72, normal strength 0.65, samostatnú AO mapu a Unity occlusion strength 0.7; ide o prípadové hodnoty, nie univerzálny preset. Nezvyšuj AO tak, aby sa zdvojnásobili už zachytené tiene. V Blender porovnaní bola AO primiešaná do base color len pre render; v Unity samostatná occlusion mapa. Rozdiely shaderov a color managementu zaznamenaj. Over mapovanie kanálov, lineárny color space, mipmapy a runtime kompresiu; pri inom render pipeline nastav jeho vlastné material sloty.
4. **Visual gate:** porovnaj MASTER a GAME pri identickej kamere, mierke, osvetlení, expozícii, pozadí, rozlíšení a rovnakom materiálovom protokole. Ulož referenciu aj detail hrán, siluety, otvorov, UV švov a povrchov z viacerých uhlov; porovnaj reprezentatívnu hernú vzdialenosť. FIX01 Blender porovnanie používalo spoločné 2K mapy aj na MASTER, teda izolovalo geometriu/normály, nie plnú kvalitu 8K originálu. Na iPhone boli tri deriváty v rovnakej Unity scéne; Blender a Unity nemali identické osvetlenie navzájom. Nezamieňaj marketingový render za kontrolovaný baseline. Pred rozhodnutím skontroluj reálne engine/device screenshoty.
5. **Physical-device gate:** vytvor izolovanú podpísanú QA aplikáciu s jedinečným bundle ID a bez zmeny hry. Over skutočné tris po importe a runtime formát každej textúry; ASTC 6×6 môže byť vhodný, ale over vizuálne artefakty, mipmapy a podporu najstaršieho cieľa. Meraj FPS, frame times, pamäť, build size a vizuál na fyzickom zariadení. Použi aj samostatný unloaded baseline, CPU/GPU profiler a dlhší tepelný test pre produkčnú bránu; renderer-off alebo deaktivácia objektu nie je uvoľnenie všetkých jeho zdrojov.
6. **Benchmark integrity:** zaznamenaj model/build identitu, zariadenie, OS, GPU, rozlíšenie, FPS cap, warmup, počet snímok, jednotlivé frame times, priemer, P95/P99 a maximum; opíš percentilovú metódu. Pri pause/background, strate focusu, suspend/resume či inej interferencii označ dotknutý beh INVALID/INTERRUPTED, uchovaj pôvodné dáta, zopakuj celý porovnávací beh v popredí a over počet vzoriek a absenciu neplatných intervalov. Nevylučuj outliery potichu. FIX01 prvý 10K/60 test obsahoval suspend gap (3.48 FPS priemer); čistý rerun tento údaj nahradil ako akceptačný, nie prepísaním histórie. Pri ďalších benchmarkoch zaznamenávaj aj lifecycle events a časové značky.
7. **Storage and tools gate:** dodrž [AGENTS.md](../../AGENTS.md), povinný wrapper, exclusive heavy lock, disk guard/UUID, free-space receipt, izolované externé run roots a cleanup po každom výsledku. Na macOS over reálny Editor root, Hub metadata, dostupný modul a BuildPipeline.IsBuildTargetSupported. V tomto konkrétnom Unity 6000.3.25f1 externom install bol iOSSupport v `<editor-version>/PlaybackEngines/iOSSupport` vedľa `Unity.app`, nie iba pod `Unity.app/Contents/PlaybackEngines`. Nie je to univerzálna cesta pre každý install. Modul už existoval, fungoval a nebol preinštalovaný. Over podpis/obsah/cieľ balíka pred akoukoľvek autorizovanou inštaláciou; štandardný installer môže cieliť inú cestu. Pri Unix socket limite IL2CPP skráť jedinečný externý job label/root, nepresúvaj cache na interný disk a neobchádzaj wrapper. Veľké cache/buildy externe, systémové metadata podľa OWNER rozsahu; netvrď nulový interný zápis bez dôkazu.
8. **OWNER gate:** autorizovaná publikácia iba v existujúcom Asset Viewer workflow; predlož presnú revíziu a porovnania, označ PASS/FIX/HOLD. Pri odmietnutí zachovaj kandidáta a začni samostatný FIX. Zaznamenaj rozhodnutie aditívne s hashmi geometrie, materiálu, textúr, import nastavení a dôkazov. Pre hernú integráciu vyžaduj samostatné GO a game-specific QA/OWNER REVIEW; release je ďalšia samostatná brána.

## Nameraný výsledok FIX01 (historický, nie nový test)

Blender 5.2.1, Unity 6000.3.25f1, Xcode 27.1 RC, fyzický iPhone 16 Pro Max (iOS 27.2, A18 Pro, 2868 × 1320). 60 warmup + 240 meraných snímok na scenár, 6 scenárov, 1440 individuálnych frame times v čistom behu.

| GAME tris | FPS cap 60 | P95 ms | FPS cap 120 | P95 ms |
| --- | --- | --- | --- | --- |
| 3000 | 59.99 | 16.748 | 119.99 | 8.383 |
| 10000 | 59.99 | 16.723 | 119.99 | 8.381 |
| 20000 | 59.99 | 16.707 | 119.99 | 8.387 |

Štyri runtime mapy (BaseColor, Normal, AO, Smoothness) mali každá 2048², ASTC 6×6, 12 mipmap úrovní a 2 498 160 B podľa Unity. Peak Unity allocated približne 42.5–42.6 MB; spoločný development build 62 124 709 B. Všetky tri modely boli v jednej aplikácii, preto údaje nie sú samostatná pamäťová cena variantu, OS physical footprint ani maximálny GPU výkon. FPS bolo limitované. Žiadny dôkaz o tepelnom soak, staršom iPhone, produkčnej scéne, kolíziách či výkone celej hry. 3K vyhral vizuálne/rozpočtovým kompromisom pri testovanej kamere; 10K zostal alternatívou pre close-up, 20K nemal preukázaný prínos v tomto pohľade.

## Primary sources and authority

- [Blender Weighted Normal modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/normals/weighted_normal.html).
- [Unity iOS environment setup](https://docs.unity3d.com/6000.0/Documentation/Manual/ios-environment-setup.html).
- [Unity texture import settings](https://docs.unity3d.com/6000.0/Documentation/Manual/texture-type-default.html) a [texture formats in memory](https://docs.unity3d.com/6000.0/Documentation/Manual/texture-compression-formats.html).
- [Fab Standard License](https://www.fab.com/eula); zdrojová registrácia [Quixel guide](QUIXEL-MEGASCANS.md).

Tieto zdroje vysvetľujú nástroje a licenciu; konkrétne výsledky a externý layout vyššie sú owner-side pilot evidence. Dokument je iba poznatok, nie vykonávací príkaz, entitlement ani autorizácia ďalších assetov, inštalácií, uploadu, importu, merge alebo release.
