import spacy
import streamlit as st
import re

# Load the spaCy model for natural language processing
nlp = spacy.load('en_core_web_sm')

# Sample dataset of electric 2-wheelers
electric_vehicles = [
    {"name": "E-Scooter 3000", "price": 950, "range": 45, "vehicle_type": "scooter"},
    {"name": "EcoBike 200", "price": 1200, "range": 60, "vehicle_type": "bike"},
    {"name": "Speedster EV", "price": 800, "range": 50, "vehicle_type": "scooter"}
]

# Function to preprocess user input
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return tokens

# Function to extract key entities from the user's input
def extract_entities(text):
    doc = nlp(text)
    entities = {
        'price': None,
        'range': None,
        'vehicle_type': None
    }
    
    # Extract price and range using NER
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            entities['price'] = ent.text
        if ent.label_ == "QUANTITY":
            # Ensure to extract only numeric part of the range
            if "mile" in ent.text:
                entities['range'] = re.search(r'\d+', ent.text).group()
    
    # Determine vehicle type from the text
    if "scooter" in text.lower():
        entities['vehicle_type'] = "scooter"
    elif "bike" in text.lower():
        entities['vehicle_type'] = "bike"
    
    return entities

# Function to recommend vehicles based on user preferences
def recommend_vehicle(user_preferences, dataset):
       recommendations = []
       for vehicle in dataset:
           price = user_preferences['price']
           range_ = user_preferences['range']
           
           if price:
               try:
                   price = int(price.replace('$', '').replace(',', ''))
               except ValueError:
                   price = None
           
           if range_:
               try:
                   range_ = int(range_.replace(' miles', ''))
               except ValueError:
                   range_ = None
           
           if (price is None or vehicle['price'] <= price) and \
              (range_ is None or vehicle['range'] >= range_) and \
              (user_preferences['vehicle_type'] is None or user_preferences['vehicle_type'] == vehicle['vehicle_type']):
               recommendations.append(vehicle['name'])
       
       return recommendations

# Streamlit interface for user input and displaying recommendations
st.title("Electric 2-Wheeler Recommendation System")

# Input box for the user to describe their requirements
user_input = st.text_input("Tell us what you're looking for in an electric vehicle:")

if user_input:
    # Process the input and extract user preferences
    user_preferences = extract_entities(user_input)
    
    # Recommend vehicles based on the user's input
    recommended_vehicles = recommend_vehicle(user_preferences, electric_vehicles)
    
    # Display the recommendations
    if recommended_vehicles:
        st.write("Recommended Vehicles:")
        for vehicle in recommended_vehicles:
            st.write(vehicle)
    else:
        st.write("No vehicles found matching your criteria.")
