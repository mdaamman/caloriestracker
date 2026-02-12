from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import UserProfile, Food, DailyFoodLog
from .forms import UserRegistrationForm, UserProfileForm, FoodLogForm, LoginForm


def home(request):
    """
    Home page - redirects to dashboard if logged in, else to login.
    """
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
    return redirect('tracker:login')


def user_signup(request):
    """
    User registration view with profile creation.
    """
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save()
            
            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Auto login after registration
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            return redirect('tracker:dashboard')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'tracker/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    """
    User login view with session-based authentication.
    """
    if request.user.is_authenticated:
        return redirect('tracker:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'tracker:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'tracker/login.html', {'form': form})


@login_required
def user_logout(request):
    """
    User logout view.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('tracker:login')


@login_required
def dashboard(request):
    """
    Main dashboard showing daily calorie goal, consumed, and remaining calories.
    """
    user = request.user
    
    # Get or create user profile
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile to see calorie goals.')
        return redirect('tracker:profile')
    
    # Get today's date
    today = timezone.now().date()
    
    # Get today's food logs
    today_logs = DailyFoodLog.objects.filter(user=user, date=today)
    
    # Calculate total calories consumed today
    total_calories_consumed = today_logs.aggregate(
        total=Sum('calories')
    )['total'] or 0
    
    # Get daily calorie target
    calorie_target = float(profile.daily_calorie_target)
    total_calories_consumed = float(total_calories_consumed)
    
    # Calculate remaining calories
    remaining_calories = calorie_target - total_calories_consumed
    remaining_calories = max(0, remaining_calories)  # Don't show negative
    
    # Calculate percentage
    percentage = (total_calories_consumed / calorie_target * 100) if calorie_target > 0 else 0
    percentage = min(100, percentage)  # Cap at 100%
    
    # Get recent food logs (last 5 entries)
    recent_logs = DailyFoodLog.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get weekly summary (last 7 days)
    week_start = today - timedelta(days=6)
    weekly_logs = DailyFoodLog.objects.filter(
        user=user,
        date__range=[week_start, today]
    ).values('date').annotate(
        total_calories=Sum('calories')
    ).order_by('date')
    
    context = {
        'profile': profile,
        'calorie_target': round(calorie_target, 2),
        'calories_consumed': round(total_calories_consumed, 2),
        'remaining_calories': round(remaining_calories, 2),
        'percentage': round(percentage, 1),
        'today_logs': today_logs,
        'recent_logs': recent_logs,
        'weekly_logs': list(weekly_logs),
        'today': today,
    }
    
    return render(request, 'tracker/dashboard.html', context)


@login_required
def profile_view(request):
    """
    View and update user profile.
    """
    user = request.user
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('tracker:dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'tracker/profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def add_food_log(request):
    """
    Add food log entry for the day.
    """
    # Check if foods exist in database
    foods_count = Food.objects.count()
    
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = request.user
            food_log.save()
            messages.success(
                request, 
                f'Added {food_log.food.name} ({food_log.quantity}g) - {food_log.calories} calories'
            )
            return redirect('tracker:dashboard')
        else:
            # Form has errors - show them
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FoodLogForm()
    
    # Get all foods grouped by category
    foods_by_category = {}
    for food in Food.objects.all().order_by('category', 'name'):
        category = food.get_category_display()
        if category not in foods_by_category:
            foods_by_category[category] = []
        foods_by_category[category].append(food)
    
    return render(request, 'tracker/add_food.html', {
        'form': form,
        'foods_by_category': foods_by_category,
        'foods_count': foods_count
    })


@login_required
def delete_food_log(request, log_id):
    """
    Delete a food log entry.
    """
    food_log = get_object_or_404(DailyFoodLog, id=log_id, user=request.user)
    
    if request.method == 'POST':
        food_log.delete()
        messages.success(request, 'Food log entry deleted successfully.')
        return redirect('tracker:dashboard')
    
    return render(request, 'tracker/delete_confirm.html', {'food_log': food_log})


@login_required
def history(request):
    """
    View food log history with date filtering.
    """
    user = request.user
    
    # Get date filter from request
    date_filter = request.GET.get('date', '')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        except ValueError:
            filter_date = timezone.now().date()
    else:
        filter_date = timezone.now().date()
    
    # Get logs for the selected date
    logs = DailyFoodLog.objects.filter(user=user, date=filter_date).order_by('-created_at')
    
    # Calculate total for the day
    total_calories = logs.aggregate(total=Sum('calories'))['total'] or 0
    
    # Get all unique dates with logs
    all_dates = DailyFoodLog.objects.filter(user=user).values_list('date', flat=True).distinct().order_by('-date')
    
    # Get weekly summary
    week_start = filter_date - timedelta(days=6)
    weekly_summary = DailyFoodLog.objects.filter(
        user=user,
        date__range=[week_start, filter_date]
    ).values('date').annotate(
        total_calories=Sum('calories'),
        entry_count=Count('id')
    ).order_by('date')
    
    context = {
        'logs': logs,
        'total_calories': round(float(total_calories), 2),
        'selected_date': filter_date,
        'all_dates': all_dates[:30],  # Show last 30 dates
        'weekly_summary': list(weekly_summary),
    }
    
    return render(request, 'tracker/history.html', context)


@login_required
def weekly_summary(request):
    """
    Detailed weekly summary view.
    """
    user = request.user
    
    # Get week range (default: current week)
    week_start_str = request.GET.get('week_start', '')
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        except ValueError:
            week_start = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
    else:
        week_start = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
    
    week_end = week_start + timedelta(days=6)
    
    # Get daily summaries
    daily_summaries_raw = DailyFoodLog.objects.filter(
        user=user,
        date__range=[week_start, week_end]
    ).values('date').annotate(
        total_calories=Sum('calories'),
        entry_count=Count('id')
    ).order_by('date')
    
    # Get user's daily target
    try:
        daily_target = float(user.profile.daily_calorie_target)
        weekly_target = daily_target * 7
    except UserProfile.DoesNotExist:
        daily_target = 0
        weekly_target = 0
    
    # Calculate difference for each day
    daily_summaries = []
    for day in daily_summaries_raw:
        total = float(day['total_calories'])
        diff = total - daily_target
        day['difference'] = round(diff, 2)
        daily_summaries.append(day)
    
    # Calculate weekly total
    weekly_total = sum(day['total_calories'] for day in daily_summaries)
    
    context = {
        'week_start': week_start,
        'week_end': week_end,
        'daily_summaries': daily_summaries,
        'weekly_total': round(weekly_total, 2),
        'weekly_target': round(weekly_target, 2),
        'daily_target': round(daily_target, 2),
    }
    
    return render(request, 'tracker/weekly_summary.html', context)
