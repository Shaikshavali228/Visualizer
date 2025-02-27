from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Temporary folder to store code files
TEMP_FOLDER = "temp_codes"
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Language configurations
LANGUAGES = {
    "python": {"ext": ".py", "run": "python"},
    "java": {"ext": ".java", "run": "javac && java"},
    "c": {"ext": ".c", "run": "gcc -o temp_code temp_code.c && temp_code"},
    "cpp": {"ext": ".cpp", "run": "g++ -o temp_code temp_code.cpp && temp_code"}
}

def execute_code(code, lang):
    if lang not in LANGUAGES:
        return "Unsupported language", 400
    
    lang_info = LANGUAGES[lang]
    file_path = os.path.join(TEMP_FOLDER, f"temp_code{lang_info['ext']}")

    with open(file_path, "w") as file:
        file.write(code)
    
    try:
        if lang == "java":
            subprocess.run(["javac", file_path], check=True)
            output = subprocess.run(["java", "-cp", TEMP_FOLDER, "temp_code"], capture_output=True, text=True, check=True)
        else:
            output = subprocess.run(lang_info["run"].split() + [file_path], capture_output=True, text=True, shell=True, check=True)

        return output.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    code = data.get("code", "")
    lang = data.get("language", "python").lower()
    
    output = execute_code(code, lang)
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
