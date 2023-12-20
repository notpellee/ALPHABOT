from flask import Flask, render_template, redirect, url_for, request
import AlphaBot
import RPi.GPIO as GPIO
import time
import sqlite3
import string
import random
import hashlib

#credenziali: mario rossi, jhon doe

app = Flask(__name__)

t = AlphaBot.AlphaBot()

comandi = {"1": t.forward, "4": t.backward, "2":t.left, "3": t.right}

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

token = get_random_string(40)
print(f'./{token}')

def calcola_hash_sha256(testo):
    # Crea un oggetto hash SHA-256
    hash_object = hashlib.sha256()

    # Aggiunge il testo al quale si vuole calcolare l'hash
    hash_object.update(testo.encode('utf-8'))

    # Ottieni l'hash in formato esadecimale
    hash_hex = hash_object.hexdigest()

    return hash_hex


def validate(username, password):
    completion = False
    con = sqlite3.connect('./movements.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, calcola_hash_sha256(password))
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)


#@app.route(f'/{token}', methods=['GET', 'POST'])
@app.route('/secret', methods=['GET', 'POST'])
def secret():
    
    if request.method == 'POST':
        #print(request.form.get('action1'))
        if request.form.get('AVANTI') == 'AVANTI':
            print("AVANTI")
            t.forward()
            time.sleep(0.3)
            t.stop()
        elif  request.form.get('INDIETRO') == 'INDIETRO':
            print("INDIETRO")
            t.backward()
            time.sleep(0.3)
            t.stop()
        elif  request.form.get('DESTRA') == 'DESTRA':
            print("DESTRA")
            t.right()
            time.sleep(0.3)
            t.stop()
        elif  request.form.get('SINISTRA') == 'SINISTRA':
            print("SINISTRA")
            t.left()
            time.sleep(0.3)
            t.stop()
        elif  request.form.get('invia') == 'invia':
            data_from_html = str(request.form['input_command'])
            print(data_from_html)
            conSQL = sqlite3.connect("movements.db")
            cur = conSQL.cursor()
            research = cur.execute(f"SELECT Mov_sequence FROM movements WHERE Shortcut = '{data_from_html}'")
            db_list = research.fetchall()[0][0]
            conSQL.close()
            db_list = str(db_list).split('-')
            for elem in db_list:
                list = elem.split(';') 
                print(list)
                cont = 0
                try:
                    comandi[list[0]]()
                    while cont < float(list[1]):
                        time.sleep(0.1)
                        cont += 0.1
                    t.stop()
                    time.sleep(0.2)
                except:
                    print("errore database")
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')