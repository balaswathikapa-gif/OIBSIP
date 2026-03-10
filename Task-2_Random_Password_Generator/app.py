from flask import Flask, request, render_template_string
import string
import secrets

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Generator</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(120deg, #667eea, #764ba2);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .box {
            background: white;
            padding: 25px;
            width: 320px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        h2 {
            text-align: center;
        }
        input, button {
            width: 100%;
            padding: 8px;
            margin-top: 10px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .result {
            margin-top: 15px;
            padding: 10px;
            background: #f3f3f3;
            border-radius: 6px;
            text-align: center;
            word-break: break-all;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>🔐 Password Generator</h2>
    <form method="post">
        <input type="number" name="length" placeholder="Password Length" min="4" required>

        <label><input type="checkbox" name="letters"> Letters</label><br>
        <label><input type="checkbox" name="digits"> Numbers</label><br>
        <label><input type="checkbox" name="symbols"> Symbols</label><br>

        <input type="text" name="exclude" placeholder="Exclude characters (optional)">

        <button type="submit">Generate</button>
    </form>

    {% if password %}
    <div class="result">
        <strong>{{ password }}</strong>
    </div>
    {% endif %}
</div>

</body>
</html>
"""

def generate_password(length, letters, digits, symbols, exclude):
    characters = ""

    if letters:
        characters += string.ascii_letters
    if digits:
        characters += string.digits
    if symbols:
        characters += string.punctuation

    if not characters:
        return "❌ Select at least one character type"

    # Exclude characters ONLY if user entered something
    if exclude:
        for ch in exclude:
            characters = characters.replace(ch, "")

    if not characters:
        return "❌ All characters removed"

    return "".join(secrets.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    if request.method == "POST":
        password = generate_password(
            int(request.form["length"]),
            "letters" in request.form,
            "digits" in request.form,
            "symbols" in request.form,
            request.form.get("exclude", "")
        )
    return render_template_string(HTML, password=password)


if __name__ == "__main__":
    app.run(debug=True)
