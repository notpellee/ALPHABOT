import socket
import threading

class TrisServer:
    def __init__(self):
        self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_server.bind(('127.0.0.1', 8000))
        self.s_server.listen()

        self.griglia = [[' ' for _ in range(3)] for _ in range(3)]
        self.turno = 'client_a'

        self.lock = threading.Lock()

        print("In attesa di connessioni...")

    def gestisci_connessioni(self):
        conn_a, addr_a = self.s_server.accept()
        print(f"Connessione accettata da {addr_a}")
        conn_a.sendall("Benvenuto! Sei il giocatore A".encode())

        conn_b, addr_b = self.s_server.accept()
        print(f"Connessione accettata da {addr_b}")
        conn_b.sendall("Benvenuto! Sei il giocatore B".encode())

        threading.Thread(target=self.gestisci_partita, args=(conn_a, conn_b)).start()

    def gestisci_partita(self, conn_a, conn_b):
        connessioni = {'client_a': conn_a, 'client_b': conn_b}

        while True:
            with self.lock:
                giocatore_corrente = self.turno
                avversario = 'client_b' if giocatore_corrente == 'client_a' else 'client_a'

                connessioni[giocatore_corrente].sendall("È il tuo turno. La griglia attuale:".encode())
                connessioni[giocatore_corrente].sendall(str(self.griglia).encode())
                connessioni[giocatore_corrente].sendall("Inserisci la tua mossa (riga,colonna): ".encode())

                mossa = connessioni[giocatore_corrente].recv(1024).decode().split(',')
                riga, colonna = map(int, mossa)

                if 0 <= riga < 3 and 0 <= colonna < 3 and self.griglia[riga][colonna] == ' ':
                    self.griglia[riga][colonna] = 'X' if giocatore_corrente == 'client_a' else 'O'
                else:
                    connessioni[giocatore_corrente].sendall("Mossa non valida. Riprova.".encode())
                    continue

                self.turno = avversario

                if all(cell != ' ' for riga in self.griglia for cell in riga):
                    for conn in connessioni.values():
                        conn.sendall("La partita è finita in pareggio!".encode())
                    break

    def avvia_server(self):
        threading.Thread(target=self.gestisci_connessioni).start()

if __name__ == "__main__":
    server = TrisServer()
    server.avvia_server()
