from tris_db_config import (
    get_connection, cerca_giocatore, registra_giocatore, 
    salva_partita, top_5_vittorie, statistiche_giocatore
)
from tris import gioca_tris



def gestisci_giocatore(connection, numero_giocatore):
    """
    Gestisce la registrazione o il recupero di un giocatore.
    Restituisce il nickname del giocatore.
    """
    print(f"\n--- GIOCATORE {numero_giocatore} ---")
    nickname = input("Nickname: ").strip()
    
    if not nickname:
        print("Nickname non valido!")
        return gestisci_giocatore(connection, numero_giocatore)
    
    # Cerca se il nickname esiste già
    giocatore = cerca_giocatore(connection, nickname)
    
    if giocatore:
        # Nickname esistente
        print(f"\nIl nickname '{nickname}' è già presente nel database.")
        print("1 - Utilizzare il nickname esistente")
        print("2 - Scegliere un nuovo nickname")
        
        scelta = input("Scegli (1/2): ").strip()
        
        if scelta == "1":
            print(f"Benvenuto {nickname}!")
            return nickname
        else:
            return gestisci_giocatore(connection, numero_giocatore)
    else:
        # Nuovo giocatore: richiedi nome e cognome
        print(f"\nNuovo giocatore! Completa la registrazione:")
        nome = input("Nome: ").strip()
        cognome = input("Cognome: ").strip()
        
        if not nome or not cognome:
            print("Nome e cognome sono obbligatori!")
            return gestisci_giocatore(connection, numero_giocatore)
        
        registra_giocatore(connection, nickname, nome, cognome)
        print(f"Registrazione completata! Benvenuto {nickname}!")
        return nickname




def main():
    conn = None
    try:
        conn = get_connection()
        print("Connessione al database riuscita!\n")
        
        while True:
            print("         T R I S - M E N Ù")
            print("1. Nuova partita")
            print("2. Top 5 giocatori per vittorie")
            print("3. Statistiche giocatore")
            print("4. Esci")
            
            scelta = input("Scegli (1-4): ").strip()
            
            if scelta == "1":
                print("       NUOVA PARTITA")
                nickname1 = gestisci_giocatore(conn, 1)
                nickname2 = gestisci_giocatore(conn, 2)
                
                print(f"\n{nickname1} gioca con X")
                print(f"{nickname2} gioca con O")
                
                input("\nPremi INVIO per iniziare la partita...")
                
                vincitore = gioca_tris(nickname1, nickname2)
                
                # Salva la partita nel database
                salva_partita(conn, nickname1, nickname2, vincitore)
                
                if vincitore is None:
                    print("\nPartita terminata in pareggio e salvata nel database!")
                else:
                    print(f"\nPartita vinta da {vincitore} e salvata nel database!")
                
                input("\nPremi INVIO per tornare al menu...")

            elif scelta == "2":
                print("   TOP 5 GIOCATORI PER VITTORIE")
                classifica = top_5_vittorie(conn)
                
                if classifica:
                    print("\nCLASSIFICA")
                    for i, (nickname, vittorie) in enumerate(classifica, 1):
                        print(f"{i} - {nickname}: {vittorie} vittorie")
                else:
                    print("Nessun giocatore trovato.")
                
                input("\nPremi INVIO per continuare...")
            
            elif scelta == "3":
                print("     STATISTICHE GIOCATORE")
                nickname = input("Inserisci nickname: ").strip()
                stats = statistiche_giocatore(conn, nickname)
                
                if stats:
                    win_rate = (stats['p_vinte'] / stats['p_giocate'] * 100) if stats['p_giocate'] > 0 else 0
                    print(f"{stats['nickname'].upper()}")
                    print(f"Partite giocate:    {stats['p_giocate']}")
                    print(f"Partite vinte:      {stats['p_vinte']}")
                    print(f"Partite perse:      {stats['p_perse']}")
                    print(f"Partite pareggiate: {stats['p_pareggiate']}")
                    print(f"Win rate:           {win_rate:.1f}%")
                else:
                    print(f"Giocatore '{nickname}' non trovato.")
                
                input("\nPremi INVIO per continuare...")
            
            elif scelta == "4":
                print("\nGrazie per aver giocato! Arrivederci!")
                break
            
            else:
                print("Scelta non valida! Inserisci 1, 2, 3 o 4.")
    
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        if conn:
            conn.close()
            print("\nConnessione al database chiusa.")



if __name__ == "__main__":
    main()
