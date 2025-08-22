class InputState:
    @classmethod
    def init(cls, states: set[str]):
        cls._actions = {key: False for key in states}
        cls._previous_actions = cls._actions.copy()

    @classmethod
    def update(cls):
        cls.previous_actions = cls._actions.copy()

    @classmethod
    def pressed(cls, action: str) -> bool:
        return cls._actions.get(action, False)

    @classmethod
    def just_pressed(cls, action: str) -> bool:
        return cls._actions.get(action, False) and not cls.previous_actions.get(action, False)

    @classmethod
    def set_action(cls, key: str, value: bool):
        cls._actions[key] = value
