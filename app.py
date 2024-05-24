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

@app.route('/table_1A')
def table_1():
    return render_template('table_1a.html')

@app.route('/table_2A')
def table_2():
    return render_template('table_2a.html')

@app.route('/table_3A')
def table_3():
    return render_template('table_3a.html')

@app.route('/sankey_1')
def sankey_1():
    return render_template('sankey_1.html')


if __name__ == '__main__':
    app.run(debug=True)
