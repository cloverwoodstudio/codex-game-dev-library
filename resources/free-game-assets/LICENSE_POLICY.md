# Komerčné licencie — pravidlá pre Cloverwood

**Reviewed:** 2026-10-09. Praktický interný checklist, nie právne stanovisko.

## Pred každým použitím

1. Otvor **oficiálnu stránku konkrétneho balíka alebo súboru** a jeho aktuálnu licenciu (`license_url`).
2. Skontroluj: komerčná hra, mobilné distribúcie/App Store, právo na úpravu, zákaz opätovnej distribúcie surového assetu, prípadný kredit.
3. Poznamenaj verziu, autora, dátum stiahnutia a originálny ZIP / SHA-256 do [DOWNLOAD_LEDGER.template.csv](DOWNLOAD_LEDGER.template.csv).
4. Ak licenciu nevieš overiť, označ `BLOCKED_LICENSE_REVIEW`; nič neimportuj do hry.
5. Pri finalizácii hry priprav obrazovku Credits a zoznam povinných licencií/súhlasov.

| Druh licencie | Komerčné použitie | Čo strážiť |
| --- | --- | --- |
| CC0 | Typicky áno | Overenie, že asset je skutočne CC0 a zdroj neobsahuje ďalšie chránené časti. |
| CC BY | Áno | Pôvodný autor, názov, odkaz na licenciu a zmeny. |
| CC BY-SA | Podmienene | ShareAlike podmienky pre úpravy; pred distribúciou osobitná kontrola. |
| CC BY-NC / NC varianty | **Nie** pre naše platené hry | Bez osobitnej licencie od držiteľa práv nepoužiť. |
| GPL / open-source plugin | Podmienene | Povinnosti licencie na šírený kód; závisí od integrácie a balíka. |
| QAL v1.0 (Quaternius) | Áno | Povolené zabudovanie do hry, zakázaná samostatná redistribúcia assetov. |
| Adobe Mixamo | Áno | Pre humanoidné postavy, bezplatný Adobe ID, distribúcia postáv/animácií v hre. |
| Sonniss #GameAudioGDC v2.0 | Áno | Použitie v médiách/hrách; **nie na AI/ML tréning**, nerehostovať ako zdrojovú knižnicu. |
| Mixkit Sound Effects Free | Áno | Hra môže obsahovať efekty; **nesmie ich distribuovať ako samostatný stock**. |
| Mixkit Stock Music Free | **Nie vo videohrách** | Licencia výslovne uvádza Video Games ako zakázané. |

## Priame primárne licencie

- Kenney: https://kenney.nl/support
- KayKit (pozri stiahnutý pack): https://kaylousberg.itch.io/kaykit
- Quaternius QAL: https://quaternius.com/license.html
- Adobe Mixamo: https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
- Poly Haven: https://polyhaven.com/license
- Freesound: https://freesound.org/help/faq/
- Sonniss: https://sonniss.com/gdc-bundle-license/
- Mixkit SFX: https://mixkit.co/license/modal/sfxFree/
- Mixkit Music **zakázané pre hry**: https://mixkit.co/license/modal/musicFree/
- Incompetech: https://web.incompetech.com/music/royalty-free/licenses/
- Soundimage: https://soundimage.org/attribution-info/
- Godot Shaders (každý shader osobitne): https://godotshaders.com/license/
- Game-icons.net: https://game-icons.net/about.html

## Trh so zmiešanými licenciami

Freesound, OpenGameArt, Poly Pizza, itch.io, Godot Asset Library a jednotlivé shader portály nepovažujeme za univerzálne komerčne schválené. **Schválenie poskytovateľa nie je schválením každého jeho súboru.**

## Nezamieňaj licenciu nástroja s licenciou výstupu

Blender, Godot, Krita, Audacity a LMMS sú výrobné nástroje. Licencia aplikácie **automaticky neurčuje** licenciu každej práce v nej vyrobenej; externé sample balíky, fonty, pluginy a assety si uchovávajú vlastné podmienky.

## Politika repozitára

Tento repozitár obsahuje **iba odkazy, zhrnutia a metadata**. Žiadny ZIP, FBX, GLB, WAV, MP3, PNG ani celá cudzia sada sa sem nevkladá bez samostatne overených práv a rozhodnutia vlastníka. CC BY licencia dokumentácie repozitára neprepisuje licencie tretích strán.
