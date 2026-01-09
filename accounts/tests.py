from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from accounts.forms import SignUpForm, LoginForm

User = get_user_model()


class CustomUserModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating a user with email as username."""
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_email_unique(self):
        """Test that email is unique."""
        User.objects.create_user(email='test@example.com', password='testpass123')
        with self.assertRaises(Exception):
            User.objects.create_user(email='test@example.com', password='testpass456')

    def test_user_str_returns_email(self):
        """Test __str__ returns email."""
        user = User.objects.create_user(email='john@example.com', password='testpass123')
        self.assertEqual(str(user), 'john@example.com')


class SignUpFormTests(TestCase):
    def test_signup_form_valid(self):
        """Test valid signup form."""
        form = SignUpForm(data={
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_password_mismatch(self):
        """Test signup form with mismatched passwords."""
        form = SignUpForm(data={
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_duplicate_email(self):
        """Test signup form rejects duplicate email."""
        User.objects.create_user(email='test@example.com', password='testpass123')
        form = SignUpForm(data={
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LoginFormTests(TestCase):
    def test_login_form_uses_email(self):
        """Test that LoginForm uses email field."""
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertEqual(form.fields['username'].label, 'Email')


# Override middleware to exclude LoginRequiredMiddleware for auth view tests
NO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


@override_settings(MIDDLEWARE=NO_MIDDLEWARE)
class SignupViewTests(TestCase):
    def test_signup_view_get(self):
        """Test GET request to signup view."""
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_signup_view_post_valid(self):
        """Test POST with valid signup data."""
        response = self.client.post('/accounts/signup/', data={
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        # Check user is logged in (redirected to survey for onboarding)
        self.assertRedirects(response, '/accounts/survey/')

    def test_signup_view_post_invalid(self):
        """Test POST with invalid signup data."""
        response = self.client.post('/accounts/signup/', data={
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

    def test_signup_view_authenticated_redirects(self):
        """Test that authenticated users are redirected to dashboard."""
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get('/accounts/signup/')
        self.assertRedirects(response, '/')


@override_settings(MIDDLEWARE=NO_MIDDLEWARE)
class LoginViewTests(TestCase):
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')

    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_valid(self):
        """Test POST with valid login credentials."""
        response = self.client.post('/accounts/login/', data={
            'username': 'test@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        # Unonboarded user redirects to survey
        self.assertRedirects(response, '/accounts/survey/')

    def test_login_view_post_invalid(self):
        """Test POST with invalid credentials."""
        response = self.client.post('/accounts/login/', data={
            'username': 'test@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_authenticated_user_redirected(self):
        """Test that unonboarded authenticated users are redirected to survey."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get('/accounts/login/')
        # Unonboarded user redirects to survey
        self.assertRedirects(response, '/accounts/survey/')


@override_settings(MIDDLEWARE=NO_MIDDLEWARE)
class LogoutViewTests(TestCase):
    def setUp(self):
        """Create and log in a test user."""
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.client.login(username='test@example.com', password='testpass123')

    def test_logout_view(self):
        """Test logout removes session."""
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        # After logout, user should not be authenticated
        response2 = self.client.get('/')
        self.assertFalse(response2.wsgi_request.user.is_authenticated)


@override_settings(MIDDLEWARE=NO_MIDDLEWARE)
class SurveyViewTests(TestCase):
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')

    def test_survey_view_requires_login(self):
        """Test that survey view requires authentication."""
        response = self.client.get('/accounts/survey/')
        # Should redirect to login since not authenticated
        self.assertEqual(response.status_code, 302)

    def test_survey_view_get_unonboarded(self):
        """Test GET request to survey view for unonboarded user."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get('/accounts/survey/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/survey.html')

    def test_survey_view_post_valid(self):
        """Test POST with valid survey data."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.post('/accounts/survey/', data={
            'monthly_income': '50000',
            'necessary_needs': '30000',
            'goals_and_wants': 'Car: 500000 by Dec 2026',
            'monthly_unwanted_limit': '5000',
        })
        self.assertEqual(response.status_code, 302)
        # Redirect to dashboard (root path)
        self.assertRedirects(response, '/')
        # Check user is now onboarded
        self.user.refresh_from_db()
        self.assertTrue(self.user.onboarding_completed)

    def test_survey_view_skip_if_onboarded(self):
        """Test that survey redirects to dashboard if already onboarded."""
        self.user.onboarding_completed = True
        self.user.save()
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get('/accounts/survey/')
        # Redirect to dashboard (root path)
        self.assertRedirects(response, '/')
