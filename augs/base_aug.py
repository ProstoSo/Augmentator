class BaseAug:

    def apply(self, text: str) -> str:
        raise NotImplementedError
