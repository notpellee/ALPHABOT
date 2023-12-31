from flask import Flask, render_template, request
import AlphaBot
import RPi.GPIO as GPIO
import time
app = Flask(__name__)

t = AlphaBot.AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #print(request.form.get('action1'))
        if request.form.get('AVANTI') == 'value1':
            print("AVANTI")
            t.forward()
            time.sleep(2)
            t.stop()
        elif  request.form.get('INDIETRO') == 'value2':
            print("INDIETRO")
            t.backward()
            time.sleep(2)
            t.stop()
        elif  request.form.get('DESTRA') == 'value3':
            print("DESTRA")
            t.right()
            time.sleep(2)
            t.stop()
        elif  request.form.get('SINISTRA') == 'value4':
            print("SINISTRA")
            t.left()
            time.sleep(2)
            t.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')