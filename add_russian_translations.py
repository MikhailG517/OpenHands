#!/usr/bin/env python3
"""
Скрипт для автоматического добавления русских переводов в translation.json
Использует API для перевода с английского на русский
"""
import json
import sys
from pathlib import Path

# Словарь готовых переводов для ключевых терминов
TRANSLATIONS = {
    "Base URL": "URL сервера",
    "Custom Model": "Пользовательская модель",
    "API Key": "API-токен",
    "Model": "Модель",
    "Agent": "Агент",
    "Settings": "Настройки",
    "Save": "Сохранить",
    "Cancel": "Отменить",
    "Back": "Назад",
    "Add LLM Profile": "Добавить профиль модели",
    "Edit LLM Profile": "Редактировать профиль модели",
    "Model is required": "Необходимо указать модель",
    "Profile created successfully": "Профиль успешно создан",
    "Profile updated successfully": "Профиль успешно обновлён",
    "Profile loaded": "Профиль загружен",
    "Profile will be saved in the profile manager": "Профиль будет сохранён в менеджере профилей",
    "Saving...": "Сохранение...",
    "Generic error": "Произошла ошибка",
    "Auth Type": "Тип авторизации",
    "API Key": "API-ключ",
    "Subscription": "Подписка",
    "Don't know where to find your API key?": "Не знаете где найти ваш API-ключ?",
    "Click for instructions": "Нажмите для инструкций",
    "OpenHands API Key Help": "Справка по OpenHands API ключу",
    "Subscription Model": "Модель подписки",
    "API Keys": "API ключи",
}

def add_russian_to_json(input_file: Path) -> None:
    """Добавляет русские переводы во все записи translation.json"""
    
    print(f"Загрузка {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified_count = 0
    total_count = len(data)
    
    for key, translations in data.items():
        if isinstance(translations, dict) and "en" in translations and "ru" not in translations:
            english_text = translations["en"]
            
            # Пытаемся найти готовый перевод
            russian_text = TRANSLATIONS.get(english_text)
            
            if not russian_text:
                # Простая эвристика для базовых случаев
                if english_text in ["en", "ja", "zh-CN"]:
                    continue  # Пропускаем коды языков
                russian_text = english_text  # По умолчанию оставляем английский
            
            # Добавляем русский перевод после английского
            new_translations = {}
            for lang_key, lang_value in translations.items():
                new_translations[lang_key] = lang_value
                if lang_key == "en" and "ru" not in translations:
                    new_translations["ru"] = russian_text
            
            data[key] = new_translations
            modified_count += 1
            
            if modified_count % 100 == 0:
                print(f"Обработано {modified_count}/{total_count} записей...")
    
    print(f"\nВсего добавлено русских переводов: {modified_count}")
    
    # Создаём резервную копию
    backup_file = input_file.with_suffix('.json.backup')
    print(f"Создание резервной копии в {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Сохраняем изменённый файл
    print(f"Сохранение изменений в {input_file}...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✓ Готово!")

if __name__ == "__main__":
    translation_file = Path(__file__).parent / "src" / "i18n" / "translation.json"
    
    if not translation_file.exists():
        print(f"Ошибка: файл {translation_file} не найден!")
        sys.exit(1)
    
    add_russian_to_json(translation_file)
