import json

# Load translation file
with open('src/i18n/translation.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Keys to add with base English values
new_keys = {
    "SETTINGS$DETECTING_PROVIDER": {
        "en": "Detecting provider",
        "ru": "Определение провайдера"
    },
    "SETTINGS$MODELS_FOUND": {
        "en": "models found",
        "ru": "моделей найдено"
    },
    "SETTINGS$AUTO_DETECT_PROVIDER": {
        "en": "Auto-detect Provider",
        "ru": "Автоопределение провайдера"
    },
    "SETTINGS$AUTO_DETECT_PROVIDER_HINT": {
        "en": "Automatically detect provider type and load available models",
        "ru": "Автоматически определить провайдера и загрузить список моделей"
    },
    "SETTINGS$DETECTING": {
        "en": "Detecting...",
        "ru": "Определение..."
    },
    "SETTINGS$PROVIDER_DETECTED": {
        "en": "Provider detected",
        "ru": "Провайдер определен"
    },
    "SETTINGS$PROVIDER_DETECTION_FAILED": {
        "en": "Provider detection failed",
        "ru": "Ошибка определения провайдера"
    }
}

# All languages in the project
languages = ["en", "ja", "zh-CN", "zh-TW", "ko-KR", "no", "ar", "de", "fr", "it", "pt", "es", "ca", "tr", "uk", "ru"]

# Add each key with all languages
for key, translations in new_keys.items():
    if key not in data:
        data[key] = {}
    
    # Add all languages, using English as fallback
    for lang in languages:
        if lang not in data[key]:
            data[key][lang] = translations.get(lang, translations["en"])

# Save back
with open('src/i18n/translation.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Added missing translation keys with all languages")
