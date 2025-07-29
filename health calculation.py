"""
Health calculation utilities for the Swasthya app
"""

import math
from datetime import datetime, timedelta

class HealthCalculator:
    """Class for various health-related calculations"""
    
    @staticmethod
    def calculate_bmi(weight_kg, height_cm):
        """Calculate Body Mass Index"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 1)
    
    @staticmethod
    def get_bmi_category(bmi):
        """Get BMI category and recommendations"""
        if bmi < 18.5:
            return {
                'category': 'Underweight',
                'color': '#3B82F6',
                'recommendation': 'Consider increasing calorie intake with healthy foods'
            }
        elif 18.5 <= bmi < 25:
            return {
                'category': 'Normal Weight',
                'color': '#22C55E',
                'recommendation': 'Maintain your current healthy weight'
            }
        elif 25 <= bmi < 30:
            return {
                'category': 'Overweight',
                'color': '#F59E0B',
                'recommendation': 'Consider reducing calorie intake and increasing exercise'
            }
        else:
            return {
                'category': 'Obese',
                'color': '#EF4444',
                'recommendation': 'Consult healthcare provider for weight management plan'
            }
    
    @staticmethod
    def calculate_bmr(weight_kg, height_cm, age_years, gender):
        """Calculate Basal Metabolic Rate using Harris-Benedict equation"""
        if gender.lower() == 'female':
            bmr = 655 + (9.6 * weight_kg) + (1.8 * height_cm) - (4.7 * age_years)
        else:
            bmr = 66 + (13.7 * weight_kg) + (5 * height_cm) - (6.8 * age_years)
        
        return round(bmr, 0)
    
    @staticmethod
    def calculate_daily_calories(bmr, activity_level, goal):
        """Calculate daily calorie needs based on activity level and goals"""
        activity_multipliers = {
            'Sedentary': 1.2,
            'Light': 1.375,
            'Moderate': 1.55,
            'Active': 1.725,
            'Very Active': 1.9
        }
        
        maintenance_calories = bmr * activity_multipliers.get(activity_level, 1.55)
        
        if goal == 'Lose Weight':
            return int(maintenance_calories - 500)  # 500 cal deficit for 1 lb/week loss
        elif goal == 'Gain Weight':
            return int(maintenance_calories + 500)  # 500 cal surplus for 1 lb/week gain
        else:
            return int(maintenance_calories)
    
    @staticmethod
    def calculate_macronutrient_needs(daily_calories, goal):
        """Calculate recommended macronutrient distribution"""
        if goal == 'Lose Weight':
            # Higher protein for weight loss
            protein_percent = 0.30
            carb_percent = 0.40
            fat_percent = 0.30
        elif goal == 'Gain Weight':
            # Higher carbs for weight gain
            protein_percent = 0.25
            carb_percent = 0.45
            fat_percent = 0.30
        else:
            # Balanced for maintenance
            protein_percent = 0.25
            carb_percent = 0.45
            fat_percent = 0.30
        
        protein_calories = daily_calories * protein_percent
        carb_calories = daily_calories * carb_percent
        fat_calories = daily_calories * fat_percent
        
        return {
            'protein_grams': round(protein_calories / 4, 1),  # 4 cal per gram
            'carb_grams': round(carb_calories / 4, 1),        # 4 cal per gram
            'fat_grams': round(fat_calories / 9, 1),          # 9 cal per gram
            'protein_percent': protein_percent * 100,
            'carb_percent': carb_percent * 100,
            'fat_percent': fat_percent * 100
        }
    
    @staticmethod
    def calculate_water_needs(weight_kg, activity_level):
        """Calculate daily water needs in liters"""
        base_water = weight_kg * 0.035  # 35ml per kg body weight
        
        # Adjust for activity level
        if activity_level in ['Active', 'Very Active']:
            base_water *= 1.2
        elif activity_level == 'Moderate':
            base_water *= 1.1
        
        return round(base_water, 1)
    
    @staticmethod
    def estimate_calories_burned(exercise_type, duration_minutes, weight_kg):
        """Estimate calories burned during exercise"""
        # MET (Metabolic Equivalent) values for different activities
        met_values = {
            'Walking': 3.5,
            'Jogging': 7.0,
            'Cycling': 6.0,
            'Swimming': 8.0,
            'Yoga': 2.5,
            'Strength Training': 6.0,
            'Dancing': 5.0,
            'Stair Climbing': 8.0,
            'Jumping Jacks': 8.0
        }
        
        met = met_values.get(exercise_type, 4.0)  # Default MET value
        calories_per_minute = (met * weight_kg * 3.5) / 200
        total_calories = calories_per_minute * duration_minutes
        
        return round(total_calories, 0)
    
    @staticmethod
    def get_health_recommendations(user_profile, health_conditions):
        """Generate personalized health recommendations"""
        recommendations = []
        
        # BMI-based recommendations
        bmi = HealthCalculator.calculate_bmi(user_profile['weight'], user_profile['height'])
        bmi_info = HealthCalculator.get_bmi_category(bmi)
        recommendations.append(bmi_info['recommendation'])
        
        # Health condition specific recommendations
        for condition in health_conditions:
            if condition == 'Diabetes':
                recommendations.extend([
                    'Choose brown rice over white rice in Dal Bhat',
                    'Monitor portion sizes and eat regular meals',
                    'Include high-fiber vegetables in every meal'
                ])
            elif condition == 'Hypertension':
                recommendations.extend([
                    'Reduce salt in cooking and avoid pickled foods',
                    'Include potassium-rich foods like bananas',
                    'Limit processed and canned foods'
                ])
            elif condition == 'Heart Disease':
                recommendations.extend([
                    'Choose lean proteins and limit red meat',
                    'Include omega-3 rich foods like fish',
                    'Use minimal ghee and oil in cooking'
                ])
        
        # Activity-based recommendations
        if user_profile['activity_level'] == 'Sedentary':
            recommendations.append('Try to include at least 30 minutes of walking daily')
        
        return recommendations

class NutritionAnalyzer:
    """Class for analyzing nutritional content of meals"""
    
    @staticmethod
    def analyze_daily_intake(food_items):
        """Analyze nutritional content of daily food intake"""
        total_calories = sum(item.get('calories', 0) for item in food_items)
        total_protein = sum(item.get('protein', 0) for item in food_items)
        total_carbs = sum(item.get('carbs', 0) for item in food_items)
        total_fat = sum(item.get('fat', 0) for item in food_items)
        
        return {
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_carbs': total_carbs,
            'total_fat': total_fat,
            'protein_percent': (total_protein * 4 / total_calories * 100) if total_calories > 0 else 0,
            'carb_percent': (total_carbs * 4 / total_calories * 100) if total_calories > 0 else 0,
            'fat_percent': (total_fat * 9 / total_calories * 100) if total_calories > 0 else 0
        }
    
    @staticmethod
    def get_meal_timing_recommendations():
        """Get recommendations for meal timing"""
        return {
            'breakfast': '7:00-9:00 AM',
            'morning_snack': '10:00-11:00 AM',
            'lunch': '12:00-2:00 PM',
            'afternoon_snack': '3:00-4:00 PM',
            'dinner': '6:00-8:00 PM',
            'tips': [
                'Eat breakfast within 2 hours of waking up',
                'Have your largest meal at lunch time',
                'Keep dinner light and early',
                'Maintain 3-4 hour gaps between major meals'
            ]
        }
    
    @staticmethod
    def suggest_meal_improvements(current_meal, health_conditions):
        """Suggest improvements for current meal based on health conditions"""
        suggestions = []
        
        for condition in health_conditions:
            if condition == 'Diabetes':
                suggestions.extend([
                    'Add more fiber-rich vegetables',
                    'Choose whole grains over refined grains',
                    'Include lean protein to slow carb absorption'
                ])
            elif condition == 'Hypertension':
                suggestions.extend([
                    'Reduce salt and use herbs for flavor',
                    'Add potassium-rich foods like tomatoes',
                    'Include garlic for natural blood pressure support'
                ])
            elif condition == 'Heart Disease':
                suggestions.extend([
                    'Use minimal oil and choose healthy fats',
                    'Include antioxidant-rich colorful vegetables',
                    'Add omega-3 sources like walnuts or fish'
                ])
        
        return suggestions