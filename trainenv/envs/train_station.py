import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

# author: llzhang
# 括号内表示继承了gym的env类
class TrainStation(gym.Env):

    # 构造函数，self相当于this
    def __init__(self, render_mode="human"):
        self.size = 5

        # 图形化窗口大小
        self.window_width = 500
        self.window_height = 300    
        
        # 观测者空间，有效观测值
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, self.size, shape=(2,), dtype=int),
                "target": spaces.Box(0, self.size, shape=(2,), dtype=int)
            }
        )

        # 动作空间，地铁有三种动作 停车、等待、发车
        self.action_space = spaces.Discrete(3)

        # 检测render_mode是否有效
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # 如果使用人工渲染，使用window
        self.window = None

        # 可使用时钟确保正确帧率
        self.clock = None
    
    # gym元数据 render_modes-human表示连续渲染，rgb_array表示将画面内容转为rgb数组（截图）
    metadata = {"render_modes": "human", "render_fps": 60}


    # env方法，下一步动作
    def step(self, action):
        terminated = 0
        reward = 1
        prinobservation = self._get_obs()
        observation = self._get_obs()
        self.render()

        return observation, reward, terminated, {}
    
    # env方法，重置环境
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        observation = self._get_obs()
        self.render()
        
        return observation

    def render(self):

        # pygame窗口初始化
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        # pygame时钟初始化
        if self.clock is None:
            self.clock = pygame.time.Clock()

        # 绘制白色背景
        canvas = pygame.Surface((self.window_width, self.window_height))
        canvas.fill((255, 255, 255))

        # 画个火车站
        pygame.draw.rect(
            canvas,
            (0, 178, 255),
            pygame.Rect(0, self.window_height-50, self.window_width, 50),
        )

        # 画个地铁
        pygame.draw.rect(
            canvas,
            (0, 255, 139),
            pygame.Rect((self.window_width/2)-100, (self.window_height/2)-50, 200, 100),
        )

        # 绘制一个人
        pygame.draw.circle(
            canvas,
            (255, 0, 0),
            (70, 70),
            10,
            10
        )

        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        # 渲染速率
        self.clock.tick(self.metadata["render_fps"])

    # env方法，退出环境
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
        

    # 获取观测信息
    def _get_obs(self):
        return {"agent": 1, "target": 2}
    

    # def _get_info(self):
    #     return {
    #         "distance": np.linalg.norm(
    #             self._agent_location
    #         )
    #     }