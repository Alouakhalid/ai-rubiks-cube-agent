class BaseExceptionGroup(BaseException):
    def __init__(self, message, exceptions):
        super().__init__(message, exceptions)
        self.message = message
        self.exceptions = tuple(exceptions)

    def derive(self, excs):
        return BaseExceptionGroup(self.message, excs)

    def subgroup(self, condition):
        matched = [e for e in self.exceptions if condition(e)]
        if matched:
            return self.derive(matched)
        return None

    def split(self, condition):
        matched = [e for e in self.exceptions if condition(e)]
        unmatched = [e for e in self.exceptions if not condition(e)]
        m = self.derive(matched) if matched else None
        u = self.derive(unmatched) if unmatched else None
        return (m, u)

    def __class_getitem__(cls, item):
        return cls


class ExceptionGroup(BaseExceptionGroup, Exception):
    pass
