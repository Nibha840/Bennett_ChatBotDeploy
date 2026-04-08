from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
import bu_chatbot

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Initialize the model when the app starts
try:
    model = bu_chatbot.initialize_model()
    bu_chatbot._model = model
    bu_chatbot.model = model  # Update the exported model variable
    print("Model initialized successfully!")
except Exception as e:
    print(f"Error initializing model: {e}")
    model = None
    bu_chatbot._model = None

# Get references to the needed variables and functions
words = bu_chatbot.words
classes = bu_chatbot.classes
generate_response = bu_chatbot.generate_response

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend"""
    if model is None:
        return jsonify({'reply': "Sorry, the chatbot model is not available. Please check the server logs."}), 500
    
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'reply': "Please provide a message in your request."}), 400
        
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'reply': "Please enter a message."}), 400
        
        bot_reply = generate_response(user_input, model, words, classes)
        return jsonify({'reply': bot_reply})
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'reply': f"An error occurred: {str(e)}"}), 500

# Serve static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
