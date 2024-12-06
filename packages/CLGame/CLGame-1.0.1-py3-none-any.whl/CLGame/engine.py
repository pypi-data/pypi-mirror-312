from time import sleep, time
from playsound import playsound
from pynput import keyboard
from os import system
from threading import Thread

class Screen():
    def __init__(self, width: int, height: int, title: str = "CLGame", border: bool = True, border_symbols: str = "┌─┐││└─┘", space_symbol: str = "`"):
        self.set_geometry(width, height)
        self.set_border(border)
        self.set_title(title)
        self.set_border_symbols(border_symbols)
        self.set_space_symbol(space_symbol)

    def print(self):
        system("cls||clear")
        if self.border:
            print(self.border_symbols[0] + self.title.ljust(self.width, self.border_symbols[1]) + self.border_symbols[2])
            print(*[self.border_symbols[3] + "".join(i) + self.border_symbols[4] for i in self.symbols], sep="\n")
            print(self.border_symbols[5] + self.border_symbols[6]*self.width + self.border_symbols[7])
        else:
            print(*["".join(i) for i in self.symbols], sep="\n")

    def draw_symbol(self, x: int, y: int, symbol: str):
        if 0 <= x <= self.width-1 and 0 <= y <= self.height-1:
            self.symbols[y][x] = symbol[0]

    def draw_sprite(self, x: int, y: int, sprite: str):
        sprite = sprite.split("\n")
        for i in range(len(sprite)):
            for j in range(len(sprite[i])):
                if sprite[i][j] != self.space_symbol:
                    self.draw_symbol(x+j, y+i, sprite[i][j])

    def draw_file(self, x: int, y: int, path: str):
        with open(path, mode="r") as file:
            sprite = file.read()
            self.draw_sprite(x, y, sprite)

    def clear(self):
        self.fill(" ")
                
    def fill(self, symbol: str):
        self.symbols = [[symbol[0]] * self.width for _ in range(self.height)]

    def set_geometry(self, width: int, height: int):
        self.width = width
        self.height = height
        self.clear()

    def set_title(self, title: str):
        self.title = title

    def set_border(self, border: bool):
        self.border = border

    def set_border_symbols(self, symbols: str):
        self.border_symbols = symbols

    def set_space_symbol(self, symbol: str):
        self.space_symbol = symbol

class Clock():
    def __init__(self, tps: float = 30):
        self.set_tps(tps)
        
        self.last_tick_time = time()
        
    def tick(self):
        self.processes_end_time = time()
        
        wait_time = self.tick_speed - (self.processes_end_time - self.last_tick_time)
        sleep(wait_time) if wait_time >= 0 else print("Overloading!")
        
        self.last_tick_time = time()

    def set_tps(self, tps: float):
        self.tps = tps
        self.tick_speed = 1 / tps

class Speaker():
    def play(self, path: str):
        playsound(path, False)

class Reader():
    def __init__(self):
        self.binds = {}
        self.listener = keyboard.Listener(on_press=self.key_press, on_release=lambda x: 0)
        self.listener.start()

    def key_press(self, key):
        try:
            if key.char in self.binds:
                self.binds[key.char]()
        except AttributeError:
            pass

    def bind(self, key: str, func):
        self.binds[key] = func

    def unbind(self, key: str):
        del self.binds[key]
