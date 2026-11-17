from random import random

from Personaje import Magician, Warrior
from Habilidades import Habilidades
from database import database

db = database()
fireball = Habilidades("Bola de fuego", "Magico", 15, 1.5)
slash = Habilidades("Corte Feroz", "Fisico", 10, 2.0)

mago = Magician("Gandalf", "Mago", "Humano", 15, 10, 80, 100, 50, 2.0)
mago.habilidades.append(fireball)

guerrero = Warrior("Aragorn", "Guerrero", "Humano", 40, 25, 20, 120, 80, 1.2)
guerrero.habilidades.append(slash)

db.guardar_personaje(mago)
db.guardar_personaje(guerrero)

print("\n--- CARGANDO DESDE LA BASE DE DATOS ---")
personajes_cargados = db.cargar_personajes()

for p in personajes_cargados:

    p.atributos()
    print("=" * 40)

db.cerrar()