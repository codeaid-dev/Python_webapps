from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)

@app.route('/drill9')
def index():
    page = request.args.get('page')
    if page:
        page = int(page)
    else:
        return redirect(url_for('index',page=1))

    return render_template('drill9.html', page=page)

if __name__ == '__main__':
    app.run(port='8000', debug=True)