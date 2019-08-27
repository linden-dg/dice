from utils import single_attack
from utils.dice import d8

class Attack:
    def __init__(self, name="default attack", hit=d8, crit=-99, mod=4, prof=3, bonus_damage=0, number_of_attacks=1, include_dmg_mod=True):
        self.name = name
        self.hit = hit
        self.crit = 2 * hit if crit == -99 else crit
        self.mod = mod
        self.prof = prof
        self.bonus_damage = bonus_damage
        self.number_of_attacks = number_of_attacks
        self.include_dmg_mod = include_dmg_mod

    def values(self):
        return {
            "name": self.name,
            "damage": self.damage,
            "crit": self.crit,
            "mod": self.mod,
            "prof": self.prof,
            "bonus_damage": self.bonus_damage
        }

    def hit_damage(self):
        return self.hit + (self.mod if self.include_dmg_mod else 0) + self.bonus_damage

    def crit_damage(self):
        return self.crit + (self.mod if self.include_dmg_mod else 0) + self.bonus_damage

    def attack(self):
        return single_attack(
                hit=self.hit_damage(),
                crit=self.crit_damage(),
                mod=self.mod,
                prof=self.prof,
                ac=0
            ) * self.number_of_attacks

    def plot(self):
        return (
            self.attack(),
            self.name
        )