# Mini Project: Flask for ML Tasks - Bar Chart Generator

This project is a simple Flask web application that allows users to input categories and corresponding values, and then generates a bar chart visualization of the data.

## Project Structure

```
mini_flask_ml_project/
├── app.py                # Main Flask application logic
├── requirements.txt      # Python dependencies
├── static/
│   └── styles.css        # CSS for styling the webpage
└── templates/
    └── index.html        # HTML template for the user interface
```

## Features

- User-friendly web interface to input data (categories and values).
- Dynamic generation of a bar chart based on user input.
- Uses Matplotlib for chart generation and Flask for the web framework.
- Includes ngrok integration to (optionally) expose the local server to the internet.

## Setup and Installation

1.  **Clone or Download the Project:**
    Ensure you have all the project files in a directory named `mini_flask_ml_project`.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Navigate to the project root directory (`mini_flask_ml_project`) and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ngrok Authentication (Important for Public URL):**
    This application uses `ngrok` to create a public URL for your local Flask server. To use this feature, you need an ngrok account and an authtoken.

    *   Sign up for a free ngrok account at [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup).
    *   Get your authtoken from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).
    *   Authenticate ngrok in your terminal (you only need to do this once per machine usually):
        ```bash
        ngrok authtoken YOUR_AUTHTOKEN
        ```
        Replace `YOUR_AUTHTOKEN` with the token you copied.
    *   The `app.py` script also includes a section that *would* prompt for the token if run interactively with `getpass`. However, for automated environments or if you've already configured ngrok globally, this might be skipped or handled differently. The most reliable way is to configure ngrok globally using the command above.

## Running the Application

1.  **Navigate to the project directory:**
    ```bash
    cd path/to/mini_flask_ml_project
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```

3.  **Access the Application:**
    *   **Locally:** Open your web browser and go to `http://127.0.0.1:5000`.
    *   **Publicly (if ngrok is successful):** The script will print an ngrok URL to the console (e.g., `* ngrok tunnel "https://xxxx-xxxx.ngrok.io" -> "http://127.0.0.1:5000"`). You can use this public URL to access the application from anywhere.
        *Note: If ngrok authentication fails, the public URL will not be generated, but the application will still be accessible locally.*

## How to Use

1.  Open the application in your browser.
2.  In the "Categories" field, enter comma-separated category names (e.g., `Apples, Oranges, Bananas`).
3.  In the "Values" field, enter comma-separated numerical values corresponding to the categories (e.g., `10, 15, 7`).
4.  Click the "Generate Bar Chart" button.
5.  The bar chart will be displayed below the form.

## Code Overview

*   **`app.py`**: Contains the Flask routes and logic.
    *   `generate_bar_chart(categories, values)`: Takes lists of categories and values, generates a bar chart using Matplotlib, and returns it as a base64 encoded image string.
    *   `index()`: Handles both GET (displaying the form) and POST (processing form data and displaying the chart) requests for the root URL (`/`).
*   **`templates/index.html`**: Defines the HTML structure of the web page, including the form for data input and a placeholder for the chart image. It uses Jinja2 templating to display the chart dynamically.
*   **`static/styles.css`**: Contains basic CSS rules for styling the page and the chart container.
*   **`requirements.txt`**: Lists the Python packages required for the project (`Flask`, `matplotlib`, `pyngrok`).

## Notes

*   The project uses `matplotlib.use('Agg')` to ensure Matplotlib runs in a headless environment (without requiring a display server), which is suitable for web server backends.
*   Error handling is included for empty inputs, mismatched numbers of categories and values, and non-numeric values.
*   The Flask development server is used. For production, a more robust WSGI server (like Gunicorn or uWSGI) should be used.

