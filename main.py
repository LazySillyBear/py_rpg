from classes.characters import Person
from classes.game import bcolors, gui
from classes.magic import Spell
from classes.inventory import Item
import random


# TODO Add AI to NPCs
# TODO Add Shop where you can buy/sell items. Shop has it's own inventory that gets expanded with stuff you sell
# TODO Move spells into own file
# TODO Add character classes with different attributes
# TODO Add Spellbook (own file)
# TODO Add class trainers where you can learn new spells depending on your class
# TODO Refactor main.py so it's just runs the game
# TODO Add title screen with "Play", "Help" and "Quit" options
# TODO import sys and os for clearing screen
# TODO fix bug with names

# Spell library
# Damage
fire = Spell("Fire", 10, 100, "Fire", "black")
thunder = Spell("Thunder", 12, 124, "Lightning", "black")
blizzard = Spell("Blizzard", 10, 100, "Frost", "black")
meteor = Spell("Meteor", 10, 100, "Fire", "black")
quake = Spell("Quake", 14, 140, "Earth", "black")

# Heal
cure = Spell("Cure", 12, 120, "Light", "white")
cura = Spell("Cura", 18, 200, "Light", "white")

# Item Stock
# Healing-Items
potion = Item("Potion", "potion", "Heals 50HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 999)
megaelixir = Item("Mega Elixir", "elixir", "Fully restores HP/MP of all party members", 999)

# Attack-Items
bomb = Item("Bomb", "attack", "A throwable bomb. BIG BOOM", 500)
knife = Item("Throwing Knife", "attack", "A small throwing knife.", 50)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "qty": 15}, {"item": hipotion, "qty": 5},
                {"item": superpotion, "qty": 5}, {"item": elixir, "qty": 5},
                {"item": megaelixir, "qty": 2}, {"item": bomb, "qty": 2},
                {"item": knife, "qty": 20}]
player_name = "Dan"
party_name = ["Healer", "Druid"]

# Player & Enemies
player1 = Person("Dan:     ", 1460, 165, 60, 34, player_spells, player_items)
player2 = Person("Priest:  ", 1250, 499, 15, 34, player_spells, player_items)
player3 = Person("Druid:   ", 1600, 250, 60, 85, player_spells, player_items)

players = [player1, player2, player3]

enemy = Person("Goblin:  ", 1200, 65, 45, 25, [], [])

enemies = [enemy]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print(gui.separatorA)

    print("\n")
    print(bcolors.BOLD + "NAME                  HP                                 MP")
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()


    for player in players:
        player.choose_action()
        choice = input("\nChoose action:    ")
        index = int(choice) - 1

        print("You chose", choice + "\n")

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            if enemy.hp is 0:
                print("\nYou have attacked for", dmg, "and killed", enemy.name, "!")
                break
            else:
                print("\nYou attacked for", dmg, "points of damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:    ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don't have enough MP!" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                if enemy.hp is 0:
                    print(bcolors.OKBLUE + "You deal", magic_dmg, "damage with", spell.name, "and killed", enemy.name, "!" + bcolors.ENDC)
                    break
                else:
                    print(bcolors.OKBLUE + "You deal", magic_dmg, "damage with", spell.name + bcolors.ENDC)

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose item:    ")) - 1

            if item_choice == -1:
                continue

            item = player_items[item_choice]["item"]
            player.items[item_choice]["qty"] -= 1
            if player.items[item_choice]["qty"] == 0:
                del player.items[item_choice]

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop) + "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restored" + " HP and MP of your party" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restored" + "HP and MP" + bcolors.ENDC)
            elif item.type == "attack":
                item_dmg = item.generate_damage()
                enemy.take_damage(item_dmg)
                if enemy.hp is 0:
                    print(bcolors.OKGREEN + "\n" + item.name + " deals", item_dmg, "damage and kills", enemy.name + "!" + bcolors.ENDC)
                    break
                else:
                    print(bcolors.OKGREEN + "\n" + item.name + " deals", item_dmg, "damage" + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player1.get_hp() == 0:
        print(bcolors.FAIL + "You died!" + bcolors.ENDC)
        running = False
    else:
        enemy_choice = 1
        target = random.randrange(0, 3)
        enemy_dmg = enemy.generate_damage()
        players[target].take_damage(enemy_dmg)
        print(enemy.name + " attacks", players[target].name, "for", enemy_dmg, "points of damage.")
