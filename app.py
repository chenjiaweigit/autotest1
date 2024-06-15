
import os,time
import subprocess

import yaml
from flask import Flask, render_template, request, session, redirect, url_for
from flatform import simple
# from flask_bootstrap


app = Flask(__name__)
app.register_blueprint(simple)
app.secret_key = 'your_secret_key'  # 设置用于会话加密的密钥，可以随机生成
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 假设用户名和密码
USERNAME = 'admin'
PASSWORD = '123456'


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index1.html')  # 登录后显示的页面
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # while True:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('index'))
            # break
        else:
            return 'Invalid username/password'
            # time.sleep(3)
            # return render_template('login.html')
    return render_template('login.html')

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

@app.route('/run_pytest')
def run_pytest():
    return render_template('run_pytest.html')

@app.route('/run_test_button', methods=['POST'])
def run_tests():
    # 运行pytest框架
    subprocess.run(['python', 'run.py'])
    return 'Script started'

@app.route('/test_page')
def test_page():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
