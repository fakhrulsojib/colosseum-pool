# Upcoming Features - Pool Service (Game Engine)

## 1. Project Overview
**Service Name:** `colosseum-pool`
**Role:** The dedicated game engine for 8-Ball Pool.
**Responsibility:**
- Manages Match History and Season lifecycles.
- Calculates Elo Ratings (Standard Formula).
- Maintains Live Leaderboards.
- Enforces Governance Rules (Office Hours, Daily Limits).
**Independence:** This service is **stateless** regarding User Identity. It receives a JWT, extracts the `user_id`, and assumes the User exists. It does not access the Core User Database.

---

## 2. Technology Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL 15 (Async)
- **ORM:** SQLAlchemy 2.0+ (AsyncIO)
- **Migrations:** Alembic
- **Auth Validation:** `python-jose` (JWT decoding, HS256)
- **Environment:** Docker & Docker Compose

---

## 3. Architecture & Directory Structure
The project follows a "Domain-Driven" folder structure.

```text
/colosseum-pool
├── Dockerfile              # Multi-stage python build
├── docker-compose.yml      # Local dev setup (DB + App)
├── requirements.txt        # fastapi, uvicorn, sqlalchemy, asyncpg, alembic, python-jose, pydantic-settings
├── alembic.ini             # Migration config
├── /app
│   ├── main.py             # Entry point, Middleware setup
│   ├── /core
│   │   ├── config.py       # Pydantic Settings (Load .env)
│   │   └── security.py     # JWT Verification Logic (No DB access)
│   ├── /db
│   │   ├── session.py      # Async Engine & SessionMaker
│   │   └── base.py         # Import all models here
│   ├── /models
│   │   ├── match.py        # SQLAlchemy Model: Matches
│   │   └── stats.py        # SQLAlchemy Model: PlayerStats, Seasons
│   ├── /schemas
│   │   ├── match.py        # Pydantic: MatchCreate, MatchResponse
│   │   └── stats.py        # Pydantic: LeaderboardEntry
│   ├── /logic
│   │   ├── elo.py          # Pure Math: calculate_new_ratings()
│   │   └── rules.py        # Business Logic: Office Hours, Daily Limits
│   └── /api
│       └── /v1
│           ├── matches.py  # POST /matches
│           └── stats.py    # GET /leaderboard, GET /stats/{user_id}

```

---

## 4. Database Schema (PostgreSQL)

*Note: All tables exist in the `pool` schema, not `public`.*

### Table: `seasons`

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | Integer | PK, Auto Inc |  |
| `name` | String | Unique | e.g., "Genesis", "Brotherhood" |
| `start_date` | Date |  |  |
| `end_date` | Date |  |  |
| `is_active` | Boolean | Default False | Only one true at a time |

### Table: `player_stats` (The Leaderboard)

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `user_id` | UUID | PK (Composite) | **No FK to Users table** |
| `season_id` | Integer | PK (Composite), FK |  |
| `elo` | Integer | Default 800 |  |
| `wins` | Integer | Default 0 |  |
| `losses` | Integer | Default 0 |  |
| `streak` | Integer | Default 0 | Positive=Win Streak, Negative=Loss |

### Table: `matches`

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | PK |  |
| `season_id` | Integer | FK |  |
| `winner_id` | UUID | Indexed |  |
| `loser_id` | UUID | Indexed |  |
| `elo_change` | Integer |  | Points exchanged (e.g., 25) |
| `timestamp` | DateTime |  | UTC |
| `is_office_hours` | Boolean |  | Was this played 9-6? |

---

## 5. Business Rules Implementation

### A. The Elo Engine (`/logic/elo.py`)

* **Formula:** `R_new = R_old + K * (Score - Expected_Score)`
* **K-Factor:** 32 (Standard volatility).
* **Inputs:** `winner_elo`, `loser_elo`.
* **Outputs:** `new_winner_elo`, `new_loser_elo`, `points_exchanged`.

### B. The Governance (`/logic/rules.py`)

**Rule 1: Office Hours**

* **Definition:** 09:00 to 18:00 (Server Time/Local Config).
* **Constraint:** If `timestamp` is within Office Hours, check `matches` table.
* **Query:** `SELECT count(*) FROM matches WHERE date(timestamp) = today AND ((winner=A AND loser=B) OR (winner=B AND loser=A)) AND is_office_hours = TRUE`.
* **Result:** If count > 0, raise `400 HTTP Exception: "Daily office limit reached for this pair."`

**Rule 2: Season Locking**

* All matches must be associated with the currently `is_active=True` season.
* If no season is active, reject match submission.

---

## 6. API Endpoints Specification

### `POST /api/v1/matches`

* **Headers:** `Authorization: Bearer <JWT>`
* **Body:** `{"opponent_id": "uuid", "result": "WIN" | "LOSS"}`
* **Logic:**
1. Extract `user_id` (Player A) from JWT.
2. Identify Player B from `opponent_id`.
3. Check **Office Hours Rule**.
4. Fetch current Elo for A and B from `player_stats`.
5. Calculate new Elo.
6. Update `player_stats` (Elo, Wins/Losses, Streaks).
7. Insert row into `matches`.


* **Response:** `{"match_id": "...", "elo_change": 25, "new_elo": 825}`

### `GET /api/v1/leaderboard`

* **Query Param:** `season_id` (Optional, defaults to active).
* **Response:** List of `{user_id, elo, rank, wins, losses, streak}`.
* **Note:** Returns UUIDs. Frontend resolves names via Core Service.

### `GET /api/v1/stats/{user_id}`

* **Response:** Detailed glory metrics (Nemesis, Bunny, History Graph).

---

## 7. Step-by-Step Implementation Guide for LLM

*Use these prompts to generate code iteratively.*

**Step 1: Infrastructure**

> "Generate the Dockerfile, docker-compose.yml, and requirements.txt for a FastAPI project using Python 3.11. Include dependencies for Async SQLAlchemy, Postgres, and Alembic."

**Step 2: Configuration & Auth**

> "Create `app/core/config.py` using Pydantic Settings to load DB credentials and SECRET_KEY. Then create `app/core/security.py` to decode a JWT and return the `sub` (user_id) without connecting to a database."

**Step 3: Database Models**

> "Create the SQLAlchemy Async models for `Season`, `PlayerStats`, and `Match` based on the schema defined in Section 4. Ensure they belong to `__table_args__ = {'schema': 'pool'}`."

**Step 4: Elo & Logic**

> "Create `app/logic/elo.py` to handle the math. Then create `app/logic/rules.py` containing a function `validate_match_constraints` that checks the database for the Office Hours limit."

**Step 5: API Routes**

> "Create the FastAPI router for `POST /matches`. Use Dependency Injection to get the DB session and the Current User from JWT. Orchestrate the logic: Validate Rules -> Calc Elo -> Update DB."

**Step 6: Leaderboard**

> "Create the `GET /leaderboard` endpoint. It should return results sorted by Elo descending. Include a Pydantic schema for the response."