from django.contrib import admin
from .models import UserProfile, Food, DailyFoodLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ['user', 'age', 'gender', 'height', 'weight', 'activity_level', 'daily_calorie_target', 'created_at']
    list_filter = ['gender', 'activity_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['daily_calorie_target', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Physical Attributes', {
            'fields': ('age', 'gender', 'height', 'weight')
        }),
        ('Activity & Calories', {
            'fields': ('activity_level', 'daily_calorie_target')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    """
    Admin interface for Food model.
    Allows admins to add/edit/delete food items.
    """
    list_display = ['name', 'category', 'calories_per_100g', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'category']
    ordering = ['category', 'name']
    
    fieldsets = (
        ('Food Information', {
            'fields': ('name', 'category', 'calories_per_100g')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DailyFoodLog)
class DailyFoodLogAdmin(admin.ModelAdmin):
    """
    Admin interface for DailyFoodLog model.
    """
    list_display = ['user', 'food', 'quantity', 'calories', 'date', 'created_at']
    list_filter = ['date', 'created_at', 'food__category']
    search_fields = ['user__username', 'food__name']
    readonly_fields = ['calories', 'created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Log Information', {
            'fields': ('user', 'food', 'quantity', 'date')
        }),
        ('Calculated Values', {
            'fields': ('calories',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'food')
