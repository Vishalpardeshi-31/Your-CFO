from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, FinancialSurveyForm
from .models import UserProfile


def signup_view(request):
	"""Handle user registration (signup)."""
	if request.user.is_authenticated:
		return redirect('dashboard:home')

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Account created successfully. Complete your financial profile.')
			return redirect('accounts:survey')
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(DjangoLoginView):
	"""
	Custom login view that checks onboarding status.
	Redirects to survey if user hasn't completed onboarding.
	"""
	template_name = 'accounts/login.html'
	redirect_authenticated_user = True

	def get_success_url(self):
		"""Check if user has completed onboarding, redirect accordingly."""
		if not self.request.user.onboarding_completed:
			return '/accounts/survey/'
		return '/dashboard/'


@login_required(login_url='accounts:login')
@require_http_methods(['GET', 'POST'])
def survey_view(request):
	"""
	Financial survey form for onboarding.
	Collects monthly income, necessary needs, goals, and spending limit.
	"""
	# If already onboarded, redirect to dashboard
	if request.user.onboarding_completed:
		return redirect('dashboard:home')

	# Get or create user profile
	profile, created = UserProfile.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		form = FinancialSurveyForm(request.POST, instance=profile)
		if form.is_valid():
			profile = form.save()
			# Mark onboarding as completed
			request.user.onboarding_completed = True
			request.user.save()
			messages.success(request, 'Financial profile completed! Welcome to FinMate.')
			return redirect('dashboard:home')
	else:
		form = FinancialSurveyForm(instance=profile)

	return render(request, 'accounts/survey.html', {'form': form})


class CustomLogoutView(DjangoLogoutView):
	"""Custom logout view that redirects to signup page"""
	next_page = 'accounts:signup'
