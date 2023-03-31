DROP TABLE if EXISTS user;
DROP TABLE if EXISTS patients;
DROP TABLE if EXISTS results;

/* colname TYPE COLCONSTRAINTS */

/* Table containing the login information for the doctors*/
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

/* A patients subtable that will be associated with each doctor */
CREATE TABLE patients (
    patientid INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor TEXT NOT NULL,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    lefteyepath TEXT,
    righteyepath TEXT,
    notes TEXT,
    FOREIGN KEY (doctor) REFERENCES user (username)
);

/* Results for each patient associated with each doctor */
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patientid INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lefteye TEXT,
    righteye TEXT,
    predictions TEXT, /* probably point to a vector on disk, or store as bytes*/
    FOREIGN KEY (patientid) REFERENCES patients (id)
);
