# DevTrack System

---

## 1. Introduction

The **DevTrack System** is a web-based application designed to help ambitious students and developers manage learning, school assignments, personal projects, and ideas within a single structured platform.

Key benefits:

* Centralized dashboard connecting skills, projects, assignments, and weekly priorities.
* Improves execution clarity and reduces cognitive overload.
* Enforces structured relationships between activities for focused and measurable progress.

---

## 2. Problem Statement

Students and developers face multiple challenges:

* Disconnected tools for managing learning, assignments, projects, and ideas.
* Lack of structure leads to idea overload and low signal-to-noise ratio.
* Learning is often theoretical, not tied to practical project implementation.
* Assignments and personal projects compete for attention without clear prioritization.
* No intelligent reminder system tied to skill development and deadlines.

---

## 3. Project Objectives

The DevTrack System aims to:

* Digitally manage personal projects, academic assignments, and learning progress.
* Connect skills to real projects to enforce applied learning.
* Track deadlines and provide structured weekly priorities.
* Reduce cognitive noise by linking related tasks and goals.
* Provide reminder support for overdue assignments and inactive skills.
* Deliver a scalable, multi-user SaaS-ready backend architecture.

---

## 4. System Overview

The system provides:

* User registration and authentication.
* Project management (add, edit, track progress).
* Skill tracking with depth levels and practice history.
* Assignment tracking with deadlines.
* Idea vault for storing and evaluating product or startup ideas.
* Weekly priority generation for structured execution.
* Dashboard showing overdue tasks, inactive skills, and active projects.

---

## 5. System Users

* **Primary User:** Student / Developer
* **Future Expansion:** Admin (for system monitoring and analytics)

---

## 6. Features

* Secure JWT-based authentication (login and registration).
* Project Management Module.
* Skill Tracking Module with depth levels.
* Assignment Tracking with deadlines.
* Idea Vault for structured idea management.
* Weekly Priority Planning System.
* Dashboard summary with aggregated data.
* Reminder System (Email-based for deadlines and inactivity).

---

## 7. Technologies

**Frontend:**

* React
* Axios
* Context API

**Backend:**

* Django
* Django REST Framework
* PostgreSQL
* Simple JWT Authentication

**Background Processing (Future Enhancements):**

* Celery
* Redis

**Deployment:**

* Render
* GitHub

---

## 8. Installation (Windows Example)

1. **Clone the repository:**

```bash
git clone <repository-url>
cd DevTrack
```

2. **Set up virtual environment:**

```bash
python -m venv virtual
virtual\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```



5. **Apply migrations:**

```bash
python manage.py migrate
```

6. **Run development server:**

```bash
python manage.py runserver
```

---

## 9. Project Structure

```
DevTrack/
│
├─ core/                  # Main application models and logic
├─ dev_track/              # Django project settings
│   ├─ settings.py        # Base settings
│   └─ urls.py            # Project URLs
├─ manage.py              # Django CLI entrypoint
├─ requirements.txt       # Python dependencies
└─ .env                   # Environment variables
```

---

## 10. Future Roadmap

* Add Celery + Redis for background tasks (reminders, notifications).
* Implement React frontend with dashboards and forms.
* Expand user roles: Admins and Super Admins.
* Add analytics and reporting features.
* Deploy full SaaS version with multi-tenant support.

---

## 11. Conclusion

The **DevTrack System** provides a structured, scalable, and secure solution for managing learning, academic work, and personal development projects.

By linking skills, assignments, projects, and ideas, it improves execution discipline and reduces cognitive overload.

Its modular backend architecture ensures scalability for future SaaS deployment and demonstrates strong full-stack engineering principles suitable for academic presentation and portfolio development.

---

## 12. Author

* **Name:** Roy Mulinge
* **Email:** mutuaroymulinge@gmail.com
* **GitHub:** https://github.com/roymulinge/DevTrack.git
