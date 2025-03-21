-- 1. felhasznalo táblába rekordok beszúrása
INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Kovács Béla', 'jelszo123', 'bela.kovacs@example.com', 1, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Szabó Anna', 'anna1234', 'anna.szabo@example.com', 0, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Nagy László', 'laci789', 'laszlo.nagy@example.com', 0, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Tóth Katalin', 'kata456', 'katalin.toth@example.com', 1, CURRENT_TIMESTAMP);

INSERT INTO felhasznalo (nev, jelszo, email, szerep, bejelentkezes_idopontja)
VALUES ('Varga István', 'istvan555', 'istvan.varga@example.com', 0, CURRENT_TIMESTAMP);

-- 2. allapot_tabla táblába rekordok beszúrása
INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Aktív');

INSERT INTO allapot_tabla (allapot_nev)
VALUES ('Inaktív');
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
VALUES (1, 'pelda1.hu', 500, 1, 1);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (1, 'weboldal2.hu', 1000, 2, 2);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (0, 'uzlet3.hu', 150, NULL, 3);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (1, 'portal4.hu', 750, 3, 4);

INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
VALUES (0, 'szolgaltatas5.hu', 1200, NULL, 5);

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
VALUES (10000, CURRENT_TIMESTAMP, 2, 2);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (7500, CURRENT_TIMESTAMP, 3, 3);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (20000, CURRENT_TIMESTAMP, 4, 4);

INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
VALUES (15000, CURRENT_TIMESTAMP, 5, 5);