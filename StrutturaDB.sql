
CREATE DATABASE IF NOT EXISTS RicetteDB;

USE RicetteDB;


-- TABELLA CATEGORIA

CREATE TABLE Categoria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL
);


-- TABELLA RICETTA

CREATE TABLE Ricetta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    descrizione TEXT,
    tempo INT,
    difficolta VARCHAR(50),
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
);


-- TABELLA INGREDIENTI

CREATE TABLE Ingredienti (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL
);


-- TABELLA RICETTEINGREDIENTI


CREATE TABLE RicetteIngredienti (
    ricetta_id INT,
    ingrediente_id INT,
    qta DECIMAL(10,2),
    u_misura VARCHAR(50),
    PRIMARY KEY (ricetta_id, ingrediente_id),
    FOREIGN KEY (ricetta_id) REFERENCES Ricetta(id),
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredienti(id)
);


-- TABELLA PREPARAZIONE

CREATE TABLE Preparazione (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ricetta_id INT,
    descrizione TEXT,
    progressivo INT,
    FOREIGN KEY (ricetta_id) REFERENCES Ricetta(id)
);