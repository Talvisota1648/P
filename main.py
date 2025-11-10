import json
from collections import Counter
import re
import matplotlib.pyplot as plt
import os
import atexit

stop_words = set([
    'а', 'алло', 'без', 'близко', 'более', 'больше', 'будем', 'будет', 'будете', 'будешь',
    'будто', 'буду', 'будут', 'будь', 'бы', 'был', 'была', 'были', 'было', 'быть', 'в',
    'вам', 'вами', 'вас', 'весь', 'вдоль', 'вдруг', 'вместо', 'вне', 'вниз', 'внизу',
    'внутрь', 'вокруг', 'вот', 'впрочем', 'времени', 'всё', 'все', 'всегда', 'всего',
    'всем', 'всеми', 'всему', 'всех', 'всею', 'всю', 'вся', 'всюду', 'всякий', 'всяких',
    'всякого', 'всякое', 'всякой', 'всяком', 'всякую', 'г', 'где', 'да', 'давай', 'давать',
    'даже', 'для', 'до', 'должно', 'должный', 'другие', 'другой', 'другому', 'другую',
    'другая', 'два', 'две', 'двенадцать', 'двенадцати', 'двум', 'двух', 'десять', 'десяти',
    'е', 'его', 'ее', 'ей', 'ему', 'если', 'есть', 'еще', 'ею', 'ж', 'же', 'за', 'зачем',
    'здесь', 'затем', 'зато', 'значит', 'и', 'из', 'или', 'им', 'имеет', 'их', 'к', 'как',
    'какая', 'какие', 'какой', 'каком', 'какую', 'кем', 'когда', 'кто', 'ли', 'либо',
    'между', 'мне', 'мной', 'много', 'мог', 'может', 'можно', 'мой', 'моя', 'моё', 'мы',
    'на', 'над', 'надо', 'наконец', 'нам', 'нами', 'нас', 'наша', 'наше', 'нашего',
    'нашей', 'нашем', 'нашему', 'нашу', 'не', 'него', 'нее', 'ней', 'нем', 'нет', 'ни',
    'нибудь', 'никто', 'ним', 'них', 'ничто', 'но', 'ну', 'о', 'об', 'один', 'одна',
    'однако', 'одно', 'одной', 'одном', 'одному', 'одну', 'около', 'он', 'она', 'они',
    'оно', 'от', 'отчего', 'очень', 'перед', 'по', 'под', 'после', 'потом', 'потому',
    'почти', 'при', 'про', 'раз', 'разве', 'с', 'сам', 'сама', 'сами', 'само', 'самом',
    'самому', 'саму', 'себе', 'себя', 'сейчас', 'со', 'собой', 'собою', 'совсем', 'так',
    'также', 'такой', 'там', 'те', 'тебе', 'тебя', 'тем', 'теперь', 'то', 'тобой', 'тобою',
    'тогда', 'того', 'тоже', 'только', 'том', 'тот', 'тою', 'три', 'тут', 'ты', 'у',
    'уж', 'уже', 'хоть', 'хотя', 'чего', 'чей', 'чем', 'через', 'что', 'чтобы', 'чтоб',
    'чуть', 'эта', 'эти', 'это', 'этого', 'этой', 'этом', 'этому', 'эту', 'я'
])

def process_review(review_text):
    # Извлекаем только слова из букв (латинских и кириллических), игнорируя цифры, знаки и пунктуацию
    words = re.findall(r'[a-zа-яё]+', review_text.lower())
    # Фильтруем стоп-слова
    filtered_words = [word for word in words if word not in stop_words]
    total_words = len(filtered_words)
    # Получаем 3 самых частых слова с их частотами
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(3)
    return {
        "всего_слов": total_words,
        "топ_слова": [word for word, count in top_words],
        "топ_частоты": [count for word, count in top_words]  # Добавляем частоты для визуализации
    }

# Читаем файл с отзывами, где отзывы разделены пустыми строками
reviews = []
with open('reviews.txt', 'r', encoding='utf-8') as file:
    current_review = ''
    for line in file:
        if line.strip() == '':
            if current_review:
                reviews.append(current_review.strip())
                current_review = ''
        else:
            current_review += line
    if current_review:
        reviews.append(current_review.strip())

# Обрабатываем каждый отзыв
output = {}
processed_reviews = []
plot_files = []  # Список файлов для удаления
for i, review in enumerate(reviews, start=1):
    result = process_review(review)
    output[f"отзыв_{i}"] = {
        "всего_слов": result["всего_слов"],
        "топ_слова": result["топ_слова"]
    }
    processed_reviews.append((f"отзыв_{i}", result))

# Записываем результат в JSON файл
with open('final.json', 'w', encoding='utf-8') as json_file:
    json.dump(output, json_file, ensure_ascii=False, indent=4)

# Визуализация
# 1. Барчарт для общего количества слов в каждом отзыве
review_labels = [pr[0] for pr in processed_reviews]
total_words = [pr[1]["всего_слов"] for pr in processed_reviews]

plt.figure(figsize=(10, 5))
plt.bar(review_labels, total_words, color='skyblue')
plt.title('Количество слов в каждом отзыве')
plt.xlabel('Отзывы')
plt.ylabel('Количество слов')
plt.xticks(rotation=45)
plt.tight_layout()
total_words_file = 'total_words.png'
plt.savefig(total_words_file)  # Сохраняем график как изображение
plot_files.append(total_words_file)
plt.show()

# 2. Для каждого отзыва: барчарт топ-3 слов с частотами
for label, result in processed_reviews:
    if result["топ_слова"]:
        plt.figure(figsize=(8, 4))
        plt.bar(result["топ_слова"], result["топ_частоты"], color='lightgreen')
        plt.title(f'Топ-3 слова в {label}')
        plt.xlabel('Слова')
        plt.ylabel('Частота')
        plt.tight_layout()
        top_words_file = f'{label}_top_words.png'
        plt.savefig(top_words_file)  # Сохраняем каждый график
        plot_files.append(top_words_file)
        plt.show()

# Функция для очистки файлов
def cleanup_plots():
    for file in plot_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Удалён файл: {file}")

# Регистрируем функцию очистки при завершении программы
atexit.register(cleanup_plots)