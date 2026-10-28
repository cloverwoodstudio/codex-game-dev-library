# Komerčné licencie — pravidlá pre Cloverwood

**Reviewed:** 2026-10-09. Praktický interný checklist, nie právne stanovisko.

## Pred každým použitím

1. Otvor **oficiálnu stránku konkrétneho balíka alebo súboru** a jeho aktuálnu licenciu (`license_url`). Ak `license_url` odkazuje len na profil alebo titulnú stránku, nejde o dostatočný dôkaz; zisti osobitné podmienky balíka.
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
- Incompetech: https://incompetech.com/music/royalty-free/licenses/
- Soundimage: https://soundimage.org/attribution-info/
- Godot Shaders (každý shader osobitne): `godotshaders.com/license/` (manuálne; poskytovateľ pri automatickom overovaní vracia HTTP 455)
- Game-icons.net: https://game-icons.net/about.html

## REVIEW HOLD — bez preukázania práv nepoužiť

Aktuálny katalóg úmyselne označuje `texturecan`, `material-maker`, `jfxr` a `bosca-ceoil-blue` ako `verify-item`: prvé vydanie uvádzalo všeobecné/licenčne nešpecifické URL, ktoré ešte nie sú dôkazom práv ku konkrétnemu assetu alebo vzorkám. Záznam môže zostať ako užitočný odkaz na nástroj či materiály, ale žiadny agent z neho nesmie odvodiť hotový komerčne schválený asset.

## Trh so zmiešanými licenciami

Freesound, OpenGameArt, Poly Pizza, itch.io, Godot Asset Library a jednotlivé shader portály nepovažujeme za univerzálne komerčne schválené. **Schválenie poskytovateľa nie je schválením každého jeho súboru.**

## Hi3D v1.0 — vlastná licencia, nie MIT alebo Apache

Oficiálny zdroj: https://github.com/hi3d-official/Hi3Dv1.0 ; záväzná licencia: https://github.com/hi3d-official/Hi3Dv1.0/blob/main/LICENSE . Hi3D Open License Agreement v1.0 stanovuje oznámenia a branding pri komerčnej integrácii modelových materiálov a samostatné hranice používania pri dosiahnutí MAU/príjmov. Samostatné mesh výstupy bez zabudovaných Hi3D materiálov majú podľa dohody odlišný režim, ale externé vstupy si uchovávajú svoje práva. **Katalógový status: verify-item / REVIEW HOLD.** Neimportovať model do hry bez preverenia originálneho assetu a samostatného schválenia. Kompletný experimentálny protokol: [HI3D-V1-EXPERIMENT.md](HI3D-V1-EXPERIMENT.md).

## NVIDIA SimReady Assets — CC BY 4.0, per-package kontrola

Dataset: https://huggingface.co/datasets/nvidia/simready-assets ; znenie CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ .

K 2026-10-28 datasetová karta Hugging Face uvádza CC BY 4.0. Pri konkrétnom balíku skontroluj `com.nvidia.simready.packaging.json`, prípadný `.metadata/LICENSE.txt`, vlastníka, materiály a ďalšie závislosti. CC BY 4.0 typicky povoľuje komerčné použitie a úpravy s požadovanou atribúciou, odkazom na licenciu a uvedením zmien. **Katalógový status: verify-item / REVIEW HOLD**, nie automatické schválenie na distribúciu v App Store. Pozri [NVIDIA-SIMREADY-ASSETS.md](NVIDIA-SIMREADY-ASSETS.md).

## Nezamieňaj licenciu nástroja s licenciou výstupu

Blender, Godot, Krita, Audacity a LMMS sú výrobné nástroje. Licencia aplikácie **automaticky neurčuje** licenciu každej práce v nej vyrobenej; externé sample balíky, fonty, pluginy a assety si uchovávajú vlastné podmienky.

## Politika repozitára

Tento repozitár obsahuje **iba odkazy, zhrnutia a metadata**. Žiadny ZIP, FBX, GLB, WAV, MP3, PNG ani celá cudzia sada sa sem nevkladá bez samostatne overených práv a rozhodnutia vlastníka. CC BY licencia dokumentácie repozitára neprepisuje licencie tretích strán.
