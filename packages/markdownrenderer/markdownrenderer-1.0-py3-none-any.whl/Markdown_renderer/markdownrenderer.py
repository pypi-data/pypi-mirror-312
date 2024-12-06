import markdown
from flask import Flask, render_template_string
import threading
import webview

# Flask app setup
app = Flask(__name__)

# Global variable for Markdown content
md_text = ""

# Function to convert markdown to HTML
def parser():
    global md_text
    html_output = markdown.markdown(md_text)
    return html_output

# Flask route to serve the rendered HTML content
@app.route('/')
def home():
    # Convert Markdown to HTML
    html_content = parser()

    # Wrap HTML content in a full HTML structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Markdown Renderer</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    return render_template_string(full_html)

# Function to start the Flask server
def start_flask_server():
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)

# Function to start Flask server and open webview
def start_server_with_webview():
    # Start Flask server in a background thread
    threading.Thread(target=start_flask_server, daemon=True).start()

    # Display the URL in the terminal and open it in Webview
    url = "http://127.0.0.1:5000"
    print(f"Flask app is running at: {url}")

    # Open the URL in a webview window
    webview.create_window("Markdown Renderer", url)
    webview.start()

# The render function that can be called by the user
def render(markdown_text):
    global md_text
    md_text = markdown_text
    start_server_with_webview()

