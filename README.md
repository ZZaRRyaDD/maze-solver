# maze-solver

**Программа с графическим интерфейсом для генерации лабиринта [Алгоритмом Эллера](https://habr.com/ru/post/176671/) и решения его путем поиска в глубину**

### Установка

**Для запуска проекта вам потребуется установить [poetry](https://python-poetry.org/) и установить зависимости с помощью следующей команды**

```bash
poetry install
```

**После этого запустить виртуальное окружение и запустить программу**

```bash
python maze_solver
```

**Вы можете выбрать шесть действий**
1. Генерация лабиринта
2. Сохранение лабиринта
3. Загрузка лабиринта
4. Выбор координат начала и конца
5. Решение лабиринта
6. Генерация gif с решением лабиринта

### 1. Генерация лабиринта

**Вы должны ввести ширину, высоту, название, расширение (PNG) лабиринта. После этого вы можете увидеть изображение лабиринта на дисплее.**

### 2. Сохранение лабиринта

**Вам необходимо ввести название и выбрать расширение (PNG/TXT) лабиринта. После этого вы можете увидеть файл с лабиринтом в корневом каталоге проекта.**

### 3. Загрузка лабиринта

**Вы должны выбрать файл (файл изображения или TXT). После этого вы можете увидеть изображение лабиринта на дисплее.**

### 4. Выбор координат начала и конца

**Вы должны выбрать две точки на изображении лабиринта, а затем нажать кнопку «Решить лабиринт».**

### 5. Решение лабиринта

**Решение текущего лабиринта и отображение пути на дисплее.**

### 6. Генерация gif с решением лабиринта

**Генерация gif решения лабиринта.**

**Примеры работы программы**

![Сгенерированный лабиринт](mazes/new.png)
![Решенный лабиринт](mazes/new_solve.png)
![Решение лабиринта с заданными в ручную точками](mazes/new_txt_solve.png)
