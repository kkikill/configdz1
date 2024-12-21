****************************************************
# README
****************************************************

## Описание проекта

Этот проект представляет собой эмулятор командной строки, 
который имитирует работу операционной системы. Эмулятор работает с виртуальной файловой
системой и предоставляет базовые команды, такие как `ls`, `cd`, `exit`, `tail`, и `uniq`.
Проект предназначен для работы с `config.csv` конфигурационным файлом, содержащим параметры пути к 
виртуальной файловой системе и файлу журнала.

## Установка и использование
в config.csv пропишите:

username,fs_path,log_path
your_username,virtual_fs.tar.gz,log.xml

**Функционал:**
ls – выводит список файлов и директорий текущей директории.
cd – переходит в указанную директорию.
history — выводит историю последних команд.
uniq — выводит уникальные элементы из списка файлов и каталогов.
tail — выводит последние 10 элементов из списка файлов и каталогов.
exit — завершить работу эмулятора.