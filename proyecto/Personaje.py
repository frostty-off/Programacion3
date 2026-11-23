from Habilidades import Habilidades

class Personaje:
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

    def damage(self, enemigo):
        if self.fuerza >= enemigo.defensa:
            return self.fuerza - enemigo.defensa
        else:
            return (self.fuerza - enemigo.defensa) * -1
    
    def atacar(self, enemigo):
        dealed = self.damage(enemigo)
        enemigo.vida = enemigo.vida - dealed
        if enemigo.estavivo():
            print(f"{self.nombre} ha realizado {dealed} de daño a {enemigo.nombre}")
        else:
            enemigo.morir()

class Warrior(Personaje):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, gaunlets):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.gaunlets = gaunlets
        self.habilidades.append(Habilidades("Corte Feroz", "Fisico", 10, 2.0))
        
    def atributos(self):
        super().atributos()
        print(f"- Guanteletes: {self.gaunlets}")
        
    def damage(self, enemigo):
        poder = self.fuerza * self.gaunlets
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)
            
class Magician(Personaje):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, wand):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.wand = wand
        self.habilidades.append(Habilidades("Bola de fuego", "Magico", 15, 1.5))

    def atributos(self):
        super().atributos()
        print(f"- Báculo: {self.wand}")
    
    def damage(self, enemigo):
        poder = self.inteligencia * self.wand
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)

class Paladin(Personaje):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, shield):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.shield = shield
        self.habilidades.append(Habilidades("Luz sagrada", "Magico", 20, 1.7))

    def atributos(self):
        super().atributos()
        print(f"- Escudo: {self.shield}")
        
    def damage(self, enemigo):
        poder = self.defensa * self.shield
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)
            
class Rogue(Personaje):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, knive):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.knive = knive
        self.habilidades.append(Habilidades("Ataque furtivo", "Fisico", 10, 2.2))

    def atributos(self):
        super().atributos()
        print(f"- Daga: {self.knive}")
        
    def damage(self, enemigo):
        # Corregido el error tipográfico de __fueza y kninve
        poder = self.fuerza * self.knive
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)                

class Knight(Personaje):
    def __init__(self, nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina, sword):
        super().__init__(nombre, profesion, raza, fuerza, defensa, inteligencia, vida, estamina)
        self.sword = sword
        self.habilidades.append(Habilidades("Cañon de bola", "Fisico", 10, 2.0))

    def atributos(self):
        super().atributos()
        print(f"- Espada: {self.sword}")
        
    def damage(self, enemigo):
        poder = self.fuerza * self.sword
        if poder >= enemigo.defensa:
            return int(poder - enemigo.defensa)
        else:
            return int((poder - enemigo.defensa) * -1)