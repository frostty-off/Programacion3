from Habilidades import Habilidades
class Enemigos:
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina):
        self.nombre = nombre
        self.profesion = profesion
        self.raza = raza
        self.fuerza = fuerza
        self.defensa = defensa
        self.inteligencia = inteligencia
        self.vida = vida
        self.estamina = estamina
        self.habilidades = []

    def atributos(self):
        print(f"{self.nombre} {self.profesion} ({self.raza}): ")
        print("- Fuerza: ", self.fuerza)
        print("- Defensa: ", self.defensa)
        print("- Inteligencia: ", self.inteligencia)
        print("- Vida: ", self.vida)
        print("- Estamina: ", self.estamina)
        if self.habilidades:
            print("- Habilidades aprendidas:")
            for h in self.habilidades:
                print(f"  * {h.nombre} (Tipo: {h.tipo}, Coste: {h.coste})")
                
    def estavivo(self):
        return self.vida > 0

    def morir(self):
        self.vida = 0
        print(f"{self.nombre} ha muerto")

    def damage(self, personaje):
        if self.fuerza >= personaje.defensa:
            return self.fuerza - personaje.defensa
        else:
            return (self.fuerza - personaje.defensa) * -1
    
    def atacar(self, personaje):
        dealed = self.damage(personaje)
        personaje.vida = personaje.vida - dealed
        if personaje.estavivo():
            print(f"{self.nombre} ha realizado {dealed} de daño a {personaje.nombre}")
        else:
            personaje.morir()

class GoblinEnemy(Enemigos):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, weapon_mult=1.1):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.weapon_mult = weapon_mult
        self.habilidades.append(Habilidades("Golpe", "Fisico", 5, 1.5))
        
    def damage(self, enemigo):
        poder = self.fuerza * self.weapon_mult
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)

class LamiaEnemy(Enemigos):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, weapon_mult=1.2):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.weapon_mult = weapon_mult
        
    def damage(self, enemigo):
        poder = self.fuerza * self.weapon_mult
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)

class OgroEnemy(Enemigos):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, weapon_mult=1.3):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.weapon_mult = weapon_mult
        
    def damage(self, enemigo):
        poder = self.fuerza * self.weapon_mult
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)

class BandidoEnemy(Enemigos):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, weapon_mult=1.2):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.weapon_mult = weapon_mult
        
    def damage(self, enemigo):
        poder = self.fuerza * self.weapon_mult
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)

class DemonioEnemy(Enemigos):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, wand_mult=1.5):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.wand_mult = wand_mult

    def damage(self, enemigo):
        # El demonio usa su alta inteligencia para calcular daño mágico
        poder = self.inteligencia * self.wand_mult
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)