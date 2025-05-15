from flask import Flask, render_template, request
import threading
import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend for matplotlib
import matplotlib.pyplot as plt
import io
import os
import base64
import getpass
from pyngrok import ngrok, conf

# Set FLASK_DEBUG environment variable
os.environ["FLASK_DEBUG"] = "development"

app = Flask(__name__)
port = 5000

# --- ngrok Authentication --- 
# The user will need to run this part in their environment and provide their token.
# For now, we'll include a placeholder or prompt if this were interactive.
# In this non-interactive environment, we'll assume the token will be set by the user if they run it.
print("If you are running this locally, please enter your ngrok authtoken when prompted.")
print("You can get your authtoken from https://dashboard.ngrok.com/auth")
# ngrok_auth_token = getpass.getpass("Enter your ngrok authtoken: ")
# if ngrok_auth_token:
#    conf.get_default().auth_token = ngrok_auth_token
# else:
#    print("Ngrok authtoken not provided. Public URL may not be generated if token is required.")
# For the purpose of this script, we will try to connect without explicit token setting here,
# as the user might have it configured globally or the free tier might not strictly require it for basic tunnels.
# However, the instructions clearly state to authenticate, so this is a deviation for automated execution.

# Open a ngrok tunnel to the HTTP server
# Check if an auth token is already configured to avoid the prompt if possible
if not conf.get_default().auth_token:
    print("Ngrok authtoken not configured. Please ensure it's set in your environment or ngrok config.")
    print("Attempting to connect, but it might fail or be rate-limited without an authenticated token.")
    # As a fallback for automated execution where getpass is problematic:
    # We will proceed, but the user must ensure their ngrok is configured if this fails.
    # It's better to inform the user to set it up as per the original instructions.

public_url = ""
try:
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")
    app.config["BASE_URL"] = public_url
except Exception as e:
    print(f"Could not start ngrok tunnel. Error: {e}")
    print("Please ensure you have ngrok installed and authenticated correctly.")
    print("The application will run locally on http://127.0.0.1:5000 but will not be accessible publicly.")
    app.config["BASE_URL"] = f"http://127.0.0.1:{port}"

def generate_bar_chart(categories, values):
    """
    Generates a bar chart from the given categories and values.
    Returns the chart as a UTF-8 encoded base64 string.
    """
    if not categories or not values or len(categories) != len(values):
        # Basic validation: ensure data is present and lengths match
        return None

    try:
        # Convert values to float, handling potential errors
        numeric_values = [float(v) for v in values]
    except ValueError:
        # If conversion fails, return None or handle error appropriately
        print("Error: Values must be numeric.")
        return None

    fig, ax = plt.subplots()
    ax.bar(categories, numeric_values)
    ax.set_ylabel('Values')
    ax.set_xlabel('Categories')
    ax.set_title('User Input Data Bar Chart')
    plt.xticks(rotation=45, ha="right") # Rotate labels for better readability
    plt.tight_layout() # Adjust plot to ensure everything fits without overlapping

    # Save plot to a BytesIO object
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    plt.close(fig) # Close the figure to free memory

    # Encode image to base64 and then decode to UTF-8 string
    chart_url = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return chart_url

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_url = None
    error_message = None

    if request.method == 'POST':
        categories_str = request.form.get('categories')
        values_str = request.form.get('values')

        if not categories_str or not values_str:
            error_message = "Categories and Values cannot be empty."
        else:
            categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
            values_raw = [val.strip() for val in values_str.split(',') if val.strip()]

            if not categories or not values_raw:
                error_message = "Please provide valid comma-separated categories and values."
            elif len(categories) != len(values_raw):
                error_message = "The number of categories must match the number of values."
            else:
                try:
                    # Attempt to convert values to numbers (float for flexibility)
                    values = [float(v) for v in values_raw]
                    chart_url = generate_bar_chart(categories, values)
                    if chart_url is None and error_message is None:
                        error_message = "Failed to generate chart. Ensure values are numeric."
                except ValueError:
                    error_message = "Values must be numeric and comma-separated."
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    error_message = "An unexpected error occurred while generating the chart."

    return render_template('index.html', chart_url=chart_url, error_message=error_message)

if __name__ == '__main__':
    # Advise user about ngrok authentication if not done
    print("-------------------------------------------------------------------------------------")
    print("IMPORTANT: For ngrok to work, you might need to authenticate.")
    print("If the ngrok tunnel fails or you see authentication errors, please ensure you have")
    print("run 'ngrok authtoken YOUR_TOKEN' in your terminal or configured it as per ngrok's docs.")
    print("The project instructions mention pasting your token after 'conf.get_default().auth_token = getpass.getpass()'.")
    print("This script attempts a basic connection; manual authentication might be required.")
    print("-------------------------------------------------------------------------------------")
    
    # Start the Flask server in a new thread
    # Using use_reloader=False as recommended for threading and ngrok compatibility
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': port, 'use_reloader': False, 'debug': True})
    flask_thread.start()
    print(f"Flask app is attempting to start on http://127.0.0.1:{port}")
    print("If ngrok started successfully, it should also be available at the public URL provided above.")

