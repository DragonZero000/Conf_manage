Эмулятор оболочки ОС

Общее описание:
Эмулятор командной строки UNIX-подобной ОС, реализованный на Python. Работает с виртуальной файловой системой (VFS) из ZIP-архива в памяти, поддерживает команды ls, cd, tree, clear, vfs-info, exit. Поддерживает интерактивный режим и стартовые скрипты.

Функции и настройки:
Команды:
ls [пути]: Список файлов/директорий. Опции: -h/--help.
cd [путь]: Смена директории. Опции: -h/--help. Без пути — переход в /.
tree [пути]: Дерево директорий. Опции: -h/--help.
clear: Очистка экрана. Опции: -h/--help.
vfs-info: Имя VFS и SHA-256 хеш.
exit: Выход.
Параметры запуска:
--vfs_path <путь_к_zip>: ZIP-архив для VFS (обязательный для операций с файлами).
--script_path <путь_к_скрипту>: Скрипт с командами, выполняется с имитацией ввода.
Особенности:
Парсер команд с поддержкой кавычек (shlex.split()).
Нормализация путей (~, ., ..).
Обработка ошибок: неизвестные команды, неверные пути, проблемы с VFS.
VFS работает в памяти без распаковки.

Сборка и запуск тестов
Требования: Python 3.12+ (встроенные библиотеки).
Запуск
python shell_emulator.py --vfs_path vfs.zip --script_path script.txt
Без --script_path — интерактивный режим.

Тестирование
Можно вызвать .bat файлы для тестирования

Примеры использования
Интерактивный режим
python main.py --vfs_path test-vfs/vfs_2_level.zip

Данные из консоли с вводами и выводами:
vfs path: test-vfs/vfs_2_level.zip
start script path: null
psp4g@localhost: ~$ ды
ды is not a valid command.
psp4g@localhost: ~$ ls
vfs 2 level
psp4g@localhost: ~$ cd "vfs 2 level"
psp4g@localhost: ~vfs 2 level$ ls
home
psp4g@localhost: ~vfs 2 level$ vfs-info
vfs_2_level.zip 58b659352ced6f455d057d62e2b16292f527c04b4b51723985bbe0a155d2ff31
psp4g@localhost: ~vfs 2 level$ tree
vfs 2 level
└── home
    ├── bin
    ├── main
    └── thing.txt
psp4g@localhost: ~vfs 2 level$ exit