# from core import game

# app = game.Game()
# app.run()

from core import game
app = game.Game()
from elements.world import world
app.add_sprite(world.HexagonalWorld(app, app.screen, (5, 10, 0), (15, 15, 1), 1, app._file_manager))

app.run()