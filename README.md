# Colosseum Game Engine (Pool)

The Logic Provider for Colosseum—where matches are recorded, and legends are made.

This microservice handles the storage of match results, leaderboard calculations, and the ELO ranking algorithm.

## 🏗 Structure

```text
colosseum-pool/
├── Dockerfile                # Instructions to build the Python container.
├── requirements.txt          # Dependencies (FastAPI, SQLAlchemy, etc.).
├── app/
│   ├── main.py               # Entry point.
│   ├── api/
│   │   ├── matches.py        # POST /matches (Records results).
│   │   └── stats.py          # GET /leaderboard (Ranks players).
│   ├── logic/
│   │   └── elo.py            # Pure math for the ELO algorithm.
│   └── db/
│       └── models.py         # 'Matches' and 'Stats' table definitions.
└── migrations/               # Database schema versioning.
```

## 🚀 Features

- **Match Recording**: Validate and store match results.
- **Rank Calculation**: Real-time ELO updates.
- **Leaderboard API**: High-performance stats for the digital arena.

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Algorithm**: Custom ELO Implementation
- **Database Logic**: SQLAlchemy (Async)
- **Database**: PostgreSQL

## 📦 Local Development (via Docker)

This service is orchestrated via the `colosseum-infra` repository.

```bash
# To build the image manually
docker build -t colosseum-pool .
```
