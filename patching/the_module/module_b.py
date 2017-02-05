from .module_a import ModuleA


class ModuleB(object):
    def __init__(self, value):
        self.a = ModuleA(value)
