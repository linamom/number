from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# 전역 변수로 숫자 저장 (실제 서비스에서는 DB나 세션 사용 권장)
counter = {"value": 0}

# HTML 템플릿 (간단히 문자열로 작성)
template = """
<!doctype html>
<html>
<head>
    <title>Counter App</title>
</head>
<body>
    <h1>현재 숫자: {{ value }}</h1>
    <form method="post" action="{{ url_for('increase') }}">
        <button type="submit">증가</button>
    </form>
    <form method="post" action="{{ url_for('decrease') }}">
        <button type="submit">감소</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(template, value=counter["value"])

@app.route("/increase", methods=["POST"])
def increase():
    counter["value"] += 1
    return redirect(url_for("index"))

@app.route("/decrease", methods=["POST"])
def decrease():
    counter["value"] -= 1
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)