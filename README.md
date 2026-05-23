# 🧵 Mercha — Platforma E-commerce

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![MUI](https://img.shields.io/badge/MUI-5-007FFF?style=for-the-badge&logo=mui&logoColor=white)](https://mui.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

---

Nowoczesna platforma e-commerce dla marki odzieżowo-obuwniczej, zbudowana w architekturze **frontend + backend**. Projekt obejmuje w pełni funkcjonalny sklep internetowy dla klientów oraz rozbudowany panel administracyjny do zarządzania produktami, zamówieniami i stanami magazynowymi.

Gotowy do lokalnego uruchomienia przez Docker Compose oraz do wdrożenia na serwerze VPS z wykorzystaniem **nginx** jako reverse proxy.

---

## 🚀 Demo na żywo

| Aplikacja | URL |
|-----------|-----|
| 🛍️ **Sklep kliencki** | [http://31.3.218.196:5173](http://31.3.218.196:5173) |
| 🔧 **Panel administracyjny** | [http://31.3.218.196:5174](http://31.3.218.196:5174) |
| 📚 **Dokumentacja API (Swagger)** | [http://31.3.218.196:8000/docs](http://31.3.218.196:8000/docs) |

### Dane testowe — panel administracyjny

| Pole | Wartość |
|------|---------|
| 📧 Email | `admin@mercha.pl` |
| 🔑 Hasło | `admin123` |

---

## 🖼️ Zrzuty ekranu

| Sklep kliencki | Panel administracyjny |
|----------------|-----------------------|
| ![Shop Screenshot](https://placehold.co/600x400/1a1a2e/e0e0e0?text=Sklep+Mercha) | ![Admin Screenshot](https://placehold.co/600x400/1a1a2e/e0e0e0?text=Panel+Admina) |

> Zrzuty ekranu zostaną wkrótce zastąpione rzeczywistymi obrazami platformy.

---

## 📖 Spis treści

- [Stack technologiczny](#-stack-technologiczny)
- [Architektura](#-architektura)
- [Struktura projektu](#-struktura-projektu)
- [Funkcjonalności](#-funkcjonalności)
- [Wymagania](#-wymagania)
- [Uruchomienie lokalne (bez Dockera)](#-uruchomienie-lokalne-bez-dockera)
- [Uruchomienie przez Docker Compose](#-uruchomienie-przez-docker-compose)
- [Konfiguracja środowiska](#-konfiguracja-środowiska)
- [API Endpoints](#-api-endpoints)
- [CI/CD](#-cicd)
- [Wdrożenie produkcyjne](#-wdrożenie-produkcyjne)
- [Skrypty pomocnicze](#-skrypty-pomocnicze)
- [Plan rozwoju](#-plan-rozwoju)
- [Licencja](#-licencja)

---

## 🧱 Stack technologiczny

| Warstwa | Technologia | Wersja |
|---------|-------------|--------|
| 🖥️ **Backend API** | FastAPI + SQLAlchemy 2.0 (async) + SQLite (aiosqlite) | Python 3.12+ |
| 🛍️ **Frontend — Sklep** | Vite + React 18 + Tailwind CSS 3 + React Router | Node 18+ |
| 🔧 **Frontend — Admin** | Vite + React 18 + Material UI 5 + React Router | Node 18+ |
| 🔐 **Autoryzacja** | JWT (python-jose) + bcrypt (passlib) | — |
| 🗄️ **Baza danych** | SQLite przez aiosqlite | — |
| 🐳 **Konteneryzacja** | Docker + Docker Compose | Compose v3.8 |
| 🌐 **Reverse Proxy** | nginx (konfiguracja w `docker/nginx/`) | — |
| 🔄 **Migracje** | Alembic | — |
| 🤖 **CI/CD** | GitHub Actions | — |

---

## 🏗️ Architektura

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  frontend-   │    │  frontend-   │    │  Nginx       │
│  shop        │    │  admin       │    │  (produkcja) │
│  :5173       │    │  :5174       │    │  :80/:443    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └──────────┬────────┘                   │
                  │  HTTP / REST               │
                  ▼                            ▼
          ┌──────────────┐            ┌──────────────┐
          │  Backend     │◄───────────│  API Gateway │
          │  FastAPI     │            │  (nginx)     │
          │  :8000       │            └──────────────┘
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │  SQLite      │
          │  baza danych │
          └──────────────┘
```

Architektura opiera się na modelu **trzech kontenerów**:

1. **Backend (FastAPI)** — REST API z warstwową architekturą: route handlers → serwisy → modele ORM.
2. **Frontend Shop** — aplikacja kliencka (React + Tailwind) dla użytkowników końcowych.
3. **Frontend Admin** — panel zarządzania (React + MUI) dla administratorów.

W środowisku produkcyjnym nad całością dodatkowo pracuje **nginx** jako reverse proxy, udostępniając SSL/TLS, kompresję gzip i routing na subdomeny.

---

## 📁 Struktura projektu

```
stitchcore/
│
├── backend/                       # 🖥️ Backend API (FastAPI)
│   ├── app/
│   │   ├── main.py                #    Entry point — fabryka aplikacji FastAPI
│   │   ├── api/v1/                #    Endpoints REST (auth, products, orders, inventory)
│   │   │   ├── router.py          #    Agregacja routerów
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   └── inventory.py
│   │   ├── core/                  #    Konfiguracja, baza danych, bezpieczeństwo
│   │   │   ├── config.py          #    Ustawienia (pydantic-settings)
│   │   │   ├── database.py        #    Silnik i sesja SQLAlchemy
│   │   │   ├── security.py        #    JWT, hashowanie haseł
│   │   │   └── deps.py            #    Wstrzykiwanie zależności
│   │   ├── models/                #    Modele ORM (User, Product, Order, Inventory)
│   │   ├── schemas/               #    Schematy Pydantic
│   │   ├── services/              #    Logika biznesowa
│   │   └── scripts/               #    Skrypty (init_admin, seed_data)
│   ├── alembic/                   #    Migracje bazy danych
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend-shop/                 # 🛍️ Sklep kliencki (Vite + React + Tailwind)
│   ├── src/
│   │   ├── api/                   #    Klient HTTP (axios)
│   │   ├── contexts/              #    Stan: AuthContext, CartContext
│   │   ├── components/            #    Navbar, Footer, ProductCard
│   │   └── pages/                 #    Home, Products, Cart, Checkout, Account, Login, Register
│   ├── Dockerfile
│   └── package.json
│
├── frontend-admin/                # 🔧 Panel administracyjny (Vite + React + MUI)
│   ├── src/
│   │   ├── api/                   #    Klient HTTP (axios)
│   │   ├── contexts/              #    Stan: AuthContext
│   │   ├── components/            #    Layout z drawerem
│   │   └── pages/                 #    Dashboard, Products, Orders, Inventory
│   ├── Dockerfile
│   └── package.json
│
├── docker/                        # 🐳 Konfiguracja Docker
│   └── nginx/
│       └── nginx.conf             #    Konfiguracja reverse proxy (dev + prod)
│
├── scripts/                       # 📜 Skrypty pomocnicze
│   ├── setup.sh                   #    Automatyczna konfiguracja projektu
│   └── backup.sh                  #    Backup bazy danych
│
├── docs/                          # 📖 Dokumentacja dodatkowa
├── .github/workflows/             # 🤖 GitHub Actions CI/CD
│   └── ci.yml
│
├── docker-compose.yml             # 🐳 Orkiestracja kontenerów
├── .env.example                   # 📋 Szablon zmiennych środowiskowych
└── README.md
```

---

## ✨ Funkcjonalności

### 🛍️ Sklep kliencki (`frontend-shop`)

| Funkcja | Opis |
|---------|------|
| Przeglądanie produktów | Katalog z podziałem na kategorie |
| Szczegóły produktu | Pełne informacje, warianty, ceny |
| Koszyk | Dodawanie / usuwanie produktów, zarządzanie ilością |
| Składanie zamówień | Płatność przy odbiorze |
| Panel użytkownika | Historia zamówień, dane konta |
| Rejestracja i logowanie | JWT — access + refresh token |

### 🔧 Panel administracyjny (`frontend-admin`)

| Funkcja | Opis |
|---------|------|
| Dashboard | Podsumowanie sprzedaży, statystyki |
| Zarządzanie produktami | CRUD produktów i wariantów |
| Zarządzanie zamówieniami | Zmiana statusu, numer przesyłki |
| Zarządzanie magazynem | Stany magazynowe, lokalizacje |
| Ruchy magazynowe | Historia korekt i przesunięć |

### 🔐 Autoryzacja

- **JWT** z podwójnym tokenem: access (15 min) + refresh (7 dni)
- Role użytkowników: `customer`, `admin`
- Endpointy administracyjne chronione przez zależność `get_current_admin`

---

## 📋 Wymagania

| Narzędzie | Minimalna wersja |
|-----------|------------------|
| 🐍 Python | 3.12+ |
| 🟩 Node.js | 18+ |
| 📦 npm | 9+ |
| 🐳 Docker | 24+ (opcjonalnie) |
| 🐳 Docker Compose | v2.20+ (opcjonalnie) |

---

## 🚀 Uruchomienie lokalne (bez Dockera)

### 1. Backend

```bash
cd backend
python -m venv venv

# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend uruchomi się na **http://localhost:8000**.
Dokumentacja API (Swagger): **http://localhost:8000/docs**.

### 2. Frontend — Sklep kliencki

```bash
cd frontend-shop
npm install
npm run dev
```

Sklep uruchomi się na **http://localhost:5173**.

### 3. Frontend — Panel administracyjny

```bash
cd frontend-admin
npm install
npm run dev
```

Panel administracyjny uruchomi się na **http://localhost:5174**.

### 🧪 Pierwsze uruchomienie

Backend automatycznie przy starcie:
- ✅ Wykonuje migracje Alembic (`alembic upgrade head`)
- ✅ Tworzy domyślnego administratora: `admin@mercha.pl` / `admin123`

Po uruchomieniu wszystkich trzech aplikacji zaloguj się do panelu admina:
- **URL:** http://localhost:5174/login
- **Email:** `admin@mercha.pl`
- **Hasło:** `admin123`

### 🌱 Seed danych (opcjonalnie)

Aby wypełnić bazę przykładowymi produktami (T-shirt, Jeansy, Buty, Plecak, Czapka) wraz z wariantami i stanami magazynowymi:

```bash
cd backend
python -m app.scripts.seed_data
```

---

## 🐳 Uruchomienie przez Docker Compose

Najszybszy sposób na uruchomienie całej platformy — wszystkie trzy serwisy w jednym poleceniu.

### Krok 1: Konfiguracja środowiska

```bash
cp .env.example .env
```

Edytuj plik `.env` i ustaw prawdziwy `SECRET_KEY` (wymagane do JWT):

```ini
SECRET_KEY=wygeneruj-losowy-32-znakowy-klucz-tutaj
```

### Krok 2: Budowa i uruchomienie

```bash
docker-compose up --build
```

Po skompilowaniu obrazów dostępne będą:

| Serwis | Port | URL |
|--------|------|-----|
| Backend API | `8000` | http://localhost:8000 |
| Swagger UI | — | http://localhost:8000/docs |
| Sklep kliencki | `5173` | http://localhost:5173 |
| Panel admina | `5174` | http://localhost:5174 |

### Krok 3: Uruchomienie w tle

```bash
docker-compose up --build -d
```

### Przydatne polecenia

```bash
# Zatrzymanie wszystkich kontenerów
docker-compose down

# Podgląd logów
docker-compose logs -f

# Podgląd logów konkretnego serwisu
docker-compose logs -f backend

# Odbudowa jednego serwisu
docker-compose up -d --build frontend-shop

# Czyszczenie (usunięcie woluminów i obrazów)
docker-compose down -v
```

### Struktura plików Docker

| Plik | Przeznaczenie |
|------|---------------|
| `backend/Dockerfile` | Obraz Python 3.12-slim z FastAPI i uvicorn |
| `frontend-shop/Dockerfile` | Obraz Node 18-alpine z Vite dev server |
| `frontend-admin/Dockerfile` | Obraz Node 18-alpine z Vite dev server |
| `docker-compose.yml` | Orkiestracja 3 serwisów |
| `docker/nginx/nginx.conf` | Konfiguracja reverse proxy (dev + prod) |

---

## 🔧 Konfiguracja środowiska

### Zmienne środowiskowe

Plik `.env.example` zawiera szablon wszystkich zmiennych:

```ini
# Backend
DATABASE_URL=sqlite+aiosqlite:///./stitchcore.db
SECRET_KEY=change-this-to-a-random-secret-key-in-production
DEBUG=True
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

| Zmienna | Wymagana | Opis |
|---------|----------|------|
| `DATABASE_URL` | Tak | Connection string do bazy danych (domyślnie SQLite) |
| `SECRET_KEY` | Tak | Klucz do podpisywania tokenów JWT |
| `DEBUG` | Nie | Tryb deweloperski (`True` / `False`) |
| `CORS_ORIGINS` | Nie | Lista dozwolonych originów CORS (JSON array) |

> ⚠️ **Uwaga:** Plik `.env` NIE powinien być commitowany do repozytorium (znajduje się w `.gitignore`). Zawsze korzystaj z szablonu `.env.example`.

---

## 📡 API Endpoints

### Autoryzacja

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| `POST` | `/api/v1/auth/register` | Rejestracja nowego użytkownika | — |
| `POST` | `/api/v1/auth/login` | Logowanie (zwraca access + refresh token) | — |
| `POST` | `/api/v1/auth/refresh` | Odświeżenie access tokenu | — |
| `GET` | `/api/v1/auth/me` | Pobranie profilu bieżącego użytkownika | JWT |

### Produkty

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| `GET` | `/api/v1/products` | Lista produktów (z filtrowaniem) | — |
| `GET` | `/api/v1/products/{id}` | Szczegóły produktu z wariantami | — |
| `POST` | `/api/v1/products` | Dodanie nowego produktu | Admin |
| `PUT` | `/api/v1/products/{id}` | Edycja produktu | Admin |
| `POST` | `/api/v1/products/{id}/variants` | Dodanie wariantu (rozmiar/kolor) | Admin |
| `GET` | `/api/v1/categories` | Lista kategorii | — |
| `POST` | `/api/v1/categories` | Dodanie kategorii | Admin |

### Zamówienia

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| `GET` | `/api/v1/orders` | Lista zamówień użytkownika | JWT |
| `GET` | `/api/v1/orders/{id}` | Szczegóły zamówienia | JWT |
| `POST` | `/api/v1/orders` | Złożenie nowego zamówienia | JWT |
| `PATCH` | `/api/v1/orders/{id}/status` | Aktualizacja statusu zamówienia | Admin |

### Magazyn

| Metoda | Endpoint | Opis | Auth |
|--------|----------|------|------|
| `GET` | `/api/v1/inventory/stock` | Stan magazynowy | Admin |
| `POST` | `/api/v1/inventory/stock/adjust` | Korekta stanu magazynowego | Admin |
| `GET` | `/api/v1/inventory/locations` | Lista lokalizacji magazynowych | Admin |
| `POST` | `/api/v1/inventory/locations` | Dodanie lokalizacji magazynowej | Admin |
| `GET` | `/api/v1/inventory/movements` | Historia ruchów magazynowych | Admin |

---

## 🤖 CI/CD

Projekt zawiera konfigurację **GitHub Actions** (`.github/workflows/ci.yml`), która uruchamia się automatycznie przy pushu do `main`, `master` i `develop` oraz przy pull requestach do tych gałęzi.

### Pipeline obejmuje trzy niezależne joby:

#### Backend (Python)

- ✅ Sprawdzenie składni kodu (AST parse)
- ✅ Instalacja zależności z `requirements.txt`
- ✅ Uruchomienie serwera FastAPI
- ✅ Wykonanie testów API (`test_all.py`) z health-check pollingiem
- ✅ Czyszczenie bazy danych między uruchomieniami

#### Frontend Shop (TypeScript)

- ✅ Instalacja zależności (`npm ci`)
- ✅ Sprawdzenie typów TypeScript (`tsc --noEmit`)
- ✅ Budowa produkcyjna (`npm run build`)

#### Frontend Admin (TypeScript)

- ✅ Instalacja zależności (`npm ci`)
- ✅ Sprawdzenie typów TypeScript (`tsc --noEmit`)
- ✅ Budowa produkcyjna (`npm run build`)

### Uruchomienie testów lokalnie

```bash
# Backend — testy API
# 1. Uruchom serwer w tle
cd backend
uvicorn app.main:app --reload &
cd ..

# 2. Uruchom testy
python test_all.py

# Frontend — sprawdzenie TypeScript
cd frontend-shop && npx tsc --noEmit
cd ../frontend-admin && npx tsc --noEmit
```

---

## 🌐 Wdrożenie produkcyjne

Projekt jest gotowy do wdrożenia na serwerze VPS z wykorzystaniem **nginx** jako reverse proxy.

### Przygotowanie serwera

1. Instalacja Docker i Docker Compose na serwerze.
2. Skopiowanie projektu na serwer.
3. Konfiguracja certyfikatów SSL dla domen.

### Konfiguracja nginx

Plik `docker/nginx/nginx.conf` zawiera gotową konfigurację:

- **Tryb deweloperski** — pojedynczy serwer nasłuchujący na porcie 80, routujący na subpathy (`/api/`, `/admin/`, `/docs`).
- **Tryb produkcyjny** — osobne serwery dla subdomen z SSL/TLS:
  - `www.stitchcore.pl` → sklep kliencki
  - `api.stitchcore.pl` → backend API + Swagger
  - `admin.stitchcore.pl` → panel administracyjny

Wymagane certyfikaty SSL należy umieścić w `docker/nginx/ssl/` (ścieżka dodana do `.gitignore`).

### Zmienne produkcyjne

```ini
DEBUG=False
SECRET_KEY=<silny-klucz-64-znaki>
CORS_ORIGINS=["https://www.stitchcore.pl","https://admin.stitchcore.pl"]
```

---

## 📜 Skrypty pomocnicze

### `scripts/setup.sh`

Automatyczna konfiguracja projektu po sklonowaniu:

```bash
bash scripts/setup.sh
```

Tworzy wirtualne środowisko Python, instaluje zależności backendu oraz obu frontendów, kopiuje `.env.example` do `.env`.

### `scripts/backup.sh`

Backup bazy danych (obecnie przygotowany pod PostgreSQL — wymaga aktualizacji dla SQLite przed użyciem).

---

## 🗺️ Plan rozwoju

- [x] Podstawowa platforma e-commerce (MVP)
- [x] Panel administracyjny
- [x] Zarządzanie magazynem
- [x] Docker Compose
- [x] CI/CD (GitHub Actions)
- [ ] 🔗 Integracja z **Allegro API**
- [ ] 💳 Płatności online (**Stripe** / **Przelewy24**)
- [ ] 📦 Wysyłka (**InPost** / **DPD**)
- [ ] 📧 Powiadomienia email (**SendGrid**)
- [ ] 📊 Raporty i eksport danych (**ReportLab** / **OpenPyXL**)
- [ ] 👁️ Monitorowanie błędów (**Sentry**)
- [ ] 🗄️ Migracja na **PostgreSQL** (produkcja)
- [ ] ✅ Testy jednostkowe i integracyjne backendu
- [ ] ✅ Testy end-to-end (Cypress / Playwright)

---

## 📄 Licencja

Projekt przeznaczony wyłącznie do celów demonstracyjnych i edukacyjnych.
