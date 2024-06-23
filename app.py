
import os,time
import subprocess
from flask_socketio import SocketIO, emit
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for,jsonify, make_response, flash
import locale
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate    #就是将新增的字段合并到数据库当中

locale.setlocale(locale.LC_CTYPE,"chinese")
from flatform import simple


app = Flask(__name__)
app.register_blueprint(simple)
app.secret_key = 'your_secret_key'  # 设置用于会话加密的密钥，可以随机生成
socketio = SocketIO(app)
pytest_process = None

def connect_tadabase():
    host = "39.100.94.179"
    port = 15432
    user = "postgres"
    password = "BHU*9ol."
    database = "test"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 在app.config中设置好连接数据库的信息，然后使用SQLAlchemy(db)创建一个db对象，会自动读取app.config中的信息
    db = SQLAlchemy(app)
    return db
db = connect_tadabase()
# 测试是否连接数据库  ?charset=utf8mb4
# with app.app_context():    #处理上下文需要加这个，不然会报错
#     with db.engine.connect() as conn:
#         rs = conn.execute("select 1")
#         print(rs.fetchone())

migrate = Migrate(app, db)

# 3. 定义与数据库表的映射类（无需创建表，只是定义映射）
class Test(db.Model):
    __tablename__ = 'test_case'
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String)
    name = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String)
    PASSWORD = db.Column(db.String)

@app.route('/user/query')
def query_user():
    # get查找，根据主键查找
    # user = User_table.query.get(1)
    # print(f"{user.ID}:{user.USERNAME}:{user.PASSWORD}")
    # filter_by查找
    # users = User_table.query.filter_by(USERNAME="法外狂徒李四")
    # users = User_table.query.all()  # 获取全部数据
    # users = User_table.query.filter(User_table.USERNAME.like("%张三%")).all()    # 模糊查询
    # users = User_table.query.filter(User_table.USERNAME.contains("李四")).all()   # 包含关系
    # for user in users:
    #     print(user.ID,user.USERNAME,user.PASSWORD)
    users = User.query.filter(User.USERNAME.like("%admin%")).first()
    # users = Test.query.all()
    # for user in users:
    #     print(user.ID)
    # print(users.ID,users.USERNAME,users.PASSWORD)
    # return "数据查找成功！"
    # results = User.query.all()
    # for user in results:
    print(users.USERNAME, users.PASSWORD)
    # return ''.join([f"ID: {row.id}, Name: {row.name}<br>" for row in results])
    return ''.join(f"账号: {users.USERNAME}, 密码: {users.PASSWORD}<br>")

@app.route('/')
def index():
    if 'username' in session:
        # return render_template('index1.html')  # 登录后显示的页面
        # 设置名为“username”的cookie，其值来自会话，并设置7天的过期时间
        expires = datetime.utcnow() + timedelta(minutes=3)
        response = make_response(render_template('index1.html'))
        response.set_cookie('username', session['username'], expires=expires)
        return response
    return redirect(url_for('login'))   # 未登录，重定向到登录页面


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.filter(User.USERNAME.like("%admin%")).first()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users.USERNAME and password == users.PASSWORD:
            print(users.USERNAME, users.PASSWORD)
            session['username'] = username  # 将用户名存入会话
            # return redirect(url_for('index'))  # 登录成功，重定向到主页
            expires = datetime.utcnow() + timedelta(minutes=3)
            response = make_response(redirect(url_for('index')))
            response.set_cookie('username', username, expires=expires)
            flash("登录成功！")
            return response
        else:
            return render_template('login.html', error='账号/密码错误！')  # 登录失败，显示错误信息
    return render_template('login.html')  # GET请求，显示登录页面

@app.route('/report', methods=['GET', 'POST'])
def report():

    return app.send_static_file('report/index.html')

@app.route('/test_case')
def test_case():
    return  render_template('index.html')

@app.route('/project_environment')
def project_environment():
    return render_template('project_environment.html')


@app.route('/database_environment')
def database_environment():
    return render_template('databese_environment.html')


@app.route('/test_report')
def test_report():
    return render_template('test-report.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# @app.route('/run_pytest')
# def run_pytest():
#     return render_template('run_pytest.html')

# @app.route('/run_test_button', methods=['POST'])
# def run_tests():
#     # 运行pytest框架
#     subprocess.run(['python', 'run.py'])
#     return 'Script started'

@app.route('/test_page')
def test_page():
    return render_template('index1.html')


# 以下部分为运行并返回日志给前端调试部分

@app.route('/run_test')
def run_test():
    return render_template('run_pytest.html')

@app.route('/start_pytest')
def start_pytest():

    # try:
    # 获取原始字符串数据
    # temp_domains = request.data.decode('utf-8')
    # if not temp_domains:
    #     raise ValueError("Empty data received")
    # # 处理 temp_domains 写入setting.ini配置文件
    # modify_ini_and_write('host', 'api_root_url', temp_domains)
    # result = {"status": "success", "message": "Test started"}

    # except ValueError as ve:
    #     return jsonify({"error": str(ve)}), 400
    # except Exception as e:
        # 捕获所有其他异常
        # return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    # else:
    global pytest_process

    if pytest_process and pytest_process.poll() is None:
        return jsonify({'message': 'Pytest is already running!'})
    # elif ini_weite_status:
    # 运行pytest框架
    # log.info("=" * 25 + "开始运行pytest测试框架" + "=" * 25)
    pytest_process = subprocess.Popen(['python', 'run.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # pytest_process = subprocess.Popen(['python', 'run.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # output, error = pytest_process.communicate()
    # print(output, error)
    # return jsonify(result), 200

    def emit_logs():
        try:
            for line in iter(pytest_process.stdout.readline, b''):
                print(line)
                try:
                    socketio.emit('pytest_log', {'log': line.decode('utf-8')})
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        pytest_process.stdout.close()
        pytest_process.wait()

    thread = threading.Thread(target=emit_logs)
    thread.start()
    return jsonify({'message': 'Pytest started!'})

@socketio.on('connect')
def test_connect():
    print('Client connected')

# 以上部分为运行并返回日志给前端调试部分

if __name__ == '__main__':
    app.run(debug=True)
