from gymnasium.envs.registration import register

register(
    id="TrainStation-V1",
    entry_point="trainenv.envs:TrainStation",
)
