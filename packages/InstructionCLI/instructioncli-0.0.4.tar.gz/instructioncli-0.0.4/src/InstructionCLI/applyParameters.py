from typing import Type
from .config import CliConfiguration
from .exception import ParameterNotFoundException

def applyParameters(parametersDict : dict[str, str], configurationClass : Type):
    """
    Присваивает полученные параметры, сопоставляя с атрибутами конфигурационного класса.

    Args:
        parametersDict (dict): Новые значения атрибутов, полученные из командной строки
        configurationClass (Type): Конфигурационный класс
    """

    from .applyParameter import applyParameter

    for parameter in parametersDict:
        isFind = False
        for configPar in configurationClass.__dict__:
            if configPar.lower() == parameter.lower():
                isFind = True
                value = applyParameter(parametersDict, parameter, getattr(configurationClass, configPar))
                setattr(configurationClass, configPar, value)

        if not isFind and CliConfiguration.RAISE_EXCEPTION_IF_UNKNOWN_PARAMETER:
            raise ParameterNotFoundException("Неизвестный параметр: " + str(parameter))   
