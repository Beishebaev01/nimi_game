from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        random_hero = choice(heroes)
        self.__defence = random_hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage


    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        coeff = randint(2, 6)  # 2,3,4,5
        boss.health -= coeff * self.damage
        print(f'Warrior {self.name} hit critically: {coeff * self.damage}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')
        self.__boost_amount = 5

    def apply_super_power(self, boss, heroes):
        global round_number
        if round_number <= 4:
            for hero in heroes:
                if hero.health > 0 and type(hero) != Witcher and type(hero) != Hacker:
                    hero.damage += self.__boost_amount
            print(f'Magic {self.name} boosted all heroes damage by {self.__boost_amount}')
        # else:
        #     for hero in heroes:
        #         if hero.health > 0:
        #             # TODO return initial value
        #             pass


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_AND_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted: {self.blocked_damage}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, "REVIVE")
        self.__has_revived = False

    def apply_super_power(self, boss, heroes):
        if self.health > 0 and not self.__has_revived:
            for hero in heroes:
                if hero.health <= 0:
                    hero.health = self.health
                    self.health = 0
                    self.__has_revived = True
                    print(f"Witcher {self.name} revived {hero.name} and sacrificed himself.")
                    break
                    
                    
class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, "HACK")
        self.__steal_amount = steal_amount

    def apply_super_power(self, boss, heroes):
        global round_number
        if round_number % 2 == 0 and boss.health > 0:
            alive_heroes = [hero for hero in heroes if hero.health > 0]
            if alive_heroes:
                target_hero = choice(alive_heroes)
                boss.health -= self.__steal_amount
                target_hero.health += self.__steal_amount
                print(f"Hacker {self.name} stole {self.__steal_amount} health from the boss and "
                      f"gave it to {target_hero.name}.")
                
                
class Spitfire(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, "AGGRESSION")

    def apply_super_power(self, boss, heroes):
        alive_before = sum(hero.health > 0 for hero in heroes)
        boss.attack(heroes)
        if sum(hero.health > 0 for hero in heroes) < alive_before:
            boss.health -= 80
            print(f"Spitfire {self.name} is furious! Deals 80 extra damage to the boss.")


class Bomber(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, "EXPLOSION")

    def apply_super_power(self, boss, heroes):
        if self.health < 0:
            boss.health -= 100
            print(f"Bomber {self.name} exploded! Deals 100 extra damage to the boss.")


round_number = 0


def show_statistics(boss, heroes):
    print(f'ROUND {round_number} ------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss('Dragon', 1000, 50)
    warrior_1 = Warrior('Prince', 280, 20)
    warrior_2 = Warrior('Kon', 270, 15)
    magic = Magic('Mag', 290, 15)
    berserk = Berserk('Mars', 260, 15)
    doc = Medic('Doc', 280, 5, 15)
    assistant = Medic('Junior', 300, 5, 5)
    witcher = Witcher('Geralt', 300, 0)
    hacker = Hacker('Jim', 300, 0, 10)
    spitfire = Spitfire('Blaze', 250, 5)
    bomber = Bomber('Bob', 250, 5)

    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, spitfire, bomber]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
