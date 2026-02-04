from flask import Flask
from flask import render_template
import os


app=Flask(__name__)

@app.after_request
def allow_iframe(response):
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://your-site.com"
    return response
  
@app.route("/")
def render_index():
  return render_template("index.html")
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
