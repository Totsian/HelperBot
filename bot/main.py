import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

API_TOKEN = TOKEN

bot = Bot(
    token=API_TOKEN,
    parse_mode=types.ParseMode.HTML,
)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
conn = sqlite3.connect('helper.db')
c = conn.cursor()


class Form(StatesGroup):
    new_idea = State()
    del_idea = State()
    new_film = State()
    del_film = State()
    new_todo = State()
    del_todo = State()
    new_contact = State()
    del_contact = State()
    new_book = State()
    del_book = State()
    new_link = State()
    del_link = State()


def read_txt(filename):
    f_text = ''
    with open(filename, encoding='utf8') as file:
        f = file.readlines()
        for i in f:
            f_text += i
    return f_text


def add_user(user_id: int, username: str, first_name: str, last_name: str):
    c.execute('''SELECT user_id FROM user_inf''')
    user_list = []
    for i in c.fetchall():
        user_list += list(i)
    if user_id not in user_list:
        c.execute('''INSERT INTO user_inf(user_id, username, first_name, last_name) VALUES(?,?,?,?)''',
                  (user_id, username, first_name, last_name))
        conn.commit()
    else:
        print('Уже зарегистрирован.')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        text=read_txt('welcome.txt'),
    )
    user = message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    add_user(user_id=user_id, username=username, first_name=first_name, last_name=last_name)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(
        text=read_txt('main_func.txt'),
    )


def get_keyboard_idea():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="idea_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="idea_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="idea_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="idea_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


# если на вход приъодит команда /idea, срабатывет данный блок кода
@dp.message_handler(commands=['idea'])
async def idea_m(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_idea(),
    )


# функция, которая вытаскивает данные из базы данных и в случае, если что-то записано, выводит данные,
# если не записано - приходит сообщение 'Пока не записана ни одна идея.'
async def set_idea(message: types.Message, user_id: int):
    c.execute('''SELECT user_idea FROM ideas WHERE user_id=?''', (user_id,))
    ideas = c.fetchall()
    if len(ideas) == 0:
        await message.answer('Пока не записана ни одна идея.')
    else:
        n = 1
        ideas_list = []
        ideas_in_str = ''
        for i in ideas:
            ideas_list += list(i)

        for i in ideas_list:
            ideas_in_str += str(n) + '. ' + i + '\n'
            n += 1
        await message.answer('<b>Список идей:</b>\n' + ideas_in_str)


# функция, которая записывает сообщение пользователя в базу данных
@dp.message_handler(state=Form.new_idea)
async def get_idea(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_idea'] = message.text
        user_idea = message.from_user
        user_id = user_idea.id
        user_date = message.date
        idea_n = data['new_idea']
        c.execute('''INSERT INTO ideas VALUES(?,?,?)''', (user_id, user_date, idea_n))
        conn.commit()
        await message.reply('Идея записана!')
    await state.finish()


# функция лоя удаления записи по её порядковому номеру
# польщователь может просмотреть спикос записей и ввести номера записей, которые он хочет удалить
@dp.message_handler(state=Form.del_idea)
async def delete_idea(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_idea'] = message.text
        user_id = message.from_user.id
        num = data['del_idea']
        num = num.replace(' ', '')
        new_num = num.split(',')
        list_num = []
        c.execute('''SELECT user_idea FROM ideas WHERE user_id=?''', (user_id,))
        ideas = c.fetchall()
        len_id = len(ideas)
        for i in new_num:
            if i.isdigit() and int(i) <= len_id:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = ideas[k - 1]
                c.execute('''DELETE FROM ideas WHERE user_idea=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


# функция, которая обрабатывает, какая кнопка была нажата
@dp.callback_query_handler(Text(startswith="idea_"), state='*')
async def callback_idea(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_idea(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже свою идею.')
        await Form.new_idea.set()
    elif action == 'delete':
        await Form.del_idea.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await call.message.answer('Изменения прерваны.')
    await call.answer()


def get_keyboard_film():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="film_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="film_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="film_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="film_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['film'])
async def film(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_film(),
    )


async def set_film(message: types.Message, user_id: int):
    c.execute('''SELECT film FROM films WHERE user_id=?''', (user_id,))
    films = c.fetchall()
    if len(films) == 0:
        await message.edit_text('Пока не записан ни один фильм.')
    else:
        n = 1
        films_list = []
        films_in_str = ''
        for i in films:
            films_list += list(i)
        for i in films_list:
            films_in_str += str(n) + '. ' + i + '\n'
            n += 1
        await message.answer('<b>Список фильмов:\n</b>' + films_in_str)


@dp.message_handler(state=Form.new_film)
async def get_film(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_film'] = message.text
        user_film = message.from_user
        user_id = user_film.id
        user_date = message.date
        film_n = data['new_film']
        c.execute('''SELECT film FROM films WHERE user_id=?''', (user_id,))
        contacts = c.fetchall()
        film_list = []
        for i in contacts:
            film_list += list(i)
        if film_n in film_list:
            await message.reply('Такой фильм уже записан.')
        else:
            c.execute('''INSERT INTO films VALUES(?,?,?)''', (user_id, user_date, film_n))
            conn.commit()
            await message.answer('Фильм записан!')
    await state.finish()


@dp.message_handler(state=Form.del_film)
async def delete_film(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_film'] = message.text
        user_id = message.from_user.id
        num = data['del_film']
        num = num.replace(' ', '')
        new_num = num.split(',')
        list_num = []
        c.execute('''SELECT film FROM films WHERE user_id=?''', (user_id,))
        films = c.fetchall()
        len_f = len(films)
        for i in new_num:
            if i.isdigit() and int(i) <= len_f:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = films[k - 1]
                c.execute('''DELETE FROM films WHERE film=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


@dp.callback_query_handler(Text(startswith="film_"), state='*')
async def callback_film(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_film(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже название фильма.')
        await Form.new_film.set()
    elif action == 'delete':
        await Form.del_film.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await call.message.answer('Изменения прерваны.')
    await call.answer()


def get_keyboard_todo():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="todo_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="todo_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="todo_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="todo_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['to_do'])
async def to_do(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_todo(),
    )


async def set_to_do(message: types.Message, user_id: int):
    c.execute('''SELECT to_do FROM to_do_list WHERE user_id=?''', (user_id,))
    todo = c.fetchall()
    if len(todo) == 0:
        await message.answer('Пока ничего не записано')
    else:
        n = 1
        todo_list = []
        todo_str = ''
        for i in todo:
            todo_list += list(i)
        for i in todo_list:
            todo_str += str(n) + '. ' + i + '\n'
            n += 1
        await message.answer('<b>Список дел:</b>\n' + todo_str)


@dp.message_handler(state=Form.new_todo)
async def get_to_do(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_todo'] = message.text
        user_todo = message.from_user
        user_id = user_todo.id
        user_date = message.date
        todo_n = data['new_todo']
        text = ''
        for t in todo_n:
            text += t
            if t == '\n':
                new_todo = text.replace('\n', '')
                c.execute('''INSERT INTO to_do_list VALUES(?,?,?)''', (user_id, user_date, new_todo))
                conn.commit()
                text = ''
        c.execute('''INSERT INTO to_do_list VALUES(?,?,?)''', (user_id, user_date, text))
        await message.reply('Список обновлен!')
    await state.finish()


@dp.message_handler(state=Form.del_todo)
async def delete_todo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_todo'] = message.text
        user_id = message.from_user.id
        num = data['del_todo']
        num = num.replace(' ', '')
        new_num = num.split(',')
        list_num = []
        c.execute('''SELECT to_do FROM to_do_list WHERE user_id=?''', (user_id,))
        todos = c.fetchall()
        len_t = len(todos)
        for i in new_num:
            if i.isdigit() and int(i) <= len_t:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = todos[k - 1]
                c.execute('''DELETE FROM to_do_list WHERE to_do=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


@dp.callback_query_handler(Text(startswith="todo_"), state='*')
async def callback_todo(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_to_do(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже новое дело или несколько дел.\n'
                                  '<b>Пример для нескольких дел:</b>.\n'
                                  'Сделать домашнюю работу\n'
                                  'Купить овощи')
        await Form.new_todo.set()
    elif action == 'delete':
        await Form.del_todo.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await call.message.answer('Изменения прерваны.')

    await call.answer()


def get_keyboard_contact():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="contact_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="contact_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="contact_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="contact_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['contact'])
async def contact(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_contact(),
    )


async def set_contact(message: types.Message, user_id: int):
    c.execute('''SELECT contact_name, number FROM contacts WHERE user_id=?''', (user_id,))
    cont = c.fetchall()
    if len(cont) == 0:
        await message.answer('Пока не записана ни одна идея.')
    else:
        n = 1
        contact_str = ''
        for i in cont:
            num_list = list(i)
            m = ', '.join(str(e) for e in num_list)
            contact_str += str(n) + '. ' + m + '\n'
            n += 1
        await message.answer('<b>Список контактов:</b>\n' + contact_str)


# функция для правильной и красивой записи номера телефона
def number(num):
    if len(num) == 9:
        num = '+375' + num
    elif '+' not in num:
        num = '+' + num
    else:
        num = num
    full_number = num[:4] + '(' + num[4:6] + ')' + num[6:9] + '-' + num[9:11] + '-' + num[11:]
    return full_number


@dp.message_handler(state=Form.new_contact)
async def get_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_contact'] = message.text
        user_cont = message.from_user
        user_id = user_cont.id
        user_date = message.date
        cont_n = data['new_contact']
        p = cont_n.find('\n')
        contact_name = cont_n[:p]
        contact_number = cont_n[p + 1:]
        cont_num_form = number(contact_number)
        c.execute('''SELECT number FROM contacts WHERE user_id=?''', (user_id,))
        contacts = c.fetchall()
        cont_list = []
        for i in contacts:
            cont_list += list(i)
        if cont_num_form in cont_list:
            await message.reply('Такой контакт уже есть.')
        else:
            if len(contact_number) - 1 > 12:
                await message.reply('Номер введен неверно.')
            else:
                c.execute('''INSERT INTO contacts VALUES(?,?,?,?)''', (user_id, contact_name, cont_num_form, user_date))
                conn.commit()
        await message.answer('Контакт записан!')
    await state.finish()


@dp.message_handler(state=Form.del_contact)
async def delete_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_contact'] = message.text
        user_id = message.from_user.id
        num = data['del_contact']
        num = num.replace(' ', '')
        new_num = num.split(',')
        list_num = []
        c.execute('''SELECT number FROM contacts WHERE user_id=?''', (user_id,))
        contacts = c.fetchall()
        len_t = len(contacts)
        for i in new_num:
            if i.isdigit() and int(i) <= len_t:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = contacts[k - 1]
                c.execute('''DELETE FROM contacts WHERE number=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


@dp.callback_query_handler(Text(startswith="contact_"), state='*')
async def callback_contact(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_contact(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже новый контакт.\n'
                                  '<b>Пример:</b>\n'
                                  'Татьяна\n'
                                  '+375291111111')
        await Form.new_contact.set()
    elif action == 'delete':
        await Form.del_contact.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await call.message.answer('Изменения прерваны.')
    await call.answer()


def get_keyboard_link():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="link_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="link_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="link_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="link_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['link'])
async def link(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_link(),
    )


async def set_link(message: types.Message, user_id: int):
    c.execute('''SELECT link FROM links WHERE user_id=?''', (user_id,))
    links = c.fetchall()
    if len(links) == 0:
        await message.answer('Пока не записана ни одна идея.')
    else:
        n = 1
        links_list = []
        links_in_str = ''
        for i in links:
            links_list += list(i)
        for i in links_list:
            links_in_str += str(n) + '. ' + i + '\n'
            n += 1
        await message.answer('Список ссылок:\n' + links_in_str)


@dp.message_handler(state=Form.new_link)
async def get_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_link'] = message.text
        user_film = message.from_user
        user_id = user_film.id
        user_date = message.date
        link_n = data['new_link']
        c.execute('''INSERT INTO links VALUES(?,?,?)''', (user_id, user_date, link_n))
        conn.commit()
        await message.answer('Ссылка записана!')
    await state.finish()


@dp.message_handler(state=Form.del_link)
async def delete_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_link'] = message.text
        user_id = message.from_user.id
        num = data['del_link']
        num = num.replace(' ', '')
        new_num = num.split(',')
        print(new_num)
        list_num = []
        c.execute('''SELECT link FROM links WHERE user_id=?''', (user_id,))
        links = c.fetchall()
        len_l = len(links)
        for i in new_num:
            if i.isdigit() and int(i) <= len_l:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = links[k - 1]
                c.execute('''DELETE FROM links WHERE link=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


@dp.callback_query_handler(Text(startswith="link_"), state='*')
async def callback_link(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_link(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже ссылку.')
        await Form.new_link.set()
    elif action == 'delete':
        await Form.del_link.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await call.message.answer('Изменения прерваны.')
    await call.answer()


def get_keyboard_book():
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="book_write"),
        types.InlineKeyboardButton(text="Просмотреть", callback_data="book_read"),
        types.InlineKeyboardButton(text="Удалить", callback_data="book_delete"),
        types.InlineKeyboardButton(text="Завершить", callback_data="book_cancel"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['book'])
async def book(message: types.Message):
    await message.answer(
        text=read_txt('keyboard.txt'),
        reply_markup=get_keyboard_book(),
    )


async def set_book(message: types.Message, user_id: int):
    c.execute('''SELECT book_name, author FROM books WHERE user_id=?''', (user_id,))
    books = c.fetchall()
    if len(books) == 0:
        await message.answer('Пока ничего не записано')
    else:
        books_str = ''
        n = 1
        for t in books:
            books_list = list(t)
            m = ', '.join(str(e) for e in books_list)
            books_str += str(n) + '. ' + m + '\n'
            n += 1
        await message.answer('Список книг:\n' + books_str)


@dp.message_handler(state=Form.new_book)
async def get_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_book'] = message.text
        user_film = message.from_user
        user_id = user_film.id
        user_date = message.date
        book_n = data['new_book']
        if book_n.find('\n') == -1:
            book_name = book_n
            author = ''
        else:
            t = book_n.find('\n')
            book_name = book_n[:t]
            author = book_n[t + 1:]
        c.execute('''SELECT book_name FROM books WHERE user_id=?''', (user_id,))
        b = c.fetchall()
        book_list = []
        for i in b:
            book_list += list(i)
        if book_name in book_list:
            await message.edit_text('Такая книга уже записана.')
        else:
            c.execute('''INSERT INTO books VALUES (?,?,?,?)''', (user_id, author, book_name, user_date))
            conn.commit()
            await message.answer('Книга записана!')
    await state.finish()


@dp.message_handler(state=Form.del_book)
async def delete_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_book'] = message.text
        user_id = message.from_user.id
        num = data['del_book']
        num = num.replace(' ', '')
        new_num = num.split(',')
        list_num = []
        c.execute('''SELECT book_name FROM books WHERE user_id=?''', (user_id,))
        books = c.fetchall()
        len_b = len(books)
        for i in new_num:
            if i.isdigit() and int(i) <= len_b:
                n = int(i)
                list_num.append(n)
        if len(list_num) < len(new_num):
            await message.answer(text='Номер(а) введены неверно!\nПопробуйте снова.', reply_markup=get_keyboard_idea())
        else:
            for k in list_num:
                key = books[k - 1]
                c.execute('''DELETE FROM books WHERE book_name=?''', key)
                conn.commit()
            await message.reply('Успешно удалено!')
    await state.finish()


@dp.callback_query_handler(Text(startswith="book_"), state='*')
async def callback_book(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    action = call.data.split("_")[1]
    if action == "read":
        print(user_id)
        await set_book(call.message, user_id=user_id)
    elif action == 'write':
        await call.message.answer('Запишите ниже навзание книги и имя автора,.\n'
                                  'либо только название книги.\n'
                                  '<b>Пример:</b>\n'
                                  'Оно\n'
                                  'Стивен Кинг')
        await Form.new_book.set()
    elif action == 'delete':
        await Form.del_book.set()
        await call.message.answer(text=read_txt('number.txt'))
    elif action == 'cancel':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await call.message.answer('Изменения прерваны.')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
