
import tkinter as tk
from tkinter import ttk
import random
import time
import math


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
    return d1 + d2 + d3


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

    def __str__(self):
        return f"{self.name}, Atk={self.attack}, Def={self.defense}, Loc=[{self.location}]"

    def randomize(self):
        self.attack.set(roll3d6())
        self.defense.set(roll3d6())
        self.armor.set(roll3d6())
        self.power.set(roll3d6())
        self.speed.set(roll3d6())
        self.range.set(roll3d6())
        self.location = Location()
        self.location.randomize()
    

class PlayerAttribute:
    def __init__(self, name, cv=0, bv=0):
        self.name = name
        self.current_value = cv
        self.base_value = bv

    def set(self, base_value):
        self.base_value = base_value
        self.current_value = base_value

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


class BattleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("battle 2.0")
        self.create_widgets()
        self.players = []
        
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
        self.players.append(Player(name))
        self.text.config(state='normal')
        self.text.insert(tk.END, f"{name}\n")
        self.text.see(tk.END)
        self.text.config(state='disabled')
        self.update_status(f"New belligerent {name}, created")
        
    def randomize(self):
        self.update_status("Randomizing the players attributes...")
        for player in self.players:
            player.randomize()
        
    def runsim(self):
        self.update_status("Running simulation...")
        self.text.config(state='normal')
        for player in self.players:
            self.text.insert(tk.END, f"{player}\n")
            self.text.see(tk.END)
        self.text.config(state='disabled')

    def update_status(self, message):
        self.status.config(text=message)
        self.root.after(3000, lambda: self.status.config(text="Ready"))

    def new_game(self):
        self.players = []
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.config(state='disabled')
        self.update_status("New simulation created")


def main():
    random.seed(time.time())
    root = tk.Tk()
    app = BattleWindow(root)
    root.geometry("1024x768")
    root.mainloop()

if __name__ == "__main__":
    main()
