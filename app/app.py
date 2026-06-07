from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>Origin Web Application</h1>
    <p>This app is protected by Nginx Edge + ModSecurity WAF.</p>
    <ul>
        <li>/search?q=hello</li>
        <li>/login</li>
        <li>/health</li>
    </ul>
    """

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "origin-app"})

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"""
    <h1>Search Page</h1>
    <p>You searched for: {q}</p>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <h1>Login</h1>
        <form method="POST">
            <input name="username" placeholder="username">
            <input name="password" placeholder="password" type="password">
            <button type="submit">Login</button>
        </form>
        """

    username = request.form.get("username", "")
    return jsonify({
        "message": "login attempt received",
        "username": username
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
