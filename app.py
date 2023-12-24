import streamlit as st
import pickle
import requests
from PIL import Image


# Load the prediction model and scaler
model_path = 'https://github.com/omarabdallah235/Crop-recommendation/raw/main/Crop%20Recommendation%20Random%20Forst%20Model.pkl'
response_model = requests.get(model_path)
model = pickle.loads(response_model.content)  # Use pickle.loads here

scaler1_path = 'https://github.com/omarabdallah235/Crop-recommendation/raw/main/Crop%20Recommendation%20scale.pkl'
response_scaler = requests.get(scaler1_path)
scaler1 = pickle.loads(response_scaler.content)  # Use pickle.loads here


# Crop mapping
names = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
         'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
         'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
         'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']
num = [20, 11, 3, 9, 18, 13, 14, 2, 10, 19, 1, 12, 7, 21, 15, 0, 16,
       17, 4, 6, 8, 5]
crop_mapping = dict(zip(num, names))

crop_images = {
    'rice': 'https://upload.wikimedia.org/wikipedia/commons/0/0a/20201102.Hengnan.Hybrid_rice_Sanyou-1.6.jpg',
    'maize': 'https://upload.wikimedia.org/wikipedia/commons/0/05/YellowCorn.jpg',
    'chickpea': 'https://upload.wikimedia.org/wikipedia/commons/e/ea/Sa-whitegreen-chickpea.jpg',
    'kidneybeans': 'https://upload.wikimedia.org/wikipedia/commons/2/27/Red_Rajma_BNC.jpg',
    'pigeonpeas': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Cap-Vert-Pois_secs.jpg',
    'mothbeans': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Matki.JPG',
    'mungbean': 'https://upload.wikimedia.org/wikipedia/commons/8/86/Mung_beans_%28Vigna_radiata%29.jpg',
    'blackgram': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Black_gram.jpg',
    'lentil': 'https://upload.wikimedia.org/wikipedia/commons/f/f5/3_types_of_lentil.png',
    'pomegranate': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Pomegranate_Juice_%282019%29.jpg',
    'banana': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Banana_and_cross_section.jpg',
    'mango': 'https://upload.wikimedia.org/wikipedia/commons/7/74/Mangos_-_single_and_halved.jpg',
    'grapes': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/Abhar-iran.JPG',
    'watermelon': 'https://upload.wikimedia.org/wikipedia/commons/a/ae/Watermelon_cross_BNC.jpg',
    'muskmelon': 'https://blog-images-1.pharmeasy.in/blog/production/wp-content/uploads/2021/05/18150019/shutterstock_1376235665-1-768x512.jpg',
    'apple': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg',
    'orange': 'https://upload.wikimedia.org/wikipedia/commons/e/e3/Oranges_-_whole-halved-segment.jpg',
    'papaya': 'https://upload.wikimedia.org/wikipedia/commons/0/09/Papaya_-_longitudinal_section.jpg',
    'coconut': 'https://s3.eu-west-1.amazonaws.com/assets.saps.org.uk/content/uploads/2022/06/Coconut_istock.jpg',
    'cotton': 'https://upload.wikimedia.org/wikipedia/commons/6/68/CottonPlant.JPG',
    'jute': 'https://upload.wikimedia.org/wikipedia/commons/8/84/Jute_-_Kolkata_2003-10-31_00538.JPG',
    'coffee': 'https://upload.wikimedia.org/wikipedia/commons/c/c5/Roasted_coffee_beans.jpg'
}


def main():
    st.title("Crop Recommendation App")
    st.markdown("<h3 style='text-align: justify; font-size: 20px;'>Data-driven recommendations for achieving optimal nutrient and environmental conditions to improve crop yield.</h3>", unsafe_allow_html=True)

    # Get user inputs
    nitrogen = st.number_input("Nitrogen Level - ratio of Nitrogen content in soil", 0.0, 100.0, 50.0, 1.0)
    phosphorus = st.number_input("Phosphorus Level - ratio of Phosphorous content in soil", 0.0, 100.0, 50.0, 1.0)
    potassium = st.number_input("Potassium Level - ratio of Potassium content in soil", 0.0, 100.0, 50.0, 1.0)
    temperature = st.number_input("Temperature- temperature in degree Celsius", 0.0, 100.0, 25.0, 1.0)
    humidity = st.number_input("Humidity - relative humidity in % ", 0.0, 100.0, 50.0, 1.0)
    ph = st.number_input("pH Level - ph value of the soil", 0.0, 14.0, 7.0, 0.1)
    rainfall = st.number_input("Rainfall - rainfall in mm")

    # Display user inputs
    st.write("Your Inputs:")
    st.write(f"""
             Nitrogen: {nitrogen}, Phosphorus: {phosphorus}, Potassium: {potassium}
             Temperature: {temperature}, Humidity: {humidity}, pH: {ph}, Rainfall: {rainfall} 
             """)

    # Collect user inputs in a list
    user_inputs = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
        # Add images/icons for each crop

    # Button to trigger prediction
    if st.button("Predict"):
         # Perform prediction using the user inputs
         predicted_crop = predict_crop(user_inputs)
         # Display predicted crop with image and style
         st.write(f"<p style='font-size: 24px; font-weight: bold;'>Predicted Crop: {predicted_crop}</p>", unsafe_allow_html=True)
         if predicted_crop in crop_images:
                  image_url = crop_images[predicted_crop]
                  st.image(image_url, width=400)
         else:
                  st.warning('No image available for the predicted crop.')


# Function for prediction logic
def predict_crop(user_inputs):
    # Scale user inputs and perform prediction
    scaled_inputs = scaler1.transform([user_inputs])
    predicted_crop_num = model.predict(scaled_inputs)[0]

    # Map numerical prediction to crop name
    predicted_crop = crop_mapping.get(predicted_crop_num, 'Unknown Crop')

    return predicted_crop
background_css = f"""
    <style>
        body {{
            background-image: url('https://raw.githubusercontent.com/omarabdallah235/Crop-recommendation/main/1280px-YellowCorn.jpg');  /* Replace with your image URL */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
"""
st.markdown(background_css, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
