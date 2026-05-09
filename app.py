import webbrowser
from threading import Timer

from flask import Flask, render_template, request

from routes.api import api
from services.ml_service import (
    load_or_train,
    predict_one
)

from database.db import (
    init_db,
    save_prediction,
    get_history
)

# ======================================
# FLASK APP
# ======================================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ======================================
# INIT SYSTEM
# ======================================

load_or_train()
init_db()

# ======================================
# REGISTER API
# ======================================

app.register_blueprint(
    api,
    url_prefix="/api"
)

# ======================================
# HOME PAGE
# ======================================

@app.route("/")
def home():

    history = get_history()

    return render_template(
        "dashboard.html",
        history=history,
        pos=0,
        neg=0,
        neu=0
    )

# ======================================
# PREDICT SENTIMENT
# ======================================

@app.route("/predict", methods=["POST"])
def predict():

    text = request.form.get(
        "text",
        ""
    ).strip()

    if not text:

        return render_template(
            "dashboard.html",
            result="⚠️ Enter text",
            history=get_history(),
            pos=0,
            neg=0,
            neu=0
        )

    result = predict_one(text)

    # SAVE TO DATABASE
    save_prediction(text, result)

    history = get_history()

    return render_template(
        "dashboard.html",
        result=result,
        history=history,
        pos=0,
        neg=0,
        neu=0
    )

# ======================================
# AUTO OPEN BROWSER
# ======================================

def open_browser():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )

# ======================================
# RUN APP
# ======================================

if __name__ == "__main__":

    Timer(1, open_browser).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )