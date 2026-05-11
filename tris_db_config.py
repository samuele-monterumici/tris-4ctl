import pymysql
from datetime import datetime



# CONFIGURAZIONE CONNESSIONE 
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "4CTL_monte.s.141208", 
    "password": "Tpsit2026", 
    "database": "4CTL_monte.s.141208",
    "port": 3307,
    "cursorclass": pymysql.cursors.Cursor,
    "connect_timeout": 5,
}


def get_connection():
    """Restituisce una connessione al database."""
    return pymysql.connect(**DB_CONFIG)




# FUNZIONI DI SUPPORTO
def esegui_select(connection, query, params):
    """Esegue una query SELECT e restituisce tutte le righe."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def esegui_dml(connection, query, params):
    """Esegue INSERT, UPDATE, DELETE e restituisce righe coinvolte."""
    with connection.cursor() as cursor:
        righe_coinvolte = cursor.execute(query, params)
    connection.commit()
    return righe_coinvolte




# FUNZIONI PER LA GESTIONE DEI GIOCATORI
def cerca_giocatore(connection, nickname):
    """
    Cerca un giocatore per nickname.
    Restituisce una tupla (nickname, nome, cognome, p_giocate, p_vinte, p_perse, p_pareggiate)
    oppure None se non trovato.
    """
    query = """
        SELECT nickname, nome, cognome, p_giocate, p_vinte, p_perse, p_pareggiate 
        FROM giocatori 
        WHERE nickname = %s
    """
    risultati = esegui_select(connection, query, (nickname,))
    return risultati[0] if risultati else None


def registra_giocatore(connection, nickname, nome, cognome):
    """Registra un nuovo giocatore nel database."""
    query = "INSERT INTO giocatori (nickname, nome, cognome) VALUES (%s, %s, %s)"
    return esegui_dml(connection, query, (nickname, nome, cognome))


def aggiorna_statistiche_giocatore(connection, nickname, esito_partita):
    """
    Aggiorna i contatori di un giocatore in base all'esito della partita.
    esito_partita: 'vinta', 'persa', 'pareggiata'
    """
    if esito_partita == 'vinta':
        query = "UPDATE giocatori SET p_giocate = p_giocate + 1, p_vinte = p_vinte + 1 WHERE nickname = %s"
    elif esito_partita == 'persa':
        query = "UPDATE giocatori SET p_giocate = p_giocate + 1, p_perse = p_perse + 1 WHERE nickname = %s"
    elif esito_partita == 'pareggiata':
        query = "UPDATE giocatori SET p_giocate = p_giocate + 1, p_pareggiate = p_pareggiate + 1 WHERE nickname = %s"
    else:
        return 0
    return esegui_dml(connection, query, (nickname,))


def salva_partita(connection, nickname_x, nickname_o, vincitore):
    """
    Salva una partita nel database e aggiorna le statistiche dei giocatori.
    vincitore: nickname del vincitore (stringa) OPPURE None in caso di pareggio
    """
    # 1. Inserisci la partita (vincitore può essere NULL)
    query_partita = """
        INSERT INTO partite (giocatore_x, giocatore_o, vincitore, data_ora) 
        VALUES (%s, %s, %s, %s)
    """
    data_ora = datetime.now()
    esegui_dml(connection, query_partita, (nickname_x, nickname_o, vincitore, data_ora))
    
    # 2. Aggiorna le statistiche
    if vincitore is None:          # Pareggio
        aggiorna_statistiche_giocatore(connection, nickname_x, 'pareggiata')
        aggiorna_statistiche_giocatore(connection, nickname_o, 'pareggiata')
    elif vincitore == nickname_x:  # Vince X
        aggiorna_statistiche_giocatore(connection, nickname_x, 'vinta')
        aggiorna_statistiche_giocatore(connection, nickname_o, 'persa')
    elif vincitore == nickname_o:  # Vince O
        aggiorna_statistiche_giocatore(connection, nickname_x, 'persa')
        aggiorna_statistiche_giocatore(connection, nickname_o, 'vinta')




# FUNZIONI PER LE STATISTICHE
def top_5_vittorie(connection):
    """Restituisce i primi 5 giocatori per numero di vittorie."""
    query = """
        SELECT nickname, p_vinte 
        FROM giocatori 
        ORDER BY p_vinte DESC 
        LIMIT 5
    """
    return esegui_select(connection, query, ())


def statistiche_giocatore(connection, nickname):
    """
    Restituisce un dizionario con le statistiche complete di un giocatore.
    Restituisce None se il giocatore non esiste.
    """
    query = """
        SELECT nickname, p_giocate, p_vinte, p_perse, p_pareggiate
        FROM giocatori 
        WHERE nickname = %s
    """
    risultati = esegui_select(connection, query, (nickname,))
    
    if risultati:
        return {
            'nickname': risultati[0][0],
            'p_giocate': risultati[0][1],
            'p_vinte': risultati[0][2],
            'p_perse': risultati[0][3],
            'p_pareggiate': risultati[0][4]
        }
    return None