#!/usr/bin/env python3
"""
Улучшенные русские переводы для UI настроек моделей
"""

import json
from pathlib import Path

# Расширенный словарь качественных переводов
QUALITY_TRANSLATIONS = {
    # Основные элементы UI
    "No results found": "Результаты не найдены",
    "Results truncated": "Результаты сокращены",
    "Pattern:": "Шаблон:",
    "Include:": "Включить:",
    
    # Настройки LLM
    "LLM Settings": "Настройки языковых моделей",
    "Model Provider": "Провайдер модели",
    "Select Provider": "Выберите провайдер",
    "Profile name": "Название профиля",
    "Profile Name": "Название профиля",
    
    # Технические параметры
    "Temperature": "Температура (креативность)",
    "Max Tokens": "Максимум токенов",
    "Top P": "Top P (разнообразие)",
    "Frequency Penalty": "Штраф за повторы",
    "Presence Penalty": "Штраф за темы",
    
    # Действия
    "Add Profile": "Добавить профиль",
    "Edit Profile": "Изменить профиль",
    "Delete Profile": "Удалить профиль",
    "Test Connection": "Проверить соединение",
    "Auto-detect": "Автоопределение",
    "Detecting...": "Определение...",
    
    # Провайдеры
    "OpenAI": "OpenAI",
    "Anthropic": "Anthropic",
    "Azure": "Azure",
    "Ollama": "Ollama",
    "Custom": "Пользовательский",
    
    # Сообщения
    "Profile saved successfully": "Профиль успешно сохранён",
    "Failed to save profile": "Не удалось сохранить профиль",
    "Connection successful": "Подключение успешно",
    "Connection failed": "Подключение не удалось",
    "Auto-detection successful": "Автоопределение успешно",
    "Failed to detect API type": "Не удалось определить тип API",
    
    # Подсказки
    "Enter your API key": "Введите ваш API ключ",
    "Enter the base URL": "Введите базовый URL сервера",
    "Enter the model name": "Введите название модели",
    "Optional custom endpoint": "Дополнительный пользовательский endpoint",
    
    # Task/Subagent
    "Subagent:": "Подагент:",
    "Task ID:": "ID задачи:",
}

def improve_translations(json_file: Path):
    """Улучшает качество русских переводов"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    improved_count = 0
    
    for key, translations in data.items():
        if isinstance(translations, dict) and 'en' in translations and 'ru' in translations:
            en_text = translations['en']
            ru_text = translations['ru']
            
            # Если есть улучшенный перевод
            if en_text in QUALITY_TRANSLATIONS:
                better_translation = QUALITY_TRANSLATIONS[en_text]
                
                # Если текущий перевод совпадает с английским или хуже
                if ru_text == en_text or better_translation != ru_text:
                    translations['ru'] = better_translation
                    improved_count += 1
                    print(f"Improved: {key}")
                    print(f"  Old: '{ru_text}'")
                    print(f"  New: '{better_translation}'")
                    print()
    
    # Сохраняем
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal improved: {improved_count} translations")

if __name__ == '__main__':
    json_path = Path(__file__).parent / 'src' / 'i18n' / 'translation.json'
    improve_translations(json_path)
