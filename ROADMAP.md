# Colosseum Pool Roadmap

This document outlines the planned features and improvements for the Game Engine service.

## 🏁 Phase 1: Foundation (Completed)

-   [x] Initial FastAPI project structure.
-   [x] Database schema for `matches`, `player_stats`, and `seasons`.
-   [x] Core ELO calculation logic (K=32).
-   [x] Basic Match Recording API (`POST /matches`).
-   [x] Simple Leaderboard API (`GET /leaderboard`).

## 🛠 Phase 2: Game Logic Enhancements (In Progress)

-   [ ] **Office Hours Enforcement**: Implement strict checks for matches during work hours.
-   [ ] **Daily Limit**: Restrict number of matches per pair per day.
-   [ ] **Season Management**: Admin API to start/end seasons and archive stats.
-   [ ] **Nemesis Tracking**: specialized query to find most frequent opponent.

## 🚀 Phase 3: Extended Features (Planned)

-   [ ] **Tournaments**: Bracket generation and management.
-   [ ] **Achievements**: Badge system based on stats (e.g., "On Fire" for 5-win streak).
-   [ ] **Replay System**: Store shot-by-shot data (future scope).
-   [ ] **Live Spectating**: WebSocket updates for ongoing matches.
