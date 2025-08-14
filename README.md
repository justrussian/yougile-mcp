[![MSeeP.ai Security Assessment Badge](https://mseep.net/pr/justrussian-yougile-mcp-badge.png)](https://mseep.ai/app/justrussian-yougile-mcp)

# YouGile MCP Server

MCP сервер для интеграции с YouGile. Работает с любыми AI помощниками, поддерживающими протокол MCP (Claude Desktop, Continue, Cline и другие). Позволяет AI работать с вашими проектами, задачами и командой в YouGile.

## 🚀 Что умеет

### **Управление проектами**
- ✅ Создание и редактирование проектов
- ✅ Управление досками и колонками
- ✅ Работа с задачами (создание, обновление, комментарии)
- ✅ Управление командой (приглашения, роли)
- ✅ Отчеты и аналитика по проектам

### **Интеграция с AI помощниками**
- ✅ Автоматическое создание задач из разговора
- ✅ Умные отчеты по проектам
- ✅ Планирование спринтов
- ✅ Анализ продуктивности команды

## 📦 Установка

### 1. Скачайте проект
```bash
git clone https://github.com/justrussian/yougile-mcp.git
cd yougile-mcp
```

### 2. Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Получите данные YouGile

**Найдите свой email и пароль YouGile** - те же, что используете для входа на сайт.

**Получите ID компании:**
1. Войдите в [YouGile](https://yougile.com)
2. Нажмите `Ctrl + ~` для открытия конфигуратора
3. Перейдите во вкладку "Навигатор по объектам" справа
4. Нажмите на иконку информации (ℹ️) справа от названия вашей компании
5. Скопируйте ID компании из открывшегося окна

### 5. Настройте конфигурацию
```bash
cp .env.example .env
```

Отредактируйте файл `.env`:
```env
YOUGILE_EMAIL=ваш-email@yougile.com
YOUGILE_PASSWORD=ваш-пароль-от-yougile
YOUGILE_COMPANY_ID=ваш-company-id-из-url
```

### 6. Подключите к AI помощнику

**Для Claude Desktop - Автоматическая установка:**
```bash
python run_server.py  # Запустите один раз для проверки
# Если работает, установите в Claude Desktop:
uv run mcp install src/server.py --name "YouGile"
```

**Для любого MCP-совместимого AI (универсальный способ):**
```bash
cp mcp_config.json.example mcp_config.json
```

Отредактируйте `mcp_config.json`, укажите **полный путь** к вашей папке:
```json
{
  "mcpServers": {
    "yougile": {
      "command": "python",
      "args": ["/полный/путь/к/папке/yougile-mcp/run_server.py"],
      "cwd": "/полный/путь/к/папке/yougile-mcp",
      "env": {
        "PATH": "/полный/путь/к/папке/yougile-mcp/venv/bin:$PATH",
        "YOUGILE_BASE_URL": "https://yougile.com",
        "YOUGILE_EMAIL": "ваш-email@yougile.com",
        "YOUGILE_PASSWORD": "ваш-пароль",
        "YOUGILE_COMPANY_ID": "ваш-company-id"
      }
    }
  }
}
```

Добавьте этот JSON в конфигурацию вашего MCP-совместимого AI помощника (Claude Desktop, Continue, Cline и т.д.).

## 🎯 Как использовать с AI помощником

После подключения можно просить AI помощника:

### **Управление задачами**
- "Создай задачу 'Исправить баг с авторизацией' в проекте Мобильное приложение"
- "Покажи все мои задачи на сегодня"
- "Обнови статус задачи на 'В работе'"

### **Работа с проектами**
- "Создай новый проект 'Редизайн сайта'"
- "Покажи статистику по проекту за неделю"
- "Добавь пользователя ivan@company.com в проект"

### **Отчеты и планирование**
- "Сделай отчет по продуктивности команды"
- "Спланируй спринт на 2 недели"
- "Покажи, какие задачи просрочены"

## ⚙️ Диагностика проблем

### Проверка работы сервера
```bash
# Убедитесь что виртуальное окружение активировано
source venv/bin/activate  # На Windows: venv\Scripts\activate

python run_server.py
```
Должно показать: "🔑 Initializing YouGile authentication..." и подключиться к API.

### Частые ошибки

**"No module named 'mcp'"** - не активировано виртуальное окружение. Выполните `source venv/bin/activate`

**"No module named 'src'"** - запускайте через `python run_server.py`, не напрямую `src/server.py`

**"❌ Failed to initialize authentication"** - проверьте email, пароль и Company ID в `.env`

**"HTTP 401"** - неверные данные для входа в YouGile

**"HTTP 403"** - нет доступа к компании или API

### Получение помощи
Если что-то не работает:
1. Проверьте, что можете войти в YouGile через браузер с теми же данными
2. Убедитесь, что Company ID правильный (из URL после входа)
3. Попробуйте запустить `python run_server.py` и посмотрите на ошибки

## 🔒 Безопасность

- Все пароли хранятся только в вашем `.env` файле локально
- API ключ генерируется автоматически и тоже сохраняется локально
- Никакие данные не отправляются никуда, кроме YouGile API

## 👨‍💻 Автор

Проект разработан [HeadWise](https://headwise.ru) - Даниил Тарасенко

## 📄 Лицензия

Этот проект является открытым программным обеспечением.