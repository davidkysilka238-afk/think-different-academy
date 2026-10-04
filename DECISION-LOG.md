# Decision log – 1. fáze

## Cíl

V první fázi jsem chtěl ověřit celý základní průchod aplikací: spuštění webu,
komunikaci s REST API a trvalé uložení dat do databáze.

## Zvolený přístup

- **Frontend: Vite a čistý JavaScript.** Projekt už Vite používal a jednoduché
  rozhraní nepotřebuje další framework ani závislosti.
- **Backend: Python `http.server`.** Pro malý ověřovací základ stačí standardní
  knihovna Pythonu, takže server nevyžaduje další balíčky ani složitější
  framework. Stejný server poskytuje sestavený frontend i API.
- **Databáze: SQLite.** Pro fázi, jejímž cílem je ověřit ukládání a čtení dat,
  je souborová databáze vhodnější než samostatně provozovaný databázový server:
  snadno se spustí lokálně i v kontejneru a nevyžaduje další službu. Tabulky a
  výchozí tým jsou deklarativně definovány v `schema.sql`. Server tento soubor
  načte a provede při každém spuštění, takže připraví i prázdnou databázi po
  novém nasazení. Schéma používá `IF NOT EXISTS` a výchozí data `INSERT OR
  IGNORE`, aby šla inicializace bezpečně zopakovat. Databázi nevytvářím při
  sestavení Docker image; vytvoří ji aplikace ze stejného schématu při startu.
- **API: JSON endpointy pod `/api/v1`.** `GET /api/v1/health` ověřuje server,
  `GET /api/v1/team` čte údaje z databáze a
  `POST /api/v1/team/members` přidá člena týmu. Formulář ve webu ověřuje
  zápis i opětovné načtení výsledku přes API.
- **Licence: MIT.** Je přiložena v souboru `LICENSE` pro projekt Tour de App.

## Ověření

Frontend jsem sestavil příkazem `npm run build` a ověřil syntaxi backendu.
API jsem vyzkoušel s dočasnou SQLite databází: health a načtení týmu vrátily
úspěšnou odpověď, přidání člena vrátilo `201` a následné načtení jej obsahovalo.
Ověřil jsem také odmítnutí duplicitního jména (`409`), neplatných dat (`400`)
a nepodporovaného typu obsahu (`415`). Po restartu API zůstal člen v databázi.
Pro ruční spuštění použij `python server.py` a otevři
`http://localhost:8000`; záznam můžeš přidat formulářem na stránce.
