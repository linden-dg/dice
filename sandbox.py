from utils import plot, Attack
from utils.dice import d4, d6, d8, d12


varellion_main = Attack(hit=2*d4, number_of_attacks=2)
varellion_bonus = Attack(hit=d4)

varellion = (
    varellion_main.attack() + varellion_bonus.attack(),
    "Varellion Base"
)

aukhan = Attack(
    name="Aukhan Base",
    hit=d12,
    bonus_damage=2,
    number_of_attacks=2
)

eelfinn_main = Attack(hit=d8)
eelfinn_smite = Attack(hit=d8, crit=2*d8+4*d8)
eelfinn_bonus = Attack(hit=d6)

eelfin = (
    eelfinn_main.attack() + eelfinn_smite.attack() + eelfinn_bonus.attack(),
    "Eelfinn Base"
)

otis_main = Attack(hit=d6, number_of_attacks=2)
otis_pet = Attack(hit=2*d6)

otis = (
    otis_main.attack() + otis_pet.attack(),
    "Otis Base"
)

plot(
    varellion,
    aukhan.plot(),
    eelfin,
    otis,
    mode='atMost'
)
