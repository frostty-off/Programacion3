import random


class Combate:
    def __init__(self, personajes, enemigos, db=None):
        self.personajes = list(personajes)
        if not 1 <= len(self.personajes) <= 4:
            raise ValueError("El grupo debe tener entre uno y cuatro personajes.")
        if not enemigos:
            raise ValueError("El combate debe tener al menos un enemigo.")

        self.enemigos = list(enemigos)
        self.db = db
        self.estado = "en_curso"
        self.id_db = db.iniciar_combate(self.personajes, self.enemigos) if db else None
        self._actualizar_estado()

    @classmethod
    def aleatorio(cls, personajes, db, cantidad=None):
        if cantidad is None:
            cantidad = random.choice((3, 6))
        enemigos = db.cargar_enemigos(cantidad=cantidad)
        return cls(personajes, enemigos, db)

    @property
    def participantes(self):
        return self.personajes + self.enemigos

    def _validar_participante(self, participante):
        if participante not in self.participantes:
            raise ValueError("El participante no pertenece a este combate.")
        if not participante.estavivo():
            raise ValueError(f"{participante.nombre} ya no puede combatir.")

    def _asegurar_combate_activo(self):
        if self.estado != "en_curso":
            raise RuntimeError(f"El combate ya finalizo: {self.estado}.")

    def _actualizar_estado(self):
        if not any(personaje.estavivo() for personaje in self.personajes):
            self.estado = "derrota"
            ganador = "enemigos"
        elif not any(enemigo.estavivo() for enemigo in self.enemigos):
            self.estado = "victoria"
            ganador = ", ".join(personaje.nombre for personaje in self.personajes)
        else:
            return

        if self.db:
            self.db.finalizar_combate(
                self.id_db, self.estado, ganador, self.participantes
            )

    def reintentar(self, salud_estamina_inicial):
        if self.estado != "derrota":
            raise RuntimeError("Solo se puede reintentar una ronda perdida.")
        for personaje, (vida, estamina) in salud_estamina_inicial.items():
            personaje.vida = vida
            personaje.estamina = estamina
        self.estado = "en_curso"
        self.id_db = (
            self.db.iniciar_combate(self.personajes, self.enemigos)
            if self.db
            else None
        )
        self._actualizar_estado()

    def atacar(self, actor, objetivo):
        self._asegurar_combate_activo()
        self._validar_participante(actor)
        self._validar_participante(objetivo)
        if (
            (actor in self.personajes and objetivo not in self.enemigos)
            or (actor not in self.personajes and objetivo not in self.personajes)
        ):
            raise ValueError("El objetivo debe pertenecer al equipo contrario.")

        dano = max(0, int(actor.damage(objetivo)))
        objetivo.vida = max(0, objetivo.vida - dano)
        if not objetivo.estavivo():
            objetivo.morir()
        print(f"{actor.nombre} ha realizado {dano} de daño a {objetivo.nombre}")

        if self.db:
            self.db.registrar_accion_combate(
                self.id_db, actor.nombre, objetivo.nombre, "ataque", dano
            )
        self._actualizar_estado()
        return dano

    def usar_habilidad(self, actor, habilidad, objetivo):
        self._asegurar_combate_activo()
        self._validar_participante(actor)
        self._validar_participante(objetivo)
        if (
            (actor in self.personajes and objetivo not in self.enemigos)
            or (actor not in self.personajes and objetivo not in self.personajes)
        ):
            raise ValueError("El objetivo debe pertenecer al equipo contrario.")
        if habilidad not in actor.habilidades:
            raise ValueError(f"{habilidad.nombre} no pertenece a {actor.nombre}.")
        if actor.estamina < habilidad.coste:
            raise ValueError(f"{actor.nombre} no tiene suficiente estamina.")

        actor.estamina -= habilidad.coste
        dano = max(0, int(habilidad.dealed_skill(actor, objetivo)))
        objetivo.vida = max(0, objetivo.vida - dano)
        if not objetivo.estavivo():
            objetivo.morir()
        print(
            f"{actor.nombre} ha usado {habilidad.nombre} y ha realizado "
            f"{dano} puntos de daño a {objetivo.nombre}"
        )

        if self.db:
            self.db.registrar_accion_combate(
                self.id_db,
                actor.nombre,
                objetivo.nombre,
                "habilidad",
                dano,
                habilidad.nombre
            )
        self._actualizar_estado()
        return dano

    def turno_enemigos(self, objetivo=None):
        self._asegurar_combate_activo()
        if objetivo is not None:
            if objetivo not in self.personajes:
                raise ValueError("El objetivo debe pertenecer al equipo de personajes.")
            if not objetivo.estavivo():
                raise ValueError(f"{objetivo.nombre} ya no puede combatir.")

        for enemigo in self.enemigos:
            personajes_vivos = [
                personaje for personaje in self.personajes if personaje.estavivo()
            ]
            if not personajes_vivos:
                break
            if enemigo.estavivo():
                objetivo_enemigo = (
                    objetivo if objetivo is not None else random.choice(personajes_vivos)
                )
                habilidades_disponibles = [
                    habilidad
                    for habilidad in enemigo.habilidades
                    if enemigo.estamina >= habilidad.coste
                ]
                if (
                    habilidades_disponibles
                    and random.choice(("ataque", "habilidad")) == "habilidad"
                ):
                    habilidad = random.choice(habilidades_disponibles)
                    self.usar_habilidad(enemigo, habilidad, objetivo_enemigo)
                else:
                    self.atacar(enemigo, objetivo_enemigo)
                if objetivo is not None and not objetivo.estavivo():
                    break
        return self.estado
