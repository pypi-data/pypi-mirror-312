# DataGPT

DataGPT — это Python-пакет, упрощающий взаимодействие с OpenAI API и другими сервисами для создания и управления чатами с ИИ-ассистентом.

## Установка и использование
- Включите VPN (при необходимости)
- установить один pip-пакет `datagpt`
- Пример использования:
```python
from datagpt import chatgpt

# Замените 'OPENAI_API_KEY' на ваш действительный API-ключ, который можно получить на https://platform.openai.com/account/api-keys.
gpt = chatgpt.GPT("OPENAI_API_KEY")
# Замените 'ASSISTANT_ID' на уникальный идентификатор вашего ассистента, созданного на платформе OpenAI.
gpt.set_assistant_id("ASSISTANT_ID")

ret = gpt.new_chat_and_run("Какая  информация у вас есть?")
print(ret)
```