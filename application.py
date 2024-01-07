
import gymnasium as gym
import time
from trainenv.envs.train_station import TrainStation


# 经验池容量
capacity = 500 

# 折扣因子
discount_factor=0.8

# print(gym.envs.registry.keys())

env = gym.make("TrainStation-V1", render_mode="human")
env.reset()
# print(env.action_space.sample())
# action = env.action_space.sample()
# env.step(action)

# observation, info = env.reset()

for _ in range(10):
    time.sleep(1)
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, info = env.step(action)

    if terminated:
        observation, info = env.reset()

# env.close()
