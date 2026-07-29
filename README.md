# Kanya Jewelers — Full Website + Admin Panel

A production-ready, mobile-first jewellery showcase website with a secure
admin dashboard for managing products, gallery, gold/silver rates, and
customer enquiries. **No online payments, cart, or checkout** — this is a
pure showcase + lead-generation site, as requested.

```
kanya-jewelers/
├── backend/          FastAPI + PostgreSQL REST API
│   ├── app/
│   │   ├── main.py          FastAPI app, CORS, static files, error handlers
│   │   ├── config.py        Settings (reads .env)
│   │   ├── database.py      SQLAlchemy engine/session
│   │   ├── models.py        admin, categories, products, gallery, gold_rates,
│   │   │                    silver_rates, contact_messages tables
│   │   ├── schemas.py       Pydantic request/response models
│   │   ├── auth.py          Password hashing + JWT auth
│   │   ├── storage.py       Image upload (Cloudinary or local disk)
│   │   ├── init_db.py       Creates tables + seeds admin/categories/rates
│   │   └── routers/         admin_auth, categories, products, gallery,
│   │                        rates, contact, upload
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
└── frontend/          Static HTML/CSS/JS (no build step required)
    ├── index.html, about.html, collection.html, rates.html,
    │   contact.html, gallery.html, privacy-policy.html
    ├── assets/
    │   ├── css/style.css     Gold/black/white design system, responsive
    │   └── js/
    │       ├── config.js         Shop details + API base URL — EDIT THIS
    │       ├── main.js           Shared logic (nav, API calls, rendering)
    │       └── footer-loader.js  Injects shared footer
    └── admin/
        ├── login.html
        ├── dashboard.html
        └── assets/
            ├── admin.css
            ├── admin-auth.js
            └── admin-dashboard.js
```

## 1. Backend Setup (FastAPI + PostgreSQL)

### Prerequisites
- Python 3.11+
- A PostgreSQL database (local, or a managed service like Supabase/Railway/Neon)

### Steps

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set DATABASE_URL, JWT_SECRET_KEY, DEFAULT_ADMIN_USERNAME/PASSWORD,
# ALLOWED_ORIGINS, and optionally Cloudinary credentials.

# Create tables + seed default admin, categories, and starting rates
python -m app.init_db

# Run the API (dev)
uvicorn app.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Interactive docs are at
`http://localhost:8000/docs`.

### Image Storage
- If `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`
  are set in `.env`, all uploads go to Cloudinary and only the URL is stored
  in PostgreSQL (recommended for production).
- If left blank, images are saved locally to `backend/app/static/uploads/`
  and served at `/static/uploads/...` — fine for local development, but use
  a persistent volume or Cloudinary in production (most hosting platforms
  wipe local disk on redeploy).

### Default Admin Login
Whatever you set as `DEFAULT_ADMIN_USERNAME` / `DEFAULT_ADMIN_PASSWORD` in
`.env` before running `init_db.py`. **Change the password immediately after
first login** (see "Next Steps" below — a password-change endpoint can be
added; by default, update it directly in the database or re-run seeding with
a new password before go-live).

## 2. Frontend Setup

The frontend is plain HTML/CSS/JS — no build step, no npm install required.

1. Open `frontend/assets/js/config.js` and update:
   - `API_BASE_URL` — your deployed backend URL (e.g. `https://api.kanyajewelers.com`)
   - `SHOP_PHONE_DISPLAY`, `SHOP_WHATSAPP`, `SHOP_EMAIL`, `SHOP_ADDRESS`, `SHOP_HOURS`
   - `MAP_EMBED_SRC` — replace with your shop's actual Google Maps embed URL
     (Google Maps → Share → Embed a map → copy the `src` value)
2. Serve the `frontend` folder with any static host:
   - Local preview: `cd frontend && python -m http.server 5500`
   - Production: Netlify, Vercel, GitHub Pages, S3+CloudFront, or any static host.
3. Make sure the backend's `ALLOWED_ORIGINS` env var includes your frontend's
   deployed URL, or the API will reject browser requests (CORS).

## 3. Admin Panel

- URL: `frontend/admin/login.html`
- Log in with your seeded admin credentials.
- From the dashboard you can:
  - **Products**: add/edit/delete, upload images, set category, toggle active/hidden
  - **Gallery**: upload/delete gallery images
  - **Rates**: update gold (22K/24K) and silver (per gram/kg) rates instantly
  - **Enquiries**: view and delete contact form submissions

Admin sessions use JWT tokens stored in the browser's `localStorage` and
expire after `JWT_EXPIRE_MINUTES` (default 120 minutes).

## 4. Deployment Notes

- **Backend**: A `Dockerfile` is included. Deploy to Railway, Render, Fly.io,
  or any container host. Set all variables from `.env.example` as environment
  variables on the platform — never commit `.env`.
- **Database**: Use a managed PostgreSQL instance (Supabase, Neon, Railway,
  RDS, etc.). Run `python -m app.init_db` once against the production
  database to create tables and seed initial data.
- **Frontend**: Deploy as a static site. Update `config.js` with the
  production API URL before deploying.
- **HTTPS**: Always serve both frontend and backend over HTTPS in production
  so the admin JWT token isn't sent in plaintext.

## 5. Security Checklist Before Going Live

- [ ] Change `JWT_SECRET_KEY` to a long random string
- [ ] Change the default admin password
- [ ] Set `ALLOWED_ORIGINS` to your real frontend domain only (not `*`)
- [ ] Use Cloudinary (or another cloud storage) instead of local disk in production
- [ ] Enable HTTPS on both frontend and backend
- [ ] Take regular PostgreSQL backups

## What's intentionally NOT included (per requirements)
Online payments, shopping cart, checkout, customer registration/login,
order tracking, inventory management, wishlist. This is a showcase +
lead-generation website only.
