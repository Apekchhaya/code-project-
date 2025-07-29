import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import cv2
from PIL import Image
import io
import base64

# Configure page
st.set_page_config(
    page_title="Swasthya - Nepalese Fitness App",
    page_icon="🏃‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #22C55E, #3B82F6);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #22C55E;
        margin-bottom: 1rem;
    }
    
    .food-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 0.5rem;
    }
    
    .health-tip {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #22C55E;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #22C55E, #16A34A);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .camera-section {
        background: #f0f9ff;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #3B82F6;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Priya Sharma',
        'age': 28,
        'weight': 58,
        'height': 162,
        'gender': 'Female',
        'activity_level': 'Moderate',
        'goal': 'Maintain Weight',
        'health_conditions': ['None']
    }

if 'daily_intake' not in st.session_state:
    st.session_state.daily_intake = []

if 'exercise_log' not in st.session_state:
    st.session_state.exercise_log = []

# Nepalese food database
NEPALI_FOODS = {
    'Dal Bhat (1 plate)': {'calories': 420, 'protein': 12, 'carbs': 65, 'fat': 8, 'category': 'Main Course'},
    'Chicken Momo (6 pieces)': {'calories': 340, 'protein': 18, 'carbs': 28, 'fat': 16, 'category': 'Snack'},
    'Vegetable Momo (6 pieces)': {'calories': 280, 'protein': 8, 'carbs': 32, 'fat': 12, 'category': 'Snack'},
    'Gundruk Soup (1 bowl)': {'calories': 120, 'protein': 6, 'carbs': 15, 'fat': 4, 'category': 'Soup'},
    'Sel Roti (2 pieces)': {'calories': 180, 'protein': 3, 'carbs': 28, 'fat': 6, 'category': 'Snack'},
    'Kheer (1 bowl)': {'calories': 220, 'protein': 6, 'carbs': 35, 'fat': 8, 'category': 'Dessert'},
    'Chatamari (2 pieces)': {'calories': 240, 'protein': 8, 'carbs': 30, 'fat': 10, 'category': 'Traditional'},
    'Aloo Tama (1 bowl)': {'calories': 160, 'protein': 4, 'carbs': 22, 'fat': 6, 'category': 'Curry'},
    'Dhido (1 bowl)': {'calories': 200, 'protein': 4, 'carbs': 40, 'fat': 2, 'category': 'Main Course'},
    'Sukuti (30g)': {'calories': 120, 'protein': 20, 'carbs': 0, 'fat': 4, 'category': 'Meat'},
    'Yak Cheese (50g)': {'calories': 180, 'protein': 12, 'carbs': 2, 'fat': 14, 'category': 'Dairy'},
    'Samay Baji (1 plate)': {'calories': 380, 'protein': 15, 'carbs': 42, 'fat': 18, 'category': 'Traditional'},
    'Lapsi (1 bowl)': {'calories': 220, 'protein': 4, 'carbs': 45, 'fat': 3, 'category': 'Dessert'},
    'Newari Khaja Set': {'calories': 450, 'protein': 16, 'carbs': 48, 'fat': 22, 'category': 'Traditional'},
    'Thukpa (1 bowl)': {'calories': 280, 'protein': 12, 'carbs': 35, 'fat': 10, 'category': 'Soup'}
}

# Health condition meal plans
HEALTH_MEAL_PLANS = {
    'Diabetes': {
        'recommended': ['Brown Rice Dal Bhat', 'Cauliflower Momo', 'Methi Leaves Curry', 'Bitter Gourd Curry'],
        'avoid': ['White rice in large quantities', 'Sugary desserts', 'Deep-fried foods'],
        'tips': ['Monitor portion sizes', 'Include complex carbohydrates', 'Eat regular smaller meals']
    },
    'Hypertension': {
        'recommended': ['Steamed Dal Bhat', 'Baked Fish with Herbs', 'Low Salt Spinach Curry', 'Cucumber Raita'],
        'avoid': ['Pickles and fermented foods', 'Processed meats', 'Salted snacks'],
        'tips': ['Limit salt to 2g/day', 'Include potassium-rich foods', 'Use herbs instead of salt']
    },
    'Heart Disease': {
        'recommended': ['Oats Dhido', 'Walnut Curry', 'Green Vegetable Soup', 'Flaxseed Roti'],
        'avoid': ['Deep-fried foods', 'Red meat', 'Full-fat dairy', 'Trans fats'],
        'tips': ['Include omega-3 rich foods', 'Choose whole grains', 'Limit saturated fats']
    }
}

def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    return weight / (height_m ** 2)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight", "#3B82F6"
    elif bmi < 25:
        return "Normal", "#22C55E"
    elif bmi < 30:
        return "Overweight", "#F59E0B"
    else:
        return "Obese", "#EF4444"

def calculate_daily_calories(profile):
    """Calculate daily calorie needs using Harris-Benedict equation"""
    if profile['gender'] == 'Female':
        bmr = 655 + (9.6 * profile['weight']) + (1.8 * profile['height']) - (4.7 * profile['age'])
    else:
        bmr = 66 + (13.7 * profile['weight']) + (5 * profile['height']) - (6.8 * profile['age'])
    
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    
    maintenance = bmr * activity_multipliers[profile['activity_level']]
    
    if profile['goal'] == 'Lose Weight':
        return int(maintenance - 500)
    elif profile['goal'] == 'Gain Weight':
        return int(maintenance + 500)
    else:
        return int(maintenance)

def analyze_food_image(image):
    """Simulate food recognition and calorie estimation"""
    # This is a simulation - in a real app, you'd use ML models like YOLOv5 or TensorFlow
    # For demo purposes, we'll return random Nepali food items
    import random
    
    detected_foods = random.sample(list(NEPALI_FOODS.keys()), random.randint(1, 3))
    total_calories = sum(NEPALI_FOODS[food]['calories'] for food in detected_foods)
    
    return detected_foods, total_calories

def main():
    # Sidebar navigation
    st.sidebar.markdown("# 🏃‍♀️ Swasthya")
    st.sidebar.markdown("*Your Nepalese Health Companion*")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Dashboard", "📸 Food Scanner", "🍽️ Calorie Tracker", "📅 Meal Planner", 
         "💪 Exercise Routine", "🏥 Health Conditions", "👤 Profile"]
    )
    
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📸 Food Scanner":
        food_scanner_page()
    elif page == "🍽️ Calorie Tracker":
        calorie_tracker_page()
    elif page == "📅 Meal Planner":
        meal_planner_page()
    elif page == "💪 Exercise Routine":
        exercise_routine_page()
    elif page == "🏥 Health Conditions":
        health_conditions_page()
    elif page == "👤 Profile":
        profile_page()

def dashboard_page():
    st.markdown('<div class="main-header"><h1>🏠 Welcome to Swasthya Dashboard</h1><p>Your personalized health journey starts here</p></div>', unsafe_allow_html=True)
    
    profile = st.session_state.user_profile
    daily_calories = calculate_daily_calories(profile)
    consumed_calories = sum(item['calories'] for item in st.session_state.daily_intake)
    remaining_calories = daily_calories - consumed_calories
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Calories Consumed", f"{consumed_calories}", f"{consumed_calories - daily_calories//2}")
    
    with col2:
        st.metric("Calories Remaining", f"{remaining_calories}", f"{remaining_calories - daily_calories//4}")
    
    with col3:
        bmi = calculate_bmi(profile['weight'], profile['height'])
        category, color = get_bmi_category(bmi)
        st.metric("BMI", f"{bmi:.1f}", category)
    
    with col4:
        st.metric("Daily Goal", f"{daily_calories}", "calories")
    
    # Progress visualization
    st.subheader("📊 Today's Progress")
    
    progress_data = {
        'Metric': ['Calories', 'Water', 'Exercise', 'Sleep'],
        'Current': [consumed_calories, 6, 45, 7],
        'Target': [daily_calories, 8, 60, 8],
        'Percentage': [
            min(100, (consumed_calories/daily_calories)*100),
            75, 75, 87.5
        ]
    }
    
    fig = px.bar(
        progress_data, 
        x='Metric', 
        y='Percentage',
        title="Daily Goals Progress",
        color='Percentage',
        color_continuous_scale=['#EF4444', '#F59E0B', '#22C55E']
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent meals
    st.subheader("🍽️ Recent Meals")
    if st.session_state.daily_intake:
        for meal in st.session_state.daily_intake[-3:]:
            st.markdown(f"""
            <div class="food-card">
                <strong>{meal['name']}</strong> - {meal['calories']} calories
                <br><small>Added at {meal['time']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No meals logged today. Use the Food Scanner or Calorie Tracker to add meals!")

def food_scanner_page():
    st.markdown('<div class="main-header"><h1>📸 AI Food Scanner</h1><p>Scan your Nepalese food to get instant calorie information</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="camera-section">
        <h3>📱 Scan Your Food</h3>
        <p>Take a photo of your meal and our AI will identify Nepalese dishes and calculate calories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Camera input
    camera_input = st.camera_input("Take a picture of your food")
    
    # File upload as alternative
    st.markdown("**Or upload an image:**")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    image_to_analyze = camera_input or uploaded_file
    
    if image_to_analyze is not None:
        # Display the image
        image = Image.open(image_to_analyze)
        st.image(image, caption="Your Food Image", use_column_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Food", type="primary"):
            with st.spinner("Analyzing your food... 🤖"):
                # Simulate processing time
                import time
                time.sleep(2)
                
                detected_foods, total_calories = analyze_food_image(image)
                
                st.success("✅ Food Analysis Complete!")
                
                # Display results
                st.subheader("🍽️ Detected Foods:")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    for food in detected_foods:
                        food_info = NEPALI_FOODS[food]
                        st.markdown(f"""
                        <div class="food-card">
                            <h4>{food}</h4>
                            <p><strong>Calories:</strong> {food_info['calories']} | 
                            <strong>Protein:</strong> {food_info['protein']}g | 
                            <strong>Carbs:</strong> {food_info['carbs']}g | 
                            <strong>Fat:</strong> {food_info['fat']}g</p>
                            <span style="background: #22C55E; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
                                {food_info['category']}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Total Calories", f"{total_calories}")
                    
                    if st.button("➕ Add to Daily Intake"):
                        for food in detected_foods:
                            st.session_state.daily_intake.append({
                                'name': food,
                                'calories': NEPALI_FOODS[food]['calories'],
                                'time': datetime.now().strftime("%H:%M"),
                                'method': 'Camera Scan'
                            })
                        st.success("Foods added to your daily intake!")
                        st.rerun()
    
    # Tips for better scanning
    st.markdown("""
    <div class="health-tip">
        <h4>📋 Tips for Better Food Scanning:</h4>
        <ul>
            <li>Ensure good lighting when taking photos</li>
            <li>Place food on a plain background</li>
            <li>Include the entire dish in the frame</li>
            <li>Take photos from directly above for best results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def calorie_tracker_page():
    st.markdown('<div class="main-header"><h1>🍽️ Calorie Tracker</h1><p>Track your daily calorie intake with Nepalese foods</p></div>', unsafe_allow_html=True)
    
    # Search and add foods
    st.subheader("🔍 Add Food to Your Daily Intake")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search for Nepalese foods...", placeholder="e.g., Dal Bhat, Momo, Gundruk")
        
        # Filter foods based on search
        filtered_foods = {k: v for k, v in NEPALI_FOODS.items() 
                         if search_term.lower() in k.lower() or search_term.lower() in v['category'].lower()}
        
        if search_term:
            st.write(f"Found {len(filtered_foods)} foods matching '{search_term}':")
            
            for food_name, food_info in filtered_foods.items():
                col_food, col_cal, col_btn = st.columns([3, 1, 1])
                
                with col_food:
                    st.write(f"**{food_name}**")
                    st.caption(f"P: {food_info['protein']}g | C: {food_info['carbs']}g | F: {food_info['fat']}g | {food_info['category']}")
                
                with col_cal:
                    st.write(f"**{food_info['calories']} cal**")
                
                with col_btn:
                    if st.button("➕", key=f"add_{food_name}"):
                        st.session_state.daily_intake.append({
                            'name': food_name,
                            'calories': food_info['calories'],
                            'time': datetime.now().strftime("%H:%M"),
                            'method': 'Manual Entry'
                        })
                        st.success(f"Added {food_name}!")
                        st.rerun()
    
    with col2:
        # Quick stats
        total_calories = sum(item['calories'] for item in st.session_state.daily_intake)
        daily_goal = calculate_daily_calories(st.session_state.user_profile)
        
        st.metric("Today's Total", f"{total_calories} cal")
        st.metric("Remaining", f"{daily_goal - total_calories} cal")
        
        progress = min(100, (total_calories / daily_goal) * 100)
        st.progress(progress / 100)
        st.caption(f"{progress:.1f}% of daily goal")
    
    # Today's intake
    st.subheader("📋 Today's Food Intake")
    
    if st.session_state.daily_intake:
        intake_df = pd.DataFrame(st.session_state.daily_intake)
        
        # Display as table
        for i, meal in enumerate(st.session_state.daily_intake):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{meal['name']}**")
            with col2:
                st.write(f"{meal['calories']} cal")
            with col3:
                st.write(meal['time'])
            with col4:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.daily_intake.pop(i)
                    st.rerun()
        
        # Macronutrient breakdown
        st.subheader("📊 Macronutrient Breakdown")
        
        total_protein = sum(NEPALI_FOODS.get(item['name'], {}).get('protein', 0) for item in st.session_state.daily_intake)
        total_carbs = sum(NEPALI_FOODS.get(item['name'], {}).get('carbs', 0) for item in st.session_state.daily_intake)
        total_fat = sum(NEPALI_FOODS.get(item['name'], {}).get('fat', 0) for item in st.session_state.daily_intake)
        
        macro_data = {
            'Macronutrient': ['Protein', 'Carbohydrates', 'Fat'],
            'Grams': [total_protein, total_carbs, total_fat],
            'Calories': [total_protein * 4, total_carbs * 4, total_fat * 9]
        }
        
        fig = px.pie(macro_data, values='Calories', names='Macronutrient', 
                    title="Calorie Distribution by Macronutrient",
                    color_discrete_sequence=['#22C55E', '#3B82F6', '#F59E0B'])
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("No foods logged today. Start by searching and adding foods above!")

def meal_planner_page():
    st.markdown('<div class="main-header"><h1>📅 Weekly Meal Planner</h1><p>Plan your week with traditional Nepalese cuisine</p></div>', unsafe_allow_html=True)
    
    # Week selector
    selected_day = st.selectbox("Select Day", 
                               ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    # Sample meal plans for different days
    meal_plans = {
        'Monday': {
            'Breakfast': {'name': 'Dal Bhat with Fried Egg', 'calories': 480, 'time': '8:00 AM'},
            'Lunch': {'name': 'Chicken Momo with Chutney', 'calories': 420, 'time': '1:00 PM'},
            'Snack': {'name': 'Sel Roti with Tea', 'calories': 200, 'time': '4:00 PM'},
            'Dinner': {'name': 'Gundruk Soup with Rice', 'calories': 350, 'time': '7:30 PM'}
        },
        'Tuesday': {
            'Breakfast': {'name': 'Dhido with Honey', 'calories': 280, 'time': '8:00 AM'},
            'Lunch': {'name': 'Samay Baji Set', 'calories': 480, 'time': '1:00 PM'},
            'Snack': {'name': 'Lapsi with Nuts', 'calories': 220, 'time': '4:00 PM'},
            'Dinner': {'name': 'Aloo Tama Curry', 'calories': 320, 'time': '7:30 PM'}
        }
    }
    
    # Default plan for other days
    default_plan = meal_plans.get('Monday')
    current_plan = meal_plans.get(selected_day, default_plan)
    
    st.subheader(f"🍽️ {selected_day}'s Meal Plan")
    
    total_day_calories = 0
    
    for meal_type, meal_info in current_plan.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="food-card">
                <h4>{meal_type}</h4>
                <p><strong>{meal_info['name']}</strong></p>
                <small>⏰ {meal_info['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Calories", meal_info['calories'])
        
        with col3:
            if st.button(f"Add to Today", key=f"add_meal_{meal_type}"):
                st.session_state.daily_intake.append({
                    'name': meal_info['name'],
                    'calories': meal_info['calories'],
                    'time': datetime.now().strftime("%H:%M"),
                    'method': 'Meal Plan'
                })
                st.success(f"Added {meal_info['name']} to today's intake!")
        
        total_day_calories += meal_info['calories']
    
    st.metric("Total Daily Calories", f"{total_day_calories}")
    
    # Weekly overview
    st.subheader("📊 Weekly Calorie Overview")
    
    weekly_data = {
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Planned Calories': [1450, 1300, 1400, 1500, 1350, 1600, 1200],
        'Target': [calculate_daily_calories(st.session_state.user_profile)] * 7
    }
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Planned', x=weekly_data['Day'], y=weekly_data['Planned Calories'], 
                        marker_color='#22C55E'))
    fig.add_trace(go.Scatter(name='Target', x=weekly_data['Day'], y=weekly_data['Target'], 
                           line=dict(color='#EF4444', dash='dash')))
    
    fig.update_layout(title="Weekly Meal Plan vs Target Calories", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Shopping list
    st.subheader("🛒 Shopping List")
    
    shopping_items = {
        'Grains & Cereals': ['Basmati Rice - 2kg', 'Lentils (Dal) - 1kg', 'Wheat Flour - 500g'],
        'Vegetables': ['Onions - 1kg', 'Tomatoes - 500g', 'Gundruk - 200g', 'Potatoes - 1kg'],
        'Proteins': ['Chicken - 1kg', 'Eggs - 1 dozen', 'Paneer - 250g'],
        'Spices & Others': ['Turmeric', 'Cumin', 'Ghee', 'Honey']
    }
    
    for category, items in shopping_items.items():
        st.write(f"**{category}:**")
        for item in items:
            st.checkbox(item, key=f"shop_{item}")

def exercise_routine_page():
    st.markdown('<div class="main-header"><h1>💪 Exercise Routine</h1><p>Personalized workouts for your fitness goals</p></div>', unsafe_allow_html=True)
    
    # Exercise type selection
    exercise_type = st.selectbox("Choose Exercise Type", 
                                ['Cardio', 'Strength Training', 'Yoga', 'Traditional Dance'])
    
    fitness_level = st.selectbox("Fitness Level", ['Beginner', 'Intermediate', 'Advanced'])
    
    # Exercise routines
    exercise_routines = {
        'Beginner': {
            'Cardio': [
                {'name': 'Morning Walk', 'duration': '20 min', 'calories': 80, 'description': 'Gentle walk around neighborhood'},
                {'name': 'Stair Climbing', 'duration': '10 min', 'calories': 60, 'description': 'Use stairs in building'},
                {'name': 'Jumping Jacks', 'duration': '5 min', 'calories': 40, 'description': 'Low-impact cardio'},
                {'name': 'Marching in Place', 'duration': '15 min', 'calories': 50, 'description': 'Indoor cardio exercise'}
            ],
            'Strength Training': [
                {'name': 'Wall Push-ups', 'duration': '10 reps', 'calories': 30, 'description': 'Push-ups against wall'},
                {'name': 'Chair Squats', 'duration': '15 reps', 'calories': 40, 'description': 'Squats with chair support'},
                {'name': 'Arm Circles', 'duration': '2 min', 'calories': 20, 'description': 'Shoulder mobility'},
                {'name': 'Modified Planks', 'duration': '30 sec', 'calories': 25, 'description': 'Planks on knees'}
            ],
            'Yoga': [
                {'name': 'Sun Salutation A', 'duration': '10 min', 'calories': 35, 'description': 'Basic yoga flow'},
                {'name': 'Child\'s Pose', 'duration': '5 min', 'calories': 15, 'description': 'Relaxing stretch'},
                {'name': 'Cat-Cow Stretch', 'duration': '5 min', 'calories': 20, 'description': 'Spinal mobility'},
                {'name': 'Mountain Pose', 'duration': '3 min', 'calories': 10, 'description': 'Foundation pose'}
            ],
            'Traditional Dance': [
                {'name': 'Nepali Folk Dance', 'duration': '15 min', 'calories': 70, 'description': 'Traditional moves'},
                {'name': 'Bollywood Dance', 'duration': '20 min', 'calories': 90, 'description': 'Fun choreography'},
                {'name': 'Simple Dance Steps', 'duration': '10 min', 'calories': 45, 'description': 'Basic movements'},
                {'name': 'Stretching Dance', 'duration': '8 min', 'calories': 30, 'description': 'Gentle stretches'}
            ]
        }
    }
    
    current_exercises = exercise_routines[fitness_level][exercise_type]
    
    st.subheader(f"🎯 {fitness_level} {exercise_type} Routine")
    
    total_calories = 0
    total_time = 0
    
    for i, exercise in enumerate(current_exercises):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="food-card">
                <h4>{exercise['name']}</h4>
                <p>{exercise['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"⏱️ {exercise['duration']}")
        
        with col3:
            st.write(f"🔥 {exercise['calories']} cal")
        
        with col4:
            if st.button("✅ Complete", key=f"complete_{i}"):
                st.session_state.exercise_log.append({
                    'exercise': exercise['name'],
                    'duration': exercise['duration'],
                    'calories': exercise['calories'],
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.now().strftime("%H:%M")
                })
                st.success(f"Completed {exercise['name']}!")
        
        total_calories += exercise['calories']
        # Extract numeric duration for total time calculation
        duration_num = int(''.join(filter(str.isdigit, exercise['duration'])))
        total_time += duration_num
    
    # Workout summary
    st.markdown(f"""
    <div class="health-tip">
        <h4>💪 Workout Summary</h4>
        <p><strong>Total Time:</strong> {total_time} minutes</p>
        <p><strong>Total Calories:</strong> {total_calories} calories</p>
        <p><strong>Exercises:</strong> {len(current_exercises)} activities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercise tips
    st.subheader("💡 Exercise Tips")
    tips = [
        "🥤 Stay hydrated - drink water before, during, and after exercise",
        "🔥 Always warm up for 5 minutes before starting",
        "👂 Listen to your body and rest when needed",
        "📈 Gradually increase intensity over time",
        "🎵 Play your favorite Nepali music for motivation!"
    ]
    
    for tip in tips:
        st.write(tip)

def health_conditions_page():
    st.markdown('<div class="main-header"><h1>🏥 Health Condition Meal Plans</h1><p>Specialized Nepalese meal plans for various health conditions</p></div>', unsafe_allow_html=True)
    
    condition = st.selectbox("Select Health Condition", 
                            ['Diabetes', 'Hypertension', 'Heart Disease', 'Kidney Disease', 'High Cholesterol'])
    
    if condition in HEALTH_MEAL_PLANS:
        plan = HEALTH_MEAL_PLANS[condition]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Recommended Foods")
            for food in plan['recommended']:
                st.markdown(f"""
                <div class="health-tip">
                    <strong>{food}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("❌ Foods to Avoid")
            for food in plan['avoid']:
                st.markdown(f"""
                <div class="warning-box">
                    <strong>{food}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.subheader("💡 Dietary Tips")
        for tip in plan['tips']:
            st.write(f"• {tip}")
    
    # Medical disclaimer
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ Important Medical Disclaimer</h4>
        <p>These meal recommendations are for informational purposes only. Please consult with your healthcare provider 
        or a registered dietitian before making significant changes to your diet, especially if you have medical conditions.</p>
    </div>
    """, unsafe_allow_html=True)

def profile_page():
    st.markdown('<div class="main-header"><h1>👤 User Profile</h1><p>Manage your personal health information</p></div>', unsafe_allow_html=True)
    
    # Edit profile
    with st.form("profile_form"):
        st.subheader("📝 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.user_profile['name'])
            age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.user_profile['age'])
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=float(st.session_state.user_profile['weight']))
        
        with col2:
            height = st.number_input("Height (cm)", min_value=50, max_value=250, value=st.session_state.user_profile['height'])
            gender = st.selectbox("Gender", ['Female', 'Male', 'Other'], 
                                 index=['Female', 'Male', 'Other'].index(st.session_state.user_profile['gender']))
            activity_level = st.selectbox("Activity Level", 
                                        ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
                                        index=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'].index(st.session_state.user_profile['activity_level']))
        
        goal = st.selectbox("Primary Goal", 
                           ['Lose Weight', 'Maintain Weight', 'Gain Weight'],
                           index=['Lose Weight', 'Maintain Weight', 'Gain Weight'].index(st.session_state.user_profile['goal']))
        
        health_conditions = st.multiselect("Health Conditions", 
                                          ['None', 'Diabetes', 'Hypertension', 'Heart Disease', 'Kidney Disease', 'High Cholesterol'],
                                          default=st.session_state.user_profile['health_conditions'])
        
        if st.form_submit_button("💾 Save Profile"):
            st.session_state.user_profile.update({
                'name': name,
                'age': age,
                'weight': weight,
                'height': height,
                'gender': gender,
                'activity_level': activity_level,
                'goal': goal,
                'health_conditions': health_conditions
            })
            st.success("Profile updated successfully!")
            st.rerun()
    
    # Health metrics
    st.subheader("📊 Health Metrics")
    
    profile = st.session_state.user_profile
    bmi = calculate_bmi(profile['weight'], profile['height'])
    category, color = get_bmi_category(bmi)
    daily_calories = calculate_daily_calories(profile)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BMI", f"{bmi:.1f}", category)
    
    with col2:
        st.metric("Daily Calories", f"{daily_calories}")
    
    with col3:
        st.metric("Water Goal", "8 glasses")
    
    with col4:
        st.metric("Sleep Target", "7-8 hours")
    
    # Recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    recommendations = []
    
    if bmi < 18.5:
        recommendations.append("Consider increasing calorie intake with healthy Nepali foods like nuts and dairy")
    elif bmi > 25:
        recommendations.append("Focus on portion control and include more vegetables in your Dal Bhat")
    
    if 'Diabetes' in profile['health_conditions']:
        recommendations.append("Choose brown rice over white rice and monitor carbohydrate portions")
    
    if 'Hypertension' in profile['health_conditions']:
        recommendations.append("Reduce salt in your cooking and avoid pickled foods")
    
    if not recommendations:
        recommendations.append("Maintain your current healthy lifestyle with balanced Nepali meals!")
    
    for rec in recommendations:
        st.info(rec)

if __name__ == "__main__":
    main()