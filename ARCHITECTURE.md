# Colosseum Pool Service - Architecture & Technical Specs

The `colosseum-pool` service is the dedicated **Game Engine** for 8-Ball Pool. It handles match results, calculates ELO ratings, manages season lifecycles, and serves live leaderboards.

## 1. Role & Responsibility

-   **Match Authority**: Records and validates all competitive matches.
-   **Rating Engine**: Calculates ELO updates using a dynamic K-factor system.
-   **Leaderboard Management**: Tracks player performance across active seasons.
-   **Rule Enforcement**: Applies governance rules like "Office Hours" and "Daily Limits".

**Independence:** This service is **stateless** regarding User Identity. It receives a checked JWT from the Gateway/Core interaction, extracts the `user_id`, and assumes the User exists. It does not access the Core User Database directly.

---

## 2. Technology Stack

-   **Language:** Python 3.11+
-   **Framework:** FastAPI
-   **Database:** PostgreSQL 15 (Async via `asyncpg`)
-   **ORM:** SQLAlchemy 2.0+ (AsyncIO)
-   **Auth Validation:** `python-jose` (Stateless JWT verification)
-   **Migrations:** Alembic

---

## 3. Database Schema

*Note: All tables exist in the `pool` schema to avoid collision with Core tables if sharing an instance.*

### Table: `matches`
| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | PK | Unique Match Identifier |
| `season_id` | Integer | FK | Associated Season |
| `winner_id` | UUID | Indexed | ID of the Winner |
| `loser_id` | UUID | Indexed | ID of the Loser |
| `elo_change` | Integer | | Points exchanged (e.g., 25) |
| `timestamp` | DateTime | | UTC Time of Match |
| `is_office_hours` | Boolean | | Flag for governance rules |

### Table: `player_stats` (The Leaderboard)
| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `user_id` | UUID | PK (Composite) | **No FK to Users table** |
| `season_id` | Integer | PK (Composite), FK | Linked to specific season |
| `elo` | Integer | Default 800 | Current Rating |
| `wins` | Integer | Default 0 | Tracked wins |
| `losses` | Integer | Default 0 | Tracked losses |
| `streak` | Integer | Default 0 | + for Win Streak, - for Loss Streak |

### Table: `seasons`
| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | Integer | PK | |
| `name` | String | Unique | e.g., "Season 1: Genesis" |
| `is_active` | Boolean | Default False | Only one active at a time |

---

## 4. Key Logic Implementation

### The ELO Engine (`app/logic/elo.py`)
-   **Formula:** `R_new = R_old + K * (Score - Expected_Score)`
-   **K-Factor:** 32 (Standard volatility)
-   **Process:**
    1.  Calculate expected score based on current ratings.
    2.  Compute point exchange.
    3.  Update both Winner and Loser ratings atomically.

### Governance Rules (`app/logic/rules.py`)
-   **Office Hours:** Matches between 09:00 and 18:00 are flagged or restricted based on configuration.
-   **Season Locking:** Matches must occur within active season dates.

---

## 5. API Overview

### `POST /api/v1/matches`
-   **Input:** Opponent ID, Result (WIN/LOSS).
-   **Process:** Validate Rules -> Calculate ELO -> Update Stats -> Record Match.
-   **Output:** New ELO, Points Exchanged.

### `GET /api/v1/leaderboard`
-   **Input:** Season ID (optional).
-   **Output:** Sorted list of players by ELO descending.
-   **Note:** Returns UUIDs; Frontend resolves names via Core Service cache.
