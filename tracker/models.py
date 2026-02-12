from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class UserProfile(models.Model):
    """
    User Profile model to store user's physical attributes and calculate daily calorie needs.
    Uses Mifflin-St Jeor equation for BMR calculation (more accurate than Harris-Benedict).
    """
    
    # Activity level choices for calorie calculation
    ACTIVITY_LEVELS = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Lightly active (light exercise 1-3 days/week)'),
        ('moderate', 'Moderately active (moderate exercise 3-5 days/week)'),
        ('active', 'Very active (hard exercise 6-7 days/week)'),
        ('very_active', 'Extra active (very hard exercise & physical job)'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='sedentary')
    daily_calorie_target = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def calculate_bmr(self):
        """
        Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
        BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(years) + s
        where s = +5 for males, -161 for females
        """
        weight = float(self.weight)
        height = float(self.height)
        age = self.age
        
        if self.gender == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        return round(bmr, 2)
    
    def calculate_daily_calorie_needs(self):
        """
        Calculate daily calorie needs based on BMR and activity level.
        Uses activity multipliers:
        - Sedentary: BMR * 1.2
        - Light: BMR * 1.375
        - Moderate: BMR * 1.55
        - Active: BMR * 1.725
        - Very Active: BMR * 1.9
        """
        bmr = self.calculate_bmr()
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9,
        }
        
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        daily_calories = bmr * multiplier
        
        return round(daily_calories, 2)
    
    def save(self, *args, **kwargs):
        """Override save to automatically calculate and store daily calorie target."""
        self.daily_calorie_target = self.calculate_daily_calorie_needs()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Food(models.Model):
    """
    Food model to store food items with their nutritional information.
    Preloaded with Indian foods.
    """
    
    CATEGORY_CHOICES = [
        ('dal', 'Dal/Lentils'),
        ('rice', 'Rice'),
        ('roti', 'Roti/Chapati'),
        ('vegetables', 'Vegetables/Sabzi'),
        ('fruits', 'Fruits'),
        ('dairy', 'Dairy Products'),
        ('snacks', 'Snacks'),
        ('beverages', 'Beverages'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    calories_per_100g = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Calories per 100 grams"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class DailyFoodLog(models.Model):
    """
    Daily Food Log model to track user's daily food consumption.
    Automatically calculates calories based on quantity and food item.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_logs')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='logs')
    quantity = models.DecimalField(
        max_digits=7, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Quantity in grams"
    )
    date = models.DateField(default=timezone.now)
    calories = models.DecimalField(
        max_digits=7, 
        decimal_places=2,
        help_text="Calculated calories for this entry"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Daily Food Log"
        verbose_name_plural = "Daily Food Logs"
        ordering = ['-date', '-created_at']
        unique_together = ['user', 'food', 'date', 'created_at']  # Allow multiple entries per day
    
    def calculate_calories(self):
        """Calculate calories based on quantity and food's calories per 100g."""
        quantity = float(self.quantity)
        calories_per_100g = float(self.food.calories_per_100g)
        calculated_calories = (quantity / 100) * calories_per_100g
        return round(calculated_calories, 2)
    
    def save(self, *args, **kwargs):
        """Override save to automatically calculate calories."""
        self.calories = self.calculate_calories()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.food.name} ({self.quantity}g) on {self.date}"
    
    @staticmethod
    def get_daily_total_calories(user, date):
        """Get total calories consumed by a user on a specific date."""
        logs = DailyFoodLog.objects.filter(user=user, date=date)
        total = sum(float(log.calories) for log in logs)
        return round(total, 2)
    
    @staticmethod
    def get_weekly_summary(user, start_date, end_date):
        """Get weekly summary of calories consumed."""
        logs = DailyFoodLog.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        ).values('date').annotate(
            total_calories=models.Sum('calories')
        ).order_by('date')
        
        return logs
