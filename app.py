import os
from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import send_from_directory, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from analysis import analysis


app = Flask(__name__)

app.config['SECRET_KEY'] = 'x1csadf^23GkLKkjxiF1^32kJKd4ea'

# 最大ファイルサイズ
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# PATH一覧
app.config['HOME_DIR'] = os.getcwd()
app.config['TEMP_DIR'] = os.path.join(app.config['HOME_DIR'], 'temp')
app.config['IMAGES_DIR'] = os.path.join(
    app.config['HOME_DIR'], 'static', 'images')


@app.route('/')
def red():
    return redirect('index')


@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method != 'POST':
        max_val = 100
        min_val = 0
        future_val = 100
        return render_template('index.html', max_val=max_val, min_val=min_val, future_val=future_val)

    err_msg = ''
    max_val = request.form['max']
    min_val = request.form['min']
    future_val = request.form['future']
    file = request.files['file']

    if not max_val.isdecimal():
        err_msg += '上限値が設定されていません。'
        flash("上限値が設定されていません。", 'danger')

    if not min_val.isdecimal():
        err_msg += '下限値が設定されていません。'
        flash("下限値が設定されていません。", 'danger')

    if not future_val.isdecimal():
        err_msg += '予測日数が設定されていません。'
        flash("予測日数が設定されていません。", 'danger')

    if file.filename == '':
        err_msg += 'ファイルがありません。'
        flash("ファイルがありません。", 'danger')

    if err_msg != '':
        return render_template('index.html', max_val=max_val, min_val=min_val, future_val=future_val)


    # サニタイズ処理
    basename = secure_filename(file.filename)

    # フルパス
    filename = os.path.join(app.config['TEMP_DIR'], basename)

    file.save(filename)

    # 予測値取得
    header, datas = analysis(filename, app.config['IMAGES_DIR'], int(max_val), int(min_val), int(future_val))

    return render_template('chart.html', header=header, datas=datas)


# ファイルサイズ超過
# 開発環境だと正しくひょうじされない
@app.errorhandler(RequestEntityTooLarge)
def handle_over_max_file_size(error):
    flash('ファイルサイズ超過。', 'danger')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()