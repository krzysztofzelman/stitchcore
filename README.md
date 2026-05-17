# StitchCore

Platforma e-commerce dla marki odzieżowo-obuwniczej — uproszczona wersja demonstracyjna.

## Stack

| Warstwa | Technologia |
|---------|------------|
| Backend | FastAPI + SQLAlchemy (async) + SQLite (aiosqlite) |
| Frontend Shop | Vite + React + Tailwind CSS + React Router |
| Frontend Admin | Vite + React + Material UI + React Router |
| Auth | JWT (python-jose, passlib, bcrypt) |
| Baza | SQLite (brak PostgreSQL, brak Celery) |

## Struktura projektu

```
stitchcore/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # Entry point
│   │   ├── core/         # Config, database, security, deps
│   │   ├── models/       # SQLAlchemy ORM (user, product, order, inventory)
│   │   ├── schemas/      # Pydantic validation
│   │   ├── api/v1/       # REST endpoints (auth, products, orders, inventory)
│   │   └── services/     # Business logic
│   ├── alembic/          # Migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend-shop/        # Sklep kliencki (Vite + React + Tailwind)
│   ├── src/
│   │   ├── api/          # Axios client
│   │   ├── contexts/     # Auth, Cart
│   │   ├── components/   # Navbar, Footer, ProductCard
│   │   └── pages/        # Home, Products, Cart, Checkout, Account, Login, Register
│   └── package.json
├── frontend-admin/       # Panel administracyjny (Vite + React + MUI)
│   ├── src/
│   │   ├── api/          # Axios client
│   │   ├── contexts/     # Auth
│   │   ├── components/   # Layout with drawer
│   │   └── pages/        # Dashboard, Products, Orders, Inventory
│   └── package.json
├── docker-compose.yml
├── scripts/setup.sh
└── README.md
```

## Wymagania

- Python 3.12+
- Node.js 18+
- npm 9+

## Uruchomienie

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend uruchomi się na http://localhost:8000.

API docs: http://localhost:8000/docs

### 2. Frontend Shop

```bash
cd frontend-shop
npm install
npm run dev
```

Sklep uruchomi się na http://localhost:5173.

### 3. Frontend Admin

```bash
cd frontend-admin
npm install
npm run dev
```

Panel admina uruchomi się na http://localhost:5174.

## Pierwsze uruchomienie

Backend automatycznie:
- Tworzy tabele przy starcie (Alembic migration)
- Tworzy domyślnego administratora: **admin@stitchcore.pl** / **admin123**

Aby zalogować się do panelu admina (http://localhost:5174/login):
- Email: `admin@stitchcore.pl`
- Hasło: `admin123`

### Seed danych (opcjonalnie)

Aby wypełnić bazę przykładowymi produktami (T-shirt, Jeansy, Buty, Plecak, Czapka) wraz z wariantami i stanami magazynowymi:

```bash
cd backend
python -m app.scripts.seed_data
```

## API Endpoints

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| POST | `/api/v1/auth/register` | Rejestracja | - |
| POST | `/api/v1/auth/login` | Logowanie | - |
| POST | `/api/v1/auth/refresh` | Odświeżenie tokenu | - |
| GET | `/api/v1/auth/me` | Profil użytkownika | JWT |
| GET | `/api/v1/products` | Lista produktów | - |
| GET | `/api/v1/products/{id}` | Szczegóły produktu | - |
| POST | `/api/v1/products` | Dodaj produkt | Admin |
| PUT | `/api/v1/products/{id}` | Edytuj produkt | Admin |
| POST | `/api/v1/products/{id}/variants` | Dodaj wariant | Admin |
| GET | `/api/v1/categories` | Lista kategorii | - |
| POST | `/api/v1/categories` | Dodaj kategorię | Admin |
| GET | `/api/v1/orders` | Lista zamówień | JWT |
| GET | `/api/v1/orders/{id}` | Szczegóły zamówienia | JWT |
| POST | `/api/v1/orders` | Złóż zamówienie | JWT |
| PATCH | `/api/v1/orders/{id}/status` | Aktualizacja statusu | Admin |
| GET | `/api/v1/inventory/stock` | Stan magazynowy | Admin |
| POST | `/api/v1/inventory/stock/adjust` | Korekta stanu | Admin |
| GET | `/api/v1/inventory/locations` | Lokalizacje | Admin |
| POST | `/api/v1/inventory/locations` | Dodaj lokalizację | Admin |
| GET | `/api/v1/inventory/movements` | Ruchy magazynowe | Admin |

## Funkcjonalności

- **Sklep**: przeglądanie produktów, dodawanie do koszyka, składanie zamówienia, historia zamówień
- **Panel admina**: zarządzanie produktami, wariantami, zamówieniami, stanami magazynowymi, lokalizacjami
- **Autoryzacja**: JWT z odświeżaniem tokenu, role (customer/admin)
- **Płatność**: tylko pobranie (offline)
- **Wysyłka**: ręczne dodanie numeru przesyłki w panelu admina

## Planowane moduły (do dodania w przyszłości)

- Allegro API
- Płatności online (Stripe / Przelewy24)
- Wysyłka (InPost / DPD)
- Powiadomienia email (SendGrid)
- Raporty (ReportLab / OpenPyXL)
- Monitorowanie (Sentry)

## GitHub / Wdrażanie

### Push do repozytorium

```bash
# Zainicjuj repozytorium (jeśli jeszcze nie istnieje)
git init
git add .
git commit -m "Initial commit - StitchCore e-commerce"

# Połącz z zdalnym repozytorium i wypchnij
git remote add origin https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/stitchcore.git
git branch -M main
git push -u origin main
```

### CI/CD

Projekt zawiera konfigurację GitHub Actions (`.github/workflows/ci.yml`), która automatycznie:
- Sprawdza poprawność kodu backendu (Python) — uruchamia testy API
- Sprawdza poprawność kodu frontend-shop (TypeScript) — kompilacja
- Sprawdza poprawność kodu frontend-admin (TypeScript) — kompilacja

Aby uruchomić testy lokalnie przed wypchnięciem:

```bash
# Backend - uruchom serwer w tle, a następnie testy
cd backend
uvicorn app.main:app --reload &
cd ..
python test_all.py

# Frontend - sprawdź TypeScript
cd frontend-shop && npx tsc --noEmit
cd ../frontend-admin && npx tsc --noEmit
```

> **Uwaga:** Upewnij się, że plik `.env` NIE jest commitowany do repozytorium (znajduje się w `.gitignore`). Skorzystaj z szablonu `.env.example`.
