# Лабораторная работа №2 — Структурное программирование на Python

**Боканов Сергей Николаевич, группа 221141, вариант 4, лабораторная №2**

Дисциплина «Методы и технологии программирования» (часть 1).

Репозиторий: <https://github.com/kyoug3n/mtp-lab-2>

## Содержание

- [Цель](#цель)
- [Задания варианта 4](#задания-варианта-4)
- [Структура проекта](#структура-проекта)
- [Как запустить и проверить](#как-запустить-и-проверить)
- [1. НОД двух чисел (средняя №4)](#1-нод-двух-чисел-средняя-4)
- [2. Калькулятор (средняя №6)](#2-калькулятор-средняя-6)
- [3. Словарь квадратов чисел (средняя №10)](#3-словарь-квадратов-чисел-средняя-10)
- [4. Игра «Угадай число» (повышенная №5)](#4-игра-угадай-число-повышенная-5)
- [5. Рекурсивная сумма чисел (повышенная №9)](#5-рекурсивная-сумма-чисел-повышенная-9)
- [Темы лабораторной работы в коде](#темы-лабораторной-работы-в-коде)
- [Тесты и PEP 8](#тесты-и-pep-8)

## Цель

Освоить базовые конструкции Python: переменные, условия, циклы, функции, стиль PEP 8,
модули `math` и `random`.

## Задания варианта 4

| Уровень | № | Задание | Раздел | Код | Тесты | Коммиты |
|---|---|---|---|---|---|---|
| Средний | 4 | НОД двух чисел | [1](#1-нод-двух-чисел-средняя-4) | [`structlab/gcd.py`](structlab/gcd.py) | [`tests/test_gcd.py`](tests/test_gcd.py) | `58535ba`, `704daca` |
| Средний | 6 | Калькулятор | [2](#2-калькулятор-средняя-6) | [`structlab/calculator/`](structlab/calculator) | [`test_tokenizer.py`](tests/test_tokenizer.py), [`test_evaluate.py`](tests/test_evaluate.py), [`test_calculator_cli.py`](tests/test_calculator_cli.py) | `79126d4`, `ac8c2ab`, `c16aeae`, `e671586`, `9cac734` |
| Средний | 10 | Словарь квадратов чисел | [3](#3-словарь-квадратов-чисел-средняя-10) | [`structlab/squares.py`](structlab/squares.py) | [`tests/test_squares.py`](tests/test_squares.py) | `a6e6e7d` |
| Повышенный | 5 | Игра «Угадай число» | [4](#4-игра-угадай-число-повышенная-5) | [`structlab/guess_game.py`](structlab/guess_game.py) | [`tests/test_guess_game.py`](tests/test_guess_game.py) | `b13c60d` |
| Повышенный | 9 | Рекурсивная сумма чисел | [5](#5-рекурсивная-сумма-чисел-повышенная-9) | [`structlab/recursive_sum.py`](structlab/recursive_sum.py) | [`tests/test_recursive_sum.py`](tests/test_recursive_sum.py) | `6b94d70`, `1f459e9` |

Протоколы работы всех заданий с реальным вводом и выводом собраны в
[`reports/demo.txt`](reports/demo.txt); фрагменты из него приведены в разделах ниже.

## Структура проекта

```
mtp-lab-2/
├── structlab/                  # пакет, запуск меню: python -m structlab
│   ├── __main__.py
│   ├── main.py                 # меню заданий
│   ├── console.py              # общий ввод: read_line, read_int, ScriptedConsole
│   ├── formatting.py           # вывод чисел: 5, 3.5, 0.3, 1+2i
│   ├── gcd.py                  # средняя №4
│   ├── squares.py              # средняя №10
│   ├── guess_game.py           # повышенная №5
│   ├── recursive_sum.py        # повышенная №9
│   ├── calculator/             # средняя №6
│   │   ├── __main__.py         # запуск: python -m structlab.calculator
│   │   ├── tokenizer.py        # строка → токены
│   │   ├── parser.py           # разбор рекурсивным спуском и вычисление
│   │   ├── operations.py       # арифметика с проверкой результата
│   │   ├── errors.py           # CalcError: сообщение и позиция ошибки
│   │   └── cli.py              # интерактивный режим
│   └── demo.py                 # демонстрационные сессии → reports/demo.txt
├── tests/                      # unittest, по файлу на модуль
├── reports/demo.txt            # протокол сессий всех заданий
├── .gitignore
└── README.md
```

Все интерактивные задания устроены одинаково: функция `run(input_func=input,
output_func=print)` ведёт диалог через переданные функции ввода и вывода. Из меню и из
командной строки они вызываются со встроенными `input` и `print`, а тесты и `demo.py`
подставляют заранее заданный ввод через `ScriptedConsole` — поэтому каждый диалог
проверен тестами. Слово `выход` (или конец ввода Ctrl+Z/Ctrl+D) в любом задании
завершает его.

## Как запустить и проверить

Нужен Python 3.10 или новее (в аннотациях используется запись `int | None`), внешних
зависимостей нет. Проверено на Python 3.14.5.

```bash
git clone https://github.com/kyoug3n/mtp-lab-2.git
cd mtp-lab-2

python -m structlab                     # меню со всеми заданиями
python -m structlab.gcd                 # каждое задание отдельно
python -m structlab.calculator
python -m structlab.squares
python -m structlab.guess_game          # --seed N — повторяемая партия
python -m structlab.recursive_sum

python -m unittest -v                   # тесты
python -m flake8 structlab tests        # PEP 8 (pip install flake8)
python -m structlab.demo reports/demo.txt   # пересоздать протокол сессий
```

В начале [`reports/demo.txt`](reports/demo.txt) записаны команда, ревизия и версия Python,
на которых он получен. Тест `test_committed_report_is_up_to_date` сравнивает сессии
из файла со свежим прогоном, так что протокол в репозитории не может незаметно
разойтись с кодом. Протокол и выводы проверок в этом README обновлены последним
коммитом: в штампе указана ревизия `704daca`, после которой изменены только
`reports/demo.txt` и `README.md` (проверка: `git log --stat 704daca..main`).

## 1. НОД двух чисел (средняя №4)

Функция `gcd(a, b)` в [`structlab/gcd.py`](structlab/gcd.py) — алгоритм Евклида с
остатком от деления:

```python
a, b = abs(a), abs(b)
while b != 0:
    a, b = b, a % b
return a
```

Пара `(a, b)` на каждом шаге заменяется на `(b, a % b)`: общие делители у этих пар
одинаковые, а числа уменьшаются. Когда остаток становится нулём, в `a` остаётся НОД.
Знаки на результат не влияют, `gcd(0, 0) == 0` (как у `math.gcd`), для нецелых
аргументов — `TypeError`. `True` и `False` тоже отклоняются: `bool` в Python —
подкласс `int`, и `math.gcd(True, 6)` вернул бы 1, но логическое значение — не число.

**Почему остаток, а не вычитание.** Исходная формулировка алгоритма — вычитать меньшее
число из большего, пока числа не сравняются. Остаток `a % b` — это результат всех
вычитаний `b` из `a` сразу, за одну операцию; метод с остатком делает то же, что
вычитание, только сжато. Разница видна, когда числа сильно различаются (число шагов
следует из рассуждения: при `b = 1` вычитаний ровно `a − 1`):

| Пара | Шагов с остатком | Шагов вычитанием |
|---|---|---|
| НОД(48, 18) | 3 | 4 |
| НОД(1 000 000, 1) | 1 | 999 999 |
| НОД(10¹⁸, 1) | 1 | 10¹⁸ − 1 — программа фактически зависает |

Метод с остатком делает число шагов, растущее как логарифм меньшего числа (теорема
Ламе: не больше пятикратного числа его десятичных цифр). У вычитания есть и ловушка
с нулём: НОД(5, 0) без отдельной проверки зациклился бы, потому что 5 − 0 = 5.
Поэтому реализован только метод с остатком.

Сессии из [`reports/demo.txt`](reports/demo.txt):

```
=== 2. НОД двух чисел (Средн. 4): python -m structlab.gcd ===
НОД двух целых чисел («выход» — завершить).
Первое число: -24
Второе число: abc
Нужно целое число, например 42.
Второе число: 36
НОД(-24, 36) = 12

=== 3. НОД очень больших чисел: python -m structlab.gcd ===
НОД двух целых чисел («выход» — завершить).
Первое число: 1000000000000000000
Второе число: 1
НОД(1000000000000000000, 1) = 1
```

Тесты: известные значения, нули, отрицательные числа, НОД(10¹⁸, 1) и чисел порядка
2²⁰⁰, отказ для `float`, строк и `bool`, диалог с некорректным вводом и **сверка с `math.gcd` на
1000 случайных парах** чисел до 10¹² (`random.Random(4)`, воспроизводимо).

## 2. Калькулятор (средняя №6)

Калькулятор вычисляет выражения целиком — с приоритетами операций, скобками,
квадратным корнем и комплексными числами. `eval` не используется: выражение
разбирается собственным кодом.

| Запись | Операция |
|---|---|
| `+` `-` `*` `/` | сложение, вычитание, умножение, деление |
| `//` `%` | целочисленное деление (вниз) и остаток — как в Python |
| `^` или `**` | степень (в самом Python `^` — это XOR, здесь это степень) |
| `-x`, `+x` | знак числа |
| `(` `)` | скобки |
| `sqrt 16`, `sqrt16`, `sqrt(16)` | квадратный корень; регистр не важен |
| `i` (или `j`), `4i`, `2.5i` | мнимая единица и мнимые числа |

Пробелы между частями выражения можно ставить в любом количестве или не ставить совсем:
`2+3*4`, `2 + 3 * 4` и `  2 +3*  4` — одно и то же.

### Как устроен разбор

1. **Токенизатор** ([`tokenizer.py`](structlab/calculator/tokenizer.py)) проходит
   строку циклом `while` и выделяет числа, операции (двухсимвольные `**` и `//`
   проверяются раньше односимвольных), скобки и имена. У каждого токена запоминается
   позиция — по ней потом указывается место ошибки.
2. **Разборщик** ([`parser.py`](structlab/calculator/parser.py)) работает методом
   рекурсивного спуска по грамматике (от низшего приоритета к высшему — как в Python):

   ```
   выражение := слагаемое (("+" | "-") слагаемое)*
   слагаемое := унарное (("*" | "/" | "//" | "%") унарное)*
   унарное   := ("+" | "-") унарное | степень
   степень   := первичное (("**" | "^") унарное)?
   первичное := ЧИСЛО | "(" выражение ")" | "sqrt" первичное
   ```

   Каждому правилу соответствует метод; правила вызывают друг друга, и выражение
   в скобках разбирается тем же кодом, что и всё выражение. Значение вычисляется сразу
   во время разбора:

   ```python
   def _expression(self) -> Number:
       """выражение := слагаемое (("+" | "-") слагаемое)*"""
       value = self._term()
       while self._next_is_operator(ADDITIVE):
           token = self._advance()
           right = self._term()
           value = apply_operator(token.operator, value, right,
                                  token.position)
       return value
   ```

3. **Операции** ([`operations.py`](structlab/calculator/operations.py)) выполняются
   обычными операторами Python в цепочке `if/elif`, а ошибки Python превращаются
   в понятные сообщения `CalcError`.

Что следует из грамматики:

| Выражение | Результат | Почему |
|---|---|---|
| `2 + 3 * 4` | `14` | умножение раньше сложения |
| `2 - 3 - 4` | `-5` | операции одного уровня — слева направо |
| `2 ^ 3 ^ 2` | `512` | степень — справа налево: 2 ^ (3 ^ 2) |
| `-2 ^ 2` | `-4` | степень раньше унарного минуса |
| `2 ^ -1` | `0.5` | у показателя может быть знак |
| `-7 % 3` | `2` | остаток имеет знак делителя, как в Python |
| `sqrt 16 + 9` | `13` | `sqrt` применяется к ближайшему числу или скобке, как вызов функции |
| `sqrt(-4) ^ 2` | `-4` | сначала корень (`2i`), потом степень |

### Числа и вывод

- Целые числа остаются целыми и не ограничены по размеру: `2 ^ 100` печатается
  полностью. Дробные — `float`, мнимые — `complex`.
- Целый результат печатается без `.0` (`6 / 2` → `3`), дробный — с 12 значащими
  цифрами, поэтому ошибка округления двоичной арифметики не видна: `0.1 + 0.2` → `0.3`.
- Комплексные числа выводятся в математической записи: `5+5i`, `-i`. Часть, которая
  в 10¹² раз меньше другой, считается шумом округления: у `(-8) ^ 0.5` Python даёт
  `1.7e-16+2.83j`, калькулятор печатает `2.82842712475i`.
- `sqrt` отрицательного числа даёт мнимый результат: `sqrt(-4)` → `2i`.

### Ошибки

На каждую ошибку выводится сообщение, а под введённой строкой — указатель `^` на место
ошибки; после этого калькулятор ждёт следующее выражение:

- неизвестный символ или имя, пропущенное число, лишняя или незакрытая скобка;
- пропущенный знак операции между двумя операндами (`2 3`, `2sqrt 4`, `2(3)`) —
  умножение не подразумевается, и калькулятор подсказывает, перед чем нужен знак;
- деление на ноль (`/`, `//`, `%`), ноль в отрицательной или комплексной степени;
- `//` и `%` с комплексными числами — для них эти операции не определены;
- слишком большой результат. Целые числа длиннее 4300 цифр не допускаются: столько
  по умолчанию разрешает переводить в строку сам Python. Для степени длина результата
  оценивается **заранее** как `показатель × log10(|основание|)`, поэтому `9 ^ 9 ^ 9`
  отклоняется мгновенно, а не зависает. Переполнение дробных чисел (`10.0 ^ 400`)
  тоже перехватывается.
- слишком глубокая вложенность: каждая пара скобок добавляет несколько вложенных
  вызовов разборщика, и при стандартном пределе рекурсии калькулятор справляется
  примерно с двумястами уровнями скобок — сам Python допускает 200.

### Ограничения

- Из функций есть только `sqrt`; экспоненциальная запись чисел (`1e5`) не
  поддерживается.
- Дробная степень отрицательного числа, как и в Python, даёт главное значение корня:
  `(-8) ^ (1/3)` — это `1+1.73205080757i`, а не `-2`.

### Сессия

Из [`reports/demo.txt`](reports/demo.txt):

```
=== 4. Калькулятор (Средн. 6): python -m structlab.calculator ===
Калькулятор выражений: + - * / // % ^ (или **), скобки, sqrt,
мнимая единица i. Пустая строка пропускается, «выход» — завершить.
> 2 + 3 * 4
= 14
> (2 + 3) * 4
= 20
> 2 - 3 - 4
= -5
> 2 ^ 3 ^ 2
= 512
> -2 ^ 2
= -4
> 2 ^ -1
= 0.5
> 7 / 2
= 3.5
> 7 // 2
= 3
> -7 % 3
= 2
> 0.1 + 0.2
= 0.3
> 2+3*4
= 14
> 2 ^ 100
= 1267650600228229401496703205376
> sqrt 16 + 9
= 13
> sqrt(16 + 9)
= 5
> sqrt(-4)
= 2i
> (1 + 2i) * (3 - i)
= 5+5i
> i ^ 2
= -1
> (-8) ^ (1/3)
= 1+1.73205080757i
> 
> 2 + * 3
      ^
Ошибка: Ожидалось число или «(», а встретилось «*».
> (2 + 3
  ^
Ошибка: Скобка не закрыта.
> 2 + 3)
       ^
Ошибка: Лишняя закрывающая скобка.
> 2sqrt 4
   ^
Ошибка: Пропущен знак операции перед «sqrt» (например, «*»).
> 1 / 0
    ^
Ошибка: Деление на ноль.
> 0 ^ -1
    ^
Ошибка: Ноль нельзя возвести в отрицательную или комплексную степень.
> 9 ^ 9 ^ 9
    ^
Ошибка: Результат слишком велик: больше 4300 цифр.
> 10.0 ^ 400
       ^
Ошибка: Слишком большое число для дробной арифметики (переполнение).
> (1 + i) // 2
          ^
Ошибка: Операция «//» не определена для комплексных чисел.
> 2 & 3
    ^
Ошибка: Неизвестный символ «&».
> 1e5
   ^
Ошибка: Неизвестное имя «e».
> выход
```

### Тесты калькулятора

Кроме проверок на отдельных примерах (приоритеты, ассоциативность, унарные знаки,
`sqrt`, комплексные числа, все сообщения об ошибках вместе с позициями, диалог
с указателем `^`), калькулятор **сверяется с самим Python на 3000 случайных
выражениях** (`MatchesPythonTests`). Генератор строит выражения глубиной до 4 уровней
со всеми операциями, скобками, знаками, `sqrt`, мнимыми числами и случайными
пробелами, параллельно записывая то же выражение на Python (`^` → `**`, `4i` → `4j`).
Грамматика калькулятора совпадает с грамматикой Python, поэтому результат должен
совпасть **точно, вплоть до типа** (`int`, `float` или `complex`); если Python выдаёт
ошибку (деление на ноль, `//` с комплексным числом, переполнение), калькулятор тоже
обязан выдать `CalcError`. Тест требует, чтобы больше 2000 выражений из 3000
вычислились без ошибки — иначе проверка была бы пустой. `eval` используется только
в этом тесте и только для строк, которые тест сгенерировал сам.

## 3. Словарь квадратов чисел (средняя №10)

`squares(n)` в [`structlab/squares.py`](structlab/squares.py) строит словарь
`{1: 1, 2: 4, ..., n: n²}` циклом `for`:

```python
result = {}
for number in range(1, n + 1):
    result[number] = number * number
return result
```

Ключи идут по возрастанию, потому что словари Python сохраняют порядок вставки. Для
`n = 0` получается пустой словарь, отрицательное `n` отклоняется (`ValueError`), а в
диалоге — просьбой ввести число не меньше 0.

```
=== 5. Словарь квадратов чисел (Средн. 10): python -m structlab.squares ===
Словарь квадратов чисел от 1 до n («выход» — завершить).
n = -1
Число должно быть не меньше 0.
n = 10
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81, 10: 100}
```

Тесты: первые значения, `n = 0` и `n = 1`, порядок ключей и значения для `n = 500`,
отказ для отрицательного `n`, диалог.

## 4. Игра «Угадай число» (повышенная №5)

[`structlab/guess_game.py`](structlab/guess_game.py): программа загадывает число
от 1 до 100 (`random.randint`), игрок называет варианты и получает подсказки:

```python
def check_guess(secret: int, guess: int) -> str:
    """Сравнить вариант с загаданным числом и вернуть подсказку."""
    if guess < secret:
        return GREATER
    elif guess > secret:
        return LESS
    else:
        return CORRECT
```

- Партия идёт в цикле `while` до угадывания; попытки считаются.
- Нечисловой ввод и числа вне диапазона 1–100 **не засчитываются** как попытки.
- `выход` — сдаться, программа показывает загаданное число.
- Слово «попытка» согласуется с числом (`attempts_word`: за 1 попытку, за 3 попытки,
  за 5 попыток, за 21 попытку, за 11 попыток).
- В конце игра сообщает, сколько попыток всегда хватает стратегии «называть середину
  оставшегося диапазона»: каждая попытка оставляет не больше половины чисел, поэтому
  для n чисел нужно ⌊log₂ n⌋ + 1 попыток, для 1–100 — **7** (`max_attempts_needed`,
  через `math.log2`). Это проверено перебором: тест играет за такого игрока против
  всех 100 загаданных чисел, и худший случай — ровно 7 попыток.
- Ключ `--seed N` задаёт зерно генератора (`random.Random(N)`), и партию можно
  повторить — так получена сессия ниже.

```
=== 6. Игра «Угадай число» (Повыш. 5): python -m structlab.guess_game --seed 4 ===
Я загадал целое число от 1 до 100. Угадайте его!
«выход» — сдаться.
Ваш вариант: abc
Нужно целое число от 1 до 100.
Ваш вариант: 150
Число должно быть от 1 до 100.
Ваш вариант: 50
Загаданное число меньше.
Ваш вариант: 25
Загаданное число больше.
Ваш вариант: 37
Загаданное число меньше.
Ваш вариант: 31
Угадали!
Число 31 угадано за 4 попытки.
Если называть середину оставшегося диапазона, любое число угадывается не больше чем за 7 попыток.
```

Тесты: подсказки, число попыток для разных диапазонов, формы слова «попытка»,
партия с некорректным вводом, угадывание с первой попытки, отказ от игры, повторяемость
партии с `--seed`, попадание загаданного числа в диапазон 1–100 на 1000 партиях.

## 5. Рекурсивная сумма чисел (повышенная №9)

[`structlab/recursive_sum.py`](structlab/recursive_sum.py) считает сумму списка
чисел двумя рекурсивными функциями. Обе не копируют список срезами, а передают
в рекурсивный вызов границы обрабатываемой части.

**Классическая схема — «первый элемент + сумма остальных»:**

```python
def _sum_from(numbers: Sequence[Real], start: int) -> Real:
    """Сумма элементов начиная с индекса ``start``."""
    if start == len(numbers):  # базовый случай: элементов не осталось
        return 0
    return numbers[start] + _sum_from(numbers, start + 1)
```

Это прямая запись определения S(список) = первый + S(остальные) с базовым случаем
«пустой список — 0». Но каждый элемент добавляет вложенный вызов, глубина рекурсии
равна длине списка, а Python ограничивает глубину (`sys.getrecursionlimit()`, по
умолчанию 1000) и не оптимизирует хвостовую рекурсию. Поэтому на списке из нескольких
тысяч чисел функция падает с `RecursionError`.

**«Разделяй и властвуй» — сумма левой половины плюс сумма правой:**

```python
def _sum_range(numbers: Sequence[Real], start: int, stop: int) -> Real:
    """Сумма элементов с индексами от ``start`` до ``stop`` (не включая)."""
    if stop - start == 0:  # базовый случай: пустой отрезок
        return 0
    if stop - start == 1:  # базовый случай: один элемент
        return numbers[start]
    middle = (start + stop) // 2
    left = _sum_range(numbers, start, middle)
    right = _sum_range(numbers, middle, stop)
    return left + right
```

Отрезок каждый раз уменьшается вдвое, поэтому глубина рекурсии — около log₂ n:
для миллиона чисел около 20 уровней вместо миллиона.

Разница проверена тестами:

- `test_linear_recursion_hits_the_depth_limit` — классическая функция на списке
  в 5 раз длиннее предела рекурсии падает с `RecursionError`;
- `test_halving_depth_is_logarithmic` — предел рекурсии временно ставится всего
  на 30 вызовов больше текущей глубины: деление пополам суммирует миллион чисел,
  а классической функции не хватает даже на 100;
- обе функции совпадают со встроенной `sum` на 200 случайных списках и на дробных
  числах.

Диалог показывает результат обоих способов; если классической функции не хватает
глубины, вместо суммы выводится «не хватило глубины рекурсии (предел — 1000 вызовов)»
(это тоже проверено тестом).

```
=== 7. Рекурсивная сумма (Повыш. 9): python -m structlab.recursive_sum ===
Рекурсивная сумма чисел («выход» — завершить).
Числа через пробел: 3 1 четыре
Ошибка: «четыре» — не число.
Числа через пробел: 3 1 4 1 5 9 2 6
Количество чисел: 8
Сумма (первый + остальные): 31
Сумма (деление пополам): 31

=== 8. Рекурсивная сумма дробных: python -m structlab.recursive_sum ===
Рекурсивная сумма чисел («выход» — завершить).
Числа через пробел: 0.1 0.2 0.3 -1.5
Количество чисел: 4
Сумма (первый + остальные): -0.9
Сумма (деление пополам): -0.9
```

Числа вводятся через пробел; целые остаются `int`, остальные становятся `float`,
`inf` и `nan` отклоняются.

## Темы лабораторной работы в коде

| Тема | Где используется |
|---|---|
| Типы `int`, `float`, `str` | разбор ввода в `read_int` и `parse_numbers` (`int`, затем `float`); целые числа произвольной длины в `gcd` и калькуляторе |
| `list`, `dict` | список токенов и список чисел; словарь в `squares`, словарь псевдонимов операций `OPERATOR_ALIASES` |
| `complex` | мнимые числа калькулятора, `cmath.sqrt` |
| `if/elif/else` | `check_guess`, выбор операции в `apply_operator`, `attempts_word`, форматирование чисел |
| Цикл `for` | `squares`, вывод меню |
| Цикл `while` | алгоритм Евклида, токенизатор, игровой цикл, повтор ввода в `read_int`, циклы меню и калькулятора |
| Функции `def`, параметры, `return` | все задания; параметры по умолчанию (`input_func=input`), необязательный `rng` |
| Рекурсия | две суммы; разбор выражений рекурсивным спуском |
| Модуль `math` | `log10` (оценка длины степени), `sqrt`, `isfinite`, `floor` и `log2` (число попыток) |
| Модуль `random` | `randint` для загаданного числа, `Random(seed)` для повторяемых партий и тестов |
| PEP 8 | `flake8` без замечаний; имена функций в `snake_case`, константы в `UPPER_CASE`, строки до 79 символов, docstring и аннотации типов у функций |

## Тесты и PEP 8

```
$ python -m flake8 structlab tests
$ echo $?
0
```

Тесты: `python -m unittest -v` — 96 тестов, все проходят.

<details>
<summary>Полный вывод <code>python -m unittest -v</code></summary>

```
test_empty_lines_are_skipped (tests.test_calculator_cli.CalculatorDialogTests.test_empty_lines_are_skipped) ... ok
test_error_pointer_under_the_input (tests.test_calculator_cli.CalculatorDialogTests.test_error_pointer_under_the_input) ... ok
test_error_without_position (tests.test_calculator_cli.CalculatorDialogTests.test_error_without_position) ... ok
test_results_are_formatted (tests.test_calculator_cli.CalculatorDialogTests.test_results_are_formatted) ... ok
test_exit (tests.test_console.ReadIntTests.test_exit) ... ok
test_minimum (tests.test_console.ReadIntTests.test_minimum) ... ok
test_repeats_until_integer (tests.test_console.ReadIntTests.test_repeats_until_integer) ... ok
test_end_of_input (tests.test_console.ReadLineTests.test_end_of_input) ... ok
test_exit_word_in_any_case (tests.test_console.ReadLineTests.test_exit_word_in_any_case) ... ok
test_keyboard_interrupt (tests.test_console.ReadLineTests.test_keyboard_interrupt) ... ok
test_strips_spaces (tests.test_console.ReadLineTests.test_strips_spaces) ... ok
test_raises_eof_when_lines_run_out (tests.test_console.ScriptedConsoleTests.test_raises_eof_when_lines_run_out) ... ok
test_transcript_shows_prompt_with_typed_text (tests.test_console.ScriptedConsoleTests.test_transcript_shows_prompt_with_typed_text) ... ok
test_all_sessions_are_present (tests.test_demo.DemoTests.test_all_sessions_are_present) ... ok
test_committed_report_is_up_to_date (tests.test_demo.DemoTests.test_committed_report_is_up_to_date)
Протокол в репозитории совпадает со свежим прогоном сессий. ... ok
test_division_by_zero (tests.test_evaluate.ErrorTests.test_division_by_zero) ... ok
test_exponent_notation_is_not_supported (tests.test_evaluate.ErrorTests.test_exponent_notation_is_not_supported) ... ok
test_float_overflow (tests.test_evaluate.ErrorTests.test_float_overflow) ... ok
test_huge_integer_powers_are_refused_quickly (tests.test_evaluate.ErrorTests.test_huge_integer_powers_are_refused_quickly) ... ok
test_integer_digit_limit (tests.test_evaluate.ErrorTests.test_integer_digit_limit) ... ok
test_integer_operations_with_complex_numbers (tests.test_evaluate.ErrorTests.test_integer_operations_with_complex_numbers) ... ok
test_missing_operator (tests.test_evaluate.ErrorTests.test_missing_operator) ... ok
test_sqrt_errors (tests.test_evaluate.ErrorTests.test_sqrt_errors) ... ok
test_syntax_errors (tests.test_evaluate.ErrorTests.test_syntax_errors) ... ok
test_too_deep_nesting (tests.test_evaluate.ErrorTests.test_too_deep_nesting) ... ok
test_zero_to_negative_or_complex_power (tests.test_evaluate.ErrorTests.test_zero_to_negative_or_complex_power) ... ok
test_random_expressions (tests.test_evaluate.MatchesPythonTests.test_random_expressions) ... ok
test_floor_division_and_remainder_follow_python (tests.test_evaluate.PrecedenceTests.test_floor_division_and_remainder_follow_python) ... ok
test_left_to_right (tests.test_evaluate.PrecedenceTests.test_left_to_right) ... ok
test_multiplication_before_addition (tests.test_evaluate.PrecedenceTests.test_multiplication_before_addition) ... ok
test_nested_parentheses (tests.test_evaluate.PrecedenceTests.test_nested_parentheses) ... ok
test_power_is_right_associative (tests.test_evaluate.PrecedenceTests.test_power_is_right_associative) ... ok
test_single_operations (tests.test_evaluate.PrecedenceTests.test_single_operations) ... ok
test_spaces_do_not_matter (tests.test_evaluate.PrecedenceTests.test_spaces_do_not_matter) ... ok
test_unary_signs (tests.test_evaluate.PrecedenceTests.test_unary_signs) ... ok
test_complex_arithmetic_matches_python (tests.test_evaluate.SqrtAndComplexTests.test_complex_arithmetic_matches_python) ... ok
test_fractional_power_of_negative_number (tests.test_evaluate.SqrtAndComplexTests.test_fractional_power_of_negative_number) ... ok
test_imaginary_unit (tests.test_evaluate.SqrtAndComplexTests.test_imaginary_unit) ... ok
test_sqrt_binds_like_a_function_call (tests.test_evaluate.SqrtAndComplexTests.test_sqrt_binds_like_a_function_call) ... ok
test_sqrt_forms (tests.test_evaluate.SqrtAndComplexTests.test_sqrt_forms) ... ok
test_sqrt_of_negative_and_complex_numbers (tests.test_evaluate.SqrtAndComplexTests.test_sqrt_of_negative_and_complex_numbers) ... ok
test_complex (tests.test_formatting.FormatNumberTests.test_complex) ... ok
test_complex_rounding_noise_is_dropped (tests.test_formatting.FormatNumberTests.test_complex_rounding_noise_is_dropped) ... ok
test_floats (tests.test_formatting.FormatNumberTests.test_floats) ... ok
test_integers (tests.test_formatting.FormatNumberTests.test_integers) ... ok
test_rejects_non_numbers (tests.test_formatting.FormatNumberTests.test_rejects_non_numbers) ... ok
test_dialog (tests.test_gcd.GcdDialogTests.test_dialog) ... ok
test_exit_before_second_number (tests.test_gcd.GcdDialogTests.test_exit_before_second_number) ... ok
test_huge_numbers_are_fast (tests.test_gcd.GcdTests.test_huge_numbers_are_fast) ... ok
test_known_values (tests.test_gcd.GcdTests.test_known_values) ... ok
test_matches_math_gcd_on_random_pairs (tests.test_gcd.GcdTests.test_matches_math_gcd_on_random_pairs) ... ok
test_negative_numbers (tests.test_gcd.GcdTests.test_negative_numbers) ... ok
test_order_does_not_matter (tests.test_gcd.GcdTests.test_order_does_not_matter) ... ok
test_rejects_non_integers (tests.test_gcd.GcdTests.test_rejects_non_integers) ... ok
test_zero (tests.test_gcd.GcdTests.test_zero) ... ok
test_forms (tests.test_guess_game.AttemptsWordTests.test_forms) ... ok
test_hints (tests.test_guess_game.CheckGuessTests.test_hints) ... ok
test_bisection_always_wins_in_time (tests.test_guess_game.MaxAttemptsTests.test_bisection_always_wins_in_time) ... ok
test_values (tests.test_guess_game.MaxAttemptsTests.test_values) ... ok
test_first_try (tests.test_guess_game.PlayTests.test_first_try) ... ok
test_game_with_invalid_input (tests.test_guess_game.PlayTests.test_game_with_invalid_input) ... ok
test_giving_up (tests.test_guess_game.PlayTests.test_giving_up) ... ok
test_run_uses_given_generator (tests.test_guess_game.SeedTests.test_run_uses_given_generator) ... ok
test_secret_is_in_range (tests.test_guess_game.SeedTests.test_secret_is_in_range) ... ok
test_seed_option_makes_game_repeatable (tests.test_guess_game.SeedTests.test_seed_option_makes_game_repeatable) ... ok
test_exits_on_exit_word_and_end_of_input (tests.test_main.MenuTests.test_exits_on_exit_word_and_end_of_input) ... ok
test_rejects_unknown_items (tests.test_main.MenuTests.test_rejects_unknown_items) ... ok
test_shows_all_items_and_exits_on_zero (tests.test_main.MenuTests.test_shows_all_items_and_exits_on_zero) ... ok
test_does_not_change_the_list (tests.test_recursive_sum.BothSumsTests.test_does_not_change_the_list) ... ok
test_floats_match_builtin_sum (tests.test_recursive_sum.BothSumsTests.test_floats_match_builtin_sum) ... ok
test_match_builtin_sum_on_random_lists (tests.test_recursive_sum.BothSumsTests.test_match_builtin_sum_on_random_lists) ... ok
test_small_lists (tests.test_recursive_sum.BothSumsTests.test_small_lists) ... ok
test_works_with_tuples (tests.test_recursive_sum.BothSumsTests.test_works_with_tuples) ... ok
test_integers_and_floats (tests.test_recursive_sum.ParseNumbersTests.test_integers_and_floats) ... ok
test_rejects_words_and_infinity (tests.test_recursive_sum.ParseNumbersTests.test_rejects_words_and_infinity) ... ok
test_halving_depth_is_logarithmic (tests.test_recursive_sum.RecursionDepthTests.test_halving_depth_is_logarithmic)
Миллиону чисел хватает 30 дополнительных уровней стека. ... ok
test_halving_handles_long_lists (tests.test_recursive_sum.RecursionDepthTests.test_halving_handles_long_lists) ... ok
test_linear_recursion_hits_the_depth_limit (tests.test_recursive_sum.RecursionDepthTests.test_linear_recursion_hits_the_depth_limit) ... ok
test_dialog (tests.test_recursive_sum.RecursiveSumDialogTests.test_dialog) ... ok
test_dialog_reports_recursion_limit (tests.test_recursive_sum.RecursiveSumDialogTests.test_dialog_reports_recursion_limit) ... ok
test_dialog (tests.test_squares.SquaresDialogTests.test_dialog) ... ok
test_first_five (tests.test_squares.SquaresTests.test_first_five) ... ok
test_keys_in_order_and_values_are_squares (tests.test_squares.SquaresTests.test_keys_in_order_and_values_are_squares) ... ok
test_negative_n_is_rejected (tests.test_squares.SquaresTests.test_negative_n_is_rejected) ... ok
test_small_n (tests.test_squares.SquaresTests.test_small_n) ... ok
test_caret_means_power (tests.test_tokenizer.TokenizeTests.test_caret_means_power) ... ok
test_empty_expression (tests.test_tokenizer.TokenizeTests.test_empty_expression) ... ok
test_function_name_after_number_is_separate_token (tests.test_tokenizer.TokenizeTests.test_function_name_after_number_is_separate_token) ... ok
test_imaginary_numbers (tests.test_tokenizer.TokenizeTests.test_imaginary_numbers) ... ok
test_numbers (tests.test_tokenizer.TokenizeTests.test_numbers) ... ok
test_parentheses_and_positions (tests.test_tokenizer.TokenizeTests.test_parentheses_and_positions) ... ok
test_spaces_are_optional (tests.test_tokenizer.TokenizeTests.test_spaces_are_optional) ... ok
test_sqrt_in_any_case (tests.test_tokenizer.TokenizeTests.test_sqrt_in_any_case) ... ok
test_two_character_operators (tests.test_tokenizer.TokenizeTests.test_two_character_operators) ... ok
test_unknown_character (tests.test_tokenizer.TokenizeTests.test_unknown_character) ... ok
test_unknown_names (tests.test_tokenizer.TokenizeTests.test_unknown_names) ... ok

----------------------------------------------------------------------
Ran 96 tests in 0.801s

OK
```

</details>
