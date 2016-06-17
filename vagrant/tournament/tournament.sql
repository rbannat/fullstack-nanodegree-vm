-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
    id serial primary key,
    name varchar(40) NOT NULL
);

DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches (
    id serial primary key,
    winner integer references players(id),
    loser integer references players(id)
);

CREATE VIEW standings AS
SELECT players.id, players.name,
(SELECT COUNT(matches.winner)
    FROM matches
    WHERE players.id = matches.winner)
    AS wins,
(SELECT count(matches.id)
    FROM matches
    WHERE players.id = matches.winner
    OR players.id = matches.loser)
    AS matches
FROM players
ORDER BY wins DESC, matches DESC;