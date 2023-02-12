import data_checking
import func_bot
import keyboard
import state
from create_bot import bot
from state import FSMAdmin, FSMContext
from aiogram.types import InlineKeyboardMarkup
from data_checking import cheak_input_text
import func_bot



async def start_handler(message):
    await bot.send_message(message.from_user.id, f"Добро пожаловать в главное мню{message.from_user.first_name}", reply_markup=keyboard.kb_main_inline)


async def edit_handler(call):
    await bot.edit_message_text(text="Кого хотите отредактировать?", message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher)

async def back_inline_menu_main(call, state:FSMContext):
    await state.finish()
    await bot.edit_message_text(
        text=f"Добро пожаловать в главное мню{call.message.from_user.first_name}",
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard.kb_main_inline)

#Редактирование
async def edit_handler_student(call, state:FSMContext):
    if call.data == "student_2":
        inline_student_butt = InlineKeyboardMarkup()
        records = func_bot.name_list_db_student_and_teacher(key="student")[0]
        keyboard.inline_student(records, inline_student_butt)
        await bot.edit_message_text(
            text="Все студенты SkillBox",
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=inline_student_butt)
        async with state.proxy() as data:
            data["key_student_call"] = True
    else:
        inline_teacher_butt = InlineKeyboardMarkup()
        records = func_bot.name_list_db_student_and_teacher(key="teacher")[0]
        keyboard.inline_teacher(records, inline_teacher_butt)
        await bot.edit_message_text(
            text="Все кураторы SkillBox",
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=inline_teacher_butt)
        async with state.proxy() as data:
            data["key_student_call"] = False



async def back_menu_student_teacher(call):
    await bot.edit_message_text(text="Кого хотите отредактировать?", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher)


async def edit_handler_message_student(call, state:FSMContext):
    async with state.proxy() as data:
        key = data["key_student_call"]
    if key:
        await bot.edit_message_text(
            text=func_bot.info_list(call.data[-1],key="student")[0],
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=keyboard.butt_back_and_del_prod)
        async with state.proxy() as data:
            data["id_student"] = func_bot.info_list(call.data[-1],key="student")[1]

async def edit_handler_message_teacher(call, state: FSMContext):
    await bot.edit_message_text(
        text=func_bot.info_list(call.data[-1], key="teacher")[0],
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=keyboard.butt_back_and_del_prod)
    async with state.proxy() as data:
        data["id_teacher"] = func_bot.info_list(call.data[-1], key="teacher")[1]



async def bak_and_del_student_handler(call, state:FSMContext):
    async with state.proxy() as data:
        key = data["key_student_call"]
    if key:
        if call.data == "del":
            async with state.proxy() as data:
                id_student = data["id_student"]
            func_bot.removing_student(id_student)
        inline_student_butt = InlineKeyboardMarkup()
        records = func_bot.name_list_db_student_and_teacher(key="student")[0]
        keyboard.inline_student(records, inline_student_butt)
        await bot.edit_message_text(
            text="Все студенты SkillBox",
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=inline_student_butt)
    else:
        if call.data == "del":
            async with state.proxy() as data:
                id_student = data["id_teacher"]
            func_bot.removing_student(id_student)
        inline_teacher_butt = InlineKeyboardMarkup()
        records = func_bot.name_list_db_student_and_teacher(key="teacher")[0]
        keyboard.inline_teacher(records, inline_teacher_butt)
        await bot.edit_message_text(
            text="Все Кураторы SkillBox",
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
            reply_markup=inline_teacher_butt)







#Добавление
async def add_handler(call, state:FSMContext):
    if call.data == "add":
        await bot.edit_message_text(text="*Инструкция по добавлению*", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
    else:
        await bot.edit_message_text(text="*Инструкция по добавлению*", message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
        await state.finish()


#Добавление типов профессии
async def add_type_handler(call, state:FSMContext):
    async with state.proxy() as data:
        data["message_id_type"] = call.message.message_id
        data["chat_id_type"] = call.message.chat.id
    await bot.edit_message_text(text=f"Введите название типа профессии", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
    await FSMAdmin.state_add_type_profession.set()


async def add_name_type_handler(message, state:FSMContext):
    async with state.proxy() as data:
        data["type_name"] = message.text
        message_id = data["message_id_type"]
        chat_id = data["chat_id_type"]
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        await bot.edit_message_text(text=f"Вы уверены что хотите добавить тип профессии - {message.text}", message_id=message_id, chat_id=chat_id, reply_markup=keyboard.accept_and_reject_2)
        await FSMAdmin.next()


async def accept_or_reject_type_handler(call, state:FSMContext):
    if call.data == "accept_2":
        async with state.proxy() as data:
            type_name = data["type_name"]
            func_bot.add_type(type_name)
        await bot.edit_message_text(text=f"Тип профессии - {type_name} успешно добавлен\n\nЧто ещё хотите добавить?", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
    else:
        await bot.edit_message_text(text=f"Хорошо\nЧто то хотите добавить?", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
    await state.finish()






#Добавление
async def add_studenta_or_teacher_handler(call, state:FSMContext):
    if call.data == "student":
        await bot.edit_message_text(text=f"Введите имя студента", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
        async with state.proxy() as data:
            data["message_id"] = call.message.message_id
            data["chat_id"] = call.message.chat.id
            data["student"] = True
    else:
        async with state.proxy() as data:
            data["message_id_teacher"] = call.message.message_id
            data["chat_id_teacher"] = call.message.chat.id
            data["student"] = False
        await bot.edit_message_text(text=f"Введите имя куратора", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
    await FSMAdmin.state_add_name.set()

async def add_name_student_or_teacher_handler(message, state:FSMContext):
    async with state.proxy() as data:
        key_student = data["student"]
        inline_type_butt = InlineKeyboardMarkup()
        list_type = [i[1] for i in func_bot.db("Type_and_articul")]
        keyboard.inline_type(list_type, inline_type_butt)
        staus = data_checking.cheak_input_text(message.text, key="имени")
    if key_student:
        async with state.proxy() as data:
            data["name"] = staus[-1]
            chat_id = data["chat_id"]
            message_id = data["message_id"]
            await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        if staus[1] == "ok":
            await bot.edit_message_text(text=f"Хорошо, теперь выбери профессию студента", message_id=message_id, chat_id=chat_id, reply_markup=inline_type_butt)
            await FSMAdmin.next()
            await FSMAdmin.next()
        elif staus[1] == "normal":
            await bot.edit_message_text(text=staus[0], message_id=message_id, chat_id=chat_id, reply_markup=keyboard.yes_and_no)
            await FSMAdmin.next()
        else:
            await bot.edit_message_text(text=staus[0], message_id=message_id, chat_id=chat_id, reply_markup=keyboard.back_inline_menu_butt)
            await FSMAdmin.state_add_name.set()
    else:
        async with state.proxy() as data:
            data["name_teacher"] = staus[-1]
            chat_id = data["chat_id_teacher"]
            message_id = data["message_id_teacher"]
            await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        if staus[1] == "ok":
            await bot.edit_message_text(text=f"Хорошо, теперь выбери направления куратора", message_id=message_id, chat_id=chat_id, reply_markup=inline_type_butt)
            await FSMAdmin.next()
            await FSMAdmin.next()
        elif staus[1] == "normal":
            await bot.edit_message_text(text=staus[0], message_id=message_id, chat_id=chat_id, reply_markup=keyboard.yes_and_no)
            await FSMAdmin.next()
        else:
            await bot.edit_message_text(text=staus[0], message_id=message_id, chat_id=chat_id, reply_markup=keyboard.back_inline_menu_butt)
            await FSMAdmin.state_add_name.set()


async def yes_and_no_handler(call, state:FSMContext):
    async with state.proxy() as data:
        key_student = data["student"]
        inline_type_butt = InlineKeyboardMarkup()
        list_type = [i[1] for i in func_bot.db("Type_and_articul")]
        keyboard.inline_type(list_type, inline_type_butt)
    if call.data == "yes":
            if key_student:
                await bot.edit_message_text(text=f"Хорошо, теперь выбери профессию студента", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=inline_type_butt)
                await FSMAdmin.next()
            else:
                await bot.edit_message_text(text=f"Хорошо, теперь выбери профессию куратора", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=inline_type_butt)
                await FSMAdmin.next()
    else:
        if key_student:
            await bot.edit_message_text(text=f"Введите имя студента", message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
            await FSMAdmin.state_add_name.set()
        else:
            await bot.edit_message_text(text=f"Введите имя куратора", message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
            await FSMAdmin.state_add_name.set()




async def add_type_student_or_teacher_handler(call, state:FSMContext):
    async with state.proxy() as data:
        key_student = data["student"]
    if key_student:
        await bot.edit_message_text(text="Теперь введи ТГ id студента", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
        async with state.proxy() as data:
            data["type"] = func_bot.db("Type_and_articul")[int(call.data[-1]) - 1][1]
            data["articul"] = func_bot.db("Type_and_articul")[int(call.data[-1]) - 1][0]
            data["call_message_id"] = call.message.message_id
            data["call_chat_id"] = call.message.chat.id
    else:
        await bot.edit_message_text(text="Теперь введи ТГ id куратора", message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=keyboard.back_inline_menu_butt)
        async with state.proxy() as data:
            data["type_teacher"] = func_bot.db("Type_and_articul")[int(call.data[-1]) - 1][1]
            data["articul_teacher"] = func_bot.db("Type_and_articul")[int(call.data[-1]) - 1][0]
            data["call_message_id_teacher"] = call.message.message_id
            data["call_chat_id_teacher"] = call.message.chat.id
    await FSMAdmin.next()

async def add_tg_name_student_or_teacher_handler(message, state:FSMContext):
    async with state.proxy() as data:
        key_student = data["student"]
    if key_student:
        async with state.proxy() as data:
            name = data["name"]
            type = data["type"]
            articul = data["articul"]
            data["tg_id"] = message.text
            message_id_call = data["call_message_id"]
            chat_id_call = data["call_chat_id"]
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        await bot.edit_message_text(text=f"Информация о введённых данных\n\nСтудент - {name}\n\nГруппа - {type}\nАртикул группы - {articul}\nТГ ник - {message.text}\nКласс - Студент", chat_id=chat_id_call, message_id=message_id_call, reply_markup=keyboard.accept_and_reject)
        await FSMAdmin.next()
    else:
        async with state.proxy() as data:
            name = data["name_teacher"]
            type = data["type_teacher"]
            articul = data["articul_teacher"]
            data["tg_id_teacher"] = message.text
            message_id_call = data["call_message_id_teacher"]
            chat_id_call = data["call_chat_id_teacher"]
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        await bot.edit_message_text(
            text=f"Информация о введённых данных\n\nКуратор - {name}\n\nГруппа - {type}\nАртикул группы - {articul}\nТГ ник - {message.text}\nКласс - Куратор",
            chat_id=chat_id_call, message_id=message_id_call, reply_markup=keyboard.accept_and_reject)
        await FSMAdmin.next()

async def accept_or_reject_add_student_or_teacher_handler(call, state:FSMContext):
    async with state.proxy() as data:
        key_student = data["student"]
    if key_student:
        if call.data == "accept":
            async with state.proxy() as data:
                name = data["name"]
                type = data["type"]
                articul = data["articul"]
                tg_id = data["tg_id"]
                func_bot.add_student(name=name, type=type, articul=articul, id_tg=tg_id, class_human="Студент")
                await bot.edit_message_text(text=f"Cтудент {name} успешно добавлен\nХотите ещё что-то добавить?", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
                await state.finish()
        else:
            await bot.edit_message_text(text="*Инструкция по добавлению*", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
        await state.finish()
    else:
        if call.data == "accept":
            async with state.proxy() as data:
                name = data["name_teacher"]
                type = data["type_teacher"]
                articul = data["articul_teacher"]
                tg_id = data["tg_id_teacher"]
                func_bot.add_student(name=name, type=type, articul=articul, id_tg=tg_id, class_human="Куратор")
                await bot.edit_message_text(text=f"Куратор {name} успешно добавлен\nХотите ещё что-то добавить?", message_id=call.message.message_id, chat_id=call.message.chat.id,reply_markup=keyboard.student_and_teacher_type)
        else:
            await bot.edit_message_text(text="*Инструкция по добавлению*", message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=keyboard.student_and_teacher_type)
        await state.finish()


def register_handler(dp):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_callback_query_handler(back_inline_menu_main, lambda callback: callback.data == "back_main_menu", state=None)

    dp.register_callback_query_handler(edit_handler, lambda callback: callback.data == "edit", state=None)
    dp.register_callback_query_handler(back_menu_student_teacher, lambda callback: callback.data == "back_menu_edit", state=None)
    dp.register_callback_query_handler(edit_handler_student, lambda callback: callback.data in ["student_2", "teacher_2"], state=None)
    dp.register_callback_query_handler(edit_handler_message_student, lambda callback: callback.data in [f"std_{i + 1}" for i in range(len(func_bot.name_list_db_student_and_teacher(key="student")[0]))],state=None)
    dp.register_callback_query_handler(edit_handler_message_teacher, lambda callback: callback.data in [f"tch_{i + 1}" for i in range(len(func_bot.name_list_db_student_and_teacher(key="teacher")[0]))],state=None)
    dp.register_callback_query_handler(bak_and_del_student_handler, lambda callback: callback.data in ["back", "del"], state=None)

    #Добавление
    dp.register_callback_query_handler(add_handler, lambda callback: callback.data in ["add", "back_menu"], state="*")

    #Добавление студента и куратора
    dp.register_callback_query_handler(add_studenta_or_teacher_handler, lambda callback: callback.data in ["student", "teacher"], state=None)
    dp.register_callback_query_handler(yes_and_no_handler, lambda callback: callback.data in ["yes", "no"], state=FSMAdmin.state_yes_and_no)
    dp.register_message_handler(add_name_student_or_teacher_handler, lambda message: message.text, state=FSMAdmin.state_add_name)
    dp.register_callback_query_handler(add_type_student_or_teacher_handler, lambda callback: callback.data in [f"type_{i + 1}" for i in range(len([i for i in func_bot.db("Type_and_articul")]))], state=FSMAdmin.state_add_type)
    dp.register_message_handler(add_tg_name_student_or_teacher_handler, lambda message: message.text, state=FSMAdmin.state_add_tg_name)
    dp.register_callback_query_handler(accept_or_reject_add_student_or_teacher_handler, lambda callback: callback.data in ["accept", "reject"] or callback.data in ["accept_2", "reject_2"], state=FSMAdmin.accept_or_reject)


    #Добавления типа профессии
    dp.register_callback_query_handler(add_type_handler, lambda callback: callback.data == "type", state=None)
    dp.register_message_handler(add_name_type_handler, lambda message: message.text, state=FSMAdmin.state_add_type_profession)
    dp.register_callback_query_handler(accept_or_reject_type_handler, lambda callback: callback.data in ["accept_2", "reject_2"], state=FSMAdmin.accept_or_reject_type)

