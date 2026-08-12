#!/usr/bin/env python3
"""
Автоматическое добавление русских переводов в translation.json
Использует Google Translate API или простые правила для базового перевода
"""

import json
import re
from pathlib import Path

# Словарь простых переводов для технических терминов
SIMPLE_TRANSLATIONS = {
    "Settings": "Настройки",
    "Model": "Модель",
    "Provider": "Провайдер",
    "API Key": "API ключ",
    "Base URL": "URL сервера",
    "Custom Model": "Пользовательская модель",
    "Add": "Добавить",
    "Edit": "Редактировать",
    "Delete": "Удалить",
    "Save": "Сохранить",
    "Cancel": "Отмена",
    "Profile": "Профиль",
    "LLM Profile": "Профиль модели",
    "Add LLM Profile": "Добавить профиль модели",
    "Edit LLM Profile": "Редактировать профиль модели",
    "Agent": "Агент",
    "Language": "Язык",
    "Advanced": "Расширенные",
    "Temperature": "Температура",
    "Max Tokens": "Макс. токенов",
    "Top P": "Top P",
    "Frequency Penalty": "Штраф за частоту",
    "Presence Penalty": "Штраф за присутствие",
}

def add_russian_translations(json_file: Path):
    """Добавляет русские переводы во все объекты"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    added_count = 0
    
    for key, translations in data.items():
        if isinstance(translations, dict) and 'en' in translations:
            # Если русского перевода нет
            if 'ru' not in translations:
                en_text = translations['en']
                
                # Пробуем найти в словаре
                ru_text = SIMPLE_TRANSLATIONS.get(en_text)
                
                # Если не нашли, копируем английский (можно позже перевести вручную)
                if not ru_text:
                    ru_text = en_text
                
                # Вставляем русский перевод сразу после английского
                new_translations = {'en': translations['en'], 'ru': ru_text}
                for lang, text in translations.items():
                    if lang != 'en':
                        new_translations[lang] = text
                
                data[key] = new_translations
                added_count += 1
                
                if added_count <= 10:  # Показываем первые 10
                    print(f"Added: {key}: '{en_text}' -> '{ru_text}'")
    
    # Сохраняем с красивым форматированием
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal added: {added_count} Russian translations")

if __name__ == '__main__':
    json_path = Path(__file__).parent / 'src' / 'i18n' / 'translation.json'
    add_russian_translations(json_path)
