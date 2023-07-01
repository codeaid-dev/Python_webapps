from flask import Flask, request, url_for, render_template, redirect
import random

app = Flask(__name__)

@app.route('/drill9')
def index():
    page = request.args.get('page')
    print(page)
    if page:
        page = int(page)
    else:
        return redirect(url_for('index',page=1))

    return render_template('drill9.html', page=page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)