import env
import random

game = env.Env()
game.render()

total_reward = 0
while True:
    possible_actions = list(game.possible_moves.keys())
    action = random.choice(possible_actions)
    print("Move: " + str(action))
    _, reward, done, _ = game.step(action)
    print("Move rewarded: " + str(reward))
    total_reward += reward
    game.render()
    if done:
        print("Game over.")
        break

print("Total reward: " + str(total_reward))
