from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# BMI Calculation
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# BMI Category
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Save Data
def save_data(weight, height, bmi, category):
    file_exists = os.path.isfile("bmi_data.csv")

    with open("bmi_data.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Weight", "Height", "BMI", "Category"])

        writer.writerow([weight, height, bmi, category])


@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = None
    error = None

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])

            # Validation
            if weight <= 0 or height <= 0:
                error = "Weight and Height must be positive numbers."
            elif weight > 300 or height > 3:
                error = "Please enter realistic values."
            else:
                bmi = round(calculate_bmi(weight, height), 2)
                category = bmi_category(bmi)

                save_data(weight, height, bmi, category)

        except ValueError:
            error = "Please enter valid numeric values."

    return render_template("index.html", bmi=bmi, category=category, error=error)


if __name__ == "__main__":
    app.run(debug=True)
