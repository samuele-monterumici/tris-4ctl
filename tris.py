def stampa(scacchiera):
    """
    Stampa la scacchiera del tris.
    """
    print(f" {scacchiera[0]} | {scacchiera[1]} | {scacchiera[2]} \n")
    print(f" {scacchiera[3]} | {scacchiera[4]} | {scacchiera[5]} \n")
    print(f" {scacchiera[6]} | {scacchiera[7]} | {scacchiera[8]} \n")


def vittoria(scacchiera, simbolo):
    """
    Controlla se il simbolo ha vinto.
    """
    combinazioni = [
        [0,1,2], [3,4,5], [6,7,8],  # righe
        [0,3,6], [1,4,7], [2,5,8],  # colonne
        [0,4,8], [2,4,6]            # diagonali
    ]
    
    for c in combinazioni:
        if scacchiera[c[0]] == simbolo and scacchiera[c[1]] == simbolo and scacchiera[c[2]] == simbolo:
            return True
    return False


def pareggio(scacchiera):
    """
    Controlla se la scacchiera è piena (pareggio).
    """
    return "_" not in scacchiera


def gioca_tris(nickname_x, nickname_o):
    """
    Avvia una partita tra due giocatori.
    
    Restituisce:
    - nickname del vincitore (stringa) se qualcuno vince
    - None se pareggio
    """
    # Inizializzazione scacchiera
    scacchiera = ["_", "_", "_",
                  "_", "_", "_",
                  "_", "_", "_"]
    
    turno = "X"  # X inizia sempre
    
    print(f"INIZIO PARTITA: {nickname_x} (X) vs {nickname_o} (O)")
    
    while True:
        stampa(scacchiera)
        
        # Determina il nickname del giocatore corrente
        if turno == "X":
            nome_corrente = nickname_x
        else:
            nome_corrente = nickname_o
        
        print(f"Turno di {nome_corrente} ({turno})")
        
        try:
            # Richiesta posizione (da 1 a 9)
            posizione = int(input("Scegli posizione (1-9): ")) - 1
        except ValueError:
            print("Inserisci un numero valido!")
            continue
        
        # Controllo posizione valida
        if posizione < 0 or posizione > 8:
            print("Posizione non valida! Scegli un numero tra 1 e 9.")
            continue
        
        # Controllo posizione libera
        if scacchiera[posizione] != "_":
            print("Posizione già occupata!")
            continue
        
        # Inserisci il simbolo
        scacchiera[posizione] = turno
        
        # Controlla vittoria
        if vittoria(scacchiera, turno):
            stampa(scacchiera)
            print(f"\n{nome_corrente} VINCE LA PARTITA!")
            return nome_corrente  # Restituisce il nickname del vincitore
        
        # Controlla pareggio
        if pareggio(scacchiera):
            stampa(scacchiera)
            print("\nPAREGGIO!")
            return None  # Restituisce None per pareggio
        
        # Cambia turno
        turno = "O" if turno == "X" else "X"