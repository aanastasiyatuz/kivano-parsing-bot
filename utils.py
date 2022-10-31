import json

def get_db() -> dict:
    with open('db.json') as file:
        db = json.load(file)
    return db

def get_categories() -> list:
    db = get_db()
    return list(db.keys())

def get_products_by_category(category:str, page=1) -> list:
    """
    Принимает название категории и страницу

    Возвращает список с продуктами из данной категории на данной странице
    """
    db = get_db()
    if category in db:
        if str(page) in db[category]:
            return db[category][str(page)]

def get_last_page(category:str) -> int:
    """
    Принимает название категории

    Возвращает кол-во страниц в данной категории
    """
    db = get_db()
    if category in db:
        return len(db[category])
    # db[category] = {'1':[...], '2':[...], '3':[...]} 

