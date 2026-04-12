# ASCENDANCY MVP

A production-structured MVP implementation of the ASCENDANCY strategy board game.

## Project structure

```text
app/
  api/routes/games.py          # FastAPI routes
  core/seed_data.py            # Board, assets, card seed data
  models/schemas.py            # Pydantic models/DTOs/state
  services/game_service.py     # Core game engine + rule logic
  static/                      # Frontend (home/setup/game UI)
    index.html
    styles.css
    script.js
tests/
  test_game_engine.py          # Unit tests for core logic
RULES_ASSUMPTIONS.md
TODO.md
requirements.txt
```

## Features implemented

- New game (2–4 players)
- Turn progression and movement on 52-square board
- Start pass rewards (+200 money or +50 reputation)
- Round engine with synchronized payouts
- Money, reputation, and power score tracking
- 13 properties with L1/L2/L3 rent and upgrade costs
- B2C/B2B/B2G company systems
- HQ/store conflict resolution (buyout vs revenue-share)
- White House + presidency mechanics
- Jail, hospital, airport, court, black market, lobbying, intelligence, investment hubs
- Main/story/media decks (data-driven, expandable)
- Action log and round progression
- In-memory saveable game state

## API endpoints

- `POST /games`
- `GET /games/{id}`
- `POST /games/{id}/start`
- `POST /games/{id}/next-turn`
- `POST /games/{id}/move`
- `POST /games/{id}/resolve-square`
- `POST /games/{id}/buy-property`
- `POST /games/{id}/buy-hq`
- `POST /games/{id}/upgrade-asset`
- `POST /games/{id}/draw-main-card`
- `POST /games/{id}/draw-media-card`
- `POST /games/{id}/draw-story-card`
- `POST /games/{id}/run-for-president`
- `POST /games/{id}/presidential-policy`
- `POST /games/{id}/choose-white-house-option`
- `POST /games/{id}/lobby`
- `POST /games/{id}/airport-travel`
- `POST /games/{id}/investment`
- `POST /games/{id}/resolve-hq-store-choice`
- `POST /games/{id}/court`
- `POST /games/{id}/intelligence`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

App URL: `http://localhost:8000`

## Testing

```bash
pytest -q
```
