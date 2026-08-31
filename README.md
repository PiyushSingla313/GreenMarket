# 🌿 FarmersMarket

The integrated GreenMarket app — the original static frontend (`files/`) wired
up to the FastAPI backend (`greenmarket-backend/`), served together as one
running website on a single port.

Every page that used to render hardcoded demo data now calls the real API:
listings, live mandi prices, cold storage, rentals & supplies, government
schemes, and login/register all read from and write to a database.

## 1. Run it

```bash
cd FarmersMarket
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** — that's the whole site: homepage, marketplace,
prices, storage, rentals, schemes, login, register. The API lives alongside
it under `/api/*` (interactive docs at `/docs`).

No database setup needed: it defaults to a local SQLite file
(`greenmarket.db`, auto-created) seeded with the same demo data the original
static site used to hardcode. To use PostgreSQL instead, copy `.env.example`
to `.env` and set `DATABASE_URL` (you'll also need to
`pip install psycopg2-binary`, which is commented out in `requirements.txt`
since it requires PostgreSQL build tools).

## 2. How it's wired together

```
FarmersMarket/
├── app/                  FastAPI backend
│   ├── main.py           App, CORS, DB startup/seeding, mounts static/ at "/"
│   ├── config.py, database.py, models.py, schemas.py, auth.py, seed.py
│   └── routers/          /api/auth, /api/listings, /api/prices,
│                         /api/storage, /api/rentals, /api/schemes
├── static/                Frontend (served directly by FastAPI)
│   ├── index.html, marketplace.html, prices.html, storage.html,
│   │   rentals.html, schemes.html, login.html, register.html
│   ├── style.css
│   └── app.js             Shared JS: language switcher + a small `api()`
│                         fetch helper + session (JWT) storage
└── requirements.txt
```

`app/main.py` mounts `static/` as a catch-all at `/` *after* the `/api/*`
routers, so API routes take priority and everything else falls through to
the static files — one process, one port, no CORS juggling needed.

Each page's inline `<script>` was rewritten from a hardcoded array to a
`fetch()`-backed one via the shared `api()` helper in `app.js`:

| Page | Talks to |
|---|---|
| `index.html` | `GET /api/listings` (homepage preview) |
| `marketplace.html` | `GET/POST /api/listings`, `POST /api/listings/{id}/contact` |
| `prices.html` | `GET /api/prices/mandi`, `GET /api/prices/msp` |
| `storage.html` | `GET /api/storage`, `POST /api/storage/{id}/book` |
| `rentals.html` | `GET/POST /api/rentals/machines`, `GET/POST /api/rentals/supplies` |
| `schemes.html` | `GET /api/schemes`, `POST /api/schemes/{id}/apply` |
| `login.html` / `register.html` | `POST /api/auth/login` / `/register`, JWT stored via `setSession()` in `localStorage` |

All the booking/order/apply/contact modals that used to just `alert()` a
fake reference number now actually create a row in the database and show
the real reference/order/application ID the API returns.

## 3. Notes

- Passwords are hashed with `bcrypt` directly (the backend's original
  `passlib` dependency was dropped — it's unmaintained and incompatible with
  recent `bcrypt` releases).
- `SECRET_KEY` in `.env.example` is a placeholder — set a real random value
  before deploying this anywhere public.
- Security/production checklist from the original frontend README still
  applies: HTTPS, rate limiting, OTP verification, restricting CORS origins,
  encrypting Aadhar numbers, etc.
