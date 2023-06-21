import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_team(conn, team):
    sql = """INSERT INTO Teams(id,name,city) VALUES(?,?,?);"""
    cur = conn.cursor()
    cur.execute(sql, team)
    conn.commit()

def create_player(conn, player):
    sql = """INSERT INTO Players(first_name,last_name) VALUES(?,?);"""
    cur = conn.cursor()
    cur.execute(sql, player)
    conn.commit()


if __name__ == '__main__':
    database = "./db_stats.db"

    sql_create_players_table = """CREATE TABLE IF NOT EXISTS Players (
        id integer,
        first_name varchar(50) NOT NULL,
        last_name varchar(50) NOT NULL,
        nationality varchar(50),
        position varchar(10),
        age tinyint unsigned,
        height tinyint unsigned,
        weight tinyint unsigned,
        CONSTRAINT PK_Players PRIMARY KEY (id)
        );"""

    sql_create_team_table = """CREATE TABLE IF NOT EXISTS Teams (
        id integer NOT NULL,
        current_name varchar(50) NOT NULL,
        CONSTRAINT PK_Teams PRIMARY KEY (id)
        );"""

    sql_create_teamsHistory_table = """CREATE TABLE IF NOT EXISTS TeamsHistory (
        team_id integer NOT NULL,
        team_name varchar(50) NOT NULL,
        team_city varchar(50) NOT NULL,
        start_year year NOT NULL,
        end_year year,
        CONSTRAINT PK_TeamsHistory PRIMARY KEY (team_id, start_year)
        CONSTRAINT FK_Games_team_id FOREIGN KEY team_id REFERENCES Teams(id)
        );"""

    sql_create_games_table = """CREATE TABLE IF NOT EXISTS Games (
            id_teamHome integer NOT NULL,
            name_teamHome varchar(50) NOT NULL,
            id_teamAway integer NOT NULL,
            name_teamAway varchar(50) NOT NULL,
            game_date date NOT NULL,
            league varchar(4) NOT NULL,
            idx_win tinyint NOT NULL,
            url_boxscore varchar(100),
            CONSTRAINT PK_Games PRIMARY KEY (id_teamHome, id_teamAway, game_date),
            CONSTRAINT FK_Games_teamHome FOREIGN KEY (id_teamHome, name_teamHome) REFERENCES Teams(id, name),
            CONSTRAINT FK_Games_teamAway FOREIGN KEY (id_teamAway, name_teamAway) REFERENCES Teams(id, name)
            );"""

    sql_create_performance_table = """"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn:
        print("Connection to database established")
        # create players table
        create_table(conn, sql_create_players_table)
        # create team table
        create_table(conn, sql_create_team_table)
        # create games table
        create_table(conn, sql_create_games_table)
        # create performance table
        # create_table(conn, sql_create_performance_table)

    else:
        print("Error! cannot create the database connection.")

    team = (1, "Duesseldorf Panthers", "Duesseldorf")
    create_team(conn, team)
    team = (1, "Duesseldorf Lions", "Duesseldorf")
    create_team(conn, team)

    player = ("Maeric", "Achiepi")
    create_player(conn, player)
