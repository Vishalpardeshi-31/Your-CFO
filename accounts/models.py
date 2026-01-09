from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from django.core.validators import MinValueValidator


class CustomUserManager(DefaultUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email as username."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with email as username."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses email as the unique identifier for authentication.
    """
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="User's contact phone number"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True,
        help_text="User biography"
    )
    onboarding_completed = models.BooleanField(
        default=False,
        help_text="Tracks if user has completed onboarding"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name() or self.email}"


class UserProfile(models.Model):
    """
    User profile storing financial survey and onboarding data.
    Created after user completes the initial financial survey.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Financial Survey Data
    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="User's monthly income in currency"
    )
    necessary_needs = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Monthly expenses for rent, EMI, groceries, etc."
    )
    goals_and_wants = models.TextField(
        blank=True,
        help_text="User's goals and wants (JSON format or text)"
    )
    monthly_unwanted_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Monthly limit for unwanted/discretionary spending"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"Profile for {self.user.email}"
