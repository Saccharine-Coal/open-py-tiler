from core import game
from core.world import world


app = game.Game(False)
app.add_sprite(world.WorldQRSZ((1, 1, 1)))
app.run()
