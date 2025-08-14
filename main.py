
import tkinter as tk
from tkinter import ttk
import sys
import random
import time
import math
import logging


MAXTURNS = 256


def get_random_name():
    with open('resources/names.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        names = content.split()
        name = random.choice(names)
        return name


def roll3d6():
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    d3 = random.randint(1, 6)
    # logging.debug(f"roll 3d6 = {d1} {d2} {d3}")
    return d1 + d2 + d3


def roll1d8():
    d1 = random.randint(1, 8)
    return d1


def roll1d20():
    d1 = random.randint(1, 20)
    return d1


class Player:
    def __init__(self, name):
        self.name = name
        self.attack = PlayerAttribute("Attack")
        self.defense = PlayerAttribute("Defense")
        self.armor = PlayerAttribute("Armor")
        self.power = PlayerAttribute("Power")
        self.speed = PlayerAttribute("Speed")
        self.range = PlayerAttribute("Range")
        self.location = Location()

    def __str__(self):
        return f"{self.name}, Atk={self.attack}, Def={self.defense}, Loc=[{self.location}], Arm={self.armor}"

    def randomize(self):
        self.attack.set(roll3d6())
        self.defense.set(roll3d6())
        self.armor.set(roll3d6())
        self.power.set(roll3d6())
        self.speed.set(roll3d6())
        self.range.set(roll3d6())
        self.location.randomize()
        logging.debug(f"{self.name}=[{self.attack} {self.defense} {self.armor} {self.power} {self.speed} {self.range} @({self.location})]")

    def moveTowards(self, location):
        # Calculate direction vector (dx, dy)
        dx = location.x - self.location.x
        dy = location.y = self.location.y

        # Calculate distance between points
        distance = math.hypot(dx, dy)

        # If already at (or very close to) the target, return target
        if distance <= self.speed.current_value:
            return

        # Normalize direction vector and scale by speed
        dx_normalized = dx / distance
        dy_normalized = dy / distance
    
        # Calculate new position
        new_x = self.location.x + dx_normalized * self.speed.current_value
        new_y = self.location.y + dy_normalized * self.speed.current_value
        self.location.x = new_x
        self.location.y = new_y
        logging.debug(f"{self.name} moved {self.location}")

    def isWithinRangeForAttack(self, target):
        range = self.location.distance(target.location)
        return range <= self.range.current_value

    def attackTarget(self, target):
        roll = roll1d20()
        if (self.attack.bonus() + roll) >= target.defense.current_value:
            # we have a hit!
            return True
        return False

    def damage(self, target):
        damage_inflicted = roll1d8() + self.power.bonus()
        target.armor.current_value -= damage_inflicted
        return damage_inflicted

    def is_dead(self):
        if self.armor.current_value < 1:
            return True
        return False


class PlayerAttribute:
    def __init__(self, name, cv=0, bv=0):
        self.name = name
        self.current_value = cv
        self.base_value = bv

    def set(self, base_value):
        self.base_value = base_value
        self.current_value = base_value

    def bonus(self):
        bv = int((self.current_value -10.5)/2.0)
        return bv

    def __str__(self):
        return f"{self.current_value}"


class Location:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, source):
        dx = self.x - source.x
        dy = self.y - source.y
        dz = self.z - source.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def randomize(self):
        self.x = float(roll3d6() + roll3d6() + roll3d6())
        self.y = float(roll3d6() + roll3d6() + roll3d6())
        self.z = 0.0

    def __str__(self):
        return f"x{self.x}, y{self.y}"


class Game:
    def __init__(self):
        self.turns = 0
        self.players = []

    def getNearestEnemy(self, source):
        min_dist = sys.float_info.max
        target = None
        for player in self.players:
            if source.name != player.name:
                distance = player.location.distance(source.location)
                if distance < min_dist:
                    target = player
                    min_dist = distance
        return target


class BattleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("battle 2.0")
        self.create_widgets()
        self.game = Game()
        
    def create_widgets(self):
        # Create toolbar with 3 buttons
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Toolbar buttons
        self.add_btn = ttk.Button(toolbar, text="Add Player", command=self.add_player)
        self.add_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.rand_btn = ttk.Button(toolbar, text="Randomize", command=self.randomize)
        self.rand_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.run_btn = ttk.Button(toolbar, text="Run!", command=self.runsim)
        self.run_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.new_btn = ttk.Button(toolbar, text="New Game", command=self.new_game)
        self.new_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        
        # Text widget in the center (with scrollbar)
        text_frame = tk.Frame(self.root)
        text_frame.pack(expand=True, fill=tk.BOTH)
        
        self.text = tk.Text(text_frame, wrap=tk.WORD, state="disabled",
            bg='black',        # Background color (white)
            fg='white',       # Foreground (text) color (black)
            insertbackground='white',  # Cursor color
            selectbackground='gray',   # Selection background
            selectforeground='white'   # Selection text color
        )
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar at the bottom
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def add_player(self):
        name = get_random_name()
        self.game.players.append(Player(name))
        self.console_write(f"{name}\n")
        self.update_status(f"New belligerent {name}, created")
        
    def randomize(self):
        self.update_status("Randomizing the players attributes...")
        for player in self.game.players:
            player.randomize()
        
    def runsim(self):
        self.update_status("Running simulation...")
        self.text.config(state='normal')
        while len(self.game.players) > 1:
            self.game.turns += 1
            logging.info(f"Turn {self.game.turns}")
            self.console_write(f"Turn {self.game.turns}\n")
            if self.game.turns > MAXTURNS:
                logging.warn(f"Battle is taking too many turns: {self.game.turns}")
                break
            for player in self.game.players:
                self.console_write(f"{player}\n")
                self.text.see(tk.END)
                target = self.game.getNearestEnemy(player)
                logging.info(f"{player.name} targets {target.name}")
                if player.isWithinRangeForAttack(target):
                    logging.info(f"{player.name} attacks {target.name}")
                    if player.attackTarget(target):
                        logging.info(f"{player.name} hits {target}")
                        dam = player.damage(target)
                        logging.info(f"{dam} points of damage")
                        if target.is_dead():
                            logging.info(f"{player.name} defeated {target}!")
                            self.game.players.remove(target)
                    else:
                        logging.info(f"{player.name} missed {target.name}")
                else:
                    logging.info(f"{player.name} moves towards {target.name}")
                    player.moveTowards(target.location)
        self.console_write(f"game ended in {self.game.turns} turns\n")
        self.console_write(f"winner is {self.game.players[0]}")
        logging.info(f"winner is {self.game.players[0]}")


    def update_status(self, message):
        logging.info(message)
        self.status.config(text=message)
        self.root.after(3000, lambda: self.status.config(text="Ready"))

    def new_game(self):
        self.game = Game()
        self.console_clear()
        self.console_write("new game\n")
        self.update_status("New simulation created")

    def console_write(self, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, message)
        self.text.see(tk.END)
        self.text.config(state='disabled')

    def console_clear(self):
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.config(state='disabled')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]  # Log to console
    )
    logging.info("battle/2.1.0")
    random.seed(time.time())
    root = tk.Tk()
    app = BattleWindow(root)
    root.geometry("1024x768")
    root.mainloop()

if __name__ == "__main__":
    main()
