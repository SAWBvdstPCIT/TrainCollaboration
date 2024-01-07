import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import time

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

        # 动作空间，地铁有两种动作 停车（0）、发车（1）
        # Discrete 离散动作，所有操作的可能
        self.action_space = spaces.Discrete(2)

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
    """
    env方法，下一步动作

    参数
        self    类自身
        action  行为

    返回值
        observation 环境
        reward      奖励
        terminated  是否达到结果（bool）
        truncated   时间限制（bool）
        info        调试信息（dict）
    """
    def step(self, action):
        
        if action == 1:
            print('action: 发车')
            self.is_departure = True
        else:
            print('action:', '不发车')
        self.render()
        if self.train.x <= 0:
            terminated = True
            # self.reset()
        else: 
            terminated = False
        
        reward = 1
        prinobservation = self._get_obs()
        observation = self._get_obs()
        self.render()

        return observation, reward, terminated, {}
    
    # env方法，重置环境
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # 地铁初始化
        self.train = pygame.Rect(self.window_width-200, 50, 200, 100)
        # 地铁行驶速度
        self.train_speed = 2

        # 站点初始化
        self.station_point = pygame.Vector2(70, 150)

        # 人员初始化
        self.human_position = pygame.Vector2(170, 200)
        # 人员行走速度
        self.human_speed = 0.3
        
        # 是否发车
        self.is_departure = False

        observation = self._get_obs()
        self.render()
        
        return observation

    def render(self):

        print("初始化")

        # pygame窗口初始化
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # pygame时钟初始化
        if self.clock is None:
            self.clock = pygame.time.Clock()

        # 画个火车站
        

        newHu = pygame.Vector2(170, 200)

        # 绘制一个人
        # pygame.draw.circle(
        #     self.window,
        #     (255, 0, 0),
        #     # self.human_position,
        #     newHu,
        #     10
        # )

        

        running = True
        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.close()

            self.window.fill("gray")

            pygame.draw.rect(
                self.window,
                (0, 178, 255),
                pygame.Rect(0, self.window_height-50, self.window_width, 50),
            )

            # 画个地铁
            pygame.draw.rect(
                self.window,
                (0, 255, 139),
                self.train
            )

            pygame.draw.circle(
                self.window,
                (255, 0, 0),
                # self.human_position,
                newHu,
                10
            )
            
            # 人员走到地铁口
            # if self.human_position.y > self.station_point.y+10:
            if newHu.y > self.station_point.y+10:
                # print(self.human_position.y, self.station_point.y+10)
                # self.human_position.y -= self.human_speed
                print(newHu.y, self.station_point.y+10)
                newHu.y -= self.human_speed
                if self.is_departure:
                    self.train.x -= self.train_speed
            else :
                running = False
            self.clock.tick(self.metadata["render_fps"])
            # 刷新屏幕显示
            pygame.display.flip()
            

        # 如果已发车则等待
        # if self.is_departure:
        #     # 人员等待地铁进站
        #     while self.train.x >= self.station_point.x:
        #         self.train.x -= self.train_speed

        #     # 人员进入地铁
        #     if self.human_position.y > self.station_point.y:
        #         self.human_position.y -= 15

        #     while self.train.x > 0:
        #         self.train.x -= self.train_speed        

        # 乘客等待上车，待优化
        # if train.x > 0 :
        #     if train.x > 70:
        #         train.x -= 10
        #     elif train.x == 70:
        #         if human_position.y > 100:
        #             human_position.y -= 10
        #         else:
        #             train.x -= 10
        #     else:
        #         train.x -= 10
        #         human_position.x -= 10

        # 渲染速率
        # self.clock.tick(self.metadata["render_fps"])

        # 刷新屏幕显示
        # pygame.display.flip()
                
        
                
        

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