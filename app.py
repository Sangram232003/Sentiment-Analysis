from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

# =========================================================
# LOAD MODEL + VECTORIZER
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "sentiment.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vector.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# =========================================================
# HTML
# =========================================================

HTML = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Sentiment AI Studio</title>


<style>

/* =====================================================
   RESET
===================================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


/* =====================================================
   BODY
===================================================== */

body {

    min-height: 100vh;

    font-family:
        Inter,
        Segoe UI,
        Arial,
        sans-serif;

    color: #ffffff;

    overflow-x: hidden;

    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(0, 255, 204, 0.18),
            transparent 28%
        ),

        radial-gradient(
            circle at 85% 20%,
            rgba(145, 70, 255, 0.22),
            transparent 30%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(255, 45, 135, 0.16),
            transparent 35%
        ),

        #070712;

}


/* =====================================================
   BACKGROUND GRID
===================================================== */

body::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background-image:

        linear-gradient(
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        );

    background-size: 45px 45px;

    mask-image:
        linear-gradient(
            to bottom,
            black,
            transparent
        );

    z-index: -5;

}


/* =====================================================
   GLOW ORBS
===================================================== */

.orb {

    position: fixed;

    border-radius: 50%;

    filter: blur(80px);

    pointer-events: none;

    z-index: -3;

}


.orb.one {

    width: 280px;
    height: 280px;

    background: #00ffd5;

    opacity: 0.12;

    top: -80px;
    left: -60px;

    animation: orbOne 12s infinite alternate ease-in-out;

}


.orb.two {

    width: 320px;
    height: 320px;

    background: #8b5cf6;

    opacity: 0.12;

    right: -100px;
    top: 25%;

    animation: orbTwo 15s infinite alternate ease-in-out;

}


.orb.three {

    width: 250px;
    height: 250px;

    background: #ff2f92;

    opacity: 0.10;

    bottom: -100px;
    left: 35%;

    animation: orbThree 11s infinite alternate ease-in-out;

}


@keyframes orbOne {

    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(220px, 180px);
    }

}


@keyframes orbTwo {

    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(-180px, 100px);
    }

}


@keyframes orbThree {

    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(150px, -100px);
    }

}


/* =====================================================
   PARTICLES
===================================================== */

.particles {

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: -2;

}


.particle {

    position: absolute;

    width: 4px;
    height: 4px;

    border-radius: 50%;

    background: #00ffe1;

    box-shadow:
        0 0 8px #00ffe1,
        0 0 18px #00ffe1;

    animation:
        particleMove linear infinite;

}


@keyframes particleMove {

    0% {

        transform:
            translateY(110vh)
            scale(0.5);

        opacity: 0;

    }

    15% {

        opacity: 1;

    }

    85% {

        opacity: 1;

    }

    100% {

        transform:
            translateY(-10vh)
            scale(1.2);

        opacity: 0;

    }

}


/* =====================================================
   MAIN WRAPPER
===================================================== */

.wrapper {

    width: 94%;

    max-width: 1050px;

    margin: auto;

    padding:
        55px 0 40px;

}


/* =====================================================
   HEADER
===================================================== */

.header {

    text-align: center;

    margin-bottom: 35px;

}


.status-pill {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    padding:
        8px 15px;

    border-radius: 50px;

    border:
        1px solid
        rgba(0,255,214,0.25);

    background:
        rgba(0,255,214,0.06);

    color: #64ffe7;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-bottom: 18px;

    box-shadow:
        0 0 25px
        rgba(0,255,214,0.07);

}


.status-dot {

    width: 7px;
    height: 7px;

    background: #00ffd5;

    border-radius: 50%;

    box-shadow:
        0 0 12px #00ffd5;

    animation:
        dotPulse 1.2s infinite;

}


@keyframes dotPulse {

    50% {

        transform: scale(1.5);

        opacity: 0.5;

    }

}


.header h1 {

    font-size:
        clamp(42px, 7vw, 78px);

    line-height: 0.95;

    font-weight: 900;

    letter-spacing: -4px;

    background:

        linear-gradient(
            90deg,
            #00ffe0,
            #8b5cf6,
            #ff3c9d,
            #00ffe0
        );

    background-size: 300%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        titleGradient 6s linear infinite;

}


@keyframes titleGradient {

    to {

        background-position:
            300%;

    }

}


.header p {

    margin-top: 17px;

    color: #9898b0;

    font-size: 15px;

}


/* =====================================================
   MAIN GLASS PANEL
===================================================== */

.panel {

    position: relative;

    border-radius: 30px;

    padding: 32px;

    background:

        linear-gradient(
            135deg,
            rgba(255,255,255,0.09),
            rgba(255,255,255,0.025)
        );

    border:
        1px solid
        rgba(255,255,255,0.10);

    backdrop-filter:
        blur(25px);

    -webkit-backdrop-filter:
        blur(25px);

    box-shadow:

        0 35px 100px
        rgba(0,0,0,0.50),

        inset
        0 1px 0
        rgba(255,255,255,0.08);

    transition:
        transform 0.2s ease;

}


/* top glow */

.panel::before {

    content: "";

    position: absolute;

    top: 0;
    left: 12%;

    width: 76%;
    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00ffe0,
            #8b5cf6,
            #ff3c9d,
            transparent
        );

    box-shadow:
        0 0 20px #8b5cf6;

}


/* =====================================================
   EDITOR HEADER
===================================================== */

.editor-header {

    display: flex;

    justify-content:
        space-between;

    align-items: center;

    margin-bottom: 15px;

}


.editor-title {

    display: flex;

    align-items: center;

    gap: 10px;

    color: #dddded;

    font-size: 14px;

    font-weight: 700;

}


.ai-icon {

    width: 30px;
    height: 30px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background:
        linear-gradient(
            135deg,
            #00d9bb,
            #7655ff
        );

    box-shadow:
        0 0 18px
        rgba(0,220,190,0.20);

}


/* =====================================================
   TEXTAREA
===================================================== */

.textarea-wrapper {

    position: relative;

}


textarea {

    width: 100%;

    min-height: 260px;

    resize: vertical;

    padding: 25px;

    border-radius: 22px;

    border:
        1px solid
        rgba(255,255,255,0.10);

    outline: none;

    color: #ffffff;

    background:

        linear-gradient(
            145deg,
            rgba(5,5,18,0.85),
            rgba(17,12,35,0.72)
        );

    font-family:
        inherit;

    font-size: 17px;

    line-height: 1.7;

    transition:
        0.35s;

    box-shadow:
        inset
        0 0 40px
        rgba(0,0,0,0.18);

}


textarea::placeholder {

    color: #66667c;

}


textarea:focus {

    border-color:
        rgba(0,255,215,0.65);

    box-shadow:

        0 0 0 4px
        rgba(0,255,215,0.06),

        0 0 45px
        rgba(0,255,215,0.10),

        inset
        0 0 40px
        rgba(0,255,215,0.025);

}


/* =====================================================
   TEXTAREA CORNER EFFECT
===================================================== */

.corner-light {

    position: absolute;

    width: 65px;
    height: 65px;

    right: -1px;
    bottom: -1px;

    border-right:
        2px solid #ff3c9d;

    border-bottom:
        2px solid #8b5cf6;

    border-radius:
        0 0 22px 0;

    pointer-events: none;

}


/* =====================================================
   CHARACTER COUNTER
===================================================== */

.editor-footer {

    display: flex;

    justify-content:
        space-between;

    align-items: center;

    margin-top: 10px;

    color: #68687d;

    font-size: 12px;

}


.hint {

    color: #78788d;

}


/* =====================================================
   PREDICT BUTTON AREA
===================================================== */

.action-area {

    display: flex;

    justify-content:
        center;

    margin-top: 25px;

}


.predict-btn {

    position: relative;

    width: 330px;

    max-width: 100%;

    padding: 17px 25px;

    border: none;

    border-radius: 16px;

    cursor: pointer;

    color: white;

    font-size: 14px;

    font-weight: 900;

    letter-spacing: 2px;

    overflow: hidden;

    background:

        linear-gradient(
            100deg,
            #00cdb3,
            #7155ff,
            #f72e91,
            #00cdb3
        );

    background-size: 300%;

    animation:
        buttonGradient 5s linear infinite;

    box-shadow:

        0 10px 35px
        rgba(0,0,0,0.35),

        0 0 25px
        rgba(0,220,190,0.15);

    transition:
        transform 0.25s,
        box-shadow 0.25s;

}


@keyframes buttonGradient {

    to {

        background-position:
            300%;

    }

}


.predict-btn:hover {

    transform:
        translateY(-4px)
        scale(1.02);

    box-shadow:

        0 15px 40px
        rgba(0,0,0,0.40),

        0 0 45px
        rgba(130,80,255,0.30);

}


.predict-btn:active {

    transform:
        scale(0.96);

}


/* moving shine */

.predict-btn::before {

    content: "";

    position: absolute;

    top: 0;

    left: -100%;

    width: 55%;

    height: 100%;

    background:
        linear-gradient(
            100deg,
            transparent,
            rgba(255,255,255,0.45),
            transparent
        );

    transform:
        skewX(-20deg);

}


.predict-btn:hover::before {

    animation:
        shine 0.8s;

}


@keyframes shine {

    to {

        left: 150%;

    }

}


/* =====================================================
   RESULT
===================================================== */

.result {

    margin-top: 30px;

    padding: 30px;

    border-radius: 25px;

    text-align: center;

    animation:
        resultEnter
        0.8s
        cubic-bezier(.16,1,.3,1);

}


.positive {

    border:
        1px solid
        rgba(0,255,150,0.35);

    background:
        linear-gradient(
            145deg,
            rgba(0,255,150,0.10),
            rgba(0,255,210,0.025)
        );

    box-shadow:
        0 0 50px
        rgba(0,255,150,0.08);

}


.negative {

    border:
        1px solid
        rgba(255,65,110,0.35);

    background:
        linear-gradient(
            145deg,
            rgba(255,50,100,0.10),
            rgba(255,0,80,0.025)
        );

    box-shadow:
        0 0 50px
        rgba(255,50,100,0.08);

}


@keyframes resultEnter {

    0% {

        opacity: 0;

        transform:
            translateY(40px)
            scale(0.88);

    }

    70% {

        transform:
            translateY(-5px)
            scale(1.02);

    }

    100% {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }

}


.result-icon {

    width: 90px;
    height: 90px;

    margin:
        0 auto 18px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    font-size: 40px;

    animation:
        resultPulse 1.5s
        infinite alternate;

}


.positive .result-icon {

    background:
        rgba(0,255,150,0.08);

    border:
        2px solid #00ff9d;

    box-shadow:
        0 0 30px
        rgba(0,255,150,0.25);

}


.negative .result-icon {

    background:
        rgba(255,50,100,0.08);

    border:
        2px solid #ff4770;

    box-shadow:
        0 0 30px
        rgba(255,50,100,0.25);

}


@keyframes resultPulse {

    from {

        transform:
            scale(1);

    }

    to {

        transform:
            scale(1.08);

    }

}


.result h2 {

    font-size: 30px;

    margin-bottom: 8px;

}


.result p {

    color: #a4a4b8;

}


/* =====================================================
   CONFIDENCE BAR
===================================================== */

.confidence {

    max-width: 480px;

    margin:
        25px auto 0;

    text-align: left;

}


.confidence-top {

    display: flex;

    justify-content:
        space-between;

    color: #85859a;

    font-size: 12px;

    margin-bottom: 8px;

}


.confidence-track {

    height: 8px;

    border-radius: 20px;

    background:
        rgba(255,255,255,0.07);

    overflow: hidden;

}


.confidence-fill {

    height: 100%;

    border-radius: 20px;

    width: {{ confidence }}%;

    background:
        linear-gradient(
            90deg,
            #00e0bd,
            #8b5cf6,
            #ff3c9d
        );

    box-shadow:
        0 0 15px
        rgba(120,80,255,0.5);

    animation:
        confidenceGrow
        1.2s ease-out;

}


@keyframes confidenceGrow {

    from {

        width: 0;

    }

}


/* =====================================================
   FOOTER
===================================================== */

.footer {

    text-align: center;

    margin-top: 25px;

    color: #57576d;

    font-size: 11px;

    letter-spacing: 1px;

}


/* =====================================================
   SCANNING SCREEN
===================================================== */

.scan-screen {

    position: fixed;

    inset: 0;

    z-index: 9999;

    display: none;

    align-items: center;

    justify-content: center;

    flex-direction: column;

    background:
        rgba(4,4,15,0.92);

    backdrop-filter:
        blur(14px);

}


.scan-screen.active {

    display: flex;

}


.scanner {

    position: relative;

    width: 150px;
    height: 150px;

    border-radius: 50%;

    border:
        2px solid
        rgba(0,255,215,0.15);

    box-shadow:
        0 0 60px
        rgba(0,255,215,0.08);

}


.scanner::before {

    content: "";

    position: absolute;

    inset: 12px;

    border-radius: 50%;

    border:
        2px solid
        transparent;

    border-top-color:
        #00ffe0;

    border-right-color:
        #8b5cf6;

    border-bottom-color:
        #ff3c9d;

    animation:
        scannerSpin
        1s linear infinite;

}


.scanner::after {

    content: "AI";

    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    font-weight: 900;

    font-size: 28px;

    color: #ffffff;

    text-shadow:
        0 0 20px
        #00ffe0;

}


@keyframes scannerSpin {

    to {

        transform:
            rotate(360deg);

    }

}


.scan-line {

    position: absolute;

    width: 170px;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00ffe0,
            transparent
        );

    box-shadow:
        0 0 15px
        #00ffe0;

    animation:
        scanLine
        1.5s
        infinite;

}


@keyframes scanLine {

    0% {

        transform:
            translateY(-85px);

        opacity: 0;

    }

    20% {

        opacity: 1;

    }

    80% {

        opacity: 1;

    }

    100% {

        transform:
            translateY(85px);

        opacity: 0;

    }

}


.scan-title {

    margin-top: 30px;

    font-size: 16px;

    font-weight: 900;

    letter-spacing: 4px;

    color: #00ffe0;

    animation:
        scanBlink
        0.8s
        infinite alternate;

}


.scan-subtitle {

    margin-top: 9px;

    color: #707089;

    font-size: 12px;

}


@keyframes scanBlink {

    from {

        opacity: 0.35;

    }

    to {

        opacity: 1;

    }

}


/* =====================================================
   RESPONSIVE
===================================================== */

@media(max-width: 700px) {

    .wrapper {

        padding-top: 30px;

    }

    .panel {

        padding: 18px;

        border-radius: 22px;

    }

    textarea {

        min-height: 230px;

        padding: 18px;

        font-size: 15px;

    }

    .header h1 {

        letter-spacing: -2px;

    }

    .editor-footer {

        flex-direction: column;

        align-items: flex-start;

        gap: 5px;

    }

}

</style>

</head>


<body>


<!-- Background -->

<div class="orb one"></div>
<div class="orb two"></div>
<div class="orb three"></div>


<div class="particles">

    <div class="particle"
         style="left:5%; animation-duration:10s;"></div>

    <div class="particle"
         style="left:16%; animation-duration:14s;"></div>

    <div class="particle"
         style="left:29%; animation-duration:9s;"></div>

    <div class="particle"
         style="left:42%; animation-duration:12s;"></div>

    <div class="particle"
         style="left:56%; animation-duration:15s;"></div>

    <div class="particle"
         style="left:69%; animation-duration:10s;"></div>

    <div class="particle"
         style="left:82%; animation-duration:13s;"></div>

    <div class="particle"
         style="left:94%; animation-duration:8s;"></div>

</div>


<!-- =================================================
     AI SCANNING SCREEN
================================================= -->

<div
    class="scan-screen"
    id="scanScreen"
>

    <div class="scanner">

        <div class="scan-line"></div>

    </div>

    <div class="scan-title">

        AI ANALYZING SENTIMENT

    </div>

    <div class="scan-subtitle">

        Processing your text with machine learning...

    </div>

</div>


<!-- =================================================
     MAIN
================================================= -->

<div class="wrapper">


    <!-- HEADER -->

    <div class="header">

        <div class="status-pill">

            <span class="status-dot"></span>

            AI SENTIMENT ENGINE ONLINE

        </div>


        <h1>

            Sentiment<br>

            AI Studio

        </h1>


        <p>

            Transform your words into intelligent sentiment insights.

        </p>

    </div>


    <!-- PANEL -->

    <div class="panel" id="panel">


        <form
            method="POST"
            id="sentimentForm"
        >


            <div class="editor-header">

                <div class="editor-title">

                    <div class="ai-icon">

                        ✦

                    </div>

                    Review Analyzer

                </div>


                <div>

                    NLP • ML

                </div>

            </div>


            <!-- TEXT INPUT -->

            <div class="textarea-wrapper">

                <textarea
                    name="review"
                    id="review"
                    maxlength="5000"
                    placeholder="Write or paste a review here...

Example:
The movie was absolutely amazing. I loved every moment and would definitely recommend it!"
                    required
                ></textarea>


                <div class="corner-light"></div>

            </div>


            <!-- EDITOR FOOTER -->

            <div class="editor-footer">

                <span class="hint">

                    💡 Tip: Enter a complete review for better analysis.

                </span>

                <span>

                    <span id="count">0</span> / 5000

                </span>

            </div>


            <!-- BUTTON -->

            <div class="action-area">

                <button
                    type="submit"
                    class="predict-btn"
                    id="predictBtn"
                >

                    <span id="buttonText">

                        ✦ PREDICT SENTIMENT

                    </span>

                </button>

            </div>


        </form>


        <!-- =================================================
             RESULT
        ================================================= -->

        {% if prediction %}

            <div
                class="result
                {% if prediction == 'positive' %}
                    positive
                {% else %}
                    negative
                {% endif %}"
            >


                <div class="result-icon">

                    {% if prediction == 'positive' %}

                        😊

                    {% else %}

                        😞

                    {% endif %}

                </div>


                {% if prediction == 'positive' %}

                    <h2>

                        Positive Sentiment

                    </h2>

                    <p>

                        Your review has been classified as positive.

                    </p>

                {% else %}

                    <h2>

                        Negative Sentiment

                    </h2>

                    <p>

                        Your review has been classified as negative.

                    </p>

                {% endif %}


                {% if confidence %}

                    <div class="confidence">

                        <div class="confidence-top">

                            <span>

                                AI Confidence

                            </span>

                            <span>

                                {{ confidence }}%

                            </span>

                        </div>


                        <div class="confidence-track">

                            <div class="confidence-fill"></div>

                        </div>

                    </div>

                {% endif %}


            </div>

        {% endif %}


    </div>


    <div class="footer">

        POWERED BY TF-IDF + MULTINOMIAL NAIVE BAYES

    </div>


</div>


<script>

/* =====================================================
   CHARACTER COUNTER
===================================================== */

const review = document.getElementById("review");

const count = document.getElementById("count");


review.addEventListener("input", function() {

    count.textContent =
        review.value.length;

});


/* =====================================================
   PREDICT BUTTON EFFECT
===================================================== */

const form =
    document.getElementById("sentimentForm");

const button =
    document.getElementById("predictBtn");

const buttonText =
    document.getElementById("buttonText");

const scanScreen =
    document.getElementById("scanScreen");


form.addEventListener("submit", function() {

    /*
       Full screen AI scanning effect
    */

    scanScreen.classList.add("active");


    /*
       Disable button
    */

    button.disabled = true;


    /*
       Change button text
    */

    buttonText.innerHTML =
        "◉ ANALYZING...";


});


/* =====================================================
   MOUSE PARALLAX EFFECT
===================================================== */

const panel =
    document.getElementById("panel");


document.addEventListener(
    "mousemove",
    function(event) {

        if (window.innerWidth < 800) {
            return;
        }


        const x =
            (window.innerWidth / 2 -
            event.clientX) / 100;


        const y =
            (window.innerHeight / 2 -
            event.clientY) / 100;


        panel.style.transform =
            `perspective(1200px)
             rotateY(${x}deg)
             rotateX(${-y}deg)`;

    }
);


document.addEventListener(
    "mouseleave",
    function() {

        panel.style.transform =
            "perspective(1200px)
             rotateY(0deg)
             rotateX(0deg)";

    }
);


/* =====================================================
   TEXTAREA GLOW
===================================================== */

review.addEventListener(
    "focus",
    function() {

        review.style.transform =
            "translateY(-2px)";

    }
);


review.addEventListener(
    "blur",
    function() {

        review.style.transform =
            "translateY(0)";

    }
);

</script>


</body>

</html>

"""


# =========================================================
# FLASK ROUTE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None

    if request.method == "POST":

        review = request.form.get("review", "").strip()

        if review:

            try:

                # -----------------------------------------
                # TRANSFORM TEXT USING TF-IDF
                # -----------------------------------------

                transformed_text = vectorizer.transform(
                    [review]
                )


                # -----------------------------------------
                # PREDICT
                # -----------------------------------------

                prediction = model.predict(
                    transformed_text
                )[0]


                # -----------------------------------------
                # CONFIDENCE
                # -----------------------------------------

                if hasattr(model, "predict_proba"):

                    probabilities = model.predict_proba(
                        transformed_text
                    )[0]

                    confidence = round(
                        max(probabilities) * 100,
                        2
                    )


                prediction = str(
                    prediction
                ).lower()


            except Exception as e:

                print("Prediction error:", e)

                prediction = None


    return render_template_string(
        HTML,
        prediction=prediction,
        confidence=confidence
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get("PORT", 5000)
        ),
        debug=False
    )
