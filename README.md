🎬 MOODFLIX: AI-Driven Recommendation Engine

A decoupled microservice architecture for real-time human emotion detection and content curation.

⚡ System Overview

MoodFlix is a production-ready, full-stack machine learning application. It utilizes a dual-node architecture to ensure that heavy neural network inference does not block the user interface.

By capturing real-time biometric data via webcam, the system encodes the video frame, transmits it securely to a RESTful processing API, and extracts the dominant emotional state using spatial feature mapping to recommend highly contextual media.

🕸️ Architecture & Data Flow

[ Client Node (Streamlit) ]                          [ Inference Node (FastAPI) ]
       │                                                    │
       ├─► 1. Capture Image Array                           │
       ├─► 2. Encode to Base64                              │
       ├─► 3. POST /api/analyze  ────────(Network)────────► ├─► 4. Decode payload
       │                                                    ├─► 5. OpenCV Matrix Conversion
       │                                                    ├─► 6. DeepFace Neural Net Inference
       │ ◄───────(JSON Response)─────────(Network)──────────┤ ◄─7. Map Emotion to Movie Vector
       ├─► 8. Render Dynamic UI                             │


🛠️ Technical Implementation

The Inference Engine (Backend)

Framework: FastAPI with Uvicorn (ASGI) for asynchronous, non-blocking request handling.

Computer Vision: cv2 (OpenCV) is used to decode incoming base64 streams into RGB numpy arrays.

Deep Learning: Integrates the DeepFace framework to perform multi-stage facial analysis, bypassing strict alignment requirements (enforce_detection=False) to ensure robustness in varied lighting and angles.

The Interactive Client (Frontend)

Framework: Streamlit for rapid, state-managed UI deployment.

Styling: Injected custom CSS to override default themes, creating a "cinematic" dark-mode layout with responsive data cards and neon typography.

🚀 Deployment / Local Setup

Run the application locally by spinning up both microservices.

1. Install Dependencies

git clone https://github.com/YOUR_USERNAME/moodflix.git
cd moodflix
pip install -r requirements.txt


2. Initialize the Inference API (Service 1)

python backend.py
# Engine active at http://localhost:8000


3. Initialize the Client UI (Service 2)

streamlit run frontend.py
# Dashboard active at http://localhost:8501


🔮 Future Scaling Roadmap

Vector Database Integration: Migrate the static movie dictionary to a vector database (e.g., Pinecone or Qdrant) for semantic search.

TMDB API Implementation: Fetch real-time movie posters, trailers, and ratings.

Automated Testing Pipeline: Implement pytest and GitHub Actions for continuous integration of the AI model endpoints.
