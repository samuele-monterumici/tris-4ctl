# PROGETTO TRIS

Monterumici Samuele, Pierozzi Cristian, Bonora Tommaso

## SUDDIVISIONE DEI RUOLI

- **Monterumici** - Responsabile database, creazione tabelle e connessione Python-SQL
- **Pierozzi** - Responsabile logica di gioco, gestione turni e controllo vittoria
- **Bonora** - Responsabile menu principale, statistiche giocatori, classifica Top 5 e documentazione

## DESCRIZIONE

Il progetto consiste in una versione del gioco del Tris realizzata in Python ed eseguibile da terminale, con l'aggiunta di un database MySQL per memorizzare giocatori e partite.

**Come funziona il gioco:**

Due giocatori si sfidano a Tris. All'inizio il programma richiede il nickname per entrambi. Se il nickname non esiste nel database, il sistema chiede di completare la registrazione con nome e cognome; se esiste già, chiede se utilizzarlo o sceglierne uno nuovo. I due giocatori vengono associati ai simboli: il primo usa **X**, il secondo usa **O**.

Il gioco si svolge a turni. Il giocatore sceglie una posizione digitando un numero da 1 a 9.

Il programma mostra la scacchiera dopo ogni mossa, controlla che la posizione sia valida e impedisce di occupare celle già utilizzate. Dopo ogni turno verifica le possibili combinazioni di vittoria: righe, colonne e diagonali. Se nessun giocatore vince entro nove mosse, la partita termina in pareggio.

**Collegamento al database:**

Il database MySQL permette di registrare gli utenti (evitando duplicati grazie al nickname come chiave primaria), salvare le partite giocate memorizzando i due giocatori, il vincitore (NULL in caso di pareggio), la data e l'ora, e aggiornare automaticamente le statistiche (partite giocate, vinte, perse, pareggiate).

Lo schema relazionale è definito nel file `tris.sql` e contiene due tabelle:
- **giocatori**: nickname (PK), nome, cognome, p_giocate, p_vinte, p_perse, p_pareggiate
- **partite**: id_partita (PK), giocatore_x, giocatore_o, vincitore, data_ora

**Analisi dei dati:**

Dal menu principale è possibile:
- Visualizzare la **classifica dei primi 5 giocatori** con il maggior numero di vittorie
- Consultare le **statistiche di un singolo giocatore**: partite giocate, vinte, perse, pareggiate e win rate

**Struttura del progetto:**

Il codice è organizzato in tre file:
- `tris_game.py`: logica del gioco (stampa scacchiera, controllo vittoria, gestione turni)
- `tris_db_config.py`: connessione al database e funzioni per interagire con esso
- `main.py`: menu principale e interfaccia utente