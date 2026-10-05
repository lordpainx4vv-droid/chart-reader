import os
from flask import Flask, render_template_string, request
from google import genai
from google.genai import types
from PIL import Image

app = Flask(__name__)

# Apnar Gemini API key ekhane ba Render Environment Variable e dite paren
# Ekhane string er bhitor apnar key-ta bosiye dite paren ba niche environment variable use korte paren
API_KEY = os.environ.get("AQ.Ab8RN6Jg8bp-J4YD8maWBct5CmHT5vNfdPuTt65GsKDW769VgQ", "APNAR_API_KEY_EKHANE_BOSABEN")

client = genai.Client(api_key=API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Chart Time & Candle Analyzer</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; text-align: center; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; max-width: 450px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        input[type="file"] { margin: 15px 0; color: #cbd5e1; }
        button { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2563eb; }
        .result { margin-top: 20px; text-align: left; background: #0f172a; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📈 Chart Time & Candle Reader</h2>
        <p>Upload trading chart screenshot</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required><br>
            <button type="submit">Analyze with AI</button>
        </form>
        {% if result %}
            <div class="result">{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                # PIL Image load kora
                image = Image.open(file.stream)
                
                # Gemini ke prompt dewa je time soho candle bole dite
                prompt = (
                    "Analyze this trading chart image. Look at the candles and the corresponding time scale at the bottom. "
                    "List out the candles sequence with their respective times in this exact format:\n"
                    "11:15 - GREEN CANDLE\n"
                    "11:20 - RED CANDLE\n"
                    "Provide a clean list of the recent candles visible on the chart."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                result = response.text
            except Exception as e:
                result = f"Error: {str.S(e) if hasattr(e, 'S') else str(e)}"
                
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
