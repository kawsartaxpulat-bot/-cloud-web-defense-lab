from flask import Flask, request, jsonify

# 创建 Flask 应用对象
app = Flask(__name__)

# 首页路由：用户访问 / 时执行 index 函数
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

# 健康检查接口：用于检测应用是否正常运行
@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "origin-app"})

# 搜索接口：从 URL 查询参数中读取 q 的值
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"""
    <h1>Search Page</h1>
    <p>You searched for: {q}</p>
    """

# 登录接口：同时支持 GET 和 POST
@app.route("/login", methods=["GET", "POST"])
def login():
    # GET 请求：返回登录表单页面
    if request.method == "GET":
        return """
        <h1>Login</h1>
        <form method="POST">
            <input name="username" placeholder="username">
            <input name="password" placeholder="password" type="password">
            <button type="submit">Login</button>
        </form>
        """

    # POST 请求：读取用户提交的表单数据
    username = request.form.get("username", "")
    return jsonify({
        "message": "login attempt received",
        "username": username
    })

# 当直接运行 app.py 时，启动 Flask Web 服务
# host="0.0.0.0" 允许容器外部访问
# port=5000 表示服务监听 5000 端口
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
