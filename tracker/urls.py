from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard and main features
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Food logging
    path('add-food/', views.add_food_log, name='add_food'),
    path('delete-log/<int:log_id>/', views.delete_food_log, name='delete_log'),
    
    # History and reports
    path('history/', views.history, name='history'),
    path('weekly-summary/', views.weekly_summary, name='weekly_summary'),
]
