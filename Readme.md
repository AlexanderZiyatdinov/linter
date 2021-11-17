# Linter

**Описание:** утилита, позволяющая проверить соответствие кода программы на языке Java и C++ установленному стилю кода (**codestyle**)
**Примечание:** Пока что работает только на .java файлах

## Содержимое

### Конфигурация

Конфигурация **codestyle** задается в файле **config.json**. На данный момент доступны следующие поля для настроек:

* "indent": int - Строго точное количество пробелов необходимых для одного сдвига
* "space_around_the_operator": bool - Проверять ли наличие пробелов вокруг операторов
* "count_of_empty_lines": int - Количество допустимых пустых строк подряд
* "practise_of_writing": str - Стиль кода (далее перечислены возможные значения)
  * "camelcase"
  * "pascalcase"
  * "snakecase"

Небольшой пример настройки конфигурационного файла:

```json
{
  "java":
  {
    "rules":
    {
      "indent": 2,
      "spaces_around_the_operator": true,
      "count_of_empty_lines": 1,
      "practice_of_writing": "camelcase"
    }
  },
  "cpp": "NIY"
}
```

### Принцип работы

Первоначально программа проходит процесс токенизации, в результате Linter получает какой-то набор токенов - элементарных объектов, из которых состоит программа.

Каждый токен - это некий объект, у которого есть:

* Позиция в коде программы
* Тип токена
* Лексическое значение токена

Ниже перечислены реализованные типы токенов:

* EMPTY_LINE - пустая строка
* INDENT - сдвиг в начале строки
* SPACE - пробел
* KEYWORD - ключевое слово языка программирования
* NAME - имя идентификатора
* VAR - переменная
* OP - оператор

Вот пример токенизации для следующей программы на языке Java:

```python
public class HelloWorld
{
  public static void main(String[] args)
  {
     System.out.print("Hello world");
  }
}
```

```
[[Token(pos=(1, 0), type='KEYWORD', value='public'),
  Token(pos=(1, 6), type='SPACE', value=' '),
  Token(pos=(1, 7), type='KEYWORD', value='class'),
  Token(pos=(1, 12), type='SPACE', value=' '),
  Token(pos=(1, 13), type='NAME', value='HelloWorld')],
 [Token(pos=(2, 0), type='OP', value='{')],
 [Token(pos=(3, 0), type='INDENT', value='  '),
  Token(pos=(3, 2), type='KEYWORD', value='public'),
  Token(pos=(3, 8), type='SPACE', value=' '),
  Token(pos=(3, 9), type='KEYWORD', value='static'),
  Token(pos=(3, 15), type='SPACE', value=' '),
  Token(pos=(3, 16), type='KEYWORD', value='void'),
  Token(pos=(3, 20), type='SPACE', value=' '),
  Token(pos=(3, 21), type='NAME', value='main'),
  Token(pos=(3, 25), type='OP', value='('),
  Token(pos=(3, 26), type='KEYWORD', value='String'),
  Token(pos=(3, 32), type='OP', value='['),
  Token(pos=(3, 33), type='OP', value=']'),
  Token(pos=(3, 34), type='SPACE', value=' '),
  Token(pos=(3, 35), type='NAME', value='args'),
  Token(pos=(3, 39), type='OP', value=')')],
 [Token(pos=(4, 2), type='OP', value='{')],
 [Token(pos=(5, 0), type='INDENT', value='     '),
  Token(pos=(5, 5), type='NAME', value='System'),
  Token(pos=(5, 11), type='OP', value='.'),
  Token(pos=(5, 11), type='OP', value='.'),
  Token(pos=(5, 12), type='NAME', value='out'),
  Token(pos=(5, 16), type='NAME', value='print'),
  Token(pos=(5, 21), type='OP', value='('),
  Token(pos=(5, 22), type='VAR', value='"Hello'),
  Token(pos=(5, 28), type='SPACE', value=' '),
  Token(pos=(5, 29), type='NAME', value='world"'),
  Token(pos=(5, 35), type='OP', value=')'),
  Token(pos=(5, 36), type='OP', value=';')],
 [Token(pos=(6, 2), type='OP', value='}')],
 [Token(pos=(7, 0), type='OP', value='}')]]
```

После токенизации осуществляется проверка правил, соответствующих полям в файле конфигурации.

### Пример использования

Официальная справка по работе с программой выглядит так:

```
python lint.py --help

usage: lint.py [-h] {files,dirs} ...

Utility for analyzing compliance with the rules of writing code

options:
  -h, --help    show this help message and exit

subcommands:
  valid subcommands

  {files,dirs}  description
    files       launching a linter for a list of files
    dirs        launching a linter for list of dirs
```

На вход программе можно отправить либо:

* Любое количество файлов поддерживаемого расширения

  ``````
  python lint.py files filename1 filename2 ... filenameN
  ``````

* Любое количество директорий, внутри которых будет осуществлен поиск подходящих файлов

  ``````
  python lint.py dirs dirname1 dirname2 ... dirnameN

**Пример:**

Пусть у нас есть следующая иерархическая структура в корневом каталоге проекта (она повторяет ту, которая находится в репозитории):

* examples
  * example.java
  * example2.java
* examples2
  * example3.java

Вот так выглядят наши файлы:

**example.java**

```java
public class helloWorld
{
  public static void main(String[] args)
   {



    String Name = "Adam";
     System.out.print("Hello"+ name);
  }
}
```

**example2.java**

```java
public class Sqrt
{
  private static void main(String[] args)
  {
    int a=4;
    System.out.println(Math.sqrt(a));
  }
}
```

**example3.java**

```java
public class camelCaseName
{
  public static void main(String[] args)
  {
    String name = "Adam";
    System.out.print("Hello" + name);
  }
}
```

Ниже приведены примеры разных запусков программы:

```
python lint.py files .\examples\example.java
```

![image-20211117133901282](C:\Users\79222\AppData\Roaming\Typora\typora-user-images\image-20211117133901282.png)

```
python lint.py files .\examples\example.java .\examples2\example3.java
```

![image-20211117133953436](C:\Users\79222\AppData\Roaming\Typora\typora-user-images\image-20211117133953436.png)

```
python lint.py dirs .\examples\
```

![image-20211117134045374](C:\Users\79222\AppData\Roaming\Typora\typora-user-images\image-20211117134045374.png)

```
python lint.py dirs .\examples\ .\examples2\
```

![image-20211117134141220](C:\Users\79222\AppData\Roaming\Typora\typora-user-images\image-20211117134141220.png)

