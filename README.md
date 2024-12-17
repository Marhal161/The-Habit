# Инструкция по настройке и запуску проекта

Этот документ содержит пошаговую инструкцию по созданию виртуального окружения, установке зависимостей и запуску приложения с использованием Buildozer.

## Предварительные требования

Убедитесь, что у вас установлено следующее:

*   **Python:**  Python 3.6 или более поздняя версия. Вы можете скачать Python с официального сайта: [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **pip:** Установщик пакетов Python. Обычно идет в комплекте с Python.
*   **virtualenv:** (Рекомендуется) Инструмент для создания изолированных виртуальных окружений. Установите его, если еще не установлен: `pip install virtualenv`
*   **Buildozer:** Инструмент для упаковки Python-приложений под Android.  Установите его, выполнив `pip install buildozer`.  Также необходимо будет установить ряд зависимостей, которые Buildozer предложит при первом запуске.

## Шаг 1: Создание виртуального окружения

1.  Перейдите в каталог вашего проекта в терминале:

    ```bash
    cd /путь/к/вашему/проекту
    ```

2.  Создайте виртуальное окружение (venv):

    ```bash
    python -m venv venv
    ```
    
    Здесь `venv` это имя вашей папки виртуального окружения. Вы можете выбрать другое имя.

3.  Активируйте виртуальное окружение:

    *   **Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    После активации вы увидите `(venv)` в начале строки терминала, что указывает на то, что вы работаете в виртуальном окружении.

## Шаг 2: Установка зависимостей

1.  Убедитесь, что у вас есть файл `requirements.txt` в корне вашего проекта. Если нет, создайте его и добавьте туда все необходимые библиотеки, которые использует ваш проект (например, `kivy`, `numpy`, `requests` и т.д.) по одному на строке.

2.  Установите зависимости, указанные в файле `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Шаг 3: Запуск приложения на сборку Buildozer

1.  Инициализируйте Buildozer (если это ваш первый запуск buildozer в данном проекте!!! Если уже создан то шаг 1 и 2 пропускаем!):

    ```bash
    buildozer init
    ```

    Эта команда создаст файл `buildozer.spec` в вашем проекте, в котором вы можете настроить параметры сборки.
2.  В файле `buildozer.spec` отредактируйте параметры `title`, `package.name`, `package.domain` и т.д., если это необходимо.

3.  Запустите сборку приложения в режиме отладки:

    ```bash
    buildozer -v android debug
    ```

    *   `-v` означает verbose режим (детальный вывод)
    *   `android` указывает на то, что вы хотите собрать приложение под Android
    *   `debug` указывает на то, что это отладочная сборка.

Buildozer начнет загрузку необходимых компонентов (SDK, NDK и др.), а затем скомпилирует ваше приложение. Процесс может занять некоторое время. После завершения сборки вы найдете файл `.apk` в каталоге `bin`.

## Дополнительно

*   **Проблемы при сборке:** Если у вас возникают проблемы при сборке, посмотрите на вывод терминала для получения подсказок. Часто ошибки связаны с неправильными настройками в `buildozer.spec`, отсутствующими пакетами или несовместимыми версиями.
*   **Обновление зависимостей:**  Когда вы меняете зависимости, обновите файл `requirements.txt` и установите их заново:
    
    ```bash
    pip freeze > requirements.txt
    pip install -r requirements.txt
    ```
    
    Первая команда запишет в `requirements.txt` все установленные пакеты, вторая обновит пакеты из `requirements.txt`.

*   **Выход из виртуального окружения:** Когда вы закончили работу, отключите виртуальное окружение, выполнив команду:
    ```bash
    deactivate
    ```

## Заключение

Следуя этой инструкции, вы сможете создать виртуальное окружение, установить зависимости и запустить ваше Python-приложение для Android.
Удачи!