# Calorie Tracker - Django Web Application

A production-ready calorie tracking web application built with Django, featuring Indian food database, BMR-based calorie calculation, and comprehensive food logging system.

## Features

### 🔐 Authentication
- User signup with profile creation
- Session-based login/logout
- Secure password validation
- User-specific data isolation

### 📊 User Profile & Calorie Calculation
- User profile with age, gender, height, weight, and activity level
- Automatic BMR calculation using **Mifflin-St Jeor Equation** (more accurate than Harris-Benedict)
- Daily calorie target calculation based on activity level
- Activity multipliers:
  - Sedentary: BMR × 1.2
  - Light: BMR × 1.375
  - Moderate: BMR × 1.55
  - Active: BMR × 1.725
  - Very Active: BMR × 1.9

### 🍛 Food Database (Indian Foods)
- Preloaded with 60+ Indian food items
- Categories: Dal, Rice, Roti, Vegetables, Fruits, Dairy, Snacks, Beverages
- Calories per 100g for each food item
- Admin panel to add/edit/delete foods

### 📝 Daily Food Logging
- Log food consumption with quantity (grams)
- Automatic calorie calculation
- Date-based filtering
- Multiple entries per day supported
- Delete entries functionality

### 📈 Dashboard
- Daily calorie goal display
- Calories consumed today
- Remaining calories calculation
- Visual progress bar
- Recent food entries
- Weekly summary preview

### 📅 History & Reports
- View food logs by date
- Weekly summary with daily breakdown
- Visual charts using Chart.js
- Progress tracking vs daily target

### 👨‍💼 Admin Panel
- Full CRUD operations for Food model
- View and manage user profiles
- Monitor food logs
- Date hierarchy filtering

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js 3.9.1
- **Database**: SQLite (default)

## Project Structure

```
project/
├── calorie_tracker/          # Main project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── tracker/                   # Main application
│   ├── models.py             # UserProfile, Food, DailyFoodLog models
│   ├── views.py              # All view functions
│   ├── forms.py              # Django forms
│   ├── urls.py               # App URL routing
│   ├── admin.py              # Admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── load_indian_foods.py  # Management command
│   └── templates/
│       └── tracker/
│           ├── base.html
│           ├── login.html
│           ├── signup.html
│           ├── dashboard.html
│           ├── add_food.html
│           ├── history.html
│           ├── weekly_summary.html
│           ├── profile.html
│           └── delete_confirm.html
├── manage.py
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps

1. **Navigate to project directory**
   ```bash
   cd "c:\Users\HP VICTUS\Desktop\New folder\django-project\project"
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Django**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load Indian foods database**
   ```bash
   python manage.py load_indian_foods
   ```
   This command will preload 60+ Indian food items with their calorie information.

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage Guide

### For Users

1. **Sign Up**
   - Click "Sign up" on the login page
   - Fill in account information (username, email, password)
   - Complete your profile (age, gender, height, weight, activity level)
   - Your daily calorie target will be automatically calculated

2. **Dashboard**
   - View your daily calorie goal and progress
   - See calories consumed and remaining
   - Check recent food entries

3. **Add Food**
   - Click "Add Food" in navigation
   - Select food item from dropdown
   - Enter quantity in grams
   - Select date (defaults to today)
   - Calories are automatically calculated

4. **View History**
   - Access "History" from navigation
   - Filter by date
   - View weekly summary

5. **Update Profile**
   - Go to "Profile" section
   - Update your physical attributes
   - Daily calorie target recalculates automatically

### For Administrators

1. **Admin Panel**
   - Login at `/admin/` with superuser credentials
   - Manage Food items (add/edit/delete)
   - View user profiles and food logs
   - Monitor application usage

2. **Add New Foods**
   - Go to Admin → Foods → Add Food
   - Enter name, category, and calories per 100g
   - Save to make it available to all users

## Models Overview

### UserProfile
- One-to-one relationship with User
- Stores: age, gender, height, weight, activity_level
- Calculates: BMR and daily_calorie_target

### Food
- Stores food items with name, category, calories_per_100g
- Categories: dal, rice, roti, vegetables, fruits, dairy, snacks, beverages, other

### DailyFoodLog
- Links User, Food, quantity, date
- Automatically calculates calories based on quantity
- Supports multiple entries per day

## Key Features Explained

### BMR Calculation (Mifflin-St Jeor)
```
Men:   BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
Women: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
```

### Daily Calorie Needs
```
Daily Calories = BMR × Activity Multiplier
```

### Food Log Calories
```
Calories = (Quantity in grams / 100) × Calories per 100g
```

## Security Features

- CSRF protection enabled
- Session-based authentication
- User data isolation (users can only access their own data)
- Password validation
- Secure admin panel access

## Future Enhancements

- [ ] Weight tracking over time
- [ ] Goal setting (weight loss/gain)
- [ ] Meal planning
- [ ] Export data to CSV/PDF
- [ ] Mobile app API
- [ ] Social features (share progress)
- [ ] Advanced analytics and charts
- [ ] Custom food recipes
- [ ] Nutrition tracking (protein, carbs, fats)

## Contributing

This is a production-ready application. To extend:

1. Add new models in `models.py`
2. Create forms in `forms.py`
3. Add views in `views.py`
4. Update URLs in `urls.py`
5. Create templates in `templates/tracker/`

## License

This project is created for educational and personal use.

## Support

For issues or questions, please check:
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/

---

**Built with ❤️ using Django**
