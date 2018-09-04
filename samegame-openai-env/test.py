import env

game = env.Env()

while True:
  _, reward, done, _ = game.step((0, 1))
  game.render()
  break