# тестовое задание на стажировку VK
### Реализовано:
1. Консольное приложение (CLI/cli.py), функционал которого: валидация JSON схем, генерация pydantic модели (через её JSON схему), генерация REST контроллеров для документов (представленных в JSON)
2. Создана таблица Apps c помощью SqlAlchemy (Postgres), находится в db/create_table.py (db/config.py - данные для подключения к Postgres)
3. C помощью cli сгенерирована модель Example (generated_model.py) на основе её JSON схемы (CLI/example_schema.json) и REST контроллеры (generated_rest.py) для документа (CLI/example_schema.json), соответствующего этой схеме (валидация идёт в запросе с помощью FastApi по сгенерированной модели).

версия питона 3.10

### От себя:
Спасибо за интересное задание! Был бы рад услышать фидбек, а ещё хотел бы задать некоторые вопросы по заданию, но не нашёл куда (кажется в самой тестовой системе есть возможность задать вопрос только по самой тестовой системе).
