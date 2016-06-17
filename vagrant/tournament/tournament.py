#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.Error as e:
        print(e.pgerror)


def delete_matches():
    """Remove all the match records from the database."""

    db, c = connect()
    c.execute("TRUNCATE matches;")
    db.commit()
    db.close()


def delete_players():
    """Remove all the player records from the database."""

    db, c = connect()
    c.execute("TRUNCATE players CASCADE;")
    db.commit()
    db.close()


def count_players():
    """Returns the number of players currently registered."""

    db, c = connect()
    query = "SELECT count(*) as num FROM players;"
    c.execute(query)
    row = c.fetchone()
    count = int(row[0])
    db.close()

    return count


def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    db, c = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    param = (name,)
    c.execute(query, param)
    db.commit()
    db.close()


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, c = connect()
    query = "SELECT * FROM standings;"
    c.execute(query)
    player_wins = [(int(row[0]), str(row[1]), int(row[2]), int(row[3])) for row in c.fetchall()]
    db.close()

    return player_wins


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, c = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    param = (winner, loser,)
    c.execute(query, param)
    db.commit()
    db.close()


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    db, c = connect()
    query = "SELECT id, name FROM standings ORDER BY wins DESC;"
    c.execute(query)
    standings = c.fetchall()
    db.close()

    # create pairing by adding every pair of two
    pairings = [(standings[i][0], standings[i][0], standings[i + 1][0], standings[i + 1][1]) for i in
                range(0, len(standings), 2)]

    return pairings
