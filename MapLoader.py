import pygame
import json
from pygame.locals import *

# Har ansvar for å laste inn maps fra Tiled (json fil)
class MapLoader:
    # Tar inn en fil-plassering når man lager en MapLoader
    def __init__(self, path):
        with open(path, "r") as file:
            self.data = json.load(file)

    #Returnerer en liste over alle ID'ene som en 2D-liste i et spesifikt layer, fra filen man har lastet inn
    def getTiles(self, layerName):
        tiles = []
        layers = self.data["layers"]
        #Looper gjennom alle layer for å finne den som er ønsket fra parameteren til funksjonen
        for layer in layers:
            if layer["name"] == layerName:
                # Gjør om fra en 1D-liste til 2D
                self.width = int(layer["width"])
                tileData = layer["data"]
                numRows = len(tileData)//self.width
                for r in range(numRows):
                    row = []
                    for c in range(self.width):
                        row.append(tileData[r*self.width + c])
                    tiles.append(row)
                break
        return tiles
    
    # Søker gjennom filen for å finne om det er en "Spawn"-objekt som har posisjonen til der spilleren skal starte på Level'en
    def getPlayerSpawn(self):
        layers = self.data["layers"]
        for layer in layers:
            if layer["name"] == "Objects":
                for obj in layer["objects"]:
                    if obj["name"] == "spawn":
                        return [float(obj["x"]), float(obj["y"])]
        return [0.0, 0.0]
    
    # Søker gjennom filen for å finne om det er en "Goal"-objekt, som er et rektangel der mål er
    def getGoalRect(self):
        layers = self.data["layers"]
        for layer in layers:
            if layer["name"] == "Objects":
                for obj in layer["objects"]:
                    if obj["name"] == "goal":
                        x = int(obj["x"])
                        y = int(obj["y"])
                        width = int(obj["width"])
                        height = int(obj["height"])
                        return Rect(x, y, width, height)
        return Rect(100, 100, 300, 300)


