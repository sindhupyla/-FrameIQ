# -FrameIQ
# 🎥 Video Feature Vector API

A FastAPI application that:

- Accepts video file uploads
- Extracts frames from the video every second
- Computes feature vectors (color histograms)
- Stores them in a Qdrant vector database
- Allows similarity search based on an input image

---

## 🚀 Features

- Upload `.mp4` video files
- Extract frames using OpenCV
- Compute 512-dimensional color histogram vectors
- Store vectors with frame names in Qdrant
- Query similar frames using an image

---

## 🛠️ Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- OpenCV
- NumPy
- Qdrant Client

---

## 📁 Folder Structure

-FrameIQ/
├── main.py
├── utils.py
├── qdrant_setup.py
├── requirements.txt
├── README.md
├── frames/ # Stores extracted frames
├── query_images/ # Stores uploaded query images


# 1️⃣ Clone the repository
git clone https://github.com/your-username/FrameIQ.git
cd FrameIQ

# 2️⃣ Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # For Windows

# 3️⃣ Upgrade pip and setuptools to avoid distutils errors
python -m pip install --upgrade pip setuptools

# 4️⃣ Install required dependencies
pip install -r requirements.txt

# 5️⃣ Run the FastAPI app
uvicorn main:app --reload
🌐 Access the App
Home page (welcome + link): http://127.0.0.1:8000

Swagger UI (API testing): http://127.0.0.1:8000/docs


📤 API Endpoints

▶️ POST /upload-video/
Upload an MP4 file

Extracts 1 frame per second

Saves them in /frames/

Computes and stores feature vectors in Qdrant

Example response:

{
  "message": "Frames extracted and feature vectors stored.",
  "frames": [
    "frames/frame_0.jpg",
    "frames/frame_1.jpg"
  ]
}
🔍 POST /query/
Upload an image to search for similar frames.

[
  {
    "frame": "frame_1.jpg",
    "score": 0.02
  },
  ...
]
🔧 Optional: Add Welcome Route
Already included in main.py:

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>🎥 Welcome to the Video Feature API</h2>
    <p>Use <a href="/docs">/docs</a> to access the Swagger UI and test the API endpoints.</p>
    """
💾 Sample Video Format
Format: .mp4

Recommendation: short videos with clear visuals for testing

All extracted frames are saved as .jpg files in the frames/ directory

📸 Sample Query Image
Upload .jpg or .png image

The image is processed into a feature vector and compared with stored frame vectors

🧹 Cleanup
Manually delete contents of /frames/ and /query_images/ if needed

Or automate it by adding cleanup code to main.py

🧠 Qdrant Backend
The app uses in-memory Qdrant:

No need for a separate Qdrant server

Data is temporary (resets on restart)

To persist data, you can connect to a local Qdrant instance

🐞 Troubleshooting
❌ No module named 'distutils'?
Run:
pip install --upgrade pip setuptools

❌ Python 3.12 Compatibility Issues?
Make sure you're using this updated requirements.txt:

fastapi==0.95.2
uvicorn[standard]==0.22.0
opencv-python==4.9.0.80
numpy==1.26.4
qdrant-client==1.6.0
python-multipart==0.0.9
