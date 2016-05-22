CREATE TABLE IF NOT EXISTS boxes (
    boxID       TEXT    PRIMARY KEY NOT NULL,
    connected   BOOL    NOT NULL,
    inUse       BOOL    NOT NULL
);
