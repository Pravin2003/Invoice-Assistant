# Invoice Assistant

## Overview

The Invoice Assistant is a Flask-based web application designed to analyze and provide information from invoice documents. It utilizes Google Generative AI for natural language processing and Chroma for document retrieval. This application allows users to upload invoices and ask questions about the invoice details.

## Features

- Upload and process invoice PDFs.
- Ask questions about various invoice components.
- Get responses based on the information extracted from the invoice.
- Provides clear, concise, and relevant answers about invoice data.

## Prerequisites

- Python 3.x
- Flask
- Google API Key
- Required Python libraries

## Setup

1. **Clone the repository:**

    ```bash
    git clone `https://github.com/Pravin2003/Invoice-Assistant.git`,
    cd Invoice-Assistant
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv       # On MacOS
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required Python libraries:**

    ```bash
    pip install flask langchain_community langchain_google_genai google.generativeai
    ```

4. **Set up the Google API key:**

    Ensure you have a Google API key and set it in your environment variables:

    ```bash
    export GOOGLE_API_KEY="your-google-api-key"
    ```

    On Windows, use:

    ```bash
    set GOOGLE_API_KEY="your-google-api-key"
    ```

5. **Add your invoice file:**

    Place your invoice PDF file in the `sample/` directory. The file should be named `sample-invoice.pdf` or change the file path in the code accordingly.

## Running the Application

1. **Start the Flask application:**

    ```bash
    python app.py
    ```

2. **Access the web application:**

    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Upload your invoice PDF:**

    Place the invoice PDF in the `sample/` directory.

2. **Ask Questions:**

    - Type your question into the input field on the web page.
    - Click the "Send" button to submit your question.

3. **Receive Answers:**

    - The assistant will provide answers based on the information extracted from the invoice.

## Folder Structure

- `app.py` - Main Flask application file.
- `templates/` - Directory containing HTML templates.
  - `index.html` - Main HTML file for the web interface.
- `static/` - Directory containing static files like CSS and JavaScript.
  - `styles.css` - CSS styles for the web interface.
  - `script.js` - JavaScript for handling user interactions.
- `sample/` - Directory for storing invoice PDFs.

## Troubleshooting

- **Google API Key Error:** Ensure the `GOOGLE_API_KEY` environment variable is set correctly.
- **Missing PDF File:** Ensure your invoice PDF is correctly placed in the `sample/` directory.
- **Library Issues:** Make sure all required libraries are installed and up-to-date.

## Contact

For any questions or issues, please contact [qa.pravin.misal@gmail.com](mailto:qa.pravin.misal@gmail.com).
