
import webbrowser
from flask import Flask, render_template, request

from routes.api import api
from services.ml_service import load_or_train, predict_one
from database.db import init_db, save_prediction, get_history

app = Flask(__name__, template_folder="templates", static_folder="static")

# ================= INIT SYSTEM =================
load_or_train()
init_db()

# Register API routes
app.register_blueprint(api)


# ================= HOME =================
@app.route("/")
def home():
    history = get_history()
    return render_template(
        "index.html",
        history=history,
        pos=0, neg=0, neu=0
    )


# ================= PREDICT =================
@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "").strip()

    if not text:
        return render_template(
            "index.html",
            result="⚠️ Enter text",
            history=get_history(),
            pos=0, neg=0, neu=0
        )

    result = predict_one(text)

    # 🔥 SAVE TO DATABASE
    save_prediction(text, result)

    history = get_history()

    return render_template(
        "index.html",
        result=result,
        history=history,
        pos=0, neg=0, neu=0
    )


# ================= RUN =================
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)