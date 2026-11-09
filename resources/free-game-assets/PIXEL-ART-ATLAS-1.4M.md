# Pixel Art Atlas 1.4M — kompletný archivovaný zdroj

**Reviewed:** 2026-11-09 · **Owner-specified full mirror:** yes · **Production use:** `verify-item` / REVIEW HOLD.

## Kde je celý dataset

- Originál: https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m
- GitHub Release archívu v našej knižnici: https://github.com/cloverwoodstudio/codex-game-dev-library/releases/tag/pixel-art-atlas-1.4m-hf-bf78f8c
- Súbor: `pixel-art-atlas-1.4m-source-bf78f8c.tar` (kompletný zdroj, cca 694 MB)
- Kontrola integrity: `SHA256SUMS.txt`; TAR SHA-256 `71b2a235f2162ab0471db866dd9471ad1706fdd38204f5b9834edcd47ed51993`
- Presná upstream revízia: `bf78f8c8cbafa6d07718111a94d41e2dd79ddaa7`

**Celý obsah:** 21 originálnych súborov (693 917 233 bajtov), v tom 15 tréningových Parquet častí, jedna validačná, `pixel-art-16x16-1.4m.zip`, README, LICENSE, banner a .gitattributes. TAR má navyše interný pôvodový dokument a manifest s individuálnymi SHA-256.

Dataset obsahuje 1 409 404 syntetických RGBA spriteov s natívnym rozmerom 16×16 px a anglickými popismi. Obrázky pochádzajú z Krea 2 Turbo a pixel-art LoRA. Popisy nie sú úplne overené voči obrázkom.

## Použitie v Cloverwood

Využitie: vyhľadávateľná referenčná knižnica pixel-art objektov, výber konkrétnych ikon, inventárnych položiek a prípadne podklady na budúci výskum AI dát. Dataset **nie je automaticky pripravený pre App Store**, nie je hotovou sadou animácií a nepatrí do produkcie bez konkrétnej kontroly.

Pred produkčným použitím každého výberu:
1. Skontrolovať reálny vzhľad, relevantnosť, duplicity, obsah a vizuálnu kvalitu.
2. Overiť práva konkrétneho obrázka a aktuálne podmienky súvisiaceho Krea modelu; zaznamenať výber a jeho SHA-256 do projektového asset ledgeru.
3. Dostať schválenie vlastníka pre konkrétnu hru. `verify-item` neznamená automatický zákaz ani automatické povolenie.

## Licenčné hranice

Autor Angais uvádza **CC0-1.0**, a to len v rozsahu práv, ktorých sa môže vzdať. Výstupy boli vytvorené cez Krea. CC0 neodstraňuje prípadné práva tretích strán, ochranné známky ani podmienky Krea (vrátane pravidiel komerčného použitia). Nejde o oficiálne vydanie Krea.

Tento úplný mirror je osobitná výnimka odsúhlasená vlastníkom knižnice; binárne dáta sú uložené v **GitHub Release assets**, nie v Git histórii vedomostnej knižnice. Ostatné zdroje v katalógu zostávajú len odkazmi.

## Overenie

```sh
shasum -a 256 -c SHA256SUMS.txt
tar -tf pixel-art-atlas-1.4m-source-bf78f8c.tar | head
tar -xf pixel-art-atlas-1.4m-source-bf78f8c.tar
```

Pôvodný ZIP prešiel `unzip -tqq`; všetkých 21 súborov bolo validovaných proti upstream veľkosti a SHA-256, ak bol od dodávateľa uvedený.
