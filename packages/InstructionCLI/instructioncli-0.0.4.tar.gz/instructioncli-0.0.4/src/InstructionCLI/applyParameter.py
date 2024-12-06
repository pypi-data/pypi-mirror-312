from .config import CliConfiguration
from .exception import ParameterNotFoundException, ParameterParsingErrorException


def to_bool(value) -> bool:
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Недопустимое значение для приведения к типу bool: ' + str(value))

def to_int(value) -> int:
    if str(value).lower() in ("yes", "y", "true",  "t"): return 1
    if str(value).lower() in ("no",  "n", "false", "f", "none", "[]", "{}"): return 0
    try:
        return int(value)
    except:
        raise Exception('Недопустимое значение для приведения к типу int: ' + str(value))


def applyParameter(parametersDict: dict[str, str], parameterName: str, getVariable : any): 
    try:
        parameterName = parameterName.lower()
        isFind = False
        for key in parametersDict.keys():
            if key.lower() == parameterName:
                isFind = True
                value = parametersDict[key]

                if isinstance(getVariable, bool):
                        return to_bool(value)
                elif isinstance(getVariable, int):
                    return to_int(value)
                else:
                    return value
                
        if not isFind and CliConfiguration.RAISE_EXCEPTION_IF_UNKNOWN_PARAMETER:
            raise ParameterNotFoundException("Неизвестный параметр: " + str(parameterName))

        return getVariable

    except Exception as e:
        raise ParameterParsingErrorException(parameterName, str(e))