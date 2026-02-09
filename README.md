# Colosseum Pool Service

The dedicated game engine and logic provider for the Colosseum ecosystem.

This microservice handles the core gameplay mechanics for 8-Ball Pool, including match recording, ELO rating calculations, leaderboards, and season management. It operates independently of user identity storage, focusing purely on game rules and statistics.

## 🏗 Structure

```text
colosseum-pool/
├── Dockerfile                # Instructions to build the Python container.
├── requirements.txt          # Dependencies (FastAPI, SQLAlchemy, AsyncPG).
├── app/
│   ├── main.py               # The entry point.
│   ├── api/                  # API endpoints (Matches, Stats).
│   ├── db/                   # Database connection and models.
│   ├── logic/                # Pure business logic (ELO, Rules).
│   └── schemas/              # Pydantic data models.
└── migrations/               # Database migrations (Alembic).
```

## ⚡ Quick Start

This service is part of the larger Colosseum ecosystem. To get it running quickly:

1.  **Clone the Infrastructure Repo**: This project relies on the central gateway and database managed by `colosseum-infra`.
2.  **Set up Environment**:
    -   Copy matches the `.env` configuration from `colosseum-infra`.
    -   Ensure `DATABASE_URL` points to the Pool database.
3.  **Run via Infra**:
    ```bash
    # From the colosseum-infra directory
    make dev
    ```

## 🚀 Features

-   **Match Processing**: Validates and records match results between players.
-   **ELO Engine**: Real-time rating updates using a standard ELO formula (K=32).
-   **Leaderboards**: Dynamic ranking of players based on current season performance.
-   **Rule Enforcement**: Validates office hours and daily match limits.

## 🛠 Tech Stack

Detailed architecture and technical specifications can be found in [ARCHITECTURE.md](./ARCHITECTURE.md).

-   **Framework**: FastAPI (Python 3.11+)
-   **Database**: PostgreSQL (Async)
-   **ORM**: SQLAlchemy 2.0+ (AsyncIO)
-   **Migrations**: Alembic
-   **Validation**: Pydantic

## 📦 Local Development

### Testing
To run tests inside the container (via infra):
```bash
# In colosseum-infra directory
docker-compose exec pool-service pytest
```
