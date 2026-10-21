import streamlit as st
import requests
import base64

# Page Configuration
st.set_page_config(page_title="MoodFlix AI", page_icon="🎬", layout="centered")

# Custom CSS for a Pleasant Blue Cinematic UI
st.markdown('''
<style>
    /* Main Background Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0b192c, #112d4e, #3f72af);
        color: white;
    }
    
    /* Transparent Header */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Text Colors */
    h1, h2, h3, p {
        color: #dbeafe !important;
    }
    
    /* Result Card Styling */
    .result-card {
        background: rgba(17, 45, 78, 0.6);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #3f72af;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    
    .emotion-highlight {
        color: #60a5fa !important;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        text-transform: capitalize;
        margin: 10px 0;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
    }
    
    .movie-item {
        font-size: 1.2rem;
        padding: 10px;
        border-bottom: 1px solid rgba(63, 114, 175, 0.3);
    }
</style>
''', unsafe_allow_html=True)

# UI Header
st.title("🎬 MoodFlix AI Engine")
st.markdown("Look at the camera and capture an image to let our AI detect your mood.")

# Streamlit Camera Input
picture = st.camera_input("Take a photo to analyze")

if picture is not None:
    # Convert Streamlit's image object to a base64 string
    bytes_data = picture.getvalue()
    base64_img = base64.b64encode(bytes_data).decode('utf-8')
    
    # Format payload to match what FastAPI expects
    payload = {
        "image_base64": f"data:image/jpeg;base64,{base64_img}"
    }
    
    with st.spinner("🧠 DeepFace is analyzing your facial features..."):
        try:
            # Send data to your local FastAPI backend
            response = requests.post("http://localhost:8000/api/analyze", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "success":
                    emotion = data["emotion"]
                    movies = data["recommendations"]
                    
                    # Render the Results Card via HTML injection
                    movie_list_html = "".join([f'<li class="movie-item">🍿 {movie}</li>' for movie in movies])
                    
                    st.markdown(f'''
                    <div class="result-card">
                        <h3 style="text-align: center;">Detected Mood:</h3>
                        <div class="emotion-highlight">{emotion}</div>
                        <h4 style="margin-top: 20px;">Curated Recommendations:</h4>
                        <ul style="list-style: none; padding-left: 0;">
                            {movie_list_html}
                        </ul>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("Face not detected clearly. Please try again.")
            else:
                st.error(f"Backend error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🚨 Connection Refused. Ensure your FastAPI backend (`backend.py`) is currently running on port 8000.")
