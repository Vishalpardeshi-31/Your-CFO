# Onboarding System - Code Reference

## Quick Code Examples

### 1. Using the Survey Data in Views

```python
# In any view after login
from accounts.models import UserProfile

@login_required
def my_dashboard(request):
    user = request.user
    
    # Check if user completed onboarding
    if not user.onboarding_completed:
        return redirect('accounts:survey')
    
    # Access survey data
    try:
        profile = user.profile  # Uses related_name='profile'
        monthly_income = profile.monthly_income
        necessary_needs = profile.necessary_needs
        goals = profile.goals_and_wants
        discretionary_limit = profile.monthly_unwanted_limit
    except UserProfile.DoesNotExist:
        # Handle missing profile (shouldn't happen)
        profile = None
    
    context = {
        'profile': profile,
        'income': monthly_income,
        'expenses': necessary_needs,
    }
    return render(request, 'dashboard/home.html', context)
```

### 2. Querying Survey Data

```python
from accounts.models import CustomUser, UserProfile

# Get all onboarded users
onboarded_users = CustomUser.objects.filter(onboarding_completed=True)

# Get users by income range
high_earners = UserProfile.objects.filter(monthly_income__gte=100000)

# Get users with incomplete profiles
incomplete = CustomUser.objects.filter(onboarding_completed=False)

# Find average spending limit
from django.db.models import Avg
avg_limit = UserProfile.objects.aggregate(
    avg_limit=Avg('monthly_unwanted_limit')
)

# Get all users with their profiles
users_with_profiles = CustomUser.objects.filter(
    profile__isnull=False
).select_related('profile')
```

### 3. Template Usage

```html
<!-- Display user's financial profile -->
{% if user.onboarding_completed %}
    {% with profile=user.profile %}
    <div class="financial-summary">
        <h3>Your Financial Profile</h3>
        <p>Monthly Income: ₹{{ profile.monthly_income }}</p>
        <p>Necessary Expenses: ₹{{ profile.necessary_needs }}</p>
        <p>Spending Limit: ₹{{ profile.monthly_unwanted_limit }}</p>
        {% if profile.goals_and_wants %}
            <p>Goals: {{ profile.goals_and_wants }}</p>
        {% endif %}
        <p class="text-muted">Updated: {{ profile.updated_at }}</p>
    </div>
    {% endwith %}
{% else %}
    <p><a href="{% url 'accounts:survey' %}">Complete your profile</a></p>
{% endif %}
```

### 4. Admin Actions

```python
# In Django shell
python manage.py shell

# Mark user as onboarded (should only do via survey form normally)
from accounts.models import CustomUser, UserProfile
user = CustomUser.objects.get(email='test@example.com')
user.onboarding_completed = True
user.save()

# Check if profile exists and has data
profile = user.profile
print(f"Income: {profile.monthly_income}")
print(f"Profile updated: {profile.updated_at}")

# Get all survey responses
from accounts.models import UserProfile
for profile in UserProfile.objects.all():
    print(f"{profile.user.email}: ${profile.monthly_income}")
```

### 5. Modifying Survey Data

```python
from accounts.models import UserProfile

# Update user's profile
profile = user.profile
profile.monthly_income = 150000
profile.necessary_needs = 60000
profile.goals_and_wants = "New house by 2025"
profile.monthly_unwanted_limit = 15000
profile.save()

# Auto_now will update the 'updated_at' field automatically
print(profile.updated_at)  # Shows current timestamp
```

---

## Form Examples

### Adding Survey Form to Another Page

```python
from django import forms
from accounts.forms import FinancialSurveyForm
from accounts.models import UserProfile

class EnhancedSurveyForm(FinancialSurveyForm):
    """Extended survey form with additional fields"""
    family_members = forms.IntegerField(
        min_value=1,
        label="Number of family members",
        help_text="People dependent on your income"
    )
    
    class Meta(FinancialSurveyForm.Meta):
        fields = FinancialSurveyForm.Meta.fields + ['family_members']


# In view
def survey_with_extras(request):
    if request.method == 'POST':
        form = EnhancedSurveyForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # ... additional logic
    else:
        form = EnhancedSurveyForm(instance=request.user.profile)
    return render(request, 'survey.html', {'form': form})
```

---

## Validation & Signals

### Custom Validation in Forms

```python
from django import forms
from accounts.models import UserProfile

class ValidatedSurveyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['monthly_income', 'necessary_needs', 'goals_and_wants', 
                  'monthly_unwanted_limit']
    
    def clean(self):
        cleaned_data = super().clean()
        income = cleaned_data.get('monthly_income')
        needs = cleaned_data.get('necessary_needs')
        unwanted = cleaned_data.get('monthly_unwanted_limit')
        
        # Validation: necessary needs shouldn't exceed income
        if income and needs and needs > income:
            raise forms.ValidationError(
                "Necessary needs cannot exceed monthly income!"
            )
        
        # Validation: spending limit should be reasonable
        available = income - (needs or 0)
        if unwanted and unwanted > available:
            raise forms.ValidationError(
                "Spending limit exceeds available money after expenses!"
            )
        
        return cleaned_data
```

### Using Django Signals to Track Updates

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile, CustomUser

@receiver(post_save, sender=UserProfile)
def on_profile_update(sender, instance, created, **kwargs):
    """Log when user completes survey"""
    if created:
        print(f"New profile created for {instance.user.email}")
    else:
        print(f"Profile updated for {instance.user.email}")
        # Could send notification, trigger recommendations, etc.
```

---

## Testing Examples

### Testing the Survey Form

```python
from django.test import TestCase
from accounts.models import CustomUser, UserProfile
from accounts.forms import FinancialSurveyForm

class SurveyFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(user=self.user)
    
    def test_form_valid_data(self):
        data = {
            'monthly_income': '100000.00',
            'necessary_needs': '50000.00',
            'goals_and_wants': 'Save 1 million',
            'monthly_unwanted_limit': '10000.00'
        }
        form = FinancialSurveyForm(data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_negative_income_invalid(self):
        data = {
            'monthly_income': '-100000.00',  # Negative!
            'necessary_needs': '50000.00',
            'goals_and_wants': 'Save 1 million',
            'monthly_unwanted_limit': '10000.00'
        }
        form = FinancialSurveyForm(data, instance=self.profile)
        self.assertFalse(form.is_valid())
    
    def test_empty_form_valid(self):
        data = {
            'monthly_income': '',
            'necessary_needs': '',
            'goals_and_wants': '',
            'monthly_unwanted_limit': ''
        }
        form = FinancialSurveyForm(data, instance=self.profile)
        self.assertTrue(form.is_valid())  # All fields optional
```

### Testing the Survey View

```python
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, UserProfile

class SurveyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            onboarding_completed=False
        )
    
    def test_survey_requires_login(self):
        response = self.client.get(reverse('accounts:survey'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(response.url.endswith('/accounts/login/'))
    
    def test_survey_form_renders(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('accounts:survey'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'monthly_income')
        self.assertContains(response, 'necessary_needs')
    
    def test_survey_submission(self):
        self.client.login(email='test@example.com', password='testpass123')
        data = {
            'monthly_income': '100000',
            'necessary_needs': '50000',
            'goals_and_wants': 'Save money',
            'monthly_unwanted_limit': '10000'
        }
        response = self.client.post(reverse('accounts:survey'), data)
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Check user marked as onboarded
        self.user.refresh_from_db()
        self.assertTrue(self.user.onboarding_completed)
        
        # Check data saved
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.monthly_income, 100000)
```

---

## API/AJAX Examples

### Get User Survey Data via API

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["GET"])
@login_required
def api_get_profile(request):
    """Return user's financial profile as JSON"""
    try:
        profile = request.user.profile
        data = {
            'status': 'success',
            'profile': {
                'monthly_income': float(profile.monthly_income or 0),
                'necessary_needs': float(profile.necessary_needs or 0),
                'goals_and_wants': profile.goals_and_wants,
                'monthly_unwanted_limit': float(profile.monthly_unwanted_limit or 0),
                'updated_at': profile.updated_at.isoformat()
            }
        }
    except UserProfile.DoesNotExist:
        data = {
            'status': 'error',
            'message': 'Profile not found. Please complete survey.',
            'redirect_url': '/accounts/survey/'
        }
    return JsonResponse(data)


# JavaScript/AJAX to fetch
fetch('/api/profile/')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(data.profile.monthly_income);
        } else {
            window.location.href = data.redirect_url;
        }
    });
```

### Update Survey via API

```python
# views.py
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
@login_required
def api_update_profile(request):
    """Update user's financial profile via JSON"""
    try:
        data = json.loads(request.body)
        profile = request.user.profile
        
        if 'monthly_income' in data:
            profile.monthly_income = data['monthly_income']
        if 'necessary_needs' in data:
            profile.necessary_needs = data['necessary_needs']
        if 'monthly_unwanted_limit' in data:
            profile.monthly_unwanted_limit = data['monthly_unwanted_limit']
        if 'goals_and_wants' in data:
            profile.goals_and_wants = data['goals_and_wants']
        
        profile.full_clean()  # Validate
        profile.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Profile updated',
            'updated_at': profile.updated_at.isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
```

---

## Management Commands

### Create Custom Management Command to Analyze Surveys

```python
# accounts/management/commands/survey_analytics.py
from django.core.management.base import BaseCommand
from accounts.models import UserProfile
from django.db.models import Avg, Sum, Count, Q

class Command(BaseCommand):
    help = 'Display survey analytics'
    
    def handle(self, *args, **options):
        profiles = UserProfile.objects.all()
        
        stats = profiles.aggregate(
            total_users=Count('id'),
            avg_income=Avg('monthly_income'),
            avg_needs=Avg('necessary_needs'),
            avg_limit=Avg('monthly_unwanted_limit'),
            total_income=Sum('monthly_income'),
            total_needs=Sum('necessary_needs')
        )
        
        self.stdout.write(self.style.SUCCESS(
            f"\n=== Survey Analytics ===\n"
            f"Total Users: {stats['total_users']}\n"
            f"Avg Monthly Income: ₹{stats['avg_income']:,.0f}\n"
            f"Avg Necessary Needs: ₹{stats['avg_needs']:,.0f}\n"
            f"Avg Spending Limit: ₹{stats['avg_limit']:,.0f}\n"
            f"Total Income: ₹{stats['total_income']:,.0f}\n"
            f"Total Needs: ₹{stats['total_needs']:,.0f}\n"
        ))

# Run with: python manage.py survey_analytics
```

---

## Middleware Integration

### Creating Custom Middleware Based on Survey Status

```python
# finmate/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class OnboardingRequiredMiddleware:
    """Redirect unonboarded users to survey for specific routes"""
    
    PROTECTED_ROUTES = [
        '/dashboard/',
        '/transactions/',
        '/goals/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if accessing protected route
        if any(request.path.startswith(route) for route in self.PROTECTED_ROUTES):
            # Check if user is authenticated and not onboarded
            if request.user.is_authenticated and not request.user.onboarding_completed:
                return redirect('accounts:survey')
        
        response = self.get_response(request)
        return response
```

---

## Caching & Performance

### Cache Survey Data

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 5)  # Cache for 5 minutes
@login_required
def cached_dashboard(request):
    cache_key = f'user_profile_{request.user.id}'
    profile = cache.get(cache_key)
    
    if profile is None:
        profile = request.user.profile
        cache.set(cache_key, profile, 300)  # 5 minutes
    
    return render(request, 'dashboard.html', {'profile': profile})
```

---

## Error Handling

### Robust Profile Access

```python
def safe_get_profile(user):
    """Safely get user profile or None"""
    try:
        return user.profile
    except:
        return None

# In view
profile = safe_get_profile(request.user)
if profile:
    income = profile.monthly_income
else:
    # Handle missing profile
    messages.warning(request, "Please complete your financial profile")
    return redirect('accounts:survey')
```

---

This code reference provides common patterns for working with the onboarding system!
