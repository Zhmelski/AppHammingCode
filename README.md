# Код Хэмминга (7,4) — лабораторное приложение

**Версия:** 1.0  
**Язык:** Python 3  
**Интерфейс:** Tkinter (стандартная библиотека)

---

## Русская версия

### О проекте
Приложение реализует кодирование и декодирование фраз классическим кодом Хэмминга (7,4) с исправлением однократной ошибки. Предназначено для проведения лабораторных работ по дисциплине «Статистическая радиофизика и теория информации». Поддерживает две роли: **студент** (проверка самостоятельно раскодированной фразы) и **преподаватель** (кодирование/декодирование без раскрытия ответа студенту).

### Возможности
- Кодирование текстовой фразы (ASCII, печатные символы) в битовую последовательность кодом (7,4).
- Декодирование битовой строки с автоматическим исправлением однократной ошибки.
- Интерфейс студента: ввод битовой последовательности и предполагаемой фразы, скрытая проверка совпадения (без отображения правильного ответа).
- Интерфейс преподавателя (по паролю): кодирование фразы и копирование результата, декодирование битовой строки с отображением раскодированного сообщения и информацией об исправленных ошибках.
- Валидация вводимых данных (допустимые символы, кратность длины последовательности 7).
- Системный буфер обмена для быстрого копирования результатов.

### Требования
- Python 3.6 или новее.
- Стандартная библиотека Tkinter (обычно входит в состав Python; в некоторых Linux-дистрибутивах может потребоваться отдельная установка пакета `python3-tk`).

### Запуск
```bash
python AppEncodeDecode.py
```
(предполагается, что файл с кодом называется `AppEncodeDecode.py`; при необходимости переименуйте).

### Использование

#### Роль «Студент»
1. Откройте главное окно «Студент».
2. В поле **«Битовая последовательность»** вставьте (или введите вручную) строку из `0` и `1`, полученную от преподавателя.
3. В поле **«Фраза»** введите свой вариант раскодированной фразы.
4. Нажмите **«Проверить»**.
5. При совпадении появится сообщение «Верно», иначе — «Неверно». Сама расшифрованная последовательность не отображается.

#### Роль «Преподаватель»
1. Нажмите кнопку **«Администратор»**, введите пароль (по умолчанию `admin123`).
2. В открывшемся окне:
   - **Кодирование**  
     Введите фразу, нажмите **«→ Кодировать»**. Выходная битовая строка появится в нижнем поле. Кнопка **«📋 Копировать»** поместит её в буфер обмена.
   - **Декодирование**  
     Введите битовую строку (возможны однократные ошибки), нажмите **«→ Декодировать»**. Раскодированная фраза отобразится с пометкой `(исправлена 1 ошибка)`, если была произведена корректировка. Кнопка копирования копирует только чистую фразу (без пометки).

### Настройка пароля
Измените значение константы `ADMIN_PASSWORD` в коде (строка `admin123`). Для лабораторных работ хеширование не используется.

### Структура кода
- `G` и `H` — порождающая и проверочная матрицы кода Хэмминга (7,4).
- `multiply_matrix_vector()` — умножение матрицы на вектор по модулю 2.
- `hamming_encode_block()` — кодирование 4 бит в 7.
- `hamming_decode_block()` — декодирование 7 бит с коррекцией одиночной ошибки.
- `encode_phrase()`, `decode_bits()` — преобразование фразы целиком.
- Валидация: `is_valid_phrase()`, `is_valid_bit_sequence()`.
- Класс `Application` содержит GUI и логику взаимодействия.

### Ограничения
- Поддерживаются только печатные ASCII-символы (коды 32–126).
- Длина битовой последовательности должна быть кратна 7.
- Код Хэмминга (7,4) исправляет только **одну** ошибку в каждом 7-битном блоке.

---

## English Version

### About the Project
This application implements encoding and decoding of text phrases using the classical Hamming code (7,4) with single-error correction. It is designed for lab sessions in the course «Statistical Radiophysics and Information Theory». Two roles are supported: **student** (self-check of a manually decoded phrase) and **instructor** (encoding/decoding without revealing the answer to the student).

### Features
- Encode a text phrase (printable ASCII characters) into a bit string using the (7,4) code.
- Decode a bit string with automatic correction of a single-bit error.
- Student interface: enter a bit sequence and a guessed phrase; the program silently checks if they match (the correct answer is never shown).
- Instructor interface (password-protected): encode a phrase and copy the result; decode a bit string and display the recovered text along with error-correction information.
- Input validation (allowed characters, bit-string length divisible by 7).
- System clipboard support for quick copying of results.

### Requirements
- Python 3.6 or newer.
- Tkinter (usually bundled with Python; on some Linux distributions you may need to install `python3-tk`).

### Running the application
```bash
python AppEncodeDecode.py
```
(assuming the source file is named `AppEncodeDecode.py`; rename if needed).

### Usage

#### Student role
1. Open the «Student» main window.
2. In the **«Битовая последовательность»** (Bit sequence) field, paste (or type) the `0`/`1` string received from the instructor.
3. In the **«Фраза»** (Phrase) field, type your guess for the decoded phrase.
4. Click **«Проверить»** (Check).
5. If the decoded phrase matches your guess, «Верно» (Correct) pops up; otherwise «Неверно» (Incorrect). The decoded text itself is **not** displayed.

#### Instructor role
1. Click **«Администратор»** (Administrator) and enter the password (default: `admin123`).
2. In the new window:
   - **Кодирование (Encoding)**  
     Type a phrase, click **«→ Кодировать»**. The resulting bit string appears in the read-only field below. **«📋 Копировать»** copies it to the clipboard.
   - **Декодирование (Decoding)**  
     Enter a bit string (it may contain single-bit errors), click **«→ Декодировать»**. The decoded phrase is shown, with a note `(исправлена 1 ошибка)` if an error was corrected. The copy button copies only the clean phrase (without the note).

### Password configuration
Change the `ADMIN_PASSWORD` constant in the source code (current default: `admin123`). For lab use, no password hashing is implemented.

### Code structure
- `G` and `H` — generator and parity-check matrices of the (7,4) Hamming code.
- `multiply_matrix_vector()` — binary matrix-vector multiplication.
- `hamming_encode_block()` — encode 4 data bits into 7 code bits.
- `hamming_decode_block()` — decode 7 code bits with single-error correction.
- `encode_phrase()`, `decode_bits()` — whole-phrase conversion.
- Validation functions: `is_valid_phrase()`, `is_valid_bit_sequence()`.
- The `Application` class contains the GUI and interaction logic.

### Limitations
- Only printable ASCII characters (codes 32–126) are supported.
- The length of the input bit string must be a multiple of 7.
- The (7,4) Hamming code corrects **one** error per 7-bit block; multiple errors may lead to incorrect decoding.