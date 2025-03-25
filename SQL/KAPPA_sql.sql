--DDL utasitások
CREATE TABLE kategoria_tabla (
                                 kat_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                 kategoria_nev VARCHAR2(50)
);


CREATE TABLE dijcsomag (
                           d_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                           neve VARCHAR2(50) UNIQUE NOT NULL,
                           ar NUMBER NOT NULL,
                           max_meret NUMBER
);


CREATE TABLE allapot_tabla (
                               all_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                               allapot_nev VARCHAR2(25) NOT NULL
);


CREATE TABLE felhasznalo (
                             u_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                             nev VARCHAR2(50) NOT NULL,
                             jelszo VARCHAR2(50) NOT NULL,
                             email VARCHAR2(50) UNIQUE NOT NULL,
                             szerep NUMBER(1) NOT NULL, -- BOOLEAN helyett NUMBER(1)
                             bejelentkezes_idopontja TIMESTAMP
);


CREATE TABLE webtarhely (
                            w_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            allapot NUMBER(1) NOT NULL, -- BOOLEAN helyett NUMBER(1)
                            meret NUMBER NOT NULL,
                            d_id NUMBER REFERENCES dijcsomag(d_id) ON DELETE SET NULL,
                            u_id NUMBER DEFAULT NULL REFERENCES felhasznalo(u_id) ON DELETE CASCADE
);


CREATE TABLE domain (
                        d_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        allapot NUMBER(1) NOT NULL, -- BOOLEAN helyett NUMBER(1)
                        domain_nev VARCHAR2(50) NOT NULL,
                        megtekintes NUMBER NOT NULL,
                        u_id NUMBER DEFAULT NULL REFERENCES felhasznalo(u_id) ON DELETE CASCADE,
                        dij_id NUMBER REFERENCES dijcsomag(d_id) ON DELETE SET NULL
);


CREATE TABLE tudastar (
                          t_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                          kategoria NUMBER NOT NULL REFERENCES kategoria_tabla(kat_id) ON DELETE CASCADE,
                          kerdes_szoveg VARCHAR2(1000) NOT NULL,
                          valasz_szoveg VARCHAR2(1000) NOT NULL
);


CREATE TABLE szamla (
                        sz_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        osszeg NUMBER NOT NULL,
                        letrehozas_datuma TIMESTAMP NOT NULL,
                        u_id NUMBER REFERENCES felhasznalo(u_id) ON DELETE SET NULL,
                        all_id NUMBER REFERENCES allapot_tabla(all_id) ON DELETE SET NULL
);

-- DML UTASÍTÁSOK

-- 1. felhasznalo táblába rekordok beszúrása
INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Kovács Béla', 'jelszo123', 'bela.kovacs@gmail.com', 1, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Szabó Anna', 'anna1234', 'anna.szabo@gmail.com', 0, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Nagy László', 'laci789', 'laszlo.nagy@gmail.com', 0, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Tóth Katalin', 'kata456', 'katalin.toth@gmail.com', 0, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Varga István', 'istvan555', 'istvan.varga@gmail.com', 0, CURRENT_TIMESTAMP);

-- 2. allapot_tabla táblába rekordok beszúrása
INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Aktív');

INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Inaktív');

INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Függőben');

INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Lezárt');

INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Törölt');

-- 3. dijcsomag táblába rekordok beszúrása
INSERT INTO dijcsomag (neve, ar, max_meret)
VALUES ('Alap csomag', 5000, 100);

INSERT INTO dijcsomag (neve, ar, max_meret)
VALUES ('Prémium csomag', 10000, 200);

INSERT INTO dijcsomag (neve, ar, max_meret)
VALUES ('Pro csomag', 15000, 500);

INSERT INTO dijcsomag (neve, ar, max_meret)
VALUES ('Vállalati csomag', 20000, 1000);

INSERT INTO dijcsomag (neve, ar, max_meret)
VALUES ('Speciális csomag', 25000, 2000);

-- 4. webtarhely táblába rekordok beszúrása
INSERT INTO webtarhely (allapot, meret, d_id, u_id)
VALUES (1, 50, 1, 1);

INSERT INTO webtarhely (allapot, meret, d_id, u_id)
VALUES (1, 100, 2, 2);

INSERT INTO webtarhely (allapot, meret, d_id, u_id)
VALUES (0, 150, 3, NULL);

INSERT INTO webtarhely (allapot, meret, d_id, u_id)
VALUES (1, 200, 4, 3);

INSERT INTO webtarhely (allapot, meret, d_id, u_id)
VALUES (0, 250, 5, NULL);

-- 5. domain táblába rekordok beszúrása
INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (1, 'webshop.hu', 0, 1, 1);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (1, 'weboldal.hu', 0, 2, 2);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (0, 'egyoldal.hu', 0, NULL, 3);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (1, 'hirportal.hu', 0, 3, 4);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (0, 'sport.hu', 0, NULL, 5);

-- 6. tudastar táblába rekordok beszúrása
INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
VALUES (1, 'Hogyan hozhatok létre új felhasználót?', 'A Felhasználók menüpontban kattints az Új felhasználó gombra.');

INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
VALUES (2, 'Hogyan módosíthatom a jelszavamat?', 'A Profil beállításai menüpontban kattints a Jelszó módosítása gombra.');

INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
VALUES (3, 'Mik a díjcsomagok árai?', 'Az árakat a Díjcsomagok menüpontban találhatod.');

INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
VALUES (1, 'Hogyan lehet domain nevet regisztrálni?', 'A Domain regisztráció menüpontban kattints az Új domain gombra.');

INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
VALUES (2, 'Hogyan lehet webtárhelyet vásárolni?', 'A Webtárhely menüpontban kattints a Vásárlás gombra.');

-- 7. kategoria_tabla táblába rekordok beszúrása
INSERT INTO kategoria_tabla (kategoria_nev)
VALUES ('Felhasználói fiók');

INSERT INTO kategoria_tabla (kategoria_nev)
VALUES ('Biztonság');

INSERT INTO kategoria_tabla (kategoria_nev)
VALUES ('Díjcsomagok');

INSERT INTO kategoria_tabla (kategoria_nev)
VALUES ('Domain');

INSERT INTO kategoria_tabla (kategoria_nev)
VALUES ('Webtárhely');

-- 8. szamla táblába rekordok beszúrása
INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (5000, CURRENT_TIMESTAMP, 1, 1);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (10000, CURRENT_TIMESTAMP, 2, 4);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (7500, CURRENT_TIMESTAMP, 3, 3);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (20000, CURRENT_TIMESTAMP, 2, 1);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (15000, CURRENT_TIMESTAMP, 5, 5);


--SELECT UTASITÁSOK
-- KATEGORIA_TABLA
SELECT * FROM kategoria_tabla;

-- DIJCSOMAG
SELECT * FROM dijcsomag;

-- ALLAPOT_TABLA
SELECT * FROM allapot_tabla;

-- FELHASZNALO
SELECT * FROM felhasznalo;

-- WEBTARHELY
SELECT * FROM webtarhely;

-- DOMAIN
SELECT * FROM domain;

-- TUDASTAR
SELECT * FROM tudastar;

-- SZAMLA
SELECT * FROM szamla;

SELECT * FROM kategoria_tabla;

-- DIJCSOMAG
SELECT * FROM dijcsomag;

-- ALLAPOT_TABLA
SELECT * FROM allapot_tabla;

-- FELHASZNALO
SELECT * FROM felhasznalo;

-- WEBTARHELY
SELECT * FROM webtarhely;

-- DOMAIN
SELECT * FROM domain;

-- TUDASTAR
SELECT * FROM tudastar;

-- SZAMLA
SELECT * FROM szamla;

-- Ha függőben van a számla
SELECT * FROM szamla
WHERE all_id IS NOT NULL AND all_id <> 3;
-- Az admin felhasználók
SELECT *
FROM felhasznalo
WHERE szerep = 1;
-- Azok a webtárhelyek amik userhez tartoznak
SELECT w.* FROM webtarhely w
WHERE w.u_id IS NOT NULL;
-- Azok a domainek amik userhez tartoznak
SELECT d.* FROM domain d
WHERE d.u_id IS NOT NULL;
--Azok a webtárhelyek amik aktívak.
SELECT * FROM webtarhely
WHERE allapot = 1;
--Amelyik domain nem foglalt
SELECT *
FROM domain
WHERE allapot = 0;
-- A magas árkategóriáju csomagok
SELECT *
FROM dijcsomag
WHERE ar > 15000;
