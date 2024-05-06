import random as r


def dice_roller(nbr, die, mod, adv=False, dis=False) -> int:
    sum = mod
    fumble = False
    crit = False
    for i in range(nbr):
        d = r.randint(1, die)
        if nbr == 1 and (adv or dis):
            dd = r.randint(1, die)
            if adv:
                if dd > d:
                    d = dd
            elif dis:
                if dd < d:
                    d = dd
        sum += d
        if d == 1:
            fumble = True
        elif d == die:
            crit = True
    return sum, fumble, crit


class Weapon():
    def __init__(self, num, die, ranged=False, d_type='S') -> None:
        self.num = num
        self.die = die
        self.ranged = ranged
        self.type = d_type
        self.light = False
        self.finesse = False


class Character():
    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, HP, AC, saves, proficiency, weapon=Weapon(1, 6)) -> None:
        self.name = name
        self.Str = strength
        self.Dex = dexterity
        self.Con = constitution
        self.Int = intelligence
        self.Wis = wisdom
        self.Cha = charisma
        self.HP = HP
        self.MaxHP = HP
        self.AC = AC
        self.prof = proficiency
        self.saves_profs = saves
        self.weapon = weapon
        self.initiative = 0

    def roll_save(self, save):
        d, f, c = dice_roller(1, 20, 0)
        if save == 'str':
            d += self.Str
        elif save == 'dex':
            d += self.Dex
        elif save == 'con':
            d += self.Con
        elif save == 'int':
            d += self.Int
        elif save == 'wis':
            d += self.Wis
        elif save == 'cha':
            d += self.Cha
        if save in self.saves_profs:
            d += self.prof
        return d, f, c

    def roll_initiative(self):
        d, c, f = dice_roller(1, 20, self.Dex)
        self.initiative = d
        return d

    def take_damage(self, amount):
        self.HP -= amount
        return self.HP

    def reset(self):
        self.HP = self.MaxHP
        self.initiative = 0

    def attack(self):
        mod = self.Str + self.prof
        res = []
        for i in range(1):
            res.append(list(dice_roller(1, 20, mod)))

            if res[-1][2]:
                dam, _, _ = dice_roller(2 * self.weapon.num,
                                        self.weapon.die, self.Str)
            elif res[-1][1]:
                dam = 0
            else:
                dam, _, _ = dice_roller(
                    self.weapon.num, self.weapon.die, self.Str)
            res[-1].append(dam)

        return res


class Fighter(Character):
    def attack(self):
        mod = self.Str + self.prof + 2
        res = []
        for i in range(2):
            res.append(list(dice_roller(1, 20, mod)))

            if res[-1][2]:
                dam, _, _ = dice_roller(2 * self.weapon.num,
                                        self.weapon.die, self.Str)
            elif res[-1][1]:
                dam = 0
            else:
                dam, _, _ = dice_roller(
                    self.weapon.num, self.weapon.die, self.Str)
            res[-1].append(dam)

        return res


class Barbarian(Character):
    def attack(self):
        mod = self.Str + self.prof
        res = []
        for i in range(2):
            res.append(list(dice_roller(1, 20, mod)))

            if res[-1][2]:
                dam, _, _ = dice_roller(2 * self.weapon.num,
                                        self.weapon.die, self.Str + 2)
            elif res[-1][1]:
                dam = 0
            else:
                dam, _, _ = dice_roller(
                    self.weapon.num, self.weapon.die, self.Str + 2)
            res[-1].append(dam)

        return res


def select_target(attacker, sideA, sideB, everyone):
    if attacker in sideA:
        enemy = sideB
    else:
        enemy = sideA
    s_enemy = set(enemy)
    s_everyone = set(everyone)
    inter = s_enemy.intersection(s_everyone)
    return r.choice(list(inter))


def check_victory(sideA, sideB, everyone):
    a_in = False
    b_in = False
    for a in sideA:
        if a in everyone:
            a_in = True
    for b in sideB:
        if b in everyone:
            b_in = True
    if a_in and b_in:
        return None
    if a_in:
        return 'A'
    else:
        return 'B'


if __name__ == "__main__":
    longsword = Weapon(1, 10)
    greatAxe = Weapon(1, 12)
    stats = {'A': 0, 'B': 0}
    pekka = Fighter('pekka', 3, 2, 0, 0, 0, 0, 25,
                    16, ['str', 'con'], 2, longsword)
    kalle = Barbarian('kalle', 4, 0, 0, 0, 0, 0, 30,
                      14, ['str', 'con'], 2, greatAxe)

    sideA = [pekka, kalle]

    sideB = []
    for i in range(8):
        g = Character(f'Gob {i}', 2, 2, 0, 0, -1, -1, 7, 15, [], 2)
        sideB.append(g)

    for j in range(1):
        everyone = sideA + sideB
        for c in everyone:
            c.reset()
            i = c.roll_initiative()
        everyone.sort(key=lambda item: item.initiative)

        while True:
            victory_achieved = False
            for cha in everyone:
                target = select_target(cha, sideA, sideB, everyone)
                attacks = cha.attack()
                # print(f'{cha.name} attacks {target.name}')
                for attack in attacks:
                    if target not in everyone:
                        break
                    if attack[2]:
                        # print(f'CRIT for {attack[3]} damage')
                        target.take_damage(attack[3])
                    elif attack[1]:
                        # print('MISS')
                        pass
                    else:
                        if attack[0] >= target.AC:
                            # print(
                            #     f'attack roll of {attack[0]} hits against AC {target.AC} for {attack[3]} damage')
                            target.take_damage(attack[3])
                        else:
                            # print(
                            #    f'attack roll of {attack[0]} misses against AC {target.AC}')
                            pass
                    if target.HP <= 0:
                        # print(f'{target.name} died')
                        everyone.remove(target)
                        ch = check_victory(sideA, sideB, everyone)
                        if ch is not None:
                            stats[ch] += 1
                            victory_achieved = True
                    if victory_achieved:
                        break
                if victory_achieved:
                    break
            if victory_achieved:
                break
    print(stats)
