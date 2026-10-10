import unittest


# ==========================================
# 1. ФУНКЦИИ ВАЛИДАЦИИ И ПРОВЕРКИ ДАННЫХ
# ==========================================
def validate_course_code(code: str) -> str:
    """Проверяет и возвращает код дисциплины."""
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Код дисциплины не должен быть пустым.")
    return code.strip().upper()


def validate_credits(credits: int) -> int:
    """Проверяет, что кредиты являются положительным целым числом (без учёта bool)."""
    if isinstance(credits, bool) or not isinstance(credits, int) or credits <= 0:
        raise ValueError("Количество кредитов должно быть положительным целым числом.")
    return credits


def validate_course(course: dict) -> dict:
    """Проверяет наличие и корректность полей словаря дисциплины."""
    if not isinstance(course, dict):
        raise TypeError("Запись дисциплины должна быть словарём.")
    
    required = {"code", "title", "credits"}
    missing = required - course.keys()
    if missing:
        raise ValueError(f"Отсутствуют обязательные поля: {sorted(missing)}")
    
    validated = {
        "code": validate_course_code(course["code"]),
        "title": str(course["title"]).strip(),
        "credits": validate_credits(course["credits"])
    }
    if not validated["title"]:
        raise ValueError("Название дисциплины не должно быть пустым.")
        
    return validated


# ==========================================
# 2. ПРЕДМЕТНЫЕ ВЫЧИСЛЕНИЯ И КОНТРАКТЫ
# ==========================================
def total_credits(courses: list) -> int:
    """Вычисляет общую сумму кредитов по списку курсов без изменения входного списка."""
    if not isinstance(courses, (list, tuple)):
        raise TypeError("Ожидается список или кортеж курсов.")
    
    sum_cr = 0
    for course in courses:
        validated = validate_course(course)
        sum_cr += validated["credits"]
    return sum_cr


def can_enroll(current_credits: int, new_course_credits: int, max_limit: int = 30) -> bool:
    """Определяет, можно ли добавить новый курс, не превышая лимит кредитов."""
    if not isinstance(current_credits, int) or not isinstance(new_course_credits, int) or not isinstance(max_limit, int):
        raise TypeError("Значения кредитов и лимита должны быть целыми числами.")
    return (current_credits + new_course_credits) <= max_limit


# ==========================================
# 3. ФОРМАТИРОВАНИЕ И ПРЕДСТАВЛЕНИЕ (без print)
# ==========================================
def format_plan(student_name: str, enrolled_courses: list, max_limit: int = 30) -> str:
    """Формирует текстовый отчёт по плану регистрации студента."""
    if not isinstance(student_name, str) or not student_name.strip():
        raise ValueError("Имя студента не должно быть пустым.")
    
    lines = [f"План регистрации студента: {student_name.strip()}"]
    sum_cr = 0
    
    for idx, course in enumerate(enrolled_courses, start=1):
        v_course = validate_course(course)
        sum_cr += v_course["credits"]
        lines.append(f"{idx}. [{v_course['code']}] {v_course['title']} — {v_course['credits']} кредитов")
    
    lines.append(f"Итого кредитов: {sum_cr} из {max_limit} возможных.")
    return "\n".join(lines)


# ==========================================
# 4. АВТОМАТИЧЕСКИЕ ТЕСТЫ (unittest)
# ==========================================
class RegistrationProcedureTests(unittest.TestCase):
    
    def test_total_credits_calculation(self):
        """Тест 1: Корректный подсчет суммы кредитов."""
        courses = [
            {"code": "IS-101", "title": "Парадигмы программирования", "credits": 5},
            {"code": "DB-201", "title": "Базы данных", "credits": 6}
        ]
        self.assertEqual(total_credits(courses), 11)

    def test_can_enroll_boundary_and_limit(self):
        """Тест 2: Проверка граничных условий лимита кредитов (30)."""
        self.assertTrue(can_enroll(25, 5, 30))
        self.assertFalse(can_enroll(28, 4, 30))

    def test_invalid_credits_raises_error(self):
        """Тест 3 (Ошибочный сценарий): Нулевые или отрицательные кредиты."""
        with self.assertRaises(ValueError):
            validate_credits(0)
        with self.assertRaises(ValueError):
            validate_credits(-5)

    def test_bool_as_credits_raises_error(self):
        """Тест 4 (Ошибочный сценарий): Передача bool вместо числа кредитов."""
        with self.assertRaises(ValueError):
            validate_credits(True)  # type: ignore

    def test_input_collection_is_not_modified(self):
        """Тест 5: Функции вычислений не изменяют исходные коллекции."""
        source = [{"code": "AI-301", "title": "ИИ", "credits": 4}]
        backup = [{"code": "AI-301", "title": "ИИ", "credits": 4}]
        total_credits(source)
        self.assertEqual(source, backup)

    def test_format_plan_generation(self):
        """Тест 6: Корректное формирование текстового отчета."""
        courses = [{"code": "MATH-101", "title": "Высшая математика", "credits": 5}]
        report = format_plan("Алиса", courses)
        self.assertIn("Алиса", report)
        self.assertIn("MATH-101", report)
        self.assertIn("5 кредитов", report)


# ==========================================
# 5. ТОЧКА ВХОДА (MAIN)
# ==========================================
def load_demo_catalog() -> list:
    """Демонстрационные данные каталога дисциплин."""
    return [
        {"code": "IS-101", "title": "Парадигмы программирования", "credits": 5},
        {"code": "DB-201", "title": "Базы данных", "credits": 6},
        {"code": "WEB-302", "title": "Web-технологии", "credits": 4}
    ]


def main():
    """Координация выполнения программы и вывод результатов."""
    print("=== ДЕМОНСТРАЦИЯ ПРОЦЕДУРНОЙ ПРОГРАММЫ (Вариант 2) ===")
    catalog = load_demo_catalog()
    
    # Имитируем процесс выбора курсов студентом
    selected_courses = [catalog[0], catalog[1]]
    
    # Проверяем лимит перед добавлением третьего курса
    max_credits_limit = 30
    current_sum = total_credits(selected_courses)
    
    print(f"Текущая сумма кредитов: {current_sum}")
    
    extra_course = catalog[2]
    if can_enroll(current_sum, extra_course["credits"], max_credits_limit):
        selected_courses.append(extra_course)
        print( курс '{extra_course['title']}' успешно добавлен.")
    else:
        print(f"Нельзя добавить курс: превышен лимит в {max_credits_limit} кредитов.")

    # Выводим отчет через непечатающую функцию форматирования
    print("\n" + format_plan("Дильназ", selected_courses, max_credits_limit))
    
    print("\n=== ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ ===")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    main()