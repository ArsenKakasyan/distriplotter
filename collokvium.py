import random

# Количество вопросов на экзамен
total_questions = 35
# Количество вопросов в билете
questions_per_ticket = 3
# Количество студентов в аудитории
total_students = 23

# Генерация списка всех вопросов
all_questions = list(range(1, total_questions + 1))

# Распределение билетов для каждого студента
for student in range(1, total_students + 1):
    # Перемешивание списка вопросов
    random.shuffle(all_questions)
    # Выбор трех вопросов для билета студента
    ticket = all_questions[:questions_per_ticket]
    # Вывод номеров вопросов в билете студента
    print(f"Студент {student}: {ticket}")