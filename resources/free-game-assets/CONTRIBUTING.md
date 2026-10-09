# Pridanie ďalšieho zdroja

**Reviewed:** 2026-10-09

1. Do `catalog.json` pridaj jeden záznam s unikátnym stabilným slug `id`. Použi HTTPS oficiálnu URL a samostatný `license_url`.
2. `commercial_game_use: yes` nastav len vtedy, keď oficiálny zdroj povoľuje **komerčné videohry**; ak ide o trhovisko s rôznymi licenciami, musí byť `verify-item`.
3. `free-tier` neznamená, že sú zdarma platené rozšírenia alebo zdrojové `.blend` súbory.
4. Vyplň `reviewed` v ISO dátume. Do `notes` píš vlastné krátke zhrnutie, nie kopírovaný obsah stránok.
5. Vygeneruj aktuálny index: `python3 scripts/check_free_game_assets.py --write-index`.
6. Over `python3 scripts/check_free_game_assets.py --check`, `python3 -m unittest discover -s tests -p 'test_free_game_assets*.py'` a existujúci repo link checker podľa `CONTRIBUTING.md`.
7. Zmeny patria do **DRAFT PR**. OWNER REVIEW rozhodne o merge; pridanie URL nie je schválením konkrétneho assetu.

Žiadny mirror sťahovaných zdrojových modelov, archívov, fontov alebo audio balíkov.
