import socket as sck
from sqlite3 import connect
import time
import AlphaBot

isRunning = True
address = ('192.168.1.129',8000)

s_server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s_server.bind(address)

s_server.listen()
conn, add= s_server.accept()

t = AlphaBot.AlphaBot()

comandi = {"1": t.forward, "4": t.backward, "2":t.left, "3": t.right}

while True:
    text = conn.recv(4096)
    text_decode = text.decode()

    conn.sendall(text)

    if text_decode.lower() == "exit":
        t.stop()
        break
    else:
        list = text_decode.split(';') 
        print(list)
        try:
            comandi[list[0]]()
            time.sleep(float(list[1]))
            t.stop()
        except:
            print("errore")
    
conn.close()
s_server.close()





    

   
