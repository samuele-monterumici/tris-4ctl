CREATE TABLE giocatori(
    nickname VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    p_giocate INT DEFAULT 0,
    p_pareggiate INT DEFAULT 0,
    p_vinte INT DEFAULT 0,
    p_perse INT DEFAULT 0
);


CREATE TABLE partite(
    id_partita INT PRIMARY KEY AUTO_INCREMENT,
    giocatore_x VARCHAR(50) NOT NULL,
    giocatore_o VARCHAR(50) NOT NULL,
    vincitore VARCHAR(50) DEFAULT NULL,
    data_ora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (giocatore_x) REFERENCES giocatori(nickname),
    FOREIGN KEY (giocatore_o) REFERENCES giocatori(nickname)
);