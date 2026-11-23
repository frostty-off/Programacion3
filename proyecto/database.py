import sqlite3
import random
from Personaje import Warrior, Magician, Paladin, Rogue, Knight, Personaje
from Habilidades import Habilidades
from enemigos import GoblinEnemy, LamiaEnemy, OgroEnemy, BandidoEnemy, DemonioEnemy, Enemigos

class database:
    def __init__(self, db_name="rpg_mundo.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crear_tablas()
        self.inicializar_eventos_db()
        self.inicializar_enemigos_db()

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

    def inicializar_eventos_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY,
                nombre TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        ''')
        self.cursor.executemany('''
            INSERT OR IGNORE INTO eventos (id, nombre, tipo, descripcion)
            VALUES (?, ?, ?, ?)
        ''', [
            (1, "Regeneracion", "bueno", "Restaura vida al personaje."),
            (2, "Multiplicador", "bueno", "Aumenta temporalmente el daño."),
            (3, "Combate (3 enemigos)", "combate", "Inicia un combate contra tres enemigos."),
            (4, "Combate (6 enemigos)", "combate", "Inicia un combate contra seis enemigos."),
            (5, "Trampa", "malo", "El personaje recibe daño por una trampa."),
            (6, "Anulacion de estamina", "malo", "Reduce la estamina del personaje a cero.")
        ])
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS combates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                iniciado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                finalizado_en TEXT,
                estado TEXT NOT NULL DEFAULT 'en_curso',
                ganador TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS combate_participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                combate_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                equipo TEXT NOT NULL,
                vida_inicial REAL NOT NULL,
                vida_final REAL,
                FOREIGN KEY(combate_id) REFERENCES combates(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS combate_acciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                combate_id INTEGER NOT NULL,
                actor TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                dano REAL NOT NULL DEFAULT 0,
                detalle TEXT,
                creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(combate_id) REFERENCES combates(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def iniciar_combate(self, personajes, enemigos):
        self.cursor.execute("INSERT INTO combates DEFAULT VALUES")
        combate_id = self.cursor.lastrowid
        participantes = [
            (combate_id, personaje.nombre, "personaje", personaje.vida)
            for personaje in personajes
        ] + [
            (combate_id, enemigo.nombre, "enemigo", enemigo.vida)
            for enemigo in enemigos
        ]
        self.cursor.executemany('''
            INSERT INTO combate_participantes
                (combate_id, nombre, equipo, vida_inicial)
            VALUES (?, ?, ?, ?)
        ''', participantes)
        self.conn.commit()
        return combate_id

    def registrar_accion_combate(self, combate_id, actor, objetivo, tipo, dano=0, detalle=None):
        self.cursor.execute('''
            INSERT INTO combate_acciones
                (combate_id, actor, objetivo, tipo, dano, detalle)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (combate_id, actor, objetivo, tipo, dano, detalle))
        self.conn.commit()

    def finalizar_combate(self, combate_id, estado, ganador, participantes):
        self.cursor.execute('''
            UPDATE combates
            SET estado = ?, ganador = ?, finalizado_en = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (estado, ganador, combate_id))
        self.cursor.execute('''
            SELECT id FROM combate_participantes
            WHERE combate_id = ?
            ORDER BY id
        ''', (combate_id,))
        participante_ids = [fila[0] for fila in self.cursor.fetchall()]
        if len(participante_ids) != len(participantes):
            raise RuntimeError("No coinciden los participantes registrados del combate.")
        for participante_id, participante in zip(participante_ids, participantes):
            self.cursor.execute('''
                UPDATE combate_participantes
                SET vida_final = ?
                WHERE id = ?
            ''', (participante.vida, participante_id))
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

            personajes.append(p)
            
        return personajes

#enemigos wiiiuuiiuu

    def inicializar_enemigos_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS enemigos (
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
                equipo_valor REAL)
        ''')

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS enemigo_habilidades (
                    enemigo_nombre TEXT,
                    habilidad_nombre TEXT,
                    tipo TEXT,
                    coste INTEGER,
                    dmg_base REAL,
                    FOREIGN KEY(enemigo_nombre) REFERENCES enemigos(nombre)  ) 
        ''')
        self.conn.commit()

        enemigos_iniciales = [
                ("Goblin", "Bailarin de teibol", "Goblin", 45, 50, 65, 100, 65, "GoblinEnemy", 1.1),
                ("Lamia", "Taotista", "Lamia", 60, 30, 45, 80, 70, "LamiaEnemy", 1.2),
                ("Ogro", "Jugador de lol", "Ogro", 80, 55, 10, 140, 20, "OgroEnemy", 1.3),
                ("Bandido", "Pastelero", "Humano", 60, 45, 60, 100, 70, "BandidoEnemy", 1.2),
                ("Demonio", "Vendedor de movistar", "Diablillo", 35, 45, 100, 45, 40, "DemonioEnemy", 1.5)
            ]
        for enemigo in enemigos_iniciales:
            self.cursor.execute('''
                INSERT OR REPLACE INTO enemigos (nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, clase_tipo, equipo_valor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', enemigo)
        self.conn.commit()


    #aleatorio lol
    def cargar_enemigos(self, cantidad=2):
        self.cursor.execute("SELECT * FROM enemigos")
        enemigos = self.cursor.fetchall()
        enemigos_seleccionados = []
        for _ in range(cantidad):
            f=random.choice(enemigos)
            _,nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, clase_tipo, equipo_valor = f
            if clase_tipo == "GoblinEnemy":
                enemigo_obj = GoblinEnemy(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
            elif clase_tipo == "LamiaEnemy":
                enemigo_obj = LamiaEnemy(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
            elif clase_tipo == "OgroEnemy":
                enemigo_obj = OgroEnemy(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
            elif clase_tipo == "BandidoEnemy":
                enemigo_obj = BandidoEnemy(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
            elif clase_tipo == "DemonioEnemy":
                enemigo_obj = DemonioEnemy(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
            #cargan las habilidades de enemigos
            self.cursor.execute('''
                SELECT habilidad_nombre, tipo, coste, dmg_base 
                FROM enemigo_habilidades WHERE enemigo_nombre = ?
            ''', (nombre,))
            enemigo_habilidades = self.cursor.fetchall()
            for h_nombre, h_tipo, h_coste, h_dmg_base in enemigo_habilidades:
                habilidad = Habilidades(h_nombre, h_tipo, h_coste, h_dmg_base)
                enemigo_obj.habilidades.append(habilidad)
            enemigos_seleccionados.append(enemigo_obj)
        return enemigos_seleccionados


    def cerrar(self):
        self.conn.commit()
        self.conn.close()