PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL REFERENCES teams(id),
    name TEXT NOT NULL,
    UNIQUE (team_id, name)
);

INSERT OR IGNORE INTO teams (name)
VALUES ('SPŠE Elyta');

INSERT OR IGNORE INTO members (team_id, name)
SELECT id, 'David Kysilka'
FROM teams
WHERE name = 'SPŠE Elyta';

INSERT OR IGNORE INTO members (team_id, name)
SELECT id, 'Marek Špinar'
FROM teams
WHERE name = 'SPŠE Elyta';