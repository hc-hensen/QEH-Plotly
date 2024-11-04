from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart_1A')
def chart_1():
    return render_template('chart_1a.html')


@app.route('/chart_2A')
def chart_2():
    return render_template('chart_2a.html')


@app.route('/chart_3A')
def chart_3():
    return render_template('chart_3a.html')


@app.route('/chart_4A')
def chart_4():
    return render_template('chart_4a.html')


@app.route('/chart_1W')
def chart_5():
    return render_template('chart_1w.html')


@app.route('/chart_2W')
def chart_6():
    return render_template('chart_2w.html')


@app.route('/table_1A')
def table_1():
    return render_template('table_1a.html')


@app.route('/table_2A')
def table_2():
    return render_template('table_2a.html')


@app.route('/table_3A')
def table_3():
    return render_template('table_3a.html')


@app.route('/table_4A')
def table_4():
    return render_template('table_4a.html')


@app.route('/table_1W')
def table_5():
    return render_template('table_1w.html')


@app.route('/table_2W')
def table_6():
    return render_template('table_2w.html')


if __name__ == '__main__':
    app.run(debug=True)