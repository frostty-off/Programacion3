from combate import Combate
from Personaje import *
from database import database
from eventos import Bueno_Evento


def elegir_objetivo(enemigos):
    enemigos_vivos = [enemigo for enemigo in enemigos if enemigo.estavivo()]
    for indice, enemigo in enumerate(enemigos_vivos, start=1):
        print(f"{indice}. {enemigo.nombre} (vida: {enemigo.vida})")

    while True:
        seleccion = input("Elige el numero del enemigo: ").strip()
        if seleccion.isdigit():
            indice = int(seleccion)
            if 1 <= indice <= len(enemigos_vivos):
                return enemigos_vivos[indice - 1]
        print("Seleccion invalida.")


def turno_jugador(combate, personaje):
    habilidades_disponibles = [
        habilidad
        for habilidad in personaje.habilidades
        if personaje.estamina >= habilidad.coste
    ]

    while True:
        opciones = "a (atacar)"
        if habilidades_disponibles:
            opciones += " / h (habilidad)"
        accion = input(f"Turno de {personaje.nombre}: {opciones}: ").strip().lower()

        if accion == "a":
            objetivo = elegir_objetivo(combate.enemigos)
            combate.atacar(personaje, objetivo)
            return
        if accion == "h" and habilidades_disponibles:
            for indice, habilidad in enumerate(habilidades_disponibles, start=1):
                print(f"{indice}. {habilidad.nombre} (coste: {habilidad.coste})")
            seleccion = input("Elige una habilidad: ").strip()
            if not seleccion.isdigit() or not 1 <= int(seleccion) <= len(habilidades_disponibles):
                print("Seleccion invalida.")
                continue
            habilidad = habilidades_disponibles[int(seleccion) - 1]
            objetivo = elegir_objetivo(combate.enemigos)
            combate.usar_habilidad(personaje, habilidad, objetivo)
            return
        print("Accion invalida.")


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El valor no puede quedar vacio.")


def crear_personaje(numero, nombres_existentes):
    print(f"\n--- Crear personaje {numero} de 4 ---")
    while True:
        nombre = leer_texto("Nombre: ")
        if nombre.casefold() not in nombres_existentes:
            break
        print("Ya existe un personaje con ese nombre.")

    profesion = leer_texto("Profesion: ")
    raza = leer_texto("Raza: ")
    clases = {
        "1": ("Guerrero", Warrior, (40, 25, 20, 120, 80, 1.2)),
        "2": ("Mago", Magician, (15, 10, 80, 100, 50, 2.0)),
        "3": ("Paladin", Paladin, (15, 10, 80, 100, 50, 2.0)),
        "4": ("Picaro", Rogue, (55, 15, 30, 90, 100, 1.5)),
        "5": ("Caballero", Knight, (40, 25, 20, 120, 80, 1.2))
    }
    for opcion, (nombre_clase, _, _) in clases.items():
        print(f"{opcion}. {nombre_clase}")
    while True:
        opcion = input("Clase: ").strip()
        if opcion in clases:
            _, clase_personaje, atributos = clases[opcion]
            break
        print("Seleccion de clase invalida.")

    return clase_personaje(nombre, profesion, raza, *atributos)


def personajes_predeterminados():
    mago = Magician("Gandalf", "Mago", "Humano", 15, 10, 80, 100, 50, 2.0)
    guerrero = Warrior("Aragorn", "Guerrero", "Humano", 40, 25, 20, 120, 80, 1.2)
    paladin = Paladin("Juan", "Paladin", "Humano", 15, 10, 80, 100, 50, 2.0)
    caballero = Knight("Luis", "Caballero", "Humano", 40, 25, 20, 120, 80, 1.2)
    return [mago, guerrero, paladin, caballero]


def elegir_personajes_predeterminados(db):
    predeterminados = personajes_predeterminados()

    print("\n--- Personajes predeterminados ---")
    for indice, personaje in enumerate(predeterminados, start=1):
        print(f"{indice}. {personaje.nombre} - {personaje.profesion}")

    while True:
        seleccion = input("Elige los 4 numeros separados por coma: ").strip()
        opciones = [opcion.strip() for opcion in seleccion.split(",")]
        if (
            opciones
            and all(opcion.isdigit() for opcion in opciones)
            and len(opciones) == 4
            and len({int(opcion) for opcion in opciones}) == len(opciones)
            and all(1 <= int(opcion) <= len(predeterminados) for opcion in opciones)
        ):
            personajes = [predeterminados[int(opcion) - 1] for opcion in opciones]
            for personaje in personajes:
                db.guardar_personaje(personaje)
            return personajes
        print("Seleccion invalida.")


def menu_personajes(db):
    while True:
        print("\n--- Menu de personajes ---")
        print("1. Crear cuatro personajes")
        print("2. Elegir personajes predeterminados")
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            nombres_existentes = {
                personaje.nombre.casefold()
                for personaje in db.cargar_personajes()
            }
            personajes = []
            for numero in range(1, 5):
                personaje = crear_personaje(numero, nombres_existentes)
                db.guardar_personaje(personaje)
                nombres_existentes.add(personaje.nombre.casefold())
                personajes.append(personaje)
            return personajes
        if opcion == "2":
            return elegir_personajes_predeterminados(db)
        print("Seleccion invalida.")


def elegir_grupo(personajes):
    personajes_vivos = [personaje for personaje in personajes if personaje.estavivo()]
    for indice, personaje in enumerate(personajes_vivos, start=1):
        print(f"{indice}. {personaje.nombre} (vida: {personaje.vida})")

    while True:
        seleccion = input(
            "Elige los personajes que pelearan (numeros separados por coma): "
        ).strip()
        opciones = [opcion.strip() for opcion in seleccion.split(",")]
        if (
            opciones
            and all(opcion.isdigit() for opcion in opciones)
            and len(opciones) <= 4
            and len({int(opcion) for opcion in opciones}) == len(opciones)
            and all(1 <= int(opcion) <= len(personajes_vivos) for opcion in opciones)
        ):
            return [personajes_vivos[int(opcion) - 1] for opcion in opciones]
        print("Seleccion invalida.")


def main():
    db = database()
    try:
        while True:
            juego = input("Deseas Jugar? (s/n): ").strip().lower()
            if juego == "n":
                print("Gracias por jugar o/")
                break
            if juego != "s":
                print("Seleccion invalida.")
                continue

            personajes_cargados = menu_personajes(db)
            print("\n--- CARGANDO PERSONAJES ---")

            victorias = 0
            while victorias < 6:
                if not any(personaje.estavivo() for personaje in personajes_cargados):
                    break

                print(f"\nVictorias necesarias: {victorias}/6")
                evento_bueno = Bueno_Evento("Beneficio", victorias + 1)
                if evento_bueno.regeneracion(personajes_cargados):
                    print("Evento de regeneracion aplicado a todos los personajes.")
                if evento_bueno.multiplicador(personajes_cargados):
                    print("Evento multiplicador aplicado a todos los personajes.")
                for personaje in personajes_cargados:
                    db.guardar_personaje(personaje)

                while True:
                    grupo_combate = elegir_grupo(personajes_cargados)
                    combate = Combate.aleatorio(grupo_combate, db)
                    print(f"Te enfrentas a {len(combate.enemigos)} enemigos.")
                    for enemigo in combate.enemigos:
                        enemigo.atributos()
                        print("=" * 40)

                    while combate.estado == "en_curso":
                        for personaje in grupo_combate:
                            if personaje.estavivo():
                                turno_jugador(combate, personaje)
                            if combate.estado != "en_curso":
                                break
                        if combate.estado == "en_curso":
                            combate.turno_enemigos()

                    if combate.estado == "victoria":
                        victorias += 1
                        print(f"Ronda ganada. Victorias: {victorias}/6.")
                        for personaje in personajes_cargados:
                            db.guardar_personaje(personaje)
                        break

                    for personaje in personajes_cargados:
                        db.guardar_personaje(personaje)

                    if not any(personaje.estavivo() for personaje in personajes_cargados):
                        print(f"No quedan personajes vivos. Victorias: {victorias}/6.")
                        break

                    print("El grupo cayo. Elige otro grupo para intentar esta ronda.")

            if victorias == 6:
                print("Felicidades, ganaste seis combates y terminaste el juego.")
    finally:
        db.cerrar()


if __name__ == "__main__":
    main()
