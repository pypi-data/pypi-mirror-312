import sys

from .exception import ExecuteInstructionErrorException


class Instruction:
    def template(self, expression : str) -> bool:
        """
        Шаблон инструкции.

        По этому шаблону определяется корректность ввода инструкции.

        Args:
        expression(str): будет содержать проверяемую инструкцию.

        Returns:
        bool: Если True, то выражение в "expression" корректно.
        """
        return True

    def isRequired(self) -> bool:
        """
        Обязательно ли должна быть выполнена инструкция. 
        
        Returns:
        bool: Если True, то будет выдана ошибка "Ожидалась инструкция, но был обнаружен конец строки.")
        """
        return True

    def failedInstruction(self, expression : str) -> str:
        """
        Возвращает сообщение о некорректности инструкции.

        Если все итерации с "template()" вернули "False", то вызовется этот метод.

        Args:
        expression(str): будет содержать саму некорректную инструкцию.

        Returns:
        None
        """
        return f"Некорректная инструкция \"{expression}\""

    def applyParameters(self, parameters: dict) -> bool:
        """
        Применить параметры.

        Выполняется до doInstruction().

        Args:
        parameters(dict): будет содержать все параметры после введенной инструкции. Параметрам считается слово похожее на "--mypar" или "--someParWithValue=123"
        
        Returns:
        None
        """
        print(f"{self.__class__.__name__}.applyParameters: {parameters}")
        return True

    def doInstruction(self, expression) -> bool:
        """
        Выполнение инструкции.

        Args:
        expression(str): содержит инструкцию введенную пользователем.

        Returns:
        None
        """
        print(f"{self.__class__.__name__}.doInstruction: {expression}")
        return True

    def nextInstruction(self):
        """
        Следующая инструкция.

        После выполнении инструкции, можно передать следующую. Если это последняя инструкция, то обязательно нужно вернуть "NoInstruction()"

        Returns:
        Instruction: Следующая инструкция.
        """
        return NoInstruction()

    def throwError(self, message : str):
        """
        Выводит текст ошибки
        Args:
            message (str): текст ошибки

        Raises:
            ExecuteInstructionErrorException: Ошибка обработки инструкции
        """
        raise ExecuteInstructionErrorException(message)


class NoInstruction(Instruction):
    """
    Последняя инструкция в цепочки инструкций.

    Используйте это, если далее инструкций больше не последует. 
    """
    def isRequired(self) -> bool:
        return False

    def applyParameters(self, parameters: dict):
        pass

    def doInstruction(self, expression):
        sys.exit()
