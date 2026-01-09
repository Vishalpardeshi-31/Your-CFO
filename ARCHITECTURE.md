# FinMate - Visual Architecture Guide

## 🏗️ Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         FINMATE                             │
│                   Financial Management Platform             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │    Django Application (finmate/)        │
        │  ✅ Custom User Model                   │
        │  ✅ Login-Required Middleware           │
        │  ✅ Settings Configured                 │
        │  ✅ Static/Media Folders                │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
            ┌────────┐   ┌────────┐   ┌────────┐
            │accounts│   │database│   │   ...  │
            │  ✅    │   │        │   │        │
            └────────┘   └────────┘   └────────┘
```

---

## 📊 Data Flow

```
User (Unauthenticated)
    │
    ▼ (Middleware Check)
    │
    ├──► Exempt URL? ──► ALLOW (login, register, etc.)
    │
    └──► Protected? ──► REDIRECT to /accounts/login/
              │
              ▼
    User Logs In (accounts/views.py)
              │
              ▼
    CustomUser Model ✅
    (verified credentials)
              │
              ▼
    Django Session Created
              │
              ▼
    Redirects to /dashboard/
              │
              ▼
    Dashboard App
    (Can now access protected views)
```

---

## 🎯 App Relationships

```
                          CustomUser ✅
                         (accounts app)
                              │
                              │ owns
                              ▼
        ┌─────────────────────┼──────────────────┬──────────────────┐
        │                     │                  │                  │
        ▼                     ▼                  ▼                  ▼
    ┌────────┐            ┌────────┐        ┌────────┐        ┌────────┐
    │Dashboard│            │BankAccount     │ Goals  │        │AIInsight
    │ (create)│            │(transactions)  │(goals) │        │(agents)
    └────────┘            └────────┘        └────────┘        └────────┘
        │                     │                  │                  │
        ├─ Categories        ├─ Transactions   ├─ Contribution    ├─ Analysis
        ├─ Budget Tracking   ├─ Recurring      ├─ Milestones      ├─ Recommend
        └─ Analytics         └─ Statements     └─ Progress        └─ Anomalies
```

---

## 🔐 Authentication Flow

```
┌──────────────┐
│ User Request │
└──────────────┘
       │
       ▼
┌──────────────────────────┐
│ LoginRequiredMiddleware  │
├──────────────────────────┤
│ Check if user.is_auth   │
└──────────────────────────┘
       │
    ┌──┴──┐
    │     │
   YES   NO
    │     │
    ▼     ▼
┌─────┐ ┌────────────────────┐
│ OK  │ │ Check EXEMPT_URLS  │
└─────┘ └────────────────────┘
            │
         ┌──┴──┐
        YES   NO
         │     │
         ▼     ▼
      ┌─────┐ ┌──────────────────┐
      │ OK  │ │ Redirect to      │
      └─────┘ │ /accounts/login/ │
              └──────────────────┘
```

---

## 📁 Directory Tree with Status

```
finmate/
│
├── ✅ finmate/              [Project Configuration]
│   ├── ✅ settings.py       [FULLY CONFIGURED]
│   ├── ✅ middleware.py     [LOGIN MIDDLEWARE - DONE]
│   ├── urls.py             [Needs app URLs]
│   ├── wsgi.py             [Production server]
│   └── asgi.py             [Async support]
│
├── ✅ accounts/             [Authentication - CustomUser Ready]
│   ├── ✅ models.py        [CUSTOM USER CREATED ✅]
│   ├── views.py            [TODO: Create login/register views]
│   ├── urls.py             [TODO: Create URL patterns]
│   ├── forms.py            [TODO: Create auth forms]
│   ├── admin.py            [TODO: Register CustomUser]
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py [Created after first migration]
│
├── ⚪ dashboard/            [Analytics - New App]
│   ├── models.py           [TODO: Create Dashboard model]
│   ├── views.py            [TODO: Create dashboard views]
│   ├── urls.py             [TODO: Create URL patterns]
│   ├── admin.py            [TODO: Register models]
│   └── migrations/
│
├── ⚪ transactions/         [Bank Integration - New App]
│   ├── models.py           [TODO: Transaction models]
│   ├── views.py            [TODO: Upload/list views]
│   ├── parsers.py          [TODO: CSV/Excel parser]
│   ├── urls.py             [TODO: Create URL patterns]
│   ├── admin.py            [TODO: Register models]
│   └── migrations/
│
├── ⚪ goals/               [Goal Planning - New App]
│   ├── models.py           [TODO: Goal models]
│   ├── views.py            [TODO: Goal views]
│   ├── urls.py             [TODO: Create URL patterns]
│   ├── admin.py            [TODO: Register models]
│   └── migrations/
│
├── ⚪ agents/              [AI Insights - New App]
│   ├── models.py           [TODO: AIInsight models]
│   ├── views.py            [TODO: Insight views]
│   ├── ai_service.py       [TODO: AI logic]
│   ├── urls.py             [TODO: Create URL patterns]
│   ├── admin.py            [TODO: Register models]
│   └── migrations/
│
├── ✅ templates/           [HTML Templates - Organized]
│   ├── base.html           [TODO: Create base template]
│   ├── accounts/           [Ready for auth templates]
│   │   ├── login.html      [TODO]
│   │   ├── register.html   [TODO]
│   │   └── profile.html    [TODO]
│   ├── dashboard/          [Ready for dashboard templates]
│   │   └── home.html       [TODO]
│   ├── transactions/       [Ready for transaction templates]
│   │   ├── upload.html     [TODO]
│   │   └── list.html       [TODO]
│   └── goals/              [Ready for goal templates]
│       ├── create.html     [TODO]
│       └── list.html       [TODO]
│
├── ✅ static/              [Static Assets - Ready]
│   ├── css/                [Stylesheets - Ready]
│   │   └── style.css       [TODO: Create main CSS]
│   ├── js/                 [JavaScript - Ready]
│   │   └── main.js         [TODO: Create main JS]
│   └── images/             [Images - Ready]
│
├── ✅ manage.py            [Django CLI - Ready]
├── ✅ requirements.txt      [Dependencies - Ready]
├── ✅ .env.example         [Environment Template - Ready]
│
└── 📚 Documentation
    ├── ✅ README.md                 [Complete overview]
    ├── ✅ SETUP_GUIDE.md            [Implementation steps]
    ├── ✅ MODELS_ARCHITECTURE.md    [Database design]
    ├── ✅ SUMMARY.md                [Project summary]
    ├── ✅ QUICK_REFERENCE.md        [Quick reference card]
    └── ✅ ARCHITECTURE.md           [This file]
```

---

## 🛣️ User Request Flow

```
1. User visits http://localhost:8000/
                    │
                    ▼
2. Django URL Router (finmate/urls.py)
   Matches incoming URL to app-specific urls.py
                    │
                    ▼
3. Middleware Pipeline
   ┌─────────────────────────────────┐
   │ LoginRequiredMiddleware ✅      │
   │ (Checks authentication)          │
   └─────────────────────────────────┘
                    │
                    ├─ Is user authenticated? ─► NO ─► Redirect to login
                    │
                    └─ Is URL exempt? ─► YES ─► Allow
                    │
                    └─ Otherwise allow access
                    │
                    ▼
4. App-Specific URL Router (e.g., accounts/urls.py)
   Matches to specific view
                    │
                    ▼
5. View (Function or Class-Based)
   Processes request, accesses models
                    │
                    ▼
6. Model (CustomUser, Transaction, etc.)
   Queries database
                    │
                    ▼
7. Template
   Renders HTML with context data
                    │
                    ▼
8. Response sent to user
```

---

## 🔄 Database Schema Structure

```
                    SQLite (Development)
                           │
                           ▼
                    ┌──────────────┐
                    │ db.sqlite3   │
                    └──────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐        ┌────────┐        ┌────────┐
    │accounts│        │dashboard        │transaction
    │tables  │        │tables           │tables
    └────────┘        └────────┘        └────────┘
        │                  │                  │
        ├─ CustomUser     ├─ Dashboard      ├─ Transaction
        ├─ UserProfile    ├─ Category       ├─ BankAccount
        └─ Onboarding     └─ MonthlyBudget  ├─ BankStatement
                                           └─ Recurring
        ┌────────┐        ┌────────┐
        │ goals  │        │ agents │
        │tables  │        │tables  │
        └────────┘        └────────┘
        │                  │
        ├─ Goal           ├─ AIInsight
        ├─ Contribution   ├─ Analysis
        └─ Milestone      ├─ Recommend
                          └─ Anomaly
```

**Note**: Switch to PostgreSQL for production (settings.py already configured)

---

## ⚡ Settings.py Changes at a Glance

| Change | Before | After | Why |
|--------|--------|-------|-----|
| INSTALLED_APPS | 6 apps | 11 apps | Added 5 local apps |
| MIDDLEWARE | 7 items | 8 items | Added LoginRequiredMiddleware |
| TEMPLATES['DIRS'] | [] | [templates/] | Project-level templates |
| AUTH_USER_MODEL | auth.User | accounts.CustomUser | Custom fields support |
| STATIC_ROOT | Not set | staticfiles/ | Production static files |
| MEDIA_ROOT | Not set | media/ | User uploads |
| LOGIN_URL | default | accounts:login | Custom login page |
| EXEMPT_URLS | N/A | Added | Public page access |

---

## 🎨 Frontend Layer Structure

```
┌─────────────────────────────────────────┐
│          Web Browser                    │
├─────────────────────────────────────────┤
│  HTML (templates/) + CSS (static/css/)  │
│  + JavaScript (static/js/)              │
└─────────────────────────────────────────┘
              │
              │ HTTP Requests
              ▼
┌─────────────────────────────────────────┐
│        Django Application               │
├─────────────────────────────────────────┤
│ views.py (Business Logic)               │
│ ↓                                       │
│ models.py (Data Access)                 │
│ ↓                                       │
│ Database (SQLite/PostgreSQL)            │
└─────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture (Future)

```
┌──────────────────────────────────────────────────┐
│              Production Environment              │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Nginx  │──│ Gunicorn │──│ Django   │        │
│  │ (Web)  │  │(WSGI)    │  │(App)     │        │
│  └────────┘  └──────────┘  └──────────┘        │
│                                   │             │
│                                   ▼             │
│                          ┌────────────────┐    │
│                          │ PostgreSQL     │    │
│                          │ (Database)     │    │
│                          └────────────────┘    │
│                                                  │
│  ┌────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Redis  │  │ Celery   │  │ AWS S3   │        │
│  │(Cache) │  │(Tasks)   │  │(Media)   │        │
│  └────────┘  └──────────┘  └──────────┘        │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## ✅ Completion Status

| Component | Status | Details |
|-----------|--------|---------|
| Project Structure | ✅ | finmate/ with all apps |
| CustomUser Model | ✅ | Extended AbstractUser |
| Settings Configuration | ✅ | All apps registered |
| Middleware | ✅ | Login-required active |
| Templates Folder | ✅ | Organized by app |
| Static Folder | ✅ | CSS, JS, Images ready |
| Database (SQLite) | ✅ | Development ready |
| Database (PostgreSQL) | ✅ | Configured, commented |
| Documentation | ✅ | 5 comprehensive guides |
| Requirements | ✅ | All dependencies listed |

**Next Steps**: Implement models and views for each app!

---

## 📞 Quick Navigation

- **To run migrations**: See QUICK_REFERENCE.md
- **To implement views**: See SETUP_GUIDE.md
- **For database design**: See MODELS_ARCHITECTURE.md
- **For overview**: See README.md
- **For project summary**: See SUMMARY.md

---

**Your Django project is fully scaffolded and ready for development!** 🎉
