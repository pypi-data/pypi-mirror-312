class ParameterParsingErrorException(Exception):
    def __init__(self, parameterName, *args: object) -> None:
        self.parameterName = parameterName
        super().__init__(*args)

class ParameterNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ExpressionParsingErrorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ExecuteInstructionErrorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)