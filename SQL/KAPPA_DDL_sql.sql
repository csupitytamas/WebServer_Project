
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