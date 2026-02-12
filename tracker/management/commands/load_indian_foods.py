"""
Management command to preload Indian foods into the database.
Run with: python manage.py load_indian_foods
"""
from django.core.management.base import BaseCommand
from tracker.models import Food


class Command(BaseCommand):
    help = 'Loads Indian foods into the database'

    def handle(self, *args, **options):
        """
        Preload Indian foods with their categories and calorie information.
        Calorie values are approximate per 100g.
        """
        foods_data = [
            # Dal/Lentils
            {'name': 'Toor Dal (Cooked)', 'category': 'dal', 'calories_per_100g': 100},
            {'name': 'Moong Dal (Cooked)', 'category': 'dal', 'calories_per_100g': 105},
            {'name': 'Masoor Dal (Cooked)', 'category': 'dal', 'calories_per_100g': 100},
            {'name': 'Chana Dal (Cooked)', 'category': 'dal', 'calories_per_100g': 120},
            {'name': 'Urad Dal (Cooked)', 'category': 'dal', 'calories_per_100g': 110},
            {'name': 'Rajma (Kidney Beans)', 'category': 'dal', 'calories_per_100g': 127},
            
            # Rice
            {'name': 'White Rice (Cooked)', 'category': 'rice', 'calories_per_100g': 130},
            {'name': 'Brown Rice (Cooked)', 'category': 'rice', 'calories_per_100g': 111},
            {'name': 'Basmati Rice (Cooked)', 'category': 'rice', 'calories_per_100g': 130},
            {'name': 'Jeera Rice (Cooked)', 'category': 'rice', 'calories_per_100g': 140},
            {'name': 'Biryani Rice', 'category': 'rice', 'calories_per_100g': 180},
            
            # Roti/Chapati
            {'name': 'Roti/Chapati (Wheat)', 'category': 'roti', 'calories_per_100g': 297},
            {'name': 'Phulka', 'category': 'roti', 'calories_per_100g': 280},
            {'name': 'Naan', 'category': 'roti', 'calories_per_100g': 310},
            {'name': 'Paratha', 'category': 'roti', 'calories_per_100g': 326},
            {'name': 'Bhatura', 'category': 'roti', 'calories_per_100g': 350},
            
            # Vegetables/Sabzi
            {'name': 'Aloo Sabzi (Potato)', 'category': 'vegetables', 'calories_per_100g': 150},
            {'name': 'Bhindi Sabzi (Okra)', 'category': 'vegetables', 'calories_per_100g': 80},
            {'name': 'Baingan Bharta (Eggplant)', 'category': 'vegetables', 'calories_per_100g': 90},
            {'name': 'Gobi Sabzi (Cauliflower)', 'category': 'vegetables', 'calories_per_100g': 60},
            {'name': 'Mix Vegetable Sabzi', 'category': 'vegetables', 'calories_per_100g': 70},
            {'name': 'Paneer Sabzi', 'category': 'vegetables', 'calories_per_100g': 200},
            {'name': 'Dal Makhani', 'category': 'vegetables', 'calories_per_100g': 180},
            {'name': 'Chana Masala', 'category': 'vegetables', 'calories_per_100g': 140},
            {'name': 'Palak Paneer', 'category': 'vegetables', 'calories_per_100g': 190},
            {'name': 'Matar Paneer', 'category': 'vegetables', 'calories_per_100g': 180},
            
            # Fruits
            {'name': 'Banana', 'category': 'fruits', 'calories_per_100g': 89},
            {'name': 'Apple', 'category': 'fruits', 'calories_per_100g': 52},
            {'name': 'Mango', 'category': 'fruits', 'calories_per_100g': 60},
            {'name': 'Orange', 'category': 'fruits', 'calories_per_100g': 47},
            {'name': 'Guava', 'category': 'fruits', 'calories_per_100g': 68},
            {'name': 'Papaya', 'category': 'fruits', 'calories_per_100g': 43},
            {'name': 'Watermelon', 'category': 'fruits', 'calories_per_100g': 30},
            {'name': 'Pomegranate', 'category': 'fruits', 'calories_per_100g': 83},
            
            # Dairy Products
            {'name': 'Milk (Full Cream)', 'category': 'dairy', 'calories_per_100g': 61},
            {'name': 'Milk (Skimmed)', 'category': 'dairy', 'calories_per_100g': 34},
            {'name': 'Curd/Yogurt', 'category': 'dairy', 'calories_per_100g': 59},
            {'name': 'Paneer (Cottage Cheese)', 'category': 'dairy', 'calories_per_100g': 265},
            {'name': 'Ghee', 'category': 'dairy', 'calories_per_100g': 900},
            {'name': 'Butter', 'category': 'dairy', 'calories_per_100g': 717},
            {'name': 'Cheese', 'category': 'dairy', 'calories_per_100g': 402},
            
            # Snacks
            {'name': 'Samosa', 'category': 'snacks', 'calories_per_100g': 262},
            {'name': 'Pakora', 'category': 'snacks', 'calories_per_100g': 200},
            {'name': 'Dhokla', 'category': 'snacks', 'calories_per_100g': 160},
            {'name': 'Vada Pav', 'category': 'snacks', 'calories_per_100g': 280},
            {'name': 'Pav Bhaji', 'category': 'snacks', 'calories_per_100g': 180},
            {'name': 'Dosa', 'category': 'snacks', 'calories_per_100g': 130},
            {'name': 'Idli', 'category': 'snacks', 'calories_per_100g': 39},
            {'name': 'Upma', 'category': 'snacks', 'calories_per_100g': 120},
            
            # Beverages
            {'name': 'Chai (Tea)', 'category': 'beverages', 'calories_per_100g': 30},
            {'name': 'Coffee', 'category': 'beverages', 'calories_per_100g': 2},
            {'name': 'Lassi (Sweet)', 'category': 'beverages', 'calories_per_100g': 90},
            {'name': 'Lassi (Salted)', 'category': 'beverages', 'calories_per_100g': 50},
            {'name': 'Buttermilk (Chaas)', 'category': 'beverages', 'calories_per_100g': 25},
            {'name': 'Fresh Juice (Orange)', 'category': 'beverages', 'calories_per_100g': 45},
            {'name': 'Fresh Juice (Mango)', 'category': 'beverages', 'calories_per_100g': 60},
        ]
        
        created_count = 0
        updated_count = 0
        
        for food_data in foods_data:
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults={
                    'category': food_data['category'],
                    'calories_per_100g': food_data['calories_per_100g']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Created: {food.name} ({food.get_category_display()})')
                )
            else:
                # Update if exists
                food.category = food_data['category']
                food.calories_per_100g = food_data['calories_per_100g']
                food.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'[UPDATED] Updated: {food.name} ({food.get_category_display()})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[SUCCESS] Successfully loaded {created_count} new foods and updated {updated_count} existing foods!'
            )
        )
