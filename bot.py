from telebot import TeleBot, types
from decouple import config
from parsing import main as parse
from utils import get_categories, get_last_page, get_products_by_category


token = config('TOKEN')
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Если хотите обновить данные /parse \nЕсли хотите увидеть каталог /catalog')

@bot.message_handler(commands=['parse'])
def update_db(message):
    bot.send_message(message.chat.id, 'начинаем парсинг...')
    parse()
    bot.send_message(message.chat.id, 'парсинг завершен')

@bot.message_handler(commands=['catalog'])
def get_catalog(message):
    # call_back = 'category='cat'&page=1&id=6'
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    categories = get_categories()
    for i in range(0, len(categories)+1, 3):
        buttons = []
        for j in range(3):
            if i+j == len(categories):
                break
            cat = categories[i+j]
            button = types.InlineKeyboardButton(cat, callback_data=f'category={cat}')
            buttons.append(button)
        keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Категории:', reply_markup=keyboard)

# @bot.message_handler(commands=['catalog2'])
# def get_catalog(message):
#     # call_back = 'category='cat'&page=1&id=6'
#     keyboard = types.InlineKeyboardMarkup()
#     categories = get_categories()
#     for cat in categories:
#         button = types.InlineKeyboardButton(cat, callback_data=f'category={cat}')
#         keyboard.add(button)
#     bot.send_message(message.chat.id, 'Категории:', reply_markup=keyboard)

def parse_params(callback_data):
    params = {}
    for items in callback_data.split('&'):
        key, value = items.split('=')
        params[key] = value
    # params = dict(x.split('=') for x in callback_data.split('&'))
    print(params)
    return params

@bot.callback_query_handler(func=lambda x: True)
def check_button(call):
    params = parse_params(call.data)
    if 'id' in params:
        send_product_details(call, params)
    else:
        send_products(call, params)

def send_products(call, params):
    category = params['category']
    page = int(params.get('page', 1))
    last_page = get_last_page(category)
    products = get_products_by_category(category, page)
    keyboard = types.InlineKeyboardMarkup()
    for id, product in enumerate(products):
        button = types.InlineKeyboardButton(
            product['title'], 
            callback_data=f'category={category}&page={page}&id={id}'
            )
        keyboard.add(button)
    
    buttons = []
    if page < last_page:
        button = types.InlineKeyboardButton(
            '>>', callback_data=f'category={category}&page={page+1}'
            )
        buttons.append(button)
    if page > 1:
        button = types.InlineKeyboardButton(
            '<<', callback_data=f'category={category}&page={page-1}'
        )
        buttons.append(button)
    keyboard.add(*buttons)

    bot.send_message(call.from_user.id, f'Страница: {page}', reply_markup=keyboard)


def send_product_details(call, params):
    category = params['category']
    page = int(params.get('page', 1))
    id = int(params['id'])
    products = get_products_by_category(category, page)
    product = products[id]

    bot.send_photo(call.from_user.id, product['image'])
    bot.send_message(call.from_user.id, f'Название: {product["title"]}\nЦена: {product["price"]}')


bot.polling() 