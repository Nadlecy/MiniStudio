import pygame, os, json
from pygame import Vector2 as vector

class Player:
    def __init__(self):
        self.position = vector(0,0)
        self.level = 0
        self.score = 0
        self.boosts = {
            "Speed":0
        }
        self.meta = {
            "time_played": 0
        }
        
    def display(self):
        print("Position: " + str(self.position) + "\nLevel: " + str(self.level) + "\nScore: " + str(self.score) + "\nBoosts: ", self.boosts, "\nTime played: " + str(self.meta["time_played"]))

plr = Player()

class SaveHandler:
    def __init__(self, name:str="Preview.json")->None:
        self.name = name
        self.path = os.path.join("saves/", self.name)
    
    def load(self)->None:
        if not os.path.exists(self.path):
            print("No file founded!")
            return
        
        with open(self.path, 'r') as f:
            data = json.load(f)
            plrData = data["player"]
            metaData = data["meta"]
            
        coords = plrData["position"].split(',')
        coords[0], coords[1] = float(coords[0]), float(coords[1])
        plr.position = vector(coords)
        plr.level = plrData["level"]
        plr.score = plrData["score"]
        plr.boosts = plrData["boosts"]
        plr.meta["time_played"] = metaData["time_played"]
        print("Successfully loaded!")
    
    def perform(self)->None:
        with open(self.path, 'w') as f:
            save = {
                "player": {
                    "position": str(plr.position.x) + ',' + str(plr.position.y),
                    "level": plr.level,
                    "score": plr.score,
                    "boosts": {}
                },
                "meta": plr.meta
            }
            
            for key, value in plr.boosts.items():
                save["player"]["boosts"][key] = value
            
            json.dump(save, f, indent=6)
            print("Successfully saved!")
            
save = SaveHandler()
save.load()
plr.display()