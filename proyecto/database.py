import sqlite3
from Personaje import Warrior, Magician, Paladin, Rogue, Knight, Personaje
from Habilidades import Habilidades

class database:
    def __init__(self, db_name="rpg_mundo.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                profesion TEXT NOT NULL,
                raza TEXT NOT NULL,
                fuerza INTEGER,
                defensa INTEGER,
                inteligencia INTEGER,
                vida INTEGER,
                estamina INTEGER,
                clase_tipo TEXT NOT NULL,
                equipo_valor REAL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personaje_habilidades (
                personaje_nombre TEXT,
                habilidad_nombre TEXT,
                tipo TEXT,
                coste INTEGER,
                dmg_base REAL,
                FOREIGN KEY(personaje_nombre) REFERENCES personajes(nombre)
            )
        ''')
        self.conn.commit()

    def guardar_personaje(self, personaje):
        clase_tipo = type(personaje).__name__
        equipo_valor = 0.0
        #extraer clase para saber equipo espefico(arma)
        if isinstance(personaje, Warrior): equipo_valor = personaje.gaunlets
        elif isinstance(personaje, Magician): equipo_valor = personaje.wand
        elif isinstance(personaje, Paladin): equipo_valor = personaje.shield
        elif isinstance(personaje, Rogue): equipo_valor = personaje.knive
        elif isinstance(personaje, Knight): equipo_valor = personaje.sword

        #actualizar datos en la tabla
        self.cursor.execute('''
            INSERT OR REPLACE INTO personajes 
            (nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, clase_tipo, equipo_valor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            personaje.nombre, personaje.profesion, personaje.raza,
            personaje.fuerza, personaje.defensa, personaje.inteligencia,
            personaje.vida, personaje.estamina, clase_tipo, equipo_valor
        ))

        #limpiar habilidades de la tabla
        self.cursor.execute('DELETE FROM personaje_habilidades WHERE personaje_nombre = ?', (personaje.nombre,))

        #guardar habilidades en una lista
        for hab in personaje.habilidades:
            self.cursor.execute('''
                INSERT INTO personaje_habilidades (personaje_nombre, habilidad_nombre, tipo, coste, dmg_base)
                VALUES (?, ?, ?, ?, ?)
            ''', (personaje.nombre, hab.nombre, hab.tipo, hab.coste, hab.dmg_base))

        self.conn.commit()
        print(f"{personaje.nombre} y sus habilidades fueron guardados con éxito")

    def cargar_personajes(self):
        self.cursor.execute('SELECT * FROM personajes')
        filas = self.cursor.fetchall()
        personajes = []

        for fila in filas:
            _, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, clase_tipo, equipo_valor = fila

            #insertar clase segun valor ingresado (como sera la seleccion???)
            if clase_tipo == "Warrior": p = Warrior(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, equipo_valor)
            elif clase_tipo == "Magician": p = Magician(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, equipo_valor)
            elif clase_tipo == "Paladin": p = Paladin(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, equipo_valor)
            elif clase_tipo == "Rogue": p = Rogue(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, equipo_valor)
            elif clase_tipo == "Knight": p = Knight(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, equipo_valor)
            else: p = Personaje(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)

            #buscar/adjuntar habilidades
            self.cursor.execute('SELECT habilidad_nombre, tipo, coste, dmg_base FROM personaje_habilidades WHERE personaje_nombre = ?', (nombre,))
            habs_filas = self.cursor.fetchall()
            for h_nombre, h_tipo, h_coste, h_dmg in habs_filas:
                habilidad_obj = Habilidades(h_nombre, h_tipo, h_coste, h_dmg)
                p.habilidades.append(habilidad_obj)

            personajes.append(p)
            
        return personajes

    def cerrar(self):
        self.conn.close()