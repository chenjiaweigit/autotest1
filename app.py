
import os,time
import subprocess
from flask_socketio import SocketIO, emit
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for,jsonify, make_response, flash

from common.Log import log
from common.yaml_util1 import modify_ini_and_write
from flatform import simple


app = Flask(__name__)
app.register_blueprint(simple)
app.secret_key = 'your_secret_key'  # 设置用于会话加密的密钥，可以随机生成
# 假设用户名和密码
USERNAME = 'admin'
PASSWORD = '123456'
socketio = SocketIO(app)
pytest_process = None


@app.route('/')
def index():
    if 'username' in session:
        # return render_template('index1.html')  # 登录后显示的页面
        # 设置名为“username”的cookie，其值来自会话，并设置7天的过期时间
        expires = datetime.utcnow() + timedelta(minutes=3)
        response = make_response(render_template('index.html'))
        response.set_cookie('username', session['username'], expires=expires)
        return response
    return redirect(url_for('login'))   # 未登录，重定向到登录页面


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
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
