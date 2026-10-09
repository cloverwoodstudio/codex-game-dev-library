# Odporúčané balíky pre hry Cloverwood

**Reviewed:** 2026-10-09. Nápady na výber zdrojov, nie rozhodnutie o integrácii.

## BLOCK BOUNCER (BB)

| Potreba | Zdroj | Kontrola pred integráciou |
| --- | --- | --- |
| Rigované humanoidné základy | [KayKit Adventurers](https://kaylousberg.itch.io/kaykit), [Mixamo](https://www.mixamo.com/) | Rig a retarget; nechceme ďalšiu skrinku ani robotický pohyb. |
| Chôdza a reakcie | [KayKit Animations](https://kaylousberg.itch.io/kaykit-character-animations), [Quaternius Universal Animations](https://quaternius.com/packs/universalanimationlibrary.html) | Hod **musí** mať náprah, kontakt, vypustenie a zotavenie. Nerieši automaticky fyziku. |
| Bar, nábytok, rekvizity | [Kenney Furniture](https://kenney.nl/assets/furniture-kit), [Food](https://kenney.nl/assets/food-kit) | Povinné prepracovanie na **matný vrstvený kartón**, podľa BB Bible 2.0. |
| Materiál | [ambientCG](https://ambientcg.com/), [Poly Haven](https://polyhaven.com/) | Štruktúra papiera a kontaktné tiene, iPhone performance/VRAM budget. |
| Zvuk komédie | [Sonniss 2026](https://gdc.sonniss.com/), [Mixkit SFX](https://mixkit.co/free-sound-effects/) | Kartónové nárazy, pád, šuchot, bezpečné limity hlasitosti. |

Pravidlo: **nepoužívať generický model ako produkčný vzhľad.** Art QA pred animáciami, potom Godot import, kolízie, skutočný fyzikálny grab/release, kamera hry, test na zariadení. **Žiadny automatický merge.**

## HOTEL PANIC

- [KayKit Adventurers](https://kaylousberg.itch.io/kaykit) — baseline animovateľných ľudských postáv.
- [Kenney Furniture](https://kenney.nl/assets/furniture-kit) — recepcia, izby, chodby.
- [Mixamo](https://www.mixamo.com/) — chôdza hostí, gestá a reakcie.
- [Sonniss](https://gdc.sonniss.com/) — kroky, hotelové dvere, kufre, chaos.
- Pri realistickejších postavách najprv asset Gate 0 a schválenie vzhľadu, až potom integrácia.

## STARFALL RESCUE

- [Kenney Modular Space Kit](https://kenney.nl/assets/modular-space-kit), [Space Station Kit](https://kenney.nl/assets/space-station-kit), [Space Kit](https://kenney.nl/assets/space-kit).
- [Kenney Sci-Fi UI](https://kenney.nl/assets/ui-pack-sci-fi) pre prototyp rozhrania.
- Godot Shaders (manuálne: `godotshaders.com`) pre efekty — licencia po konkrétnom shadere.
- iPhone a budúci foldable layout vyžadujú vlastnú QA, nie automatickú kompatibilitu z balíka.

## SPLIT a NELUVO

- [Kenney UI](https://kenney.nl/assets/ui-pack) alebo [Pixel UI](https://kenney.nl/assets/pixel-ui-pack) na prototyp.
- [Kenney UI Audio](https://kenney.nl/assets/ui-audio), [Interface Sounds](https://kenney.nl/assets/interface-sounds), [JFXR](https://jfxr.frozenfractal.com/).
- Pre Neluvo prioritne **zachovať pôvodný vizuál a zvukovú identitu**; nový asset musí prejsť samostatným owner review.
- Hudba z [Incompetech](https://incompetech.com/music/royalty-free/) alebo vybrané CC0 z OpenGameArt len s kompletnou evidenciou licencie.

## Výberový proces

Vybrať z katalógu → overiť konkrétnu licenciu → stiahnuť originál na schválené pracovné úložisko → zachovať zdroj a SHA → vyrobiť samostatný optimalizovaný GAME derivát → runtime QA → Asset Viewer → owner REVIEW → až potom samostatne schválená integrácia.
