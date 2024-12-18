from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert
import os
import logging

# Flask app setup
app = Flask(__name__, template_folder='../frontend')  # Specify the path to the templates folder
app.config['UPLOAD_FOLDER'] = '../uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# Database setup
engine = create_engine('sqlite:///../database/onboarding.db')
metadata = MetaData()

candidates = Table(
    'candidates', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('phone', String),
    Column('address', String)
)
metadata.create_all(engine)

# Home route to serve the HTML form
@app.route('/')
def home():
    logging.debug("Serving home page.")
    return render_template('index.html')  # This will render the index.html from the frontend folder

# File upload route
@app.route('/upload', methods=['POST'])
def upload_files():
    logging.debug("Received a POST request at /upload")
    
    if 'files' not in request.files:
        return jsonify({'error': 'No files found in the request'}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No valid files uploaded'}), 400

    responses = []
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logging.info(f"Saved file: {filepath}")
        
        # Extract data using the AI model (placeholder function)
        extracted_data = extract_data(filepath)
        responses.append({'filename': filename, 'data': extracted_data})
        
        # Save extracted data to the database
        save_to_database(extracted_data)

    return jsonify(responses)

# Placeholder function for AI-based data extraction
def extract_data(filepath):
    # Replace this logic with your actual AI/ML model
    logging.info(f"Processing file at: {filepath}")
    return {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'address': '123 Main Street'
    }

# Function to save data to the database
def save_to_database(data):
    with engine.connect() as conn:
        stmt = insert(candidates).values(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address']
        )
        conn.execute(stmt)
        logging.info(f"Inserted data into database: {data}")

if __name__ == '__main__':
    app.run(debug=True)
