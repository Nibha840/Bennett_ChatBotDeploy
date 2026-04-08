BU-CHATBOT PROJECT – Interview Preparation Guide
1. PROJECT UNDERSTANDING
What Problem Does This Project Solve?
Bennett University receives many repeated questions (admissions, courses, fees, placements, campus life). This chatbot gives instant, automated answers to these FAQs so that:
Prospective students get quick answers
Admissions staff spend less time on repetitive questions
Information is consistent and easy to access
Who Are the Users?
Prospective students (admissions, courses, fees, scholarships)
Parents (fees, hostel, placements)
Anyone wanting general information about Bennett University
Main Workflow
User opens the web app and sees suggestions.
User types or clicks a suggestion.
Frontend sends a POST request to /chat with { message: userText }.
Backend tokenizes and lemmatizes the text (NLTK).
Input is converted to a Bag-of-Words vector.
PyTorch neural network predicts an intent.
A random response for that intent is returned.
Frontend shows the reply with a typing effect and saves it in localStorage.
Core Features
Feature	Implementation
Intent classification	PyTorch 2-layer FCNN (Bag-of-Words)
Data augmentation	Synonym replacement (WordNet/NLTK)
Web chat UI	Vanilla HTML/CSS/JS
Dark/Light theme	CSS variables + localStorage
Chat history persistence	localStorage
Suggestion prompts	Pre-defined clickable chips
Typing effect	Word-by-word display
Fallback handling	Pattern-overlap heuristic when model confidence is low
Architecture
┌─────────────────┐     POST /chat      ┌─────────────────────┐│   Frontend      │ ──────────────────► │   Flask Backend     ││  (HTML/CSS/JS)  │ ◄────────────────── │   (app.py)          ││                 │     JSON {reply}    │                     │└─────────────────┘                     │   ┌───────────────┐  │        │                               │   │ bu_chatbot.py │  │        │                               │   │ - NLTK        │  │   localStorage                         │   │ - PyTorch     │  │   (theme, chats)                       │   │ - model.pth   │  │                                        │   └───────────────┘  │                                        └─────────────────────┘
Frontend: Static HTML/CSS/JS
Backend: Flask REST API (single server)
Database: None (in-memory intents, model, and optional localStorage on the client)
Data Flow (Text)
User Input → Tokenize (NLTK) → Lemmatize (WordNetLemmatizer)   → Bag-of-Words vector → PyTorch model → Softmax → Intent tag   → Random response from intents JSON → JSON reply → Frontend
Folder Structure
BU-CHATBOTProject/├── app.py              # Flask API, / and /chat routes, CORS├── bu_chatbot.py       # NLU: intents, model, training, inference├── index.html          # Chat UI, suggestions, form├── styles.css          # Theming, responsive layout├── script.js           # API calls, typing effect, localStorage├── requirements.txt    # Flask, torch, nltk, scikit-learn, gunicorn├── model.pth           # Trained PyTorch weights (git LFS)├── Procfile            # gunicorn for deployment├── runtime.txt         # python-3.10.12└── images/             # logo, avatar (logo.svg, user.jpg, gemini.svg)
Important Files and Logic
File	Purpose
app.py	Loads model at startup, /chat POST endpoint, static files
bu_chatbot.py	Intents, preprocessing, augmentation, FCNN, generate_response()
script.js	generateAPIResponse() → fetch(APIURL, {POST, body: {message}}), typing effect, theme toggle
index.html	Form, suggestion chips, chat container
Demo Script (Approx. 2 Minutes)
> “This is the Bennett University Chatbot, built for Bennett University in Greater Noida.
>
> It answers FAQs about admissions, courses, fees, placements, and campus life.
>
> Under the hood, it uses a PyTorch feedforward neural network trained on about 150+ patterns across 25 intents. We use NLTK for tokenization and lemmatization, and WordNet for synonym-based data augmentation.
>
> [Show UI] The UI supports dark and light mode, suggestion chips, and chat history stored in the browser.
>
> [Type: “What is the admission process?”] The user message is sent to our Flask backend, which converts it to a Bag-of-Words vector, runs the model, and returns the appropriate response.
>
> [Type: “Tell me about placements”] If the model is unsure, we fall back to a pattern-overlap heuristic before returning a generic “I don’t understand” message.
>
> The backend is stateless and can be deployed with gunicorn on platforms like Render.”
2. TECH STACK QUESTIONS
Frontend
Question	Answer
Framework/Library	Vanilla HTML5, CSS3, JavaScript (no framework)
Component structure	Single-page app: header, chat list, typing area, suggestion chips
State management	localStorage (theme, chat history) + isResponseGenerating flag
Forms	Single form with required on input, e.preventDefault() on submit
Validation	HTML5 required, JS checks userMessage.trim() and isResponseGenerating
API integration	fetch() to http://localhost:5000/chat or window.location.origin + "/chat"
Performance	Typing effect uses setInterval; DOM updates kept minimal
Error handling	try/catch, response.ok, .error class on failed messages
Backend
Question	Answer
API design	REST-like: POST /chat with { message }, returns { reply }
Controllers/Services	Single route: chat() in app.py
Repositories	None; intents stored in Python dict in bu_chatbot.py
Authentication	None
Authorization	None (public endpoint)
Middleware	CORS via flask_cors.CORS(app)
Exception handling	try/except in chat(), returns 400/500 and JSON errors
Pagination	N/A (single-turn chat)
Validation	Checks data, message, and non-empty message before processing
Database
Question	Answer
Schema design	No database; intents in Python dict
Relationships	N/A
Indexing	N/A
Normalization	N/A
Queries	Intent lookup by tag (in-memory loop)
Transactions	N/A
Note: You can say that for a FAQ chatbot you intentionally used in-memory intents to avoid DB overhead, but you’d use a DB if you added logging, analytics, or user accounts.
3. SYSTEM DESIGN
High-Level Architecture
[ Browser ] ──► [ Flask + Gunicorn ] ──► [ PyTorch Model (in-memory) ]     │                    │     │                    └── model.pth (load at startup)     │     └── localStorage (theme, chats)
Scaling for ~10k Users
Horizontal scaling: Run multiple gunicorn workers (e.g. gunicorn -w 4 app:app).
Load balancer: Put Nginx or a cloud LB in front.
Caching: Cache responses for repeated questions (e.g. Redis keyed by lemmatized input).
Model serving: Move model to a separate service (TorchServe, FastAPI) behind a queue.
Async: Use async workers (e.g. gevent) to improve concurrency.
Performance Improvements
Caching: Cache responses for common queries.
Model optimization: TorchScript, ONNX, or quantization.
Preprocessing: Pre-load NLTK data at startup.
CDN: Serve static assets via CDN.
Connection pooling: If you add a DB, use connection pooling.
Caching Strategy
Key: hash(lemmatized_input)Value: { reply, timestamp }TTL: 1 hour (optional)Flow: Check cache → hit → return; miss → model inference → store → return
Deployment Architecture
GitHub → Render (or similar)  - Build: pip install -r requirements.txt && nltk.download punkt wordnet omw-1.4  - Start: gunicorn app:app --bind 0.0.0.0:$PORT  - Env: PORT, optional FLASK_ENV
CI/CD
No CI/CD config in the repo.
Suggested: GitHub Actions for lint, tests, optional build/deploy to Render.
4. LIVE DEMO QUESTIONS
Question	Answer
Why did you build this?	To automate FAQ answers for Bennett University and reduce repetitive work for admissions.
Login flow	There is no login; the app is public.
What happens when the user clicks a suggestion?	JS reads suggestion.querySelector(".text").innerText, sets userMessage, and calls handleOutgoingChat() as if the user had typed it.
How is the API called?	fetch(APIURL, { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({ message: userMessage }) })
Where is data stored?	Chats and theme in localStorage; no server-side storage.
Edge cases	Empty input, unknown words (BoW zeros → fallback), low confidence (< 0.15), follow-up phrases like “tell me more”.
Failure scenarios	Model not loaded (500), missing model.pth (trains from scratch or fails), network errors (error message in chat).
Security concerns	No auth, no rate limiting; leftover Gemini API key in script.js (currently unused).
5. CODING QUESTIONS
CRUD
No CRUD; single-turn chat only. To add CRUD you’d introduce a DB and endpoints for intents, chats, etc.
REST APIs
Design: POST /chat with { message } and { reply }.
Status codes: 200 (success), 400 (bad input), 500 (server error).
DSA Used
Bag-of-Words (sparse binary vector).
Token lists, sets for overlap fallback (sent_set.intersection(...)).
Train/test split with sklearn.model_selection.train_test_split.
Optimizations
Lower limit_per_tag for augmentation to speed training.
Use torch.no_grad() in inference.
ensure_model() loads or trains once; avoids repeated loading.
Refactoring Suggestions
Move intents to intents.json.
Use Flask blueprints for routes.
Add rate limiting (e.g. Flask-Limiter).
Remove or move the unused Gemini API key out of source.
Add request logging and health check (/health).
6. BEHAVIORAL + PROJECT QUESTIONS
Question	Sample Answer
Biggest challenge	Balancing model accuracy with coverage; using synonym augmentation and overlap fallback helped.
Bugs faced	sentence_to_features() expects full words vocab; handling empty inputs and out-of-vocab words.
How you debugged	print in Flask, browser DevTools for network and console, CLI in bu_chatbot.py for model behavior.
What you’d improve	Add auth, rate limiting, logging, more intents, fine-tuned LLM for complex questions, proper test suite.
Team contribution	Describe your role: model design, API, frontend, deployment.
Deadline handling	Prioritized core flow (chat → response) first, then UI polish and deployment.
7. SECURITY
Topic	Your Project	Notes
SQL injection	N/A	No database
XSS	Low risk	Responses from fixed intents; still sanitize if you add dynamic content
CSRF	Not implemented	Add CSRF if you introduce sessions/forms
Auth vulnerabilities	No auth	Add auth if you add protected endpoints
Password hashing	N/A	No auth
JWT/Session	None	Stateless API
Role-based access	None	Single public endpoint
Fixes to mention:
Remove or externalize the unused Gemini API key.
Add rate limiting (e.g. 60 req/min per IP).
Add input length limits (e.g. max 500 chars).
Use HTTPS in production.
8. DEPLOYMENT
Topic	Details
Platform	Render (web service)
Build command	pip install -r requirements.txt && python -m nltk.downloader punkt wordnet averaged_perceptron_tagger
Start command	gunicorn app:app
Procfile	web: gunicorn app:app --bind 0.0.0.0:$PORT
Env variables	PORT (Render), FLASK_ENV (optional)
Production build	Static assets served by Flask from .; no separate frontend build
Docker	Not used; could add a Dockerfile for local and cloud deployment
9. FINAL INTERVIEW CHEAT SHEET
Top 20 Likely Questions
What does this project do? – Bennett University FAQ chatbot using PyTorch NLU and Flask.
Tech stack? – Python, Flask, PyTorch, NLTK, vanilla JS, HTML/CSS.
How does the model work? – Bag-of-Words → 2-layer FCNN → softmax → intent → random response.
What is Bag-of-Words? – Binary vector of vocabulary; 1 if word present, 0 otherwise.
Why PyTorch? – Flexible, good for NLP prototyping and training.
Data augmentation? – Synonym replacement with WordNet.
How do you handle unknown queries? – Confidence threshold + pattern-overlap fallback.
Frontend framework? – Vanilla JS, no framework.
Database? – None; intents in memory.
Auth? – None; public endpoint.
API design? – POST /chat with { message } → { reply }.
How to scale? – More workers, load balancer, caching, separate model service.
Biggest challenge? – Accuracy vs coverage; used augmentation and fallback logic.
How deploy? – Flask + gunicorn on Render, Procfile + build/start commands.
model.pth? – Trained PyTorch weights; loaded at startup.
Rate limiting? – Not implemented; mention Flask-Limiter as improvement.
Error handling? – Try/catch, validation, 400/500 responses.
What would you add? – Auth, analytics, more intents, better model or LLM, tests.
Difference from rule-based? – Learns patterns and handles paraphrases instead of exact matches.
CORS? – Enabled with flask_cors.CORS(app) for cross-origin requests.
One-Line Explanations
Intent classification: Mapping user text to predefined categories (e.g. admissions, fees).
Lemmatization: Reducing words to base form (e.g. “running” → “run”).
Bag-of-Words: Representation ignoring word order, only presence/absence.
Softmax: Converts logits to probabilities that sum to 1.
CORS: Lets the browser allow requests from a different origin.
Red Flags to Avoid
Claiming a database when there isn’t one.
Claiming authentication when there isn’t any.
Mentioning the Gemini API key as if it’s used in production.
Overstating scalability (you’re on a simple single-service setup).
Saying “machine learning” without being able to explain BoW and intent prediction.
Ignoring security (rate limiting, input limits, no hardcoded secrets).
Saying you’d use the Gemini API without addressing cost and latency.
Quick Diagram: Inference Flow
User: "How do I apply?"  → Tokenize: [how, do, i, apply]  → Lemmatize: [how, do, i, apply]  → BoW: [0,1,0,...,1,...] (len = vocab size)  → Model: fc1(ReLU) → fc2 → Softmax  → Intent: bennett_admissions_process  → Response: random from that intent
