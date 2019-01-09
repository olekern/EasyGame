
class Camera(object):
    def __init__(self, player):
        self.player = player
        self.x = 0
        self.y = 0
    
    def update(self):
        game = self.player.level.game
        self.x = self.player.x - game.SCREEN_WIDTH / 2
        self.y = self.player.y - game.SCREEN_HEIGHT / 2
        
        if self.x < 0:
            self.x = 0
        elif self.x > len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH:
            self.x = len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH
        
        if self.y > len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT:
            self.y = len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT