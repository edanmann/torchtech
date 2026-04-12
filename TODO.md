# TODO

## Engine
- Add full storyline branching with explicit player options and consequences.
- Add configurable event hooks for scandal/removal mechanics.
- Add airport ownership mode + SpaceX airport synergy toggle.
- Add richer lawsuit logic (legal defense, counter-sue, probabilistic outcomes).
- Add jail bribe/story interaction flow.

## Data & Persistence
- Migrate in-memory game store to SQLite/SQLModel persistence.
- Add JSON/YAML external deck loading with hot reload.
- Add migrations and versioned schema for live games.

## Frontend
- Move to React + TypeScript app with componentized board and action modals.
- Add dedicated pages: home, setup, game, round summary, end game.
- Add realtime updates (WebSocket) for future multiplayer.

## Testing
- Expand integration tests over API layer.
- Add deterministic simulations for full-match balancing.
