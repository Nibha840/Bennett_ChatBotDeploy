Bennett University Chatbot (BU-Chatbot)

This project features an AI-powered conversational chatbot specifically designed to answer Frequently Asked Questions (FAQs) about Bennett University (Greater Noida, India). It leverages a custom machine learning model to provide instant and accurate information across various topics, including admissions, courses, fees, placements, and campus life.



Key Features-------------
University-Specific Knowledge: Answers cover essential areas of the university:

Admissions Process & Deadlines

B.Tech, Management (MBA/BBA), and Law Programs

Fee Structure & Scholarship Details

Placement Statistics & Top Recruiters

Hostel Facilities & Student Life

Intuitive Web Interface: A modern, responsive chat UI (index.html, styles.css) featuring a dark/light mode toggle and pre-defined suggestion prompts.

Custom Deep Learning Model: Uses a two-layer fully connected Neural Network (FCNN) built with PyTorch for Natural Language Understanding (NLU).

Data Augmentation: Implements Synonym Replacement using nltk.corpus.wordnet to create a more robust and diverse training dataset.

Scalable Backend: Deployed via a Flask REST API (app.py) to efficiently handle chat requests from the frontend.

⚙️ Technology Stack

Category,Technology,Purpose
Backend,"Python, Flask",Serving the chatbot model and handling API requests.
Model,"PyTorch, NumPy","Building, training, and running the Neural Network model."
NLP,"NLTK (WordNet, Lemmatization)","Tokenization, text preprocessing, and data augmentation."
Frontend,"HTML5, CSS3, JavaScript",User interface and handling client-side interactions.


Model Architecture (FCNN)
The core of the chatbot is a Feedforward Neural Network implemented in PyTorch, defined in bu_chatbot.py.

Input Layer: Size equals the number of unique lemmatized words (Bag-of-Words vector).

Hidden Layers: Two hidden layers (size 8 each) with ReLU activation.

Output Layer: Size equals the number of intent tags (classes).

Activation: Softmax is used on the output layer for probability distribution.

Loss Function: nn.BCELoss()

Optimizer: optim.Adam()



🚀 Setup and Installation
Follow these steps to set up and run the project locally.

1. Clone the repository
Bash

git clone <YOUR_REPO_URL>
cd Gemini-Chatbot-Frontend-Project

2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment:


python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
.\venv_fresh\Scripts\Activate.ps1 
3. Install Required Packages
The backend requires the dependencies listed in your requirements.txt (Flask, torch, nltk, numpy, scikit-learn).

Bash

pip install -r requirements.txt
4. Ensure Model File is Present
The trained model weights, model.pth, must be present in the project's root directory. (Note: This file is intentionally ignored by Git to manage repository size.)

5. Run the Flask Backend
Start the API server by running the Flask application file:

Bash

# Ensure the virtual environment is active
python app.py
The server will run at http://127.0.0.1:5000 (or http://localhost:5000).

6. Open the Frontend
Open the index.html file in your web browser (double-click it). The JavaScript (script.js) is configured to send chat messages to the Flask endpoint at http://127.0.0.1:5000/chat.


.\venv_fresh
\Scripts\Activate.ps1 
python app.py