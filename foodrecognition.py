"""
Food Recognition Module for Nepalese Cuisine
This module simulates AI-powered food recognition for Nepalese dishes.
In a production environment, this would use computer vision models.
"""

import cv2
import numpy as np
from PIL import Image
import random

class NepaleseFoodRecognizer:
    def __init__(self):
        # Simulated food database with confidence scores
        self.food_database = {
            'Dal Bhat': {
                'calories_per_serving': 420,
                'confidence_threshold': 0.8,
                'typical_ingredients': ['rice', 'lentils', 'vegetables'],
                'visual_features': ['white_rice', 'yellow_dal', 'mixed_colors']
            },
            'Momo': {
                'calories_per_piece': 55,
                'confidence_threshold': 0.85,
                'typical_ingredients': ['flour', 'meat_or_vegetables'],
                'visual_features': ['dumpling_shape', 'pleated_edges']
            },
            'Gundruk Soup': {
                'calories_per_bowl': 120,
                'confidence_threshold': 0.75,
                'typical_ingredients': ['fermented_greens', 'broth'],
                'visual_features': ['green_color', 'liquid_consistency']
            },
            'Sel Roti': {
                'calories_per_piece': 90,
                'confidence_threshold': 0.9,
                'typical_ingredients': ['rice_flour', 'sugar'],
                'visual_features': ['ring_shape', 'golden_color']
            },
            'Chatamari': {
                'calories_per_piece': 120,
                'confidence_threshold': 0.8,
                'typical_ingredients': ['rice_flour', 'toppings'],
                'visual_features': ['flat_round', 'crepe_like']
            }
        }
    
    def preprocess_image(self, image):
        """Preprocess image for analysis"""
        # Convert PIL image to OpenCV format
        if isinstance(image, Image.Image):
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize image for processing
        height, width = image.shape[:2]
        if width > 640:
            scale = 640 / width
            new_width = 640
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        return image
    
    def detect_food_items(self, image):
        """
        Simulate food detection using computer vision
        In production, this would use trained ML models
        """
        processed_image = self.preprocess_image(image)
        
        # Simulate detection results
        detected_foods = []
        
        # Random detection simulation
        num_foods = random.randint(1, 3)
        available_foods = list(self.food_database.keys())
        
        for _ in range(num_foods):
            food_name = random.choice(available_foods)
            confidence = random.uniform(0.7, 0.95)
            
            # Estimate quantity based on food type
            if 'Momo' in food_name:
                quantity = random.randint(4, 8)
                calories = self.food_database[food_name]['calories_per_piece'] * quantity
                serving_info = f"{quantity} pieces"
            elif 'Sel Roti' in food_name:
                quantity = random.randint(1, 3)
                calories = self.food_database[food_name]['calories_per_piece'] * quantity
                serving_info = f"{quantity} pieces"
            else:
                quantity = 1
                calories = self.food_database[food_name].get('calories_per_serving', 
                          self.food_database[food_name].get('calories_per_bowl', 200))
                serving_info = "1 serving"
            
            detected_foods.append({
                'name': food_name,
                'confidence': confidence,
                'calories': calories,
                'quantity': quantity,
                'serving_info': serving_info
            })
            
            # Remove from available foods to avoid duplicates
            available_foods.remove(food_name)
        
        return detected_foods
    
    def analyze_nutritional_content(self, detected_foods):
        """Analyze nutritional content of detected foods"""
        total_calories = sum(food['calories'] for food in detected_foods)
        
        # Estimate macronutrients based on food types
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for food in detected_foods:
            food_name = food['name']
            calories = food['calories']
            
            # Rough macronutrient estimates for Nepalese foods
            if 'Dal Bhat' in food_name:
                protein_ratio = 0.12
                carb_ratio = 0.65
                fat_ratio = 0.08
            elif 'Momo' in food_name:
                protein_ratio = 0.18
                carb_ratio = 0.28
                fat_ratio = 0.16
            elif 'Gundruk' in food_name:
                protein_ratio = 0.20
                carb_ratio = 0.50
                fat_ratio = 0.13
            else:
                protein_ratio = 0.10
                carb_ratio = 0.60
                fat_ratio = 0.10
            
            total_protein += calories * protein_ratio / 4  # 4 cal per gram protein
            total_carbs += calories * carb_ratio / 4      # 4 cal per gram carbs
            total_fat += calories * fat_ratio / 9         # 9 cal per gram fat
        
        return {
            'total_calories': total_calories,
            'protein': round(total_protein, 1),
            'carbohydrates': round(total_carbs, 1),
            'fat': round(total_fat, 1)
        }
    
    def get_health_recommendations(self, detected_foods, user_health_conditions):
        """Provide health recommendations based on detected foods and user conditions"""
        recommendations = []
        
        for condition in user_health_conditions:
            if condition == 'Diabetes':
                for food in detected_foods:
                    if 'Dal Bhat' in food['name']:
                        recommendations.append("Consider brown rice instead of white rice for better blood sugar control")
                    elif 'Sel Roti' in food['name']:
                        recommendations.append("Limit sweet items like Sel Roti due to high sugar content")
            
            elif condition == 'Hypertension':
                recommendations.append("Be mindful of salt content in traditional preparations")
                recommendations.append("Consider steamed momos instead of fried versions")
            
            elif condition == 'Heart Disease':
                recommendations.append("Choose lean protein options and limit ghee usage")
                recommendations.append("Include more vegetables in your Dal Bhat")
        
        if not recommendations:
            recommendations.append("Your food choices look balanced! Maintain portion control.")
        
        return recommendations

# Example usage function
def analyze_food_image(image, user_health_conditions=None):
    """Main function to analyze food image and return results"""
    recognizer = NepaleseFoodRecognizer()
    
    # Detect foods in image
    detected_foods = recognizer.detect_food_items(image)
    
    # Analyze nutritional content
    nutrition = recognizer.analyze_nutritional_content(detected_foods)
    
    # Get health recommendations
    if user_health_conditions is None:
        user_health_conditions = ['None']
    
    recommendations = recognizer.get_health_recommendations(detected_foods, user_health_conditions)
    
    return {
        'detected_foods': detected_foods,
        'nutrition': nutrition,
        'recommendations': recommendations
    }