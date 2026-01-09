from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('email', 'first_name', 'last_name', 'onboarding_completed', 'is_staff')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
		('Onboarding', {'fields': ('onboarding_completed',)}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	model = UserProfile
	list_display = ('user', 'monthly_income', 'necessary_needs', 'monthly_unwanted_limit', 'created_at')
	search_fields = ('user__email',)
	readonly_fields = ('created_at', 'updated_at')
	fieldsets = (
		('User', {'fields': ('user',)}),
		('Financial Data', {
			'fields': ('monthly_income', 'necessary_needs', 'monthly_unwanted_limit', 'goals_and_wants'),
		}),
		('Metadata', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
	)
