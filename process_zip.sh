#!/bin/bash

# Получаем путь к ZIP-файлу
zip_path=$(realpath "$1")

# Указываем директорию для распаковки
DIRECTORY="/home/dsa-dgi/programs/pomidor/frontend/resettlement_department/"

echo "Processing file: $zip_path"
echo "Changing directory to: $DIRECTORY"

# Проверяем, существует ли указанная директория
if [ ! -d "$DIRECTORY" ]; then
    echo "Directory $DIRECTORY does not exist. Creating it..."
    mkdir -p "$DIRECTORY" || { echo "Failed to create directory $DIRECTORY"; exit 1; }
fi

# Переходим в указанную директорию
cd "$DIRECTORY" || { echo "Failed to change directory to $DIRECTORY"; exit 1; }

# Удаляем папку build, если она существует
if [ -d "build" ]; then
    echo "Removing existing 'build' directory"
    rm -r build
else
    echo "'build' directory does not exist"
fi

# Распаковываем ZIP-файл в эту директорию
echo "Unzipping file: $zip_path into $DIRECTORY"
unzip -o "$zip_path" || { echo "Failed to unzip $zip_path"; exit 1; }

echo "Unzip completed successfully in directory: $DIRECTORY"
echo "Done!"
