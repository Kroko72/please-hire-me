# тестовое задание на стажировку VK
### Реализовано:
1. Консольное приложение (```CLI/cli.py```), функционал которого: валидация JSON схем, генерация pydantic модели (через её JSON схему), генерация REST контроллеров для документов (представленных в JSON)
2. Создана таблица Apps c помощью SqlAlchemy (Postgres), находится в db/create_table.py (```db/config.py``` - данные для подключения к Postgres)
3. C помощью cli сгенерирована модель Example (```generated_model.py```) на основе её JSON схемы (```CLI/example_schema.json```) и REST контроллеры (```generated_rest.py```) для документа (```CLI/example_schema.json```), соответствующего этой схеме (валидация идёт в запросе с помощью FastApi по сгенерированной модели).

### Использование:
версия питона 3.10. Не стал делать приём аргументов из терминала, т.к. мне было легче тестировать из ide (в задании написано, что это пример, поэтому подумал, что это не требуется), в ```CLI/cli.py``` в блоке ```if __name__ == ""__main__""``` есть обычный вызов функций генерации модели и контроллеров. Перед этим нужно запустить ```db/create_table.py``` чтобы создать таблицу в бд (подразумевается что ваши данные для постгреса записаны в файле ```db/config.py```).

### От себя:
Спасибо за интересное задание! Был бы рад услышать фидбек, а ещё хотел бы задать некоторые вопросы по заданию, но не нашёл куда (кажется в самой тестовой системе есть возможность задать вопрос только по самой тестовой системе).
С кубером и кафкой на практике столкнулся впервые, не успел реализовать работу с ними (до этого только знал что это и зачем, но дело не имел).
