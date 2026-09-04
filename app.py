from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# HTML + CSS + JAVASCRIPT
# --------------------------------------------------

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Digital Wellness AI</title>

<style>

/* =================================================
   GLOBAL
================================================= */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;
    color: white;
    overflow-x: hidden;

    background:
        radial-gradient(circle at 10% 20%, rgba(0, 255, 200, 0.18), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(150, 0, 255, 0.20), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(255, 0, 100, 0.15), transparent 30%),
        #080814;
}


/* =================================================
   ANIMATED BACKGROUND
================================================= */

body::before {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;

    background: linear-gradient(
        135deg,
        #00ffe1,
        #7b2cff,
        #ff007a
    );

    filter: blur(150px);
    opacity: 0.12;

    top: -150px;
    left: -100px;

    animation: moveGlow 12s infinite alternate;

    z-index: -2;
}

body::after {
    content: "";
    position: fixed;
    width: 400px;
    height: 400px;

    background: #ff008c;

    filter: blur(160px);
    opacity: 0.10;

    right: -100px;
    bottom: -100px;

    animation: moveGlow2 10s infinite alternate;

    z-index: -2;
}

@keyframes moveGlow {

    0% {
        transform: translate(0, 0) scale(1);
    }

    100% {
        transform: translate(250px, 200px) scale(1.3);
    }

}

@keyframes moveGlow2 {

    0% {
        transform: translate(0, 0);
    }

    100% {
        transform: translate(-200px, -150px);
    }

}


/* =================================================
   FLOATING PARTICLES
================================================= */

.particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: -1;
}

.particle {
    position: absolute;
    width: 5px;
    height: 5px;

    background: #00ffe1;

    border-radius: 50%;

    box-shadow:
        0 0 10px #00ffe1,
        0 0 20px #00ffe1;

    animation: floatParticle linear infinite;
}

@keyframes floatParticle {

    from {
        transform: translateY(110vh);
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    to {
        transform: translateY(-10vh);
        opacity: 0;
    }

}


/* =================================================
   MAIN CONTAINER
================================================= */

.container {

    width: 94%;
    max-width: 1200px;

    margin: 40px auto;

}


/* =================================================
   HEADER
================================================= */

.header {
    text-align: center;
    margin-bottom: 35px;
}

.badge {

    display: inline-block;

    padding: 8px 18px;

    border: 1px solid rgba(0,255,225,0.5);

    border-radius: 50px;

    color: #00ffe1;

    background: rgba(0,255,225,0.07);

    box-shadow:
        0 0 20px rgba(0,255,225,0.12);

    font-size: 13px;

    letter-spacing: 2px;

    margin-bottom: 15px;

}

.header h1 {

    font-size: clamp(38px, 6vw, 72px);

    font-weight: 900;

    letter-spacing: -3px;

    background:
        linear-gradient(
            90deg,
            #00ffe1,
            #7b5cff,
            #ff2c9c,
            #00ffe1
        );

    background-size: 300%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation: gradientText 5s linear infinite;

}

@keyframes gradientText {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }

}

.header p {

    margin-top: 12px;

    color: #aaaabe;

    font-size: 16px;

}


/* =================================================
   MAIN CARD
================================================= */

.main-card {

    position: relative;

    padding: 30px;

    border-radius: 28px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.10);

    backdrop-filter: blur(20px);

    box-shadow:
        0 30px 100px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.08);

}


/* =================================================
   GRID
================================================= */

.form-grid {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 18px;

}


/* =================================================
   INPUT CARD
================================================= */

.input-card {

    padding: 18px;

    border-radius: 18px;

    background: rgba(8,8,25,0.65);

    border: 1px solid rgba(255,255,255,0.08);

    transition: 0.3s;

}

.input-card:hover {

    transform: translateY(-4px);

    border-color: rgba(0,255,225,0.45);

    box-shadow:
        0 10px 30px rgba(0,255,225,0.08);

}

.input-card label {

    display: block;

    font-size: 13px;

    font-weight: bold;

    margin-bottom: 9px;

    color: #d9d9eb;

}


/* =================================================
   INPUTS
================================================= */

input,
select {

    width: 100%;

    padding: 13px 14px;

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.10);

    background: rgba(255,255,255,0.055);

    color: white;

    outline: none;

    font-size: 14px;

    transition: 0.3s;

}

input:focus,
select:focus {

    border-color: #00ffe1;

    box-shadow:
        0 0 0 3px rgba(0,255,225,0.08),
        0 0 20px rgba(0,255,225,0.15);

}

select option {

    background: #101020;

    color: white;

}


/* =================================================
   SPECIAL COLORS
================================================= */

.input-card:nth-child(1) label {
    color: #00ffe1;
}

.input-card:nth-child(2) label {
    color: #ff6bd6;
}

.input-card:nth-child(3) label {
    color: #7f9cff;
}

.input-card:nth-child(4) label {
    color: #ffd166;
}

.input-card:nth-child(5) label {
    color: #ff7b9c;
}

.input-card:nth-child(6) label {
    color: #65f5a1;
}

.input-card:nth-child(7) label {
    color: #72d8ff;
}

.input-card:nth-child(8) label {
    color: #c084fc;
}

.input-card:nth-child(9) label {
    color: #ff9f43;
}

.input-card:nth-child(10) label {
    color: #00d4ff;
}

.input-card:nth-child(11) label {
    color: #ff5c8a;
}

.input-card:nth-child(12) label {
    color: #a78bfa;
}

.input-card:nth-child(13) label {
    color: #34d399;
}


/* =================================================
   PREDICT AREA
================================================= */

.predict-area {

    text-align: center;

    margin-top: 30px;

}


/* =================================================
   PREDICT BUTTON
================================================= */

.predict-btn {

    position: relative;

    width: min(100%, 430px);

    padding: 18px 35px;

    border: none;

    border-radius: 16px;

    color: white;

    font-size: 16px;

    font-weight: 800;

    letter-spacing: 2px;

    cursor: pointer;

    overflow: hidden;

    background:
        linear-gradient(
            90deg,
            #00c9a7,
            #6c5ce7,
            #ff2e93,
            #00c9a7
        );

    background-size: 300%;

    box-shadow:
        0 0 25px rgba(0,255,220,0.20),
        0 15px 40px rgba(0,0,0,0.3);

    animation: buttonGradient 5s linear infinite;

    transition: 0.3s;

}

@keyframes buttonGradient {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }

}

.predict-btn:hover {

    transform: translateY(-4px) scale(1.02);

    box-shadow:
        0 0 35px rgba(0,255,220,0.35),
        0 20px 50px rgba(0,0,0,0.4);

}

.predict-btn:active {

    transform: scale(0.96);

}


/* Shine effect */

.predict-btn::before {

    content: "";

    position: absolute;

    top: 0;
    left: -100%;

    width: 60%;
    height: 100%;

    background:
        linear-gradient(
            110deg,
            transparent,
            rgba(255,255,255,0.45),
            transparent
        );

    transform: skewX(-20deg);

}

.predict-btn:hover::before {

    animation: shine 0.8s;

}

@keyframes shine {

    from {
        left: -100%;
    }

    to {
        left: 140%;
    }

}


/* =================================================
   LOADING EFFECT
================================================= */

.predict-btn.loading {

    pointer-events: none;

    animation:
        buttonGradient 2s linear infinite,
        pulseButton 0.8s infinite alternate;

}

@keyframes pulseButton {

    from {
        box-shadow:
            0 0 20px rgba(0,255,220,0.25);
    }

    to {
        box-shadow:
            0 0 45px rgba(255,0,160,0.50);
    }

}

.spinner {

    display: inline-block;

    width: 18px;
    height: 18px;

    border: 3px solid rgba(255,255,255,0.3);

    border-top-color: white;

    border-radius: 50%;

    vertical-align: middle;

    margin-right: 10px;

    animation: spin 0.7s linear infinite;

}

@keyframes spin {

    to {
        transform: rotate(360deg);
    }

}


/* =================================================
   RESULT
================================================= */

.result {

    margin-top: 30px;

    padding: 30px;

    text-align: center;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(0,255,225,0.08),
            rgba(120,50,255,0.08)
        );

    border: 1px solid rgba(0,255,225,0.25);

    animation: resultAppear 0.8s cubic-bezier(.17,.67,.31,1.3);

}

@keyframes resultAppear {

    0% {

        opacity: 0;

        transform:
            translateY(35px)
            scale(0.85)
            rotateX(15deg);

    }

    100% {

        opacity: 1;

        transform:
            translateY(0)
            scale(1)
            rotateX(0);

    }

}

.result-icon {

    width: 90px;
    height: 90px;

    margin: 0 auto 18px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    font-size: 42px;

    background:
        rgba(0,255,225,0.08);

    border: 2px solid #00ffe1;

    box-shadow:
        0 0 20px rgba(0,255,225,0.25),
        inset 0 0 25px rgba(0,255,225,0.08);

    animation: iconPulse 1.5s infinite alternate;

}

@keyframes iconPulse {

    from {
        transform: scale(1);
    }

    to {
        transform: scale(1.08);
    }

}

.result h2 {

    font-size: 28px;

    margin-bottom: 8px;

}

.result p {

    color: #a9a9c0;

}


/* =================================================
   SCAN OVERLAY
================================================= */

.scan-overlay {

    display: none;

    position: fixed;

    inset: 0;

    background:
        rgba(3,3,15,0.88);

    backdrop-filter: blur(8px);

    z-index: 999;

    align-items: center;

    justify-content: center;

    flex-direction: column;

}

.scan-overlay.active {

    display: flex;

}

.scan-ring {

    width: 120px;
    height: 120px;

    border-radius: 50%;

    border: 2px solid rgba(0,255,225,0.2);

    border-top-color: #00ffe1;

    border-right-color: #ff2c9c;

    box-shadow:
        0 0 30px rgba(0,255,225,0.25);

    animation:
        scanSpin 1s linear infinite;

}

@keyframes scanSpin {

    to {
        transform: rotate(360deg);
    }

}

.scan-text {

    margin-top: 25px;

    color: #00ffe1;

    font-size: 15px;

    font-weight: bold;

    letter-spacing: 4px;

    animation: blink 0.8s infinite alternate;

}

@keyframes blink {

    from {
        opacity: 0.35;
    }

    to {
        opacity: 1;
    }

}


/* =================================================
   FOOTER
================================================= */

.footer {

    text-align: center;

    color: #67677d;

    margin-top: 25px;

    font-size: 12px;

}


/* =================================================
   MOBILE
================================================= */

@media(max-width: 750px) {

    .container {

        width: 94%;

        margin: 25px auto;

    }

    .main-card {

        padding: 18px;

        border-radius: 20px;

    }

    .form-grid {

        grid-template-columns: 1fr;

    }

    .header h1 {

        letter-spacing: -2px;

    }

    .predict-btn {

        width: 100%;

    }

}

</style>

</head>


<body>


<!-- Floating particles -->

<div class="particles">

    <div class="particle" style="left:5%; animation-duration:9s;"></div>
    <div class="particle" style="left:15%; animation-duration:12s;"></div>
    <div class="particle" style="left:28%; animation-duration:8s;"></div>
    <div class="particle" style="left:42%; animation-duration:14s;"></div>
    <div class="particle" style="left:55%; animation-duration:10s;"></div>
    <div class="particle" style="left:68%; animation-duration:13s;"></div>
    <div class="particle" style="left:80%; animation-duration:9s;"></div>
    <div class="particle" style="left:92%; animation-duration:15s;"></div>

</div>


<!-- AI scanning overlay -->

<div class="scan-overlay" id="scanOverlay">

    <div class="scan-ring"></div>

    <div class="scan-text">
        AI ANALYZING PROFILE...
    </div>

</div>


<div class="container">


    <!-- HEADER -->

    <div class="header">

        <div class="badge">
            ✦ AI DIGITAL WELLNESS ENGINE
        </div>

        <h1>
            Digital Wellness AI
        </h1>

        <p>
            Analyze your digital lifestyle using machine learning
        </p>

    </div>


    <!-- MAIN CARD -->

    <div class="main-card">

        <form
            method="POST"
            id="predictionForm"
        >

            <div class="form-grid">


                <!-- 1 -->

                <div class="input-card">

                    <label>👤 Age</label>

                    <input
                        type="number"
                        name="age"
                        min="1"
                        max="100"
                        placeholder="Enter your age"
                        required
                    >

                </div>


                <!-- 2 -->

                <div class="input-card">

                    <label>⚧ Gender</label>

                    <select name="gender" required>

                        <option value="">
                            Select gender
                        </option>

                        <option value="0">
                            Female
                        </option>

                        <option value="1">
                            Male
                        </option>

                    </select>

                </div>


                <!-- 3 -->

                <div class="input-card">

                    <label>📱 Daily Screen Time (Hours)</label>

                    <input
                        type="number"
                        name="daily_screen_time_hours"
                        step="0.1"
                        min="0"
                        placeholder="Example: 6.5"
                        required
                    >

                </div>


                <!-- 4 -->

                <div class="input-card">

                    <label>📲 Social Media Hours</label>

                    <input
                        type="number"
                        name="social_media_hours"
                        step="0.1"
                        min="0"
                        placeholder="Example: 2.5"
                        required
                    >

                </div>


                <!-- 5 -->

                <div class="input-card">

                    <label>🎮 Gaming Hours</label>

                    <input
                        type="number"
                        name="gaming_hours"
                        step="0.1"
                        min="0"
                        placeholder="Example: 1.5"
                        required
                    >

                </div>


                <!-- 6 -->

                <div class="input-card">

                    <label>📚 Work / Study Hours</label>

                    <input
                        type="number"
                        name="work_study_hours"
                        step="0.1"
                        min="0"
                        placeholder="Example: 7"
                        required
                    >

                </div>


                <!-- 7 -->

                <div class="input-card">

                    <label>😴 Sleep Hours</label>

                    <input
                        type="number"
                        name="sleep_hours"
                        step="0.1"
                        min="0"
                        max="24"
                        placeholder="Example: 7.5"
                        required
                    >

                </div>


                <!-- 8 -->

                <div class="input-card">

                    <label>🔔 Notifications Per Day</label>

                    <input
                        type="number"
                        name="notifications_per_day"
                        min="0"
                        placeholder="Example: 80"
                        required
                    >

                </div>


                <!-- 9 -->

                <div class="input-card">

                    <label>📈 App Opens Per Day</label>

                    <input
                        type="number"
                        name="app_opens_per_day"
                        min="0"
                        placeholder="Example: 60"
                        required
                    >

                </div>


                <!-- 10 -->

                <div class="input-card">

                    <label>🌐 Weekend Screen Time</label>

                    <input
                        type="number"
                        name="weekend_screen_time"
                        step="0.1"
                        min="0"
                        placeholder="Example: 8"
                        required
                    >

                </div>


                <!-- 11 -->

                <div class="input-card">

                    <label>🧠 Stress Level</label>

                    <select name="stress_level" required>

                        <option value="">
                            Select level
                        </option>

                        <option value="1">
                            1 — Very Low
                        </option>

                        <option value="2">
                            2 — Low
                        </option>

                        <option value="3">
                            3 — Moderate
                        </option>

                        <option value="4">
                            4 — High
                        </option>

                        <option value="5">
                            5 — Very High
                        </option>

                    </select>

                </div>


                <!-- 12 -->

                <div class="input-card">

                    <label>🎓 Academic Work Impact</label>

                    <select name="academic_work_impact" required>

                        <option value="">
                            Select impact
                        </option>

                        <option value="0">
                            0 — No Impact
                        </option>

                        <option value="1">
                            1 — Low
                        </option>

                        <option value="2">
                            2 — Moderate
                        </option>

                        <option value="3">
                            3 — High
                        </option>

                        <option value="4">
                            4 — Very High
                        </option>

                    </select>

                </div>


                <!-- 13 -->

                <div class="input-card">

                    <label>⚡ Addiction Level</label>

                    <select name="addiction_level" required>

                        <option value="">
                            Select level
                        </option>

                        <option value="1">
                            1 — Very Low
                        </option>

                        <option value="2">
                            2 — Low
                        </option>

                        <option value="3">
                            3 — Moderate
                        </option>

                        <option value="4">
                            4 — High
                        </option>

                        <option value="5">
                            5 — Very High
                        </option>

                    </select>

                </div>


            </div>


            <!-- BUTTON -->

            <div class="predict-area">

                <button
                    type="submit"
                    class="predict-btn"
                    id="predictBtn"
                >

                    <span id="buttonText">
                        ⚡ PREDICT WITH AI
                    </span>

                </button>

            </div>


        </form>


        {% if prediction is not none %}

        <div class="result">

            <div class="result-icon">

                {% if prediction == 1 %}
                    ⚠️
                {% else %}
                    ✨
                {% endif %}

            </div>


            {% if prediction == 1 %}

                <h2>
                    High Digital Wellness Risk
                </h2>

                <p>
                    The model indicates a higher level of digital dependency.
                </p>

            {% else %}

                <h2>
                    Healthy Digital Pattern
                </h2>

                <p>
                    The model indicates a healthier digital usage pattern.
                </p>

            {% endif %}

        </div>

        {% endif %}


    </div>


    <div class="footer">

        Powered by Machine Learning • Digital Wellness AI

    </div>


</div>


<script>


const form = document.getElementById("predictionForm");

const button = document.getElementById("predictBtn");

const buttonText = document.getElementById("buttonText");

const overlay = document.getElementById("scanOverlay");


form.addEventListener("submit", function() {

    /*
       Show full-screen AI scanning animation
    */

    overlay.classList.add("active");


    /*
       Change button appearance
    */

    button.classList.add("loading");

    buttonText.innerHTML =
        '<span class="spinner"></span> AI ANALYZING...';


    /*
       Prevent double clicking
    */

    button.disabled = true;

});


/*
   Add a small interactive effect
   when user moves mouse over the main card
*/

const card = document.querySelector(".main-card");

document.addEventListener("mousemove", function(e) {

    if (!card) return;

    const x =
        (window.innerWidth / 2 - e.clientX) / 80;

    const y =
        (window.innerHeight / 2 - e.clientY) / 80;

    card.style.transform =
        `perspective(1000px)
         rotateY(${x}deg)
         rotateX(${y}deg)`;

});


document.addEventListener("mouseleave", function() {

    card.style.transform =
        "perspective(1000px) rotateY(0deg) rotateX(0deg)";

});


</script>


</body>

</html>
"""


# --------------------------------------------------
# ROUTE
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        try:

            # --------------------------------------
            # GET INPUTS
            # --------------------------------------

            age = float(request.form["age"])

            gender = float(request.form["gender"])

            daily_screen_time_hours = float(
                request.form["daily_screen_time_hours"]
            )

            social_media_hours = float(
                request.form["social_media_hours"]
            )

            gaming_hours = float(
                request.form["gaming_hours"]
            )

            work_study_hours = float(
                request.form["work_study_hours"]
            )

            sleep_hours = float(
                request.form["sleep_hours"]
            )

            notifications_per_day = float(
                request.form["notifications_per_day"]
            )

            app_opens_per_day = float(
                request.form["app_opens_per_day"]
            )

            weekend_screen_time = float(
                request.form["weekend_screen_time"]
            )

            stress_level = float(
                request.form["stress_level"]
            )

            academic_work_impact = float(
                request.form["academic_work_impact"]
            )

            addiction_level = float(
                request.form["addiction_level"]
            )


            # --------------------------------------
            # MODEL INPUT
            # IMPORTANT:
            # Keep EXACT same order as training
            # --------------------------------------

            features = [[

                age,
                gender,
                daily_screen_time_hours,
                social_media_hours,
                gaming_hours,
                work_study_hours,
                sleep_hours,
                notifications_per_day,
                app_opens_per_day,
                weekend_screen_time,
                stress_level,
                academic_work_impact,
                addiction_level

            ]]


            # --------------------------------------
            # PREDICTION
            # --------------------------------------

            prediction = int(
                model.predict(features)[0]
            )


        except Exception as e:

            print("Prediction Error:", e)

            prediction = None


    return render_template_string(
        HTML,
        prediction=prediction
    )


# --------------------------------------------------
# RUN APP
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
