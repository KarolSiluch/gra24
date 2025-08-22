from engine.base_tile.modules.basic_modules import ModuleType, Module


class BaseTile:
    def __init__(self):
        self._modules: dict[ModuleType, Module] = {}

    @property
    def renderer(self):
        return self.get_module(ModuleType.Renderer)

    def update(self): ...

    def new_module(self, module_type, module, *atributes) -> Module:
        new_module: Module = module(self)
        self._modules[module_type] = new_module
        new_module.start(*atributes)
        return new_module

    def get_module(self, module_type: ModuleType):
        return self._modules.get(module_type)
