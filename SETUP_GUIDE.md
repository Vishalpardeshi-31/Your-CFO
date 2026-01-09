# FinMate Django Setup Guide

## Quick Start Checklist

### ✅ Project Created
- [x] Django project `finmate` initialized
- [x] 5 apps created: accounts, dashboard, transactions, goals, agents
- [x] Project directories: templates/, static/, media/
- [x] Custom User model configured
- [x] Login-required middleware implemented
- [x] Settings.py fully configured

---

## Step-by-Step Setup Instructions

### Phase 1: Initial Setup ✅ COMPLETED

**What was done:**
1. Created Django project: `finmate`
2. Generated 5 apps with proper organization
3. Created directory structure:
   - `templates/` with subdirectories for each app
   - `static/` with css/, js/, images/ subdirectories
   - `media/` (for user uploads)
4. Configured `settings.py` with:
   - All apps registered
   - Custom middleware added
   - Static/media paths configured
   - Custom User model set as AUTH_USER_MODEL
   - Login URLs configured
5. Created custom middleware: `finmate/middleware.py`
6. Implemented CustomUser model in `accounts/models.py`

### Phase 2: Database & Migrations

**Run these commands next:**

```bash
# Create migration files for all apps
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Phase 3: Admin Configuration

**Register models in each app's `admin.py`:**

Example for `accounts/admin.py`:
```python
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'onboarding_completed', 'created_at')
    list_filter = ('onboarding_completed', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
```

### Phase 4: Create Views & Templates

**For each app, create:**
1. `urls.py` - URL routing
2. `views.py` - Business logic
3. `forms.py` - User input validation
4. Templates in `templates/[app_name]/`

**Example: accounts/urls.py**
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
```

### Phase 5: Main URL Configuration

**Edit `finmate/urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('transactions/', include('transactions.urls')),
    path('goals/', include('goals.urls')),
    path('agents/', include('agents.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 📋 App Implementation Roadmap

### 1. **accounts** App
- [ ] Create LoginView (class-based view)
- [ ] Create RegisterView with CustomUserCreationForm
- [ ] Create ProfileView for user details
- [ ] Implement password reset flow
- [ ] Create templates: login.html, register.html, profile.html
- [ ] Add onboarding completion logic

### 2. **dashboard** App
- [ ] Create Dashboard model for user preferences
- [ ] Create DashboardView
- [ ] Create ExpenseSummaryView (aggregate data)
- [ ] Create AnalyticsChartView (JSON data for charts)
- [ ] Create templates: home.html, analytics.html
- [ ] Integrate Chart.js or Plotly for visualizations

### 3. **transactions** App
- [ ] Create Transaction model
- [ ] Create BankStatement model
- [ ] Create FileUploadView (CSV/Excel support)
- [ ] Implement CSV/Excel parser in parsers.py
- [ ] Create TransactionListView with filtering
- [ ] Create TransactionDetailView
- [ ] Create templates: upload.html, list.html, detail.html
- [ ] Add transaction categorization logic

### 4. **goals** App
- [ ] Create Goal model (name, target_amount, deadline, category)
- [ ] Create GoalProgress model for tracking
- [ ] Create GoalCreateView
- [ ] Create GoalDetailView with progress chart
- [ ] Create GoalListView with filtering by status
- [ ] Create templates: create.html, list.html, detail.html
- [ ] Implement progress calculation logic

### 5. **agents** App
- [ ] Create AIInsight model
- [ ] Create InsightView to display AI-generated insights
- [ ] Implement ai_service.py with analysis functions
- [ ] Create recommendation engine logic
- [ ] Create alert system for unusual transactions
- [ ] Create spending pattern analyzer
- [ ] Create templates: insights.html, recommendations.html

---

## 🔑 Key Configuration Files

### settings.py Changes Made:

1. **INSTALLED_APPS**
   ```python
   INSTALLED_APPS = [
       # Django apps
       'django.contrib.admin',
       'django.contrib.auth',
       # ... other apps ...
       # Local apps
       'accounts',
       'dashboard',
       'transactions',
       'goals',
       'agents',
   ]
   ```

2. **MIDDLEWARE**
   ```python
   MIDDLEWARE = [
       # ... other middleware ...
       'finmate.middleware.LoginRequiredMiddleware',
   ]
   ```

3. **AUTH_USER_MODEL**
   ```python
   AUTH_USER_MODEL = 'accounts.CustomUser'
   ```

4. **TEMPLATES DIRS**
   ```python
   'DIRS': [BASE_DIR / 'templates'],
   ```

5. **STATIC & MEDIA**
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_DIRS = [BASE_DIR / 'static']
   
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

6. **LOGIN SETTINGS**
   ```python
   LOGIN_URL = 'accounts:login'
   LOGIN_REDIRECT_URL = 'dashboard:home'
   LOGOUT_REDIRECT_URL = 'accounts:login'
   
   EXEMPT_URLS = [
       r'^accounts/login/$',
       r'^accounts/register/$',
       r'^accounts/forgot-password/$',
   ]
   ```

---

## 🗄️ Database Migration Strategy

### For Development (SQLite - Current Setup)
```bash
python manage.py makemigrations
python manage.py migrate
```

### For Production (PostgreSQL)

1. **Install PostgreSQL**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Create PostgreSQL database**:
   ```bash
   createdb finmate_db
   ```

3. **Update settings.py** (uncomment PostgreSQL section):
   ```python
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

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

---

## 🧪 Testing the Setup

### Run Django Check
```bash
python manage.py check
```

### Run Development Server
```bash
python manage.py runserver
```

### Access Points
- Main App: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- Login (once implemented): http://localhost:8000/accounts/login/

---

## 📦 Dependency Management

Install all dependencies:
```bash
pip install -r requirements.txt
```

**Key packages included:**
- `django==6.0` - Web framework
- `pillow` - Image handling (profile pictures)
- `psycopg2-binary` - PostgreSQL adapter
- `djangorestframework` - API support
- `django-cors-headers` - CORS support
- `pandas` - Data analysis (transactions)
- `openpyxl` - Excel file support
- `celery` - Async tasks (AI agents)
- `redis` - Task broker

---

## ⚙️ Environment Variables

Use `.env.example` as a template:
```bash
cp .env.example .env
```

**Important variables to configure:**
- `SECRET_KEY` - Change for production
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Add your domain
- `DATABASE_URL` - For PostgreSQL
- `EMAIL_*` - For email notifications
- `OPENAI_API_KEY` - For AI features

---

## 🚀 Deployment Checklist

Before deploying to production:
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Update SECRET_KEY
- [ ] Configure PostgreSQL database
- [ ] Set up email configuration
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure AWS S3 or CDN for media
- [ ] Set up SSL/HTTPS
- [ ] Configure Gunicorn/uWSGI
- [ ] Set up Celery for background tasks
- [ ] Configure logging
- [ ] Run security checks: `python manage.py check --deploy`

---

## 📞 Troubleshooting

### CustomUser Model Not Applied
- Delete `db.sqlite3` and migrations (except __init__.py)
- Run: `python manage.py makemigrations accounts`
- Run: `python manage.py migrate`

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Login Middleware Redirect Loop
- Check EXEMPT_URLS configuration
- Verify LOGIN_URL is in EXEMPT_URLS
- Check URL patterns match exactly

### Migration Conflicts
```bash
python manage.py migrate --fake accounts zero
python manage.py migrate accounts
```

---

**Your Django project is ready! Start building the views and templates.** 🎉
