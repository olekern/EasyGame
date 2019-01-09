

# Kamera objektet som følger spilleren i verden
class Camera:
    def __init__(self, player):
        self.player = player
        self.x = 0
        self.y = 0
    
    # Hvert bilde oppdaterer posisjonen til kamera seg til der spilleren befinner seg
    def update(self):
        game = self.player.level.game
        self.x = self.player.x - game.SCREEN_WIDTH / 2
        self.y = self.player.y - game.SCREEN_HEIGHT / 2
        
        # Disse neste linjene passer på at kameraet ikke flytter seg forbi kanten av kartet
        if self.x < 0:
            self.x = 0
        elif self.x > len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH:
            self.x = len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH
        
        if self.y > len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT:
            self.y = len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT

