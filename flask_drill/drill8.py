from flask import Flask, request, render_template

app = Flask(__name__)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

@app.route('/drill8', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        width = int(request.form['width'])
        height = int(request.form['height'])
        g = gcd(width, height)
        rw = width // g
        rh = height // g
        msg = f'{rw}:{rh}'
    else:
        width = ''
        height = ''
        msg = None

    return render_template('drill8.html', msg=msg, width=width, height=height)

if __name__ == '__main__':
    app.run(port='8000', debug=True)