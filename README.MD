# DevTrack — Backend API

> REST API powering the DevTrack productivity system. Built with Django REST Framework and PostgreSQL.

**Frontend Repo:** [DevTrack Frontend](https://github.com/roymulinge/DevTrack) · **Author:** [Roy Mulinge](https://github.com/roymulinge)

---

## What Is DevTrack?

DevTrack is a productivity system for developers and students. It replaces fragmented tools (Notion, spreadsheets, GitHub issues, notes apps) with one structured platform where skills, projects, assignments, and ideas are all linked together.

This repo is the Django backend — a fully documented REST API with JWT authentication, serving the React frontend.

---

## Features

- **JWT Authentication** — Secure login, registration, and silent token refresh
- **Project Management** — Full CRUD with skills linked to each project
- **Skill Tracking** — Depth levels, practice history, inactivity detection
- **Assignment Tracking** — Deadlines, status progression, overdue flagging
- **Idea Vault** — Store and score startup/product ideas with complexity ratings
- **Weekly Priority Planning** — Structured execution planning per week
- **Dashboard Aggregation** — Single endpoint surfacing active projects, overdue assignments, inactive skills
- **SaaS-ready architecture** — Multi-user, modular, built to scale

---

## Tech Stack

```
Python 3.11+          — Language
Django 4.x            — Web framework
Django REST Framework — API layer
PostgreSQL            — Primary database
Simple JWT            — Authentication tokens
```

**Planned additions:**
```
Celery + Redis        — Background tasks, email reminders, notifications
```

---

## API Overview

| Resource | Endpoints |
|---|---|
| Auth | `POST /api/auth/register/` `POST /api/auth/login/` `POST /api/auth/refresh/` |
| Projects | `GET POST /api/projects/` · `GET PUT DELETE /api/projects/:id/` |
| Skills | `GET POST /api/skills/` · `GET PUT DELETE /api/skills/:id/` |
| Assignments | `GET POST /api/assignments/` · `GET PUT DELETE /api/assignments/:id/` |
| Ideas | `GET POST /api/ideas/` · `GET PUT DELETE /api/ideas/:id/` |
| Planning | `GET POST /api/planning/` |
| Dashboard | `GET /api/dashboard/` |

All endpoints (except auth) require a valid JWT access token in the `Authorization: Bearer <token>` header.

---

## Project Structure

```
DevTrack/
├── core/                  # Main app — models, views, serializers, URLs
├── dev_track/
│   ├── settings.py        # Project settings
│   └── urls.py            # Root URL configuration
├── manage.py              # Django CLI entrypoint
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not committed)
```

---

## Getting Started

**Prerequisites**
- Python 3.11+
- PostgreSQL running locally

```bash
# Clone the repo
git clone https://github.com/roymulinge/DevTrack.git
cd DevTrack

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in your database credentials and secret key

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

**Environment Variables**
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/devtrack
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Authentication Flow

1. `POST /api/auth/register/` → creates user, returns tokens
2. `POST /api/auth/login/` → returns `access` + `refresh` tokens
3. Client attaches `access` token to every request header
4. On expiry → `POST /api/auth/refresh/` silently returns a new access token
5. No session cookies — fully stateless JWT authentication

---

## Deployment

Backend is designed to deploy on **Render** (free tier available).

1. Connect your GitHub repo to [render.com](https://render.com)
2. Set environment variables in Render dashboard
3. Set build command: `pip install -r requirements.txt && python manage.py migrate`
4. Set start command: `gunicorn dev_track.wsgi`

---

## Roadmap

- [ ] Celery + Redis for email reminders and deadline notifications
- [ ] Admin dashboard for system monitoring
- [ ] Analytics endpoints — learning velocity, project completion rates
- [ ] Multi-tenant support for full SaaS deployment
- [ ] WebSocket support for real-time notifications

---

## Author

**Roy Mulinge**
[GitHub](https://github.com/roymulinge) · [LinkedIn](https://www.linkedin.com/in/roy-mulinge-4b6a80251) · mutuaroymulinge@gmail.com

---

*ISC License — see LICENSE for details.*
