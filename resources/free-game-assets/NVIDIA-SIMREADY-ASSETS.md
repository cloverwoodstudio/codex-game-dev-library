# NVIDIA SimReady Assets — externý 3D zdroj (OpenUSD)

**Reviewed:** 2026-10-28  
**Status:** SOURCE PROPOSED / LINK_ONLY / PER-ASSET REVIEW HOLD  
**Catalog ID:** `nvidia-simready-assets`  
**Source:** https://huggingface.co/datasets/nvidia/simready-assets

## Overené zdroje

- Dataset na Hugging Face: https://huggingface.co/datasets/nvidia/simready-assets
- NVIDIA SimReady Central: https://docs.omniverse.nvidia.com/simready/latest/simready-central.html
- NVIDIA SimReady Packaging Workflow (manifest, BOM a validácia): https://nvidia.github.io/simready-foundation/2026.08.0/guides/packaging_workflow.html
- Creative Commons Attribution 4.0: https://creativecommons.org/licenses/by/4.0/

Pri prehliadke 2026-10-28 karta datasetu zobrazovala **2 603 3D assets**, približne **476 GB** dát a licenčný štítok **cc-by-4.0**. Ide o časovo závislý snapshot, nie počítadlo importovaných alebo pre hry optimalizovaných súborov. Formát je **OpenUSD** s fyzikálnymi / simulačnými metadátami; jednotlivé balíky môžu obsahovať textúry, materiály, metadata a ďalšie závislosti. Nie je to katalóg hotových GLB pre Godot.

## Ako sa môže hodiť Cloverwood

Potenciálne použitie: fyzikálne rekvizity, krabice, nástroje, nábytok a priemyselné objekty do prototypov **Block Bouncer**, **Hotel Panic** a všeobecného 3D testovania. To je **možnosť na preskúmanie**, nie potvrdená kompatibilita, vhodná štylizácia ani hotový herný obsah. Pre Block Bouncer musí výsledok najprv zodpovedať kartónovej art bible.

## Licencia / provenance gate

Datasetová karta aktuálne uvádza CC BY 4.0, ale pred komerčnou integráciou je povinná kontrola **konkrétneho balíka**. Skontrolovať najmä `com.nvidia.simready.packaging.json`, dostupné `.metadata/LICENSE.txt`, licenciu textúr a závislostí, autora a verziu datasetu. Zaznamenať pôvodnú revíziu, download URL, dátum, originálny SHA-256 a požadovanú atribúciu. CC BY 4.0 vyžaduje primerané uvedenie autorstva, odkaz na licenciu a informáciu o úpravách. V prípade rozdielu medzi údajmi datasetu a balíka alebo nejasných práv použiť **BLOCKED_LICENSE_REVIEW**.

**Katalóg:** `commercial_game_use=verify-item`, `attribution=per-item`. Toto neznamená zákaz komerčných hier; znamená to, že žiadny individuálny asset zatiaľ **nie je schválený** na použitie.

## Technický intake gate — až po samostatnom súhlase

1. Vybrať **jeden** malý reprezentatívny model a overiť jeho balík a licenciu.
2. Zaznamenať pôvodnú OpenUSD revíziu, materiály, referencie a SHA-256.
3. Overiť Blender import, zachovanie orientácie, mierky, textúr, geometrie a prípadných fyzikálnych vlastností.
4. Vyrobiť osobitný optimalizovaný **GAME GLB** derivát. OpenUSD metadata sa nesmú vydávať za funkčné Godot nastavenia bez testu.
5. Zmerať geometriu, draw calls, textúry, collision a reálny výkon na iPhone.
6. Game Lab QA -> vizuálna kontrola -> explicitný OWNER REVIEW; až potom potenciálna integrácia.

## Hranice tohto PR

Len odkaz, JSON katalóg a dokumentácia. **Nesťahovať** žiadnu časť približne 476 GB datasetu, nezavádzať API/sync, nespúšťať konverziu, neurobiť z toho automaticky zdroj pre Viewer ani hry. Game Lab iPhone Viewer používa samostatný pinned snapshot; jeho prípadná aktualizácia bude **osobitný krok po schválení a MERGE** kanonického katalógu. Tento PR neoprávňuje MERGE ani DEPLOY.
