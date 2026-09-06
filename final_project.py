import random
import csv

class Character:
    def __init__(self, name: str, health: int = 100, level: int = 1, experience: int = 0, max_health: int = 100):
        self.name = name
        self.level = level
        self.experience = experience
        self.max_health = max_health
        self.health = min(health, self.max_health)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.experience -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to {self.level}!")

    def is_alive(self):
        return self.health > 0

    def reset_health(self):
        self.health = self.max_health

    def __str__(self):
        return f"{self.name} has {self.health}/{self.max_health} HP, Level {self.level}, Experience {self.experience}"


class Warrior(Character):
    def __init__(self, name: str, health: int = 120, level: int = 1, experience: int = 0):
        super().__init__(name, health, level, experience, max_health=120)
        self.buff = 0  # one turn buff

    def take_damage(self, amount):
        self.battle_cry()
        reduced_damage = int(amount * 0.9)
        super().take_damage(reduced_damage)
        if self.buff > 0:
            self.health = max(0, self.health - self.buff)
            self.buff = 0  # clean buff

    def battle_cry(self):
        heal_amount = int(self.health * 0.1)
        self.buff = heal_amount
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"{self.name} used Battle Cry and temporarily healed {heal_amount} HP!")


class Mage(Character):
    def __init__(self, name: str, health: int = 80, level: int = 1, experience: int = 0):
        super().__init__(name, health, level, experience, max_health=80)

    def cast_spell(self, target: Character, damage: int):
        target.take_damage(damage)
        print(f"{self.name} cast a spell on {target.name} for {damage} damage!")

    def gain_experience(self, amount):
        extra = int(amount * 0.15)
        super().gain_experience(amount + extra)


class Archer(Character):
    def __init__(self, name: str, health: int = 100, level: int = 1, experience: int = 0):
        super().__init__(name, health, level, experience, max_health=100)

    def take_damage(self, amount):
        if random.randint(1, 10) == 1:
            print(f"{self.name} dodged the attack!")
        else:
            super().take_damage(amount)

    def rapid_shot(self, target: Character, damage: int):
        if random.randint(1, 10) <= 2:
            print(f"{self.name} used Rapid Shot successfully!")
            target.take_damage(damage * 2)
        else:
            print(f"{self.name} used Rapid Shot successfully.")
            target.take_damage(damage)

# add character
characters = {}
with open("/Users/zhilingchen/Desktop/MTH3300/final_project/characters.csv", "r") as f:
    reader = csv.DictReader(f)
    classes = {"Warrior": Warrior, "Mage": Mage, "Archer": Archer}
    for row in reader:
        name = row["name"]
        health = int(row["health"])
        level = int(row["level"])
        experience = int(row["experience"])
        char_class = row["class"]
        if char_class in classes:
            characters[name] = classes[char_class](name, health, level, experience)

# add battle
with open("/Users/zhilingchen/Desktop/MTH3300/final_project/battle.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        attacker_name = row["attacker"]
        defender_name = row["defender"]
        damage = int(row["damage"])

        if attacker_name not in characters or defender_name not in characters:
            continue

        attacker = characters[attacker_name]
        defender = characters[defender_name]

        if not attacker.is_alive():
            continue

        if isinstance(attacker, Archer):
            attacker.rapid_shot(defender, damage)
        elif isinstance(attacker, Mage):
            attacker.cast_spell(defender, damage)
        else:
            defender.take_damage(damage)

        if not defender.is_alive():
            print(f"{defender.name} has been defeated!")
            defender.reset_health()  # reset HP after dying
            attacker.gain_experience(50)
            defender.experience = max(0, defender.experience - 30)

# final result
final_result = sorted(characters.values(), key=lambda c: (-c.level, c.name))

print("\n--- Final Character States ---\n")
for c in final_result:
    print(f"{c.name}, Health: {c.health}, Level: {c.level}, Experience: {c.experience}")