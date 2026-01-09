# FinMate - Django Financial Management Platform

A comprehensive Django application for personal financial management with AI-powered insights, expense tracking, and future goal planning.

## 🚀 Quick Start

**New to the project?** Start here:
- 📖 **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Overview of the financial onboarding system (20 tests passing ✅)
- 📚 **[ONBOARDING.md](ONBOARDING.md)** - Complete documentation of the survey system, architecture, and user flow

## Project Overview

**FinMate** is built with Django and structured as a modular, scalable financial management platform. The project includes:
- ✅ **Financial Onboarding Survey** - Collects monthly income, necessary expenses, goals, and spending limits on first login
- 🔐 **Custom Email-based Authentication** - CustomUser model with email login instead of username
- 📊 **Expense Analytics** - Dashboard with spending insights
- 💳 **Transaction Management** - Bank statement upload and parsing
- 🎯 **Goal Planning** - Future financial goal tracking
- 🤖 **AI Insights** - Powered financial recommendations

---

## 📁 Project Structure

```
finmate/
├── finmate/                    # Project configuration (Django settings)
│   ├── __init__.py
│   ├── settings.py             # Django settings (configured below)
│   ├── urls.py                 # Main URL router
│   ├── asgi.py                 # ASGI config (async)
│   ├── wsgi.py                 # WSGI config (production)
│   └── middleware.py           # Custom login-required middleware
│
├── accounts/                   # User authentication & onboarding
│   ├── migrations/
│   ├── models.py               # CustomUser model
│   ├── views.py                # Login, register, profile views
│   ├── urls.py                 # Auth URL routes
│   ├── forms.py                # Custom user forms
│   ├── admin.py                # Admin configuration
│   └── apps.py
│
├── dashboard/                  # Expense overview & analytics
│   ├── migrations/
│   ├── models.py               # Dashboard data models
│   ├── views.py                # Dashboard, analytics views
│   ├── urls.py                 # Dashboard URL routes
│   ├── admin.py
│   └── apps.py
│
├── transactions/               # Bank statement upload & parsing
│   ├── migrations/
│   ├── models.py               # Transaction, BankStatement models
│   ├── views.py                # Upload, parsing, listing views
│   ├── urls.py                 # Transaction URL routes
│   ├── parsers.py              # CSV/Excel parsing logic
│   ├── admin.py
│   └── apps.py
│
├── goals/                      # Future goal planning
│   ├── migrations/
│   ├── models.py               # Goal, GoalProgress models
│   ├── views.py                # Goal creation, tracking views
│   ├── urls.py                 # Goals URL routes
│   ├── admin.py
│   └── apps.py
│
├── agents/                     # AI insight agents
│   ├── migrations/
│   ├── models.py               # AIInsight, Agent models
│   ├── views.py                # AI insights views
│   ├── urls.py                 # Agents URL routes
│   ├── ai_service.py           # AI/ML integration logic
│   ├── admin.py
│   └── apps.py
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template (nav, footer)
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── dashboard/
│   │   └── home.html
│   ├── transactions/
│   │   ├── upload.html
│   │   └── list.html
│   └── goals/
│       ├── create.html
│       └── list.html
│
├── static/                     # Static files
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Images & icons
│
├── media/                      # User uploaded files (created at runtime)
│   └── profile_pictures/
│
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database (development only)
└── requirements.txt            # Python dependencies
```

---

## 🔧 Key Configuration Changes in `settings.py`

### 1. **Installed Apps**
Added all local apps to the Django project:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'accounts',
    'dashboard',
    'transactions',
    'goals',
    'agents',
]
```

### 2. **Custom User Model**
Configured Django to use a custom user model instead of the default:
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```
**Benefit**: Allows adding financial fields to the user profile without creating separate models.

### 3. **Database Configuration**
**Development (SQLite - Default)**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL - Commented)**:
```python
# Uncomment and configure for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finmate_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. **Login-Required Middleware**
Added custom middleware to require login for protected views:
```python
MIDDLEWARE = [
    # ... other middleware ...
    'finmate.middleware.LoginRequiredMiddleware',
]

# Exempt URLs that don't require login
EXEMPT_URLS = [
    r'^accounts/login/$',
    r'^accounts/register/$',
    r'^accounts/forgot-password/$',
    r'^admin/login/$',
]
```

### 5. **Templates Configuration**
Updated to point to the project-level templates directory:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Added this line
        'APP_DIRS': True,
        # ...
    }
]
```

### 6. **Static & Media Files**
```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 7. **Login Settings**
```python
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'accounts:login'
```

---

## 📦 Apps Overview

### **accounts** - Authentication & Onboarding
- User registration and login
- Profile management
- Onboarding flow
- **CustomUser Model** includes:
  - Extended fields: phone_number, profile_picture, bio
  - Tracking: onboarding_completed status
  - Timestamps: created_at, updated_at

### **dashboard** - Expense Overview & Analytics
- Personal financial dashboard
- Expense summaries and charts
- Monthly/yearly analytics
- Budget vs. actual comparisons

### **transactions** - Bank Statement Upload & Parsing
- CSV/Excel file upload support
- Automatic transaction parsing
- Transaction categorization
- Statement management

### **goals** - Future Goal Planning
- Create and manage financial goals
- Goal progress tracking
- Target amount and deadline management
- Goal achievement analytics

### **agents** - AI Insight Agents
- Automated financial insights
- Spending pattern analysis
- Recommendations engine
- Alert system for unusual activity

---

## 🚀 Getting Started

### 1. **Install Dependencies**
```bash
pip install django pillow psycopg2-binary
```

### 2. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. **Create Superuser**
```bash
python manage.py createsuperuser
```

### 4. **Run Development Server**
```bash
python manage.py runserver
```

### 5. **Access the Application**
- **Main App**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

---

## 🔐 Security Features

1. **Login-Required Middleware**: All views require authentication (except exempted URLs)
2. **Custom User Model**: Allows for future security enhancements
3. **CSRF Protection**: Enabled by default
4. **Password Validation**: Django's built-in validators configured
5. **Environment Variables**: Secret key should be moved to `.env` for production

---

## 📝 CustomUser Model Fields

| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique identifier |
| email | EmailField | User email |
| first_name | CharField | First name |
| last_name | CharField | Last name |
| phone_number | CharField | Contact number |
| profile_picture | ImageField | Avatar/profile image |
| date_of_birth | DateField | User's birthday |
| bio | TextField | User biography |
| onboarding_completed | BooleanField | Onboarding status |
| created_at | DateTimeField | Account creation timestamp |
| updated_at | DateTimeField | Last update timestamp |

---

## 🔄 Migration Path to PostgreSQL

To switch from SQLite to PostgreSQL:

1. **Install PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update `settings.py` DATABASES setting** (uncomment the PostgreSQL section)

3. **Create PostgreSQL database**:
   ```bash
   createdb finmate_db
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

---

## 📚 Next Steps

1. Create URL configurations for each app
2. Implement views and templates
3. Build forms for data entry
4. Configure admin panels for each app
5. Add static files (CSS, JavaScript)
6. Implement AI/ML features in the agents app
7. Set up testing suite
8. Configure production settings

---

## 🛠 Development Tips

- Use Django shell for testing: `python manage.py shell`
- Check migrations status: `python manage.py showmigrations`
- Create fixtures for test data: `python manage.py dumpdata > fixture.json`
- Run Django checks: `python manage.py check`

---

**Ready to build! Start implementing views and templates for each app.**