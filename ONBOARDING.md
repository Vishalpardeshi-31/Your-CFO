# Financial Onboarding System

## Overview

The FinMate application implements a **mandatory financial survey during user onboarding**. After signup or first login, users are required to complete a financial profile before accessing the dashboard.

## Features

### 1. **Automatic Onboarding Trigger**
- **After Signup**: User is automatically logged in and redirected to the survey form
- **After First Login**: Unonboarded users are redirected to the survey instead of the dashboard
- **Skip on Re-login**: Once `onboarding_completed = True`, users go directly to the dashboard

### 2. **Financial Survey Form**
Users are asked to provide:

| Field | Type | Description |
|-------|------|-------------|
| Monthly Income | Decimal | Total monthly income from all sources |
| Necessary Needs | Decimal | Fixed expenses (rent, EMI, groceries, utilities) |
| Goals & Wants | Text | Financial goals (e.g., "Car: 500000 by Dec 2026") |
| Monthly Unwanted Limit | Decimal | Budget for discretionary spending |

### 3. **Data Persistence**
- Survey data is stored in the `UserProfile` model (OneToOne relationship with CustomUser)
- Each field is optional to allow incremental completion
- Timestamps track when profile was created/updated

## Architecture

### Models

#### CustomUser (Extended)
```python
onboarding_completed = BooleanField(default=False)
```
- Tracks if user has completed the financial survey
- Set to `True` after successful survey submission

#### UserProfile (New)
```python
class UserProfile(models.Model):
    user = OneToOneField(CustomUser, on_delete=CASCADE)
    monthly_income = DecimalField(max_digits=12, decimal_places=2)
    necessary_needs = DecimalField(max_digits=12, decimal_places=2)
    goals_and_wants = TextField()
    monthly_unwanted_limit = DecimalField(max_digits=12, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Views

#### `survey_view` (GET/POST)
- **Route**: `/accounts/survey/`
- **Login Required**: Yes (decorated with `@login_required`)
- **GET**: Renders survey form (pre-populated if profile exists)
- **POST**: Saves survey data and marks user as onboarded

#### `CustomLoginView` (Class-based)
- **Route**: `/accounts/login/`
- **Extends**: Django's `LoginView`
- **Custom Logic**: Checks `user.onboarding_completed` in `get_success_url()`
  - If `False` → redirects to `/accounts/survey/`
  - If `True` → redirects to `/dashboard/`

### Forms

#### FinancialSurveyForm
- Extends Django's `ModelForm` (uses UserProfile model)
- Validates non-negative values (MinValueValidator)
- Provides helpful placeholders and help text

### URLs

```python
path('survey/', views.survey_view, name='survey'),
```

## User Flow

### 1. New User Signup Flow
```
Signup Page → Enter email/password → Create Account
    ↓
Auto-login → Redirect to Survey Form
    ↓
Fill Financial Profile → Submit
    ↓
Set onboarding_completed=True → Redirect to Dashboard
```

### 2. Returning User Login Flow (First Time)
```
Login Page → Enter credentials → Authenticate
    ↓
Check onboarding_completed flag
    ↓
If False → Redirect to Survey
If True → Redirect to Dashboard
```

### 3. Subsequent Logins
```
Login Page → Enter credentials → Authenticate
    ↓
onboarding_completed=True → Direct to Dashboard (no survey)
```

## Database Schema

### UserProfile Table
```sql
CREATE TABLE accounts_userprofile (
    id BIGINT PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL REFERENCES customuser(id),
    monthly_income DECIMAL(12,2),
    necessary_needs DECIMAL(12,2),
    goals_and_wants TEXT,
    monthly_unwanted_limit DECIMAL(12,2),
    created_at DATETIME,
    updated_at DATETIME
);
```

## Testing

### Test Coverage (20 tests total)
- **CustomUserModel**: Email-based auth, unique email, __str__ method
- **SignUpForm**: Valid/invalid forms, duplicate email rejection
- **LoginForm**: Email field configuration
- **SignupView**: GET/POST flow, authenticated redirects
- **LoginView**: Valid/invalid credentials, onboarded user redirect
- **LogoutView**: Session removal
- **SurveyView**: 
  - Requires authentication
  - GET renders form for unonboarded users
  - POST saves data and sets onboarding_completed
  - Skips survey for already-onboarded users

### Running Tests
```bash
python manage.py test accounts --verbosity=2
```

## Implementation Details

### Middleware Integration
The survey route (`/accounts/survey/`) is exempt from `LoginRequiredMiddleware`:

```python
EXEMPT_URLS = [
    r'^/accounts/login/',
    r'^/accounts/signup/',
    r'^/accounts/survey/',
    ...
]
```

This allows the view's own `@login_required` decorator to handle authentication, preventing double redirects.

### Form Validation
- All fields except goals_and_wants are numeric (DecimalField)
- Values must be non-negative (MinValueValidator)
- Email-style placeholders guide users
- Error messages display field-specific validation results

### Data Preservation
- UserProfile is created on first survey visit (get_or_create)
- Existing data is pre-populated in the form
- Users can update their profile by revisiting survey (if needed)

## Security Considerations

1. **Authentication Required**: Survey view enforces login via `@login_required`
2. **CSRF Protection**: Form includes `{% csrf_token %}`
3. **User Isolation**: Each user only accesses their own profile (OneToOne relationship)
4. **No Privilege Escalation**: Onboarding status doesn't grant admin/staff access

## Future Enhancements

1. **Partial Completion**: Allow users to save progress without completing all fields
2. **Profile Editing**: Let users update their financial profile later
3. **Financial Recommendations**: Show insights based on survey data
4. **Category Spending**: Allow users to set different spending limits by category
5. **Email Verification**: Require email confirmation before dashboard access
6. **KYC Integration**: Add identity verification as part of onboarding

## Admin Interface

- **CustomUserAdmin**: Displays onboarding status in list view
- **UserProfileAdmin**: Shows financial data with read-only timestamps
- Easy filtering by email and date created

## Configuration

All settings are in `finmate/settings.py`:

```python
EXEMPT_URLS = [
    r'^/accounts/login/',
    r'^/accounts/signup/',
    r'^/accounts/survey/',
    ...
]

LOGIN_REDIRECT_URL = 'dashboard:home'
LOGIN_URL = 'accounts:login'
```

## Troubleshooting

### User gets stuck in redirect loop
- **Cause**: EXEMPT_URLS not configured correctly
- **Solution**: Ensure `/accounts/survey/` matches the regex pattern

### Survey data not saving
- **Cause**: Form validation failing
- **Solution**: Check browser console for form errors, verify number formats

### User marked as onboarded but survey not filled
- **Cause**: Direct database update
- **Solution**: Both `onboarding_completed` AND UserProfile data should be present

## File Structure
```
accounts/
  ├── models.py          # CustomUser + UserProfile
  ├── forms.py           # FinancialSurveyForm
  ├── views.py           # CustomLoginView, survey_view
  ├── urls.py            # survey route
  ├── admin.py           # UserProfileAdmin
  └── tests.py           # SurveyViewTests (4 tests)

templates/
  └── accounts/
      └── survey.html    # Survey form template
```
