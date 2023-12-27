
import gymnasium as gym
from gym_examples.envs.grid_world import GridWorldEnv


# 经验池容量
capacity = 500 

# 折扣因子
discount_factor=0.8

print(gym.envs.registry.keys())

env = gym.make("TrainStation-V1", render_mode="human")
env.reset()
action = env.action_space.sample()
env.step(action)

# observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, info = env.step(action)

#     if terminated or truncated:
#         observation, info = env.reset()

# env.close()
