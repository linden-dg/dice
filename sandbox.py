from utils import plot, Attack
from utils.dice import d4, d12


varellion_main = Attack(hit=2*d4, number_of_attacks=2)
varellion_bonus = Attack(hit=d4)

varellion = (
    varellion_main.attack() + varellion_bonus.attack(),
    "Varellion"
)


aukhan = Attack(
    name="Aukhan",
    hit=d12,
    bonus_damage=2,
    number_of_attacks=2
)

plot(
    varellion,
    aukhan.plot(),
    mode='atMost'
)
