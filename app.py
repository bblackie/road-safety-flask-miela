from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"

# The answers to the quiz
# Could include use of a recognised solution design pattern
# split the answers out to make adding more questions easy
# seperation of concerns
answers = {
    "SchoolBusSpeed": "20",
    "stopSignWait": "3",
    "GiveWay": "neither",
    "OpenSpeed": "100",
    "RestrictedTime": "10-5",
    "RestrictedPassengers": "FullyLicencedPassenger",
    "RainDistance": "4",
    "TyreTread": "1.5",
    "Headlights": "no",
    "Indication": "3",
}


# The logic to calculate the score
# Evidence of sound software engineering practice,
# such as use of methods and relevant parameters,
# to improved program flexibility
def calculateResult(formValues):
    score = 0
    index = 0
    incorrectQuestions = []
    for key in answers:
        index += 1
        if formValues[key] == answers[key]:
            score += 1
        else:
            incorrectQuestions.append(index)

    return [score, incorrectQuestions]


# the route for the result
@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        formValues = request.form
        score, incorrectQuestions = calculateResult(formValues)
        return render_template(
            "result.html",
            score=score,
            numberOfQuestions=len(answers),
            incorrectQuestions=incorrectQuestions,
        )
    else:
        return redirect(url_for("quiz"))


# Defining the home page of our site
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/quiz")  # this sets the route to this page
def quiz():
    return render_template("quiz.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("quiz"))
    else:
        # sequence, selection (if, if else, or case)
        # if user is logged in, redirect to quiz
        if "user" in session:
            return redirect(url_for("quiz"))

        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1111, debug=True)
