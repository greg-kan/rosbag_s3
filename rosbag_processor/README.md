## ROSBAG files processor

OS: Linux

### Назначение:

Извлекает изображения из rosbag файлов, находящихся в папке на локальном диске и складывает их в другую локальную папку.

### Сборка:

Склонировать репозиторий:

#### git clone ...

Выполнить:

#### python3 -m pip install --upgrade pip
#### python3 -m pip install --upgrade build

Перейти в директорию с файлом pyproject.toml:

#### cd rosbag_s3/rosbag_processor

Выполнить:?

#### python3 -m build

Будет создана директория с дистрибутивом:

#### rosbag_s3/rosbag_processor/dist

В ней должны появиться два файла:

#### rosbag_processor-0.1.tar.gz
#### rosbag_processor-0.1-py3-none-any.whl

### Установка:

Создать виртуальную среду для программы - тестера, например:

#### rosbag_tester_env

Активировать её, например, в случае virtualenv:

#### workon rosbag_tester_env

Далее выполнить:

#### pip install rosbag_s3/rosbag_processor/dist/rosbag_processor-0.1-py3-none-any.whl

Будет установлен пакет rosbag_processor-0.1 с зависимостями.

Зависимости можно установить отдельно:

#### pip install bagpy
#### pip install opencv-python
#### pip install rosbags-image


### Использование:

В домашней директории создать папку

#### .rosbag_processor

с файлом конфигурации

#### conf.json внутри

Содержимое json:

#### {"log_file":"rosbag_processor", "bag_file_extension":".bag"}

Создать python - файл для запуска, например, main.py с содержимым:  

`from rosbag_processor import parser as pr`

`LOCAL_BAG_FILES_PATH = '/data1/s3/bg' #  Путь к расположению rosbag файлов. Обязательно`

`LOCAL_PICTURES_DESTINATION = '/data1/s3/pictures' #  Путь, куда будут извлечены картинки. Обязательно`

`#  Можно задать Топики rosbag файлов для фильтра (опционально):`

`TOPICS = ['/realsense_gripper/aligned_depth_to_color/image_raw', '/realsense_gripper/color/image_raw/compressed']`

`#  Можно задать временные интервалы rosbag файлов для фильтра (опционально):`

`MIN_FILTER_TIME = '2023-08-22 18:33:48'`

`MAX_FILTER_TIME = '2023-08-22 18:33:52'`

`#  Вызов парсера без фильтров:`

`pr.pars_files(LOCAL_BAG_FILES_PATH, LOCAL_PICTURES_DESTINATION)`

`#  Вызов парсера с фильтрами:`

`pr.pars_files(LOCAL_BAG_FILES_PATH, LOCAL_PICTURES_DESTINATION, topics=TOPICS, start_time=MIN_FILTER_TIME, end_time=MAX_FILTER_TIME)`

Запустить в созданной виртуальной среде:

#### (rosbag_tester_env) user@lws:~/rosbag_s3/rosbag_tester$ python3 main.py
