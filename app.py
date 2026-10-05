import os
from flask import Flask, render_template_string, request
import cv2
import numpy as np

app = Flask(__name__)

# HTML Design & Frontend ek sathei rakha holo jate apnar file beshi na banate hoy
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Chart Analyzer</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; text-align: center; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; max-width: 400px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        input[type="file"] { margin: 15px 0; color: #cbd5e1; }
        button { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2563eb; }
        .result { margin-top: 20px; font-size: 18px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📈 Chart Color Analyzer</h2>
        <p>Upload your trading chart screenshot</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required><br>
            <button type="submit">Analyze Chart</button>
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
            # Image read kora
            npimg = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            
            # HSV conversion
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Green & Red Range setting
            lower_green = np.array([35, 50, 50])
            upper_green = np.array([85, 255, 255])
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            red_mask = cv2.inRange(hsv, lower_red, upper_red)
            
            green_pixels = cv2.countNonZero(green_mask)
            red_pixels = cv2.countNonZero(red_mask)
            
            if green_pixels > red_pixels:
                result = "🟢 Market Trend: Bullish (Green candles beshi)"
            else:
                result = "🔴 Market Trend: Bearish (Red candles beshi)"
                
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
