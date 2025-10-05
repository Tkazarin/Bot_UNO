USE bot;

DROP TABLE IF EXISTS participant;

CREATE TABLE participant (
    id_participant INT AUTO_INCREMENT PRIMARY KEY,
    authorization VARCHAR(3) DEFAULT 'PLR',
    chat_id_participant INT NOT NULL,
    tg_id_participant INT NOT NULL
);