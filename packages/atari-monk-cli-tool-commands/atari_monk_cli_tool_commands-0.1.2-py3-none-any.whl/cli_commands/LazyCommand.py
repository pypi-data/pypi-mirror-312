class LazyCommand:
    def __init__(self, command_cls):
        self.command_cls = command_cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.command_cls()
        return self._instance.run(*args, **kwargs)