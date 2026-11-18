class Habilidades:
    def __init__(self, nombre, tipo, coste, dmg_base):
        self.nombre = nombre
        self.tipo = tipo
        self.coste = coste
        self.dmg_base = dmg_base

    def descripcion(self):
        print(f"{self.nombre}: ")
        print("Tipo: ", self.tipo)
        print("Coste: ", self.coste)
        print("Daño base: ", self.dmg_base)

    def dmg_skill(self, caster):
        if self.tipo == "Magico":
            return caster.inteligencia * self.dmg_base
        elif self.tipo == "Fisico":
            return caster.fuerza * self.dmg_base
        return 0

    def dealed_skill(self, caster, enemigo):
        dano_calculado = self.dmg_skill(caster)
        if dano_calculado >= enemigo.defensa:
            return dano_calculado - enemigo.defensa
        else:
            return (dano_calculado - enemigo.defensa) - 1

    def skill_attack(self, caster, enemigo):
        if caster.estamina < self.coste:
            print(f"{caster.nombre} no tiene suficiente estamina.")
            return
        caster.estamina -= self.coste  
        dano_final = self.dealed_skill(caster, enemigo)
        enemigo.vida -= dano_final
        if enemigo.estavivo():
            print(f"{caster.nombre} ha usado {self.nombre} y ha realizado {dano_final} puntos de daño a {enemigo.nombre}")
        else:
            enemigo.morir()
