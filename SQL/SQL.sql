CREATE TABLE user (
    u_id NUMBER UNIQUE PRIMARY KEY,
    nev VARCHAR2(50) NOT NULL,
    jelszo VARCHAR2(50)  NOT NULL,
    email VARCHAR2(50)  UNIQUE NOT NULL,
    szerep BOOLEAN NOT NULL,
    bejelentkezes_idopontja TIMESTAMP,
    sz_id NUMBER DEFAULT NULL REFERENCES szamla(sz_id)
 );

 CREATE TABLE szamla (
    sz_id NUMBER PRIMARY KEY,
    osszeg NUMBER NOT NULL,
    letrehozas_datuma TIMESTAMP NOT NULL,
    u_id NUMBER DEFAULT NULL REFERENCES user(u_id),
    all_id NUMBER DEFAULT NULL REFERENCES allapot_tabla(all_id)

 );

 CREATE TABLE allapot_tabla (
    all_id NUMBER PRIMARY KEY,
    allapot_nev VARCHAR2(25) NOT NULL
 );

 CREATE TABLE webtarhely (
    w_id NUMBER PRIMARY KEY,
    allapot BOOLEAN NOT NULL,
    meret NUMBER NOT NULL,
    d_id NUMBER DEFAULT NOT NULL REFERENCES dijcsomag(d_id),
    u_id NUMBER DEFAULT NULL REFERENCES user(u_id)
 );

 CREATE TABLE domain (
    d_id NUMBER PRIMARY KEY,
    allapot BOOLEAN NOT NULL,
    domain_nev VARCHAR2(50) NOT NULL,
    megtekintes NUMBER NOT NULL

 );

 CREATE TABLE tudastar(
    t_id NUMBER PRIMARY KEY,
    kategoria NUMBER NOT NULL,
    kerdes_szoveg VARCHAR2(1000) NOT NULL,
    valasz_szoveg VARCHAR2 (1000) NOT NULL
 );

 CREATE TABLE kategoria_tabla(
    kat_id NUMBER PRIMARY KEY,
    kategoria_nev VARCHAR2(50)

 );

 CREATE TABLE dijcsomag (
    d_id NUMBER PRIMARY KEY,
    neve VARCHAR2(50) UNIQUE NOT NULL,
    ar NUMBER NOT NULL,
    max_meret NUMBER
 );





 