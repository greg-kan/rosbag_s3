## ROSBAG files processor

OS: Linux

### Сборка:

Склонировать репозиторий:

`git clone ...`

Выполнить:

`python3 -m pip install --upgrade pip`

`python3 -m pip install --upgrade build`

Перейти в директорию с файлом pyproject.toml:

`cd rosbag_s3/rosbag_processor`

Выполнить:

`python3 -m build`

Будет создана директория с дистрибутивом:

`rosbag_s3/rosbag_processor/dist`

В ней должны появиться два файла:

`rosbag_processor-0.1.tar.gz`

`rosbag_processor-0.1-py3-none-any.whl`

_Примечание: в папке dist уже лежит собранный пакет._

### Установка:

Создать виртуальную среду для программы-тестера, например:

`rosbag_tester_env`

Активировать её, например, в случае virtualenv:

`workon rosbag_tester_env`

Далее выполнить:

`pip install rosbag_s3/rosbag_processor/dist/rosbag_processor-0.1-py3-none-any.whl`

Будет установлен пакет rosbag_processor-0.1 с зависимостями.

Зависимости пакета можно установить и так:

`pip install boto3`

`pip install bagpy`

`pip install opencv-python`

`pip install rosbags-image`


### Использование:

В домашней директории пользователя создать папку

`.rosbag_processor`

с файлами конфигурации:

`conf.json`
`connect.json`

Содержимое `conf.json`:

`{"log_file":"rosbag_processor", "bag_file_extension":".bag"}`

Содержимое  `connect.json`:

`{"url":"https:// s3 storage url",`

` "accessKey":"your accessKey",`

` "secretKey":"your secretKey",`

` "api":"s3v4",`

` "path":"auto"}`

_Примечание: в папке `.rosbag_processor` приведены шаблоны._

Далее, создать python-скрипт для запуска, например, main.py

Пример готового скрипта есть в папке `rosbag_tester`

Запустить в созданной виртуальной среде:

`(rosbag_tester_env) user@lws:~/rosbag_s3/rosbag_tester$ python3 main.py`

### Описание интерфейса пакета.

Пакет содержит три основных модуля: `downloader.py, parser.py и uploader.py` соответственно для скачивания rosbag файлов, их парсинга и помещения результата парсинга (изображений) в хранилище.

Ниже описан интерфейс каждого из них. 

`downloader.py`

Функция `download_parallel_multithreading`

Возвращает:

Для каждого скачанного файла - словарь с именем и размером файла и результат: Success, или сообщение об ошибке.

Параметры:

- `source_bucket` - Хранилище-источник (обязательный)
- `source_prefix` - Папка-источник (обязательный)
- `path_to_bag_files` - Абсолютный путь к локальной папке для скачанных rosbag файлов (обязательный) 
- `debug_mode=False` - Режим отладки (опциональный). В случае True выводит в консоль сообщения о ходе процесса (те же, что и в лог-файлы). По умолчанию: False

`parser.py`

Функция `pars_files`

Параметры:

- `path_to_files` - Абсолютный путь к локальной папке с rosbag файлами (обязательный)
- `path_to_pictures` - Абсолютный путь к папке, в которой будут результаты парсинга (изображения) (обязательный)  
- `topics=None` - Имя Топика для парсинга топиков определенного типа (опциональный).

Функция обрабатывает топики только следующих типов:

`'/realsense_gripper/aligned_depth_to_color/image_raw', '/realsense_gripper/color/image_raw/compressed'`

- `start_time=None` - Левая граница временного интервала для обработки (опциональный)
- `end_time=None` - Правая граница временного интервала для обработки (опциональный)

Пример:

`MIN_FILTER_TIME = '2023-08-22 18:33:48'`

`MAX_FILTER_TIME = '2023-08-22 18:33:52'`

- `debug_mode=False` - Режим отладки (опциональный). В случае True выводит в консоль сообщения о ходе процесса (те же, что и в лог-файлы). По умолчанию: False

`uploader.py`

Функция `store_files_to_s3`

Параметры:

- `path_to_pictures` - Абсолютный путь к папке с изображениями (обязательный)
- `destination_bucket` - Хранилище-назначение (обязательный)
- `debug_mode=False` - Режим отладки (опциональный). В случае True выводит в консоль сообщения о ходе процесса (те же, что и в лог-файлы). По умолчанию: False

