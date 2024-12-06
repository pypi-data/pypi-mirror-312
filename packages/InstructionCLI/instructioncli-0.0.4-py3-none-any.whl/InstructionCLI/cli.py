"""
    Анализатор комадной строки.

    Автор: Боровиков С.Д. (ака Fleenko)


    Что такое инструкция?
    Каждая инструкция это подстрока имеющая вид:
    "<строка с командой> <аргументы инструкции>..."
    где 
        <строка с командой>    : Введённая пользователем команда (Важно! Слова в строке не должны содержать в начале "--". Иначе парсер будет считать это как параметр)
        <аргументы инструкции> : Агрументы инструкции. Бывают следующих видов:
                                    --myPar1=123 : Аргумент с присваиванием
                                    --myPar2     : Аргумент работающий как флаг
                                 Налчичие аргументов в комадной строке не обязятельно. При написании инструкциий нужно учитывать, что пользователь может аргументы не указыать.
    Например: "myFunc --myPar1=123 --myPar2"

    При создании собственной инструкции нужно понимать следующее:
    Инструкция это класс унаследованный от "Instruction" (Родительский класс). Название инструкции должно иметь в конце постфикс "Instruction" (Например RunInstruction, OpenFileInstruction).
    Описание инструкции происходит при помощью переопределения методов родительского класса.

    Вот основные методы которые нужно переопределить для создания иструкции:
    template(self, expression)               : Шаблон инструкции. Определяет корректность (вид) введенной инструкции. Если возвращается True, это значит, что иструкция введена
                                               корректно и это выражение будет передано в doInstruction(). Этот метод может вызываться несколько раз. Это связано с тем, что
                                               с каждой итерацией добавляется последующее слово до тех пор, пока не встретиться конец строки или агрумент.
    applyParameters(self, parameters : dict) : Обработка полученных аргументов. Данный метод будет вызван перед doInstruction(). "parameters" будет содержать полученные аргументы.
                                               Например в параметр "parameters" может быть передан словарь следующего вида "{'myPar1': '123', 'myPar2': True}".
    doInstruction(self, expression)          : Выполенение инструкции. Если template() возращает True, то будет вызвана обработка иструкции. 
    
    nextInstruction(self)                    : Следующая ожидаемая инструкция. Командная строка может состоять из нескольких инструкций. CliParser требует как минимум 2 инструкции.
                                               Одна из них стартовая инструкция, которая получает аргументы запуска командной строки, другая для обработки первой инструкции.
                                               Например в "Пример 1" в "RunInstruction.nextInstruction()" возвращает "CallInstruction()".
    
    Дополнительные методы:
    isRequired()                             : Если True, то инструкция обязательно должно выполниться. Иначе выводиться сообщение "Ожидалась инструкция, но был обнаружен конец строки."

    failedInstruction()                      : Возвращает сообщение о некорректности инструкции. Если все итерации с "template()" вернули "False", то будет вызван этот метод.          
    

    Вызов парсера
    Есть следующая строка: 
    "py mycli.py myFunc --myPar1=123 --myPar2"
    После запуска, если сделаем вывод "sys.argv", то увидим следующее:
    ["mycli.py", "myFunc", "--myPar1=123", "--myPar2"]
    Под нулевым индексом будет находится имя запущеного питоновского файла. Для анализа парсером это не требуется, поэтому вызов парсера будет иметь следующий вид:
    cli(sys.argv[1:], RunInstruction())
    
    
    Пример 1
    Рассмотрим следующую инструкцию:
    "myFunc --myPar1=123 --myPar2"

    Для обработки такой инструкции создадим инструкцию RunInstruction и CallInstruction:
    class RunInstruction(Instruction):  
    def doInstruction(self, expression):
        pass
    def applyParameters(self, parameters : dict):
        pass
    def nextInstruction(self):
        return CallInstruction()

    class CallInstruction(Instruction):
    def template(self, expression) -> bool:
        return True
    def doInstruction(self, expression):
        pass
    def applyParameters(self, parameters : dict):
        pass
    def nextInstruction(self):
        return NoInstruction()

    В вызове парсера укажем начальную инструкцию RunInstruction:
    parse(sys.argv[1:], RunInstruction())

    
    

"""

import re
import sys

from .exception import ExecuteInstructionErrorException, ExpressionParsingErrorException, ParameterNotFoundException, ParameterParsingErrorException
from .instruction import Instruction
  
def printExplanation(string, pos, length, message):
    print("[CLI] Traceback:")
    print("    " + string)
    print("    " + (" "*pos) + ("^"*length))
    offset = pos - round(len(message)/2) + 1 
    print("    " + (" "*offset) + message)

def cli(args: list[str], firstIstruction: Instruction):
    """
    Анализатор командной строки.

    Args:
        args (list[str]): аргументы из командной строки
        firstIstruction (Instruction): Первая обрабатываемая инструкция

    Returns:
    None
    """

    # Добавляем ковычки
    for num, arg in enumerate(args):
        if " " in arg:
            argHead = re.match(r'[-]{2}(\w+)\s*=\s*', arg)
            if argHead:
                pos = argHead.span()
                args[num] = args[num][:pos[1]] + '"' + args[num][pos[1]:] + '"'
        args[num] = args[num].replace("'", '"')

    cliStr = " ".join(args).strip()
    cliStrOrigin = cliStr
    cursor = 0

    # Инструкция при запуске CLI
    selectedIstruction: Instruction = firstIstruction

    istructionParameters = dict()
    istructionParametersPos = dict()
    cliExpression = ""
    isExecuteInstruction = True

    while isExecuteInstruction:
        # Вытаскиваем параметры
        parameter = re.match(r'[-]{2}(\w+)', cliStr)
        if parameter and parameter.span()[0] == 0:
            parameterName = parameter.group(1)

            parameterWithEqualSign = re.match(r'[-]{2}(\w+)\s*=\s*((?:"[^\'"]+"|[^\'" ]+))', cliStr)
            if parameterWithEqualSign and parameter.span()[0] == parameterWithEqualSign.span()[0]:
                istructionParameters[parameterName] = parameterWithEqualSign.group(2)
                istructionParametersPos[parameterName] = cursor
                lastChar = parameterWithEqualSign.span()[1]
            else:
                istructionParameters[parameterName] = True
                istructionParametersPos[parameterName] = cursor
                lastChar = parameter.span()[1]

            cliStr = cliStr[lastChar:]
            lengthBefore = len(cliStr)
            cliStr = cliStr.strip()
            cursor += lastChar + (lengthBefore-len(cliStr))

            continue

        # Применяем параметры
        try:
            selectedIstruction.applyParameters(istructionParameters)
        except ParameterParsingErrorException as e:
            cursorStart = istructionParametersPos[e.parameterName]

            try:
                index = list(istructionParametersPos.keys()).index(e.parameterName)
                problemLength = list(istructionParametersPos.values())[index + 1] - cursorStart - 1
            except:
                if cursor < len(cliStrOrigin):
                    problemLength = cursor - cursorStart - 1
                else:
                    problemLength = cursor - cursorStart

            printExplanation(cliStrOrigin, cursorStart, problemLength, str(e))
            sys.exit()
        except (ParameterNotFoundException, Exception) as e:
            print(istructionParametersPos)
            cursorStart = list(istructionParametersPos.values())[0]
            if cursor < len(cliStrOrigin):
                problemLength = cursor - cursorStart - 1
            else:
                problemLength = cursor - cursorStart
            printExplanation(cliStrOrigin, cursorStart, problemLength, str(e))
            sys.exit()        

        istructionParameters = dict()
        istructionParametersPos = dict()

        # Выполняем инструкцию
        try:
            selectedIstruction.doInstruction(cliExpression)
        except (ExpressionParsingErrorException, ExecuteInstructionErrorException) as e:
            printExplanation(cliStrOrigin, cursor - len(cliExpression), len(cliExpression), str(e))
            sys.exit()

        isExecuteInstruction = False

        selectedIstructionBefore = selectedIstruction

        # Меняем инструкцию
        selectedIstruction = selectedIstruction.nextInstruction()

        if not isinstance(selectedIstruction, Instruction):
            print(f"[CLI] Следующая инструкция выданная {selectedIstructionBefore.__class__.__name__} является {selectedIstruction}. Если это последняя инструкция в цепочке, то нужно вернуть NoInstruction()")
            sys.exit()


        if len(cliStr) == 0:
            if selectedIstruction.isRequired():
                printExplanation(cliStrOrigin, cursor, 3, "Ожидалась инструкция, но был обнаружен конец строки.")
            break

        # Проверяем следующую инструкцию на корректность
        tempArgs = cliStr.split(" ")
        lengthBefore = len(cliStr)
        argVolume = 1
        while True:
            if selectedIstruction.template(" ".join(tempArgs[:argVolume])):
                cliExpression = " ".join(tempArgs[0:argVolume])
                cliStr = " ".join(tempArgs[argVolume:]).strip()
                cursor += lengthBefore - len(cliStr)
                isExecuteInstruction = True
                break
            else:
                if len(tempArgs) > argVolume:
                    if re.match(r'[-]{2}(\w+)', tempArgs[argVolume]):
                        pass
                    else:
                        argVolume += 1
                        continue

                # Вывод сообщения о некорректной инструкции
                failedExpression = " ".join(tempArgs[:argVolume])
                printExplanation(cliStrOrigin, cursor, len(failedExpression), selectedIstruction.failedInstruction(failedExpression))
                
                sys.exit()
