import random
from Personaje import Personaje
class Evento:

    def __init__(self,nombre,id):
        self.nombre = nombre
        self.id = id
        
    def generar_evento(self):
        self.frec = random.randint(1, 6)
        return self.frec

    def _personajes_como_lista(self, personajes):
        if isinstance(personajes, Personaje):
            return [personajes]
        return list(personajes)

#Generamos los eventos buenos

class Bueno_Evento(Evento):

    def __init__(self, nombre, id):
        super().__init__(nombre, id)

    def regeneracion(self, personajes):
        if self.generar_evento() == 1:
            self.sanacion = 0.45
            self.estamina = 100
            for personaje in self._personajes_como_lista(personajes):
                personaje.vida += round(personaje.vida * self.sanacion)
                personaje.estamina = self.estamina
            return True
        return False

    def multiplicador(self, personajes):
        if self.generar_evento() == 2:
            factor = 0.15
            atributos_dano = ("gaunlets", "wand", "shield", "knive", "sword")
            for personaje in self._personajes_como_lista(personajes):
                for habilidad in personaje.habilidades:
                    habilidad.dmg_base *= 1 + factor
                atributo = next(
                    (nombre for nombre in atributos_dano if hasattr(personaje, nombre)),
                    "fuerza"
                )
                setattr(
                    personaje,
                    atributo,
                    getattr(personaje, atributo) * (1 + factor)
                )
            return True
        return False

#Generamos los eventos neutrales(combate) y si son de 3 o 6 enemigos

class Combate_Trigger(Evento):

    def __init__(self, nombre, id):
            super().__init__(nombre, id)

    def combate_3(self):
        if self.generar_evento() == 3:
            self.cantidad_enemigos = 3
            pass
        else: return

    def combate_6(self):
        if self.generar_evento() == 4:
            self.cantidad_enemigos = 6
            pass        

#Generamos los eventos desfavorables

class Malo_Evento(Evento):

    def __init__(self, nombre, id):
            super().__init__(nombre, id)

    def trampa(self):
        if self.generar_evento() == 3:
            self.trampa = 0.24
            pass
        else: return

    def anulacion_estamina(self):
        if self.generar_evento() == 3:
            Personaje.estamina = 0.0
        else: return              

#evento1 = Evento("Regeneracion", 1)  
#evento2 = Evento("Multi", 2)
#evento3 = Evento("Combate(3 enemigos)", 3)
#evento4 = Evento("Combate(6 enemigos)", 4)
#evento5 = Evento("Trampa", 5)
#evento6 = Evento("Anulacion Estamina", 6)