
import streamlit as st
import pickle
import requests  # Add this import statement

# Load the prediction model and scaler
model_path = 'https://github.com/omarabdallah235/Crop-recommendation/raw/main/Crop%20Recommendation%20Random%20Forst%20Model.pkl'
response_model = requests.get(model_path)
model = pickle.load(response_model.content)
scaler1_path = 'https://github.com/omarabdallah235/Crop-recommendation/raw/main/Crop%20Recommendation%20scale.pkl'
response_scaler = requests.get(scaler1_path)
scaler1 = pickle.load(response_scaler.content)
# Crop mapping
names = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
         'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
         'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
         'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']
num = [20, 11, 3, 9, 18, 13, 14, 2, 10, 19, 1, 12, 7, 21, 15, 0, 16,
       17, 4, 6, 8, 5]
crop_mapping = dict(zip(num, names))

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
    st.write("your Inputs:")
    st.write(f"""
             Nitrogen: {nitrogen}, Phosphorus: {phosphorus}, Potassium: {potassium}
             Temperature: {temperature}, Humidity: {humidity},pH: {ph}" , Rainfall: {rainfall} 
             """)

    # Collect user inputs in a list
    user_inputs = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]

    # Button to trigger prediction
    if st.button("Predict"):
        # Perform prediction using the user inputs
        predicted_crop = predict_crop(user_inputs)
        st.write(f"Predicted Crop: {predicted_crop}")

# Function for prediction logic
def predict_crop(user_inputs):
    # Scale user inputs and perform prediction
    scaled_inputs = scaler1.transform([user_inputs])
    predicted_crop_num = model.predict(scaled_inputs)[0]

    # Map numerical prediction to crop name
    predicted_crop = crop_mapping.get(predicted_crop_num, 'Unknown Crop')

    return predicted_crop

if __name__ == "__main__":
    main()
