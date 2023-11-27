import socket as sck
import time
from threading import Thread
import AlphaBot
import RPi.GPIO as GPIO

isRunning = True
continua = True
address = ('192.168.1.129',8000)

s_server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s_server.bind(address)

s_server.listen()
conn, add= s_server.accept()

DR_status = 0
DL_status = 0

t = AlphaBot.AlphaBot()

comandi = {"1": t.forward, "4": t.backward, "2":t.left, "3": t.right}

class Server(Thread):
    def __init__(self, c = conn):
        Thread.__init__(self)
        self.conn = c
        self.DR = 16
        self.DL = 19

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.DR,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.DL,GPIO.IN,GPIO.PUD_UP)
    def run(self):
        while True:
            time.sleep(1)
            global t 
            global continua
            global DR_status 
            DR_status= GPIO.input(self.DR)
            global DL_status 
            DL_status = GPIO.input(self.DL)
            if DR_status == 0 or DL_status == 0:
                t.backward()
                time.sleep(0.2)
                t.stop()
                if DR_status == 0:
                    if DL_status == 0:
                        mess= "ostacolo centrale"
                    else:
                        mess="ostacolo a destra"
                else:
                    mess = "ostacolo a sinistra"
                self.conn.sendall(mess.encode())
                continua = False
            else:
                continua = True

def main():

    server = Server()
    server.start()

    global continua

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
            cont = 0
            try:
                comandi[list[0]]()
                while continua and cont < float(list[1]):
                    time.sleep(0.1)
                    cont += 0.1
                t.stop()
            except:
                print("errore")
            
if __name__ == "__main__":
    main()
    
    
conn.close()
s_server.close()





    

   
