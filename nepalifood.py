"""
Comprehensive database of Nepalese foods with nutritional information
"""

NEPALI_FOODS_DATABASE = {
    # Main Courses
    'Dal Bhat (1 plate)': {
        'calories': 420,
        'protein': 12,
        'carbs': 65,
        'fat': 8,
        'fiber': 6,
        'sodium': 400,
        'category': 'Main Course',
        'ingredients': ['Rice', 'Lentils', 'Vegetables', 'Ghee'],
        'preparation': 'Steamed rice with cooked lentils',
        'health_benefits': ['High in protein', 'Good source of complex carbs', 'Rich in fiber'],
        'diabetic_friendly': False,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    'Brown Rice Dal Bhat (1 plate)': {
        'calories': 380,
        'protein': 14,
        'carbs': 58,
        'fat': 6,
        'fiber': 8,
        'sodium': 350,
        'category': 'Main Course',
        'ingredients': ['Brown Rice', 'Mixed Lentils', 'Vegetables'],
        'preparation': 'Brown rice with protein-rich lentils',
        'health_benefits': ['Lower glycemic index', 'Higher fiber', 'Better for diabetes'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    # Snacks and Appetizers
    'Chicken Momo (6 pieces)': {
        'calories': 340,
        'protein': 18,
        'carbs': 28,
        'fat': 16,
        'fiber': 2,
        'sodium': 580,
        'category': 'Snack',
        'ingredients': ['Chicken', 'Flour', 'Onions', 'Spices'],
        'preparation': 'Steamed dumplings with chicken filling',
        'health_benefits': ['High protein', 'Moderate calories'],
        'diabetic_friendly': False,
        'heart_healthy': False,
        'low_sodium': False
    },
    
    'Vegetable Momo (6 pieces)': {
        'calories': 280,
        'protein': 8,
        'carbs': 32,
        'fat': 12,
        'fiber': 4,
        'sodium': 450,
        'category': 'Snack',
        'ingredients': ['Mixed Vegetables', 'Flour', 'Spices'],
        'preparation': 'Steamed dumplings with vegetable filling',
        'health_benefits': ['Lower calories than meat version', 'Good fiber content'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    'Cauliflower Momo (6 pieces)': {
        'calories': 220,
        'protein': 8,
        'carbs': 24,
        'fat': 10,
        'fiber': 5,
        'sodium': 380,
        'category': 'Snack',
        'ingredients': ['Cauliflower', 'Flour', 'Spices'],
        'preparation': 'Low-carb dumplings with cauliflower',
        'health_benefits': ['Lower carbs', 'High fiber', 'Diabetes-friendly'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    # Traditional Dishes
    'Gundruk Soup (1 bowl)': {
        'calories': 120,
        'protein': 6,
        'carbs': 15,
        'fat': 4,
        'fiber': 4,
        'sodium': 320,
        'category': 'Soup',
        'ingredients': ['Fermented Greens', 'Tomatoes', 'Spices'],
        'preparation': 'Traditional fermented vegetable soup',
        'health_benefits': ['Probiotic benefits', 'Low calories', 'High in vitamins'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    'Samay Baji (1 plate)': {
        'calories': 380,
        'protein': 15,
        'carbs': 42,
        'fat': 18,
        'fiber': 5,
        'sodium': 650,
        'category': 'Traditional',
        'ingredients': ['Beaten Rice', 'Meat', 'Beans', 'Pickles'],
        'preparation': 'Traditional Newari feast platter',
        'health_benefits': ['Variety of nutrients', 'Cultural significance'],
        'diabetic_friendly': False,
        'heart_healthy': False,
        'low_sodium': False
    },
    
    'Chatamari (2 pieces)': {
        'calories': 240,
        'protein': 8,
        'carbs': 30,
        'fat': 10,
        'fiber': 3,
        'sodium': 280,
        'category': 'Traditional',
        'ingredients': ['Rice Flour', 'Toppings', 'Spices'],
        'preparation': 'Newari rice crepe with toppings',
        'health_benefits': ['Gluten-free', 'Customizable toppings'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    # Curries and Vegetables
    'Aloo Tama (1 bowl)': {
        'calories': 160,
        'protein': 4,
        'carbs': 22,
        'fat': 6,
        'fiber': 6,
        'sodium': 420,
        'category': 'Curry',
        'ingredients': ['Potatoes', 'Bamboo Shoots', 'Spices'],
        'preparation': 'Traditional potato and bamboo shoot curry',
        'health_benefits': ['High fiber', 'Low calories', 'Traditional flavors'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    'Methi Leaves Curry (1 bowl)': {
        'calories': 180,
        'protein': 8,
        'carbs': 12,
        'fat': 8,
        'fiber': 8,
        'sodium': 200,
        'category': 'Curry',
        'ingredients': ['Fenugreek Leaves', 'Tomatoes', 'Minimal Oil'],
        'preparation': 'Diabetes-friendly fenugreek curry',
        'health_benefits': ['Blood sugar control', 'High iron', 'Low sodium'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    'Bitter Gourd Curry (1 bowl)': {
        'calories': 120,
        'protein': 4,
        'carbs': 8,
        'fat': 6,
        'fiber': 4,
        'sodium': 180,
        'category': 'Curry',
        'ingredients': ['Bitter Gourd', 'Onions', 'Spices'],
        'preparation': 'Traditional bitter gourd preparation',
        'health_benefits': ['Natural insulin properties', 'Low calories', 'Antioxidants'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    # Grains and Staples
    'Dhido (1 bowl)': {
        'calories': 200,
        'protein': 4,
        'carbs': 40,
        'fat': 2,
        'fiber': 6,
        'sodium': 150,
        'category': 'Main Course',
        'ingredients': ['Millet Flour', 'Water', 'Salt'],
        'preparation': 'Traditional millet porridge',
        'health_benefits': ['Gluten-free', 'High fiber', 'Traditional grain'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    'Oats Dhido (1 bowl)': {
        'calories': 280,
        'protein': 8,
        'carbs': 35,
        'fat': 8,
        'fiber': 8,
        'sodium': 120,
        'category': 'Main Course',
        'ingredients': ['Oats', 'Vegetables', 'Minimal Ghee'],
        'preparation': 'Modern healthy version with oats',
        'health_benefits': ['Beta-glucan for cholesterol', 'Heart healthy', 'High fiber'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    # Desserts and Sweets
    'Kheer (1 bowl)': {
        'calories': 220,
        'protein': 6,
        'carbs': 35,
        'fat': 8,
        'fiber': 1,
        'sodium': 80,
        'category': 'Dessert',
        'ingredients': ['Milk', 'Rice', 'Sugar', 'Nuts'],
        'preparation': 'Traditional rice pudding',
        'health_benefits': ['Calcium from milk', 'Energy from carbs'],
        'diabetic_friendly': False,
        'heart_healthy': False,
        'low_sodium': True
    },
    
    'Sel Roti (2 pieces)': {
        'calories': 180,
        'protein': 3,
        'carbs': 28,
        'fat': 6,
        'fiber': 2,
        'sodium': 120,
        'category': 'Snack',
        'ingredients': ['Rice Flour', 'Sugar', 'Ghee'],
        'preparation': 'Traditional ring-shaped sweet bread',
        'health_benefits': ['Cultural significance', 'Quick energy'],
        'diabetic_friendly': False,
        'heart_healthy': False,
        'low_sodium': True
    },
    
    'Lapsi (1 bowl)': {
        'calories': 220,
        'protein': 4,
        'carbs': 45,
        'fat': 3,
        'fiber': 4,
        'sodium': 100,
        'category': 'Dessert',
        'ingredients': ['Broken Wheat', 'Ghee', 'Sugar', 'Nuts'],
        'preparation': 'Sweet broken wheat pudding',
        'health_benefits': ['Whole grain', 'Moderate calories'],
        'diabetic_friendly': False,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    # Proteins and Dairy
    'Sukuti (30g)': {
        'calories': 120,
        'protein': 20,
        'carbs': 0,
        'fat': 4,
        'fiber': 0,
        'sodium': 800,
        'category': 'Meat',
        'ingredients': ['Dried Meat', 'Spices'],
        'preparation': 'Traditional dried meat',
        'health_benefits': ['High protein', 'Low carbs', 'Long shelf life'],
        'diabetic_friendly': True,
        'heart_healthy': False,
        'low_sodium': False
    },
    
    'Yak Cheese (50g)': {
        'calories': 180,
        'protein': 12,
        'carbs': 2,
        'fat': 14,
        'fiber': 0,
        'sodium': 320,
        'category': 'Dairy',
        'ingredients': ['Yak Milk'],
        'preparation': 'Traditional high-altitude cheese',
        'health_benefits': ['High protein', 'Calcium rich', 'Traditional'],
        'diabetic_friendly': True,
        'heart_healthy': False,
        'low_sodium': False
    },
    
    # Soups and Broths
    'Thukpa (1 bowl)': {
        'calories': 280,
        'protein': 12,
        'carbs': 35,
        'fat': 10,
        'fiber': 4,
        'sodium': 650,
        'category': 'Soup',
        'ingredients': ['Noodles', 'Vegetables', 'Meat/Tofu', 'Broth'],
        'preparation': 'Tibetan-style noodle soup',
        'health_benefits': ['Complete meal', 'Warming', 'Balanced nutrition'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': False
    },
    
    # Healthy Alternatives
    'Steamed Dal Bhat (1 plate)': {
        'calories': 350,
        'protein': 14,
        'carbs': 58,
        'fat': 4,
        'fiber': 7,
        'sodium': 180,
        'category': 'Main Course',
        'ingredients': ['Rice', 'Lentils', 'Steamed Vegetables'],
        'preparation': 'Low-oil version of traditional Dal Bhat',
        'health_benefits': ['Lower calories', 'Heart healthy', 'Low sodium'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    },
    
    'Cucumber Raita (1 bowl)': {
        'calories': 80,
        'protein': 4,
        'carbs': 8,
        'fat': 3,
        'fiber': 2,
        'sodium': 45,
        'category': 'Side Dish',
        'ingredients': ['Cucumber', 'Low-fat Yogurt', 'Mint'],
        'preparation': 'Cooling yogurt-based side dish',
        'health_benefits': ['Cooling effect', 'Low sodium', 'Probiotic'],
        'diabetic_friendly': True,
        'heart_healthy': True,
        'low_sodium': True
    }
}

def get_foods_by_category(category):
    """Get all foods in a specific category"""
    return {name: info for name, info in NEPALI_FOODS_DATABASE.items() 
            if info['category'] == category}

def get_diabetic_friendly_foods():
    """Get all diabetes-friendly foods"""
    return {name: info for name, info in NEPALI_FOODS_DATABASE.items() 
            if info['diabetic_friendly']}

def get_heart_healthy_foods():
    """Get all heart-healthy foods"""
    return {name: info for name, info in NEPALI_FOODS_DATABASE.items() 
            if info['heart_healthy']}

def get_low_sodium_foods():
    """Get all low-sodium foods"""
    return {name: info for name, info in NEPALI_FOODS_DATABASE.items() 
            if info['low_sodium']}

def search_foods(query):
    """Search foods by name or ingredients"""
    query = query.lower()
    results = {}
    
    for name, info in NEPALI_FOODS_DATABASE.items():
        if (query in name.lower() or 
            any(query in ingredient.lower() for ingredient in info['ingredients']) or
            query in info['category'].lower()):
            results[name] = info
    
    return results

def get_food_recommendations(health_conditions, dietary_preferences=None):
    """Get food recommendations based on health conditions"""
    recommendations = {}
    
    for condition in health_conditions:
        if condition == 'Diabetes':
            recommendations['Diabetes-Friendly'] = get_diabetic_friendly_foods()
        elif condition == 'Hypertension':
            recommendations['Low-Sodium'] = get_low_sodium_foods()
        elif condition == 'Heart Disease':
            recommendations['Heart-Healthy'] = get_heart_healthy_foods()
    
    if not recommendations:
        recommendations['All Foods'] = NEPALI_FOODS_DATABASE
    
    return recommendations