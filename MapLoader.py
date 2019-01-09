import pygame
import json
from pygame.locals import *

class MapLoader:
    def __init__(self, path):
        with open(path, "r") as file:
            self.data = json.load(file)

    def getTiles(self, layerName):
        tiles = []
        layers = self.data["layers"]
        for layer in layers:
            if layer["name"] == layerName:
                width = int(layer["width"])
                tileData = layer["data"]
                numRows = len(tileData)//width
                for r in range(numRows):
                    row = []
                    for c in range(width):
                        row.append(tileData[r*width + c])
                    tiles.append(row)
                break
        return tiles
    
    def getPlayerSpawn(self):
        layers = self.data["layers"]
        for layer in layers:
            if layer["name"] == "Objects":
                for obj in layer["objects"]:
                    if obj["name"] == "spawn":
                        return [float(obj["x"]), float(obj["y"])]
        return [0.0, 0.0]
    
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