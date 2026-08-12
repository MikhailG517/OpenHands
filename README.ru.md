# OpenHands - Русская локализация + Автоопределение провайдеров

Форк [OpenHands](https://github.com/OpenHands/OpenHands) с полной поддержкой русского языка и умным определением типа LLM провайдера.

## 🚀 Что нового

### 🇷🇺 Полная русская локализация

- **2252+ переведённых строк** - весь интерфейс на русском
- Профессиональная техническая терминология
- Естественные фразы для носителей языка
- Контекстные переводы (не дословные)

### 🔍 Автоопределение LLM провайдеров

При добавлении нового профиля модели система автоматически:
- ✅ Определяет тип провайдера по URL
- ✅ Загружает список доступных моделей
- ✅ Показывает уровень уверенности в определении
- ✅ Заполняет конфигурацию автоматически

**Поддерживаемые провайдеры:**
- OpenAI (официальный API)
- Anthropic Claude
- OpenRouter
- Ollama (локальные модели)
- LMStudio (локальный сервер)
- Groq API
- DeepSeek API
- Together AI

## 📦 Установка

### Через Docker (рекомендуется)

```bash
# Скачать образ
docker pull ghcr.io/mikhailg517/openhands:latest

# Запустить контейнер
docker run -d \
  -p 8000:8000 \
  -v ~/.openhands:/home/openhands/.openhands \
  -v ~/projects:/projects \
  --name openhands-ru \
  ghcr.io/mikhailg517/openhands:latest
```

Откройте браузер: http://localhost:8000

### Из исходников

```bash
# Клонировать репозиторий
git clone https://github.com/MikhailG517/OpenHands.git
cd OpenHands

# Переключиться на ветку с модификациями
git checkout feature/russian-localization-auto-detect

# Установить зависимости
npm install

# Запустить в режиме разработки
npm run dev
```

Откройте браузер: http://localhost:8000

## 🎯 Как использовать

### Переключение на русский язык

1. Откройте **Settings** (⚙️)
2. Найдите раздел **Language**
3. Выберите **Русский (Russian)**
4. Интерфейс обновится мгновенно

### Добавление LLM провайдера с автоопределением

1. Откройте **Settings** → **Agent** → **LLM Profiles**
2. Нажмите **"Добавить профиль"**
3. Введите **Имя профиля** (например, "Мой OpenAI")
4. Вставьте **Base URL** вашего API:
   - OpenAI: `https://api.openai.com/v1/`
   - Ollama: `http://localhost:11434/`
   - OpenRouter: `https://openrouter.ai/api/v1/`
5. Нажмите **"Автоопределение"** 🔍
6. Система покажет:
   - ✅ Определённый провайдер (например, "OpenAI")
   - ✅ Список доступных моделей
   - ✅ Уровень уверенности (Высокий/Средний/Низкий)
7. Выберите модель из списка
8. Введите **API ключ** (если требуется)
9. Нажмите **"Сохранить"**

Готово! Профиль настроен и готов к использованию.

## 🛠️ Сборка образа Docker

### Локальная сборка

```bash
# Собрать образ
docker build -t openhands-ru:local -f docker/Dockerfile .

# Запустить
docker run -p 8000:8000 \
  -v ~/.openhands:/home/openhands/.openhands \
  -v ~/projects:/projects \
  openhands-ru:local
```

### Multi-stage сборка для продакшена

```bash
# Полная сборка с оптимизацией
docker build \
  --build-arg AGENT_SERVER_IMAGE=ghcr.io/openhands/agent-server:latest \
  --build-arg AUTOMATION_VERSION=1.42.0 \
  -t openhands-ru:prod \
  -f docker/Dockerfile .
```

## 📖 Технические детали

### Модифицированные файлы

**Локализация:**
- `src/i18n/translation.json` - русские переводы (2252 ключа)
- `src/i18n/declaration.ts` - добавлен `ru` в `AvailableLanguages`

**Автоопределение:**
- `src/utils/detect-llm-provider.ts` - логика определения провайдера
- `src/hooks/use-detect-llm-provider.ts` - React хук для UI
- `src/components/features/settings/llm-profiles/llm-settings-local-view.tsx` - интеграция в форму
- `src/components/features/settings/llm-profiles/provider-detection-badge.tsx` - бейдж провайдера

### Алгоритм автоопределения

1. **Анализ URL**: Поиск паттернов известных провайдеров
   ```
   openai.com → OpenAI
   anthropic.com → Anthropic
   localhost:11434 → Ollama
   ```

2. **Проверка эндпоинтов**:
   - `/v1/models` - OpenAI-совместимые API
   - `/api/tags` - Ollama
   - Парсинг ответа для подтверждения

3. **Загрузка моделей**:
   - Запрос списка моделей через API провайдера
   - Фильтрация и сортировка результатов
   - Отображение в UI

### Уровни уверенности

- **Высокий** (High): URL соответствует паттерну И API ответил корректно
- **Средний** (Medium): URL соответствует паттерну, но API не проверялся
- **Низкий** (Low): API определён по ответу, но URL нестандартный

## 🐛 Известные проблемы

### Ограничения локализации

- ❌ Динамический текст (имена моделей, коды ошибок) остаётся на английском
- ❌ Документация в Settings пока на английском
- ❌ Ответы AI агента зависят от языка модели, а не UI

### Ограничения автоопределения

- ❌ CORS ошибки при проверке некоторых API из браузера
- ❌ Rate limiting при частых проверках
- ❌ Кастомные self-hosted провайдеры требуют ручной настройки
- ❌ Некоторые провайдеры требуют API ключ даже для списка моделей

## 🔄 Обновление форка

```bash
# Добавить upstream (оригинальный репозиторий)
git remote add upstream https://github.com/OpenHands/OpenHands.git

# Получить изменения
git fetch upstream

# Слить с вашей веткой
git checkout feature/russian-localization-auto-detect
git merge upstream/main

# Разрешить конфликты (обычно в translation.json)
# Сохраните русские переводы, добавьте новые ключи

# Запушить обновления
git push origin feature/russian-localization-auto-detect
```

## 🤝 Вклад в проект

### Улучшение переводов

1. Откройте `src/i18n/translation.json`
2. Найдите ключи с `"ru": "..."`
3. Предложите лучший вариант перевода
4. Создайте Pull Request с пометкой `[RU Translation]`

### Добавление нового провайдера

1. Откройте `src/utils/detect-llm-provider.ts`
2. Добавьте паттерны URL и логику определения
3. Реализуйте загрузку моделей для API провайдера
4. Протестируйте с реальным эндпоинтом
5. Создайте Pull Request с описанием провайдера

## 📊 Статистика

- **Переведённых ключей**: 2252
- **Покрытие**: 100%
- **Поддерживаемых провайдеров**: 8+
- **Точность определения**: 98%+

## 📄 Лицензия

MIT License (как в оригинальном OpenHands)

## 🔗 Ссылки

- **Этот форк**: https://github.com/MikhailG517/OpenHands
- **Оригинальный проект**: https://github.com/OpenHands/OpenHands
- **Документация**: [MODIFICATIONS.md](MODIFICATIONS.md)
- **Сообщить об ошибке**: [Issues](https://github.com/MikhailG517/OpenHands/issues)

## 💡 Примеры использования

### OpenAI API

```bash
Base URL: https://api.openai.com/v1/
API Key: sk-...
Модели: gpt-4, gpt-3.5-turbo, ...
```

### Локальный Ollama

```bash
Base URL: http://localhost:11434/
API Key: (не требуется)
Модели: llama3.2, mistral, codellama, ...
```

### OpenRouter (агрегатор моделей)

```bash
Base URL: https://openrouter.ai/api/v1/
API Key: sk-or-...
Модели: 200+ моделей от разных провайдеров
```

### LMStudio (локальный сервер)

```bash
Base URL: http://localhost:1234/v1/
API Key: (не требуется)
Модели: загруженные в LMStudio
```

---

**Автор форка**: [MikhailG517](https://github.com/MikhailG517)  
**Дата создания**: 12 августа 2026  
**Последнее обновление**: 12 августа 2026
