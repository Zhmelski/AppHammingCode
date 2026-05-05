import tkinter as tk
from tkinter import messagebox

# ================== Константы и матрицы ==================
ADMIN_PASSWORD = "admin123"

# Порождающая матрица кода (7,4) в систематической форме
G = [
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1]
]

# Проверочная матрица
H = [
    [0, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
]

# ========== Вспомогательные функции для кода Хэмминга ==========
def multiply_matrix_vector(matrix, vector):
    """Умножение матрицы (list of list) на вектор-столбец (list) по модулю 2."""
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for i in range(rows):
        s = 0
        for j in range(cols):
            s ^= (matrix[i][j] & vector[j])  # побитовое AND и XOR
        result.append(s)
    return result

def hamming_encode_block(data_bits):
    """
    Кодирует 4 информационных бита в 7 бит кода Хэмминга.
    data_bits: список из 4 целых чисел (0/1).
    Возвращает строку из 7 символов '0'/'1'.
    """
    d1, d2, d3, d4 = data_bits
    p1 = d2 ^ d3 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d1 ^ d2 ^ d4
    codeword = [d1, d2, d3, d4, p1, p2, p3]
    return ''.join(str(b) for b in codeword)

def hamming_decode_block(codeword_str):
    """
    Декодирует 7-битовое слово с исправлением однократной ошибки.
    codeword_str: строка из 7 символов '0'/'1'.
    Возвращает (data_str, corrected_flag), где
    data_str: 4 бита данных (строка '0'/'1'),
    corrected_flag: True, если ошибка была исправлена.
    """
    r = [int(ch) for ch in codeword_str]  # принятый вектор

    # Вычисление синдрома s = H * r^T
    s = multiply_matrix_vector(H, r)

    error_corrected = False
    if any(s):
        # Ищем столбец матрицы H, равный синдрому
        for col_idx in range(7):
            # столбец col_idx матрицы H
            col = [H[row][col_idx] for row in range(3)]
            if col == s:
                # Инвертируем бит с номером col_idx
                r[col_idx] ^= 1
                error_corrected = True
                break
        # Если синдром не найден (теоретически невозможно), оставляем как есть.

    # Извлекаем информационные биты (первые 4)
    data_bits = r[:4]
    return ''.join(str(b) for b in data_bits), error_corrected

# ========== Кодирование / декодирование фраз ==========
def encode_phrase(phrase):
    """
    Преобразует фразу в битовую строку (код Хэмминга (7,4)).
    Возвращает строку из '0' и '1'.
    """
    bit_string = ''
    for ch in phrase:
        # Байт символа в виде 8 бит (старший бит первый)
        bits = format(ord(ch), '08b')
        bit_string += bits

    # Разбиваем на блоки по 4 бита
    encoded = ''
    for i in range(0, len(bit_string), 4):
        block = bit_string[i:i+4]
        data = [int(b) for b in block]
        encoded += hamming_encode_block(data)
    return encoded

def decode_bits(bits_str):
    """
    Декодирует битовую строку (код Хэмминга) обратно во фразу.
    bits_str: строка только из '0' и '1' (пробелов нет).
    Возвращает (phrase, error_count).
    В случае ошибок формата выбрасывает ValueError.
    """
    # Убираем пробелы на всякий случай
    bits_str = bits_str.replace(' ', '')
    if len(bits_str) % 7 != 0:
        raise ValueError("Длина битовой последовательности не кратна 7")

    # Декодируем блоки по 7 бит
    data_blocks = []
    total_errors = 0
    for i in range(0, len(bits_str), 7):
        block = bits_str[i:i+7]
        data_bits, corrected = hamming_decode_block(block)
        data_blocks.append(data_bits)
        if corrected:
            total_errors += 1

    # Собираем все 4-битные блоки в одну строку
    all_data_bits = ''.join(data_blocks)
    if len(all_data_bits) % 8 != 0:
        raise ValueError("Ошибка: после декодирования длина данных не кратна 8")

    # Разбиваем на байты по 8 бит и преобразуем в символы
    chars = []
    for i in range(0, len(all_data_bits), 8):
        byte_bits = all_data_bits[i:i+8]
        code = int(byte_bits, 2)
        # Допустимые символы – печатные ASCII (32-126), но при декодировании
        # может получиться что угодно. Ограничимся проверкой диапазона.
        if 0 <= code <= 255:
            chars.append(chr(code))
        else:
            raise ValueError("Некорректный байт после декодирования")
    phrase = ''.join(chars)
    return phrase, total_errors

# ========== Валидация ==========
def is_valid_phrase(phrase):
    """Проверяет, что строка состоит из печатных ASCII (32-126) и не пуста."""
    if not phrase:
        return False
    return all(32 <= ord(c) <= 126 for c in phrase)

def is_valid_bit_sequence(s):
    """Проверяет, что строка состоит только из '0'/'1', непуста и длина кратна 7."""
    if not s:
        return False
    if not all(ch in '01' for ch in s):
        return False
    if len(s) % 7 != 0:
        return False
    return True

# ================== Основное приложение ==================
class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Студент")
        self.root.resizable(False, False)

        # Главное окно – студент
        self._create_student_ui()

    def _create_student_ui(self):
        # Рамка для компактности
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        # Поле битовой последовательности
        tk.Label(main_frame, text="Битовая последовательность:").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.bits_var = tk.StringVar()
        self.entry_bits = tk.Entry(main_frame, textvariable=self.bits_var, width=50)
        self.entry_bits.grid(row=1, column=0, padx=5, pady=5)

        # Поле фразы
        tk.Label(main_frame, text="Фраза:").grid(row=2, column=0, sticky="w", pady=(10,2))
        self.phrase_var = tk.StringVar()
        self.entry_phrase = tk.Entry(main_frame, textvariable=self.phrase_var, width=50)
        self.entry_phrase.grid(row=3, column=0, padx=5, pady=5)

        # Кнопки
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=20)
        tk.Button(btn_frame, text="Проверить", width=15, command=self._verify).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Администратор", width=15, command=self._admin_login).pack(side=tk.LEFT, padx=10)

    # ------------------- Логика проверки студента -------------------
    def _verify(self):
        bits_str = self.bits_var.get().strip()
        phrase_in = self.phrase_var.get()  # не strip() – пробелы могут быть значимыми

        # Проверка битовой последовательности
        if not is_valid_bit_sequence(bits_str):
            messagebox.showerror(
                "Ошибка",
                "Некорректная битовая последовательность. Разрешены только 0 и 1, длина должна быть кратна 7."
            )
            return

        # Проверка фразы
        if not is_valid_phrase(phrase_in):
            messagebox.showerror(
                "Ошибка",
                "Фраза содержит недопустимые символы. Разрешены латиница, цифры, пробел и знаки пунктуации."
            )
            return

        # Декодируем битовую строку
        try:
            decoded_phrase, _ = decode_bits(bits_str)
        except Exception as e:
            messagebox.showerror("Ошибка декодирования", str(e))
            return

        # Сравнение с учётом регистра
        if decoded_phrase == phrase_in:
            messagebox.showinfo("Результат", "Верно")
        else:
            messagebox.showinfo("Результат", "Неверно")

    # ------------------- Администратор: вход -------------------
    def _admin_login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Вход администратора")
        login_win.geometry("280x130")
        login_win.resizable(False, False)
        login_win.transient(self.root)
        login_win.grab_set()

        tk.Label(login_win, text="Пароль:").pack(pady=(15, 0))
        pwd_var = tk.StringVar()
        entry_pwd = tk.Entry(login_win, textvariable=pwd_var, show="*", width=25)
        entry_pwd.pack(pady=5)

        btn_frame = tk.Frame(login_win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Войти", width=10,
                  command=lambda: self._check_password(pwd_var.get(), login_win)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", width=10, command=login_win.destroy).pack(side=tk.LEFT, padx=5)

        entry_pwd.bind('<Return>', lambda event: self._check_password(pwd_var.get(), login_win))
        entry_pwd.focus_set()

    def _check_password(self, pwd, win):
        if pwd == ADMIN_PASSWORD:
            win.destroy()
            self._open_admin_window()
        else:
            messagebox.showerror("Ошибка", "Пароль неверный", parent=win)

    # ------------------- Окно администратора -------------------
    def _open_admin_window(self):
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Администратор")
        admin_win.geometry("700x350")
        admin_win.resizable(False, False)

        # Основной контейнер
        main_frame = tk.Frame(admin_win, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------- Левая часть: кодирование ----------
        left_frame = tk.LabelFrame(main_frame, text="Кодирование", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        tk.Label(left_frame, text="Фраза:").pack(anchor="w")
        phrase_admin_var = tk.StringVar()
        entry_phrase_admin = tk.Entry(left_frame, textvariable=phrase_admin_var, width=35)
        entry_phrase_admin.pack(fill=tk.X, pady=5)

        # Кнопка кодирования
        btn_encode = tk.Button(left_frame, text="→ Кодировать", command=self._encode_admin(
            phrase_admin_var, admin_win
        ))
        btn_encode.pack(pady=5)

        # Поле вывода битовой последовательности (нередактируемое)
        tk.Label(left_frame, text="Закодированная последовательность:").pack(anchor="w", pady=(5,0))
        encoded_var = tk.StringVar()
        entry_encoded = tk.Entry(left_frame, textvariable=encoded_var, state="readonly",
                                 width=35, readonlybackground="white")
        entry_encoded.pack(fill=tk.X, pady=5)

        # Кнопка копирования
        tk.Button(left_frame, text="📋 Копировать",
                  command=lambda: self._copy_to_clipboard(admin_win, encoded_var.get())
                  ).pack(pady=5)

        # ---------- Правая часть: декодирование ----------
        right_frame = tk.LabelFrame(main_frame, text="Декодирование", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="Битовая последовательность:").pack(anchor="w")
        bits_admin_var = tk.StringVar()
        entry_bits_admin = tk.Entry(right_frame, textvariable=bits_admin_var, width=35)
        entry_bits_admin.pack(fill=tk.X, pady=5)

        # Кнопка декодирования
        btn_decode = tk.Button(right_frame, text="→ Декодировать", command=self._decode_admin(
            bits_admin_var, admin_win
        ))
        btn_decode.pack(pady=5)

        # Поле вывода раскодированной фразы
        tk.Label(right_frame, text="Раскодированная фраза:").pack(anchor="w", pady=(5,0))
        decoded_var = tk.StringVar()
        entry_decoded = tk.Entry(right_frame, textvariable=decoded_var, state="readonly",
                                 width=35, readonlybackground="white")
        entry_decoded.pack(fill=tk.X, pady=5)

        # Кнопка копирования (копирует только чистую фразу, без пометок)
        tk.Button(right_frame, text="📋 Копировать",
                  command=lambda: self._copy_decoded_phrase(admin_win, decoded_var.get())
                  ).pack(pady=5)

    # ------------------- Вспомогательные методы для админки -------------------
    # Чтобы упростить доступ к полям админки, перепишем создание окна с сохранением ссылок.
    def _open_admin_window(self):
        # Создадим переменные заранее
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Администратор")
        admin_win.geometry("700x350")
        admin_win.resizable(False, False)

        main_frame = tk.Frame(admin_win, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------- Левая часть ----------
        left_frame = tk.LabelFrame(main_frame, text="Кодирование", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        tk.Label(left_frame, text="Фраза:").pack(anchor="w")
        phrase_admin_var = tk.StringVar()
        entry_phrase_admin = tk.Entry(left_frame, textvariable=phrase_admin_var, width=35)
        entry_phrase_admin.pack(fill=tk.X, pady=5)

        # Переменная для результата кодирования
        encoded_var = tk.StringVar()
        entry_encoded = tk.Entry(left_frame, textvariable=encoded_var, state="readonly",
                                 width=35, readonlybackground="white")
        entry_encoded.pack_forget()  # временно; разместим после кнопки

        # Кнопка кодирования
        def encode_handler():
            phrase = phrase_admin_var.get()
            if not is_valid_phrase(phrase):
                messagebox.showerror("Ошибка", "Фраза пуста или содержит недопустимые символы.", parent=admin_win)
                return
            try:
                bits = encode_phrase(phrase)
            except Exception as e:
                messagebox.showerror("Ошибка кодирования", str(e), parent=admin_win)
                return
            encoded_var.set(bits)

        btn_encode = tk.Button(left_frame, text="→ Кодировать", command=encode_handler)
        btn_encode.pack(pady=5)

        # Размещаем поле вывода и кнопку копирования
        tk.Label(left_frame, text="Закодированная последовательность:").pack(anchor="w", pady=(5,0))
        entry_encoded.pack(fill=tk.X, pady=5)

        def copy_encoded():
            self._copy_to_clipboard(admin_win, encoded_var.get())

        tk.Button(left_frame, text="📋 Копировать", command=copy_encoded).pack(pady=5)

        # ---------- Правая часть ----------
        right_frame = tk.LabelFrame(main_frame, text="Декодирование", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="Битовая последовательность:").pack(anchor="w")
        bits_admin_var = tk.StringVar()
        entry_bits_admin = tk.Entry(right_frame, textvariable=bits_admin_var, width=35)
        entry_bits_admin.pack(fill=tk.X, pady=5)

        decoded_var = tk.StringVar()
        entry_decoded = tk.Entry(right_frame, textvariable=decoded_var, state="readonly",
                                 width=35, readonlybackground="white")
        entry_decoded.pack_forget()

        def decode_handler():
            bits_str = bits_admin_var.get().strip()
            if not is_valid_bit_sequence(bits_str):
                messagebox.showerror(
                    "Ошибка",
                    "Некорректная битовая последовательность. Разрешены только 0 и 1, длина должна быть кратна 7.",
                    parent=admin_win
                )
                return
            try:
                phrase, err_count = decode_bits(bits_str)
            except Exception as e:
                messagebox.showerror("Ошибка декодирования", str(e), parent=admin_win)
                return

            if err_count > 0:
                if err_count == 1:
                    note = " (исправлена 1 ошибка)"
                else:
                    note = " (исправлены ошибки)"
            else:
                note = ""
            decoded_var.set(phrase + note)

        btn_decode = tk.Button(right_frame, text="→ Декодировать", command=decode_handler)
        btn_decode.pack(pady=5)

        tk.Label(right_frame, text="Раскодированная фраза:").pack(anchor="w", pady=(5,0))
        entry_decoded.pack(fill=tk.X, pady=5)

        def copy_decoded():
            # Копируем только чистую фразу (без текста об ошибках)
            full_text = decoded_var.get()
            # Убираем известные суффиксы
            for suffix in [" (исправлена 1 ошибка)", " (исправлены ошибки)"]:
                if full_text.endswith(suffix):
                    phrase_only = full_text[:-len(suffix)]
                    break
            else:
                phrase_only = full_text
            self._copy_to_clipboard(admin_win, phrase_only)

        tk.Button(right_frame, text="📋 Копировать", command=copy_decoded).pack(pady=5)

    def _copy_to_clipboard(self, win, text):
        """Копирует текст в системный буфер обмена."""
        win.clipboard_clear()
        win.clipboard_append(text)

    def run(self):
        self.root.mainloop()

# ================== Точка входа ==================
if __name__ == "__main__":
    app = Application()
    app.run()