import streamlit as st
import pickle

# Load the prediction model and scaler
model = pickle.load(open('Crop Recommendation Random Forst Model.pkl', 'rb'))
scaler1 = pickle.load(open('Crop Recommendation scale.pkl', 'rb'))

# Crop mapping
names = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
         'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
         'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
         'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']
num = [20, 11, 3, 9, 18, 13, 14, 2, 10, 19, 1, 12, 7, 21, 15, 0, 16,
       17, 4, 6, 8, 5]
crop_mapping = dict(zip(num, names))

# Function for prediction logic
def predict_crop(user_inputs):
    # Scale user inputs and perform prediction
    scaled_inputs = scaler1.transform([user_inputs])
    predicted_crop_num = model.predict(scaled_inputs)[0]

    # Map numerical prediction to crop name
    predicted_crop = crop_mapping.get(predicted_crop_num, 'Unknown Crop')

    return predicted_crop

def main():
    st.title("Crop Recommendation App")
    st.markdown("<h3 style='text-align: justify; font-size: 20px;'>Data-driven recommendations for achieving optimal nutrient and environmental conditions to improve crop yield.</h3>", unsafe_allow_html=True)

    # Get user inputs
    # ... (your existing code for user inputs)

    # Button to trigger prediction
    if st.button("Predict"):
        # Perform prediction using the user inputs
        predicted_crop = predict_crop(user_inputs)

        # Display predicted crop with image and style
        st.write(f"<p style='font-size: 24px; font-weight: bold;'>Predicted Crop: {predicted_crop}</p>", unsafe_allow_html=True)
        
        # Add images/icons for each crop
        crop_images = {
            'rice': 'https://en.wikipedia.org/wiki/Rice#/media/File:20201102.Hengnan.Hybrid_rice_Sanyou-1.6.jpg',
            'maize': 'https://en.wikipedia.org/wiki/Maize#/media/File:YellowCorn.jpg',
            # Add paths for other crops
        }

        if predicted_crop.lower() in crop_images:
            st.image(crop_images[predicted_crop.lower()], caption=f"Image for {predicted_crop}", use_column_width=True)
        else:
            st.warning("Image not available for the predicted crop.")

if __name__ == "__main__":
    main()
