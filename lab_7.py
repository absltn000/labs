from asyncore import loop
import csv
from os import system
from unicodedata import name
from telebot import types
import telebot
import re
import time


#сравнение двух названий и вывод их процентного соотношения 
def check_city_name(user_city_name:str, org_city_name:str):
    procent = 0
    if len(user_city_name)<len(org_city_name):
        for i in range(len(user_city_name)):
            if user_city_name[i].upper()==org_city_name[i].upper():
                procent+=1
    else:
        for i in range(len(org_city_name)):
            if user_city_name[i].upper()==org_city_name[i].upper():
                procent+=1
    return procent/len(org_city_name)

#создание базы данных
def data_base(file_name:str):
    data=[]
    with open(file_name, encoding='UTF-8') as file:
        reader = csv.reader(file, dialect="excel")
        for line in reader:
            line_tmp=line[0]
            line_data=line_tmp.split(';')
            index, city=line_data[0:2]
            data.append((city, index))
    return data

#поиск индекса по названию города
def find_city(city_name:str, data):
    chance = 0 
    city = ()
    cityes=[]
    for case in data:
        if case[0]==city_name.upper():
            return ([(case[0],case[1],100)],0)
        else:
            chance_tmp=check_city_name(case[0],city_name)
            if len(cityes)<5:
                cityes.append((case[0],case[1],chance_tmp))
            else:  
                for i in range(5):
                    if cityes[i][2]<chance_tmp:
                        cityes[i]=(case[0],case[1],chance_tmp)
                        break
    city=(cityes,1)
    return city

#поиск названия города по индексу
def find_index(city_index:str, data):
    chance = 0 
    city = ()
    cityes=[]
    for case in data:
        if case[1]==city_index:
           return ([(case[0],case[1],100)],0)
        else:
            chance_tmp=check_city_name(case[0],city_index)
            if len(cityes)<5:
                cityes.append((case[0],case[1],chance_tmp))
            else:  
                for i in range(5):
                    if cityes[i][2]<chance_tmp:
                        cityes[i]=(case[0],case[1],chance_tmp)
                        break
    city=(cityes,1)
    return city
   
data=data_base("PIndx09-1.csv")
user_name=""

# Создаем экземпляр бота
token = ''
bot = telebot.TeleBot(token)
# Функция, обрабатывающая команду /start/help--
@bot.message_handler(commands=['start', 'help'])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Этот бот умеет определять индекс любого города в РФ, или же может найти город по индексу')
    global user_name 
    user_name = message.from_user.first_name
    ok=True
    ok=go(message)



# Получение сообщений от пользователей
@bot.message_handler(content_types=["text", "left_chat_member"])
def go(message):
    global user_name
    
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Индекс по названию города', callback_data='name'); #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Название города по индексу', callback_data='index')
    keyboard.add(key_no)
    bot.send_message(message.chat.id, f'{user_name}, чтобы вы хотели найти' ,reply_markup=keyboard)
        
        

def handle_text(message):
    
    print(user_name, message.text)
    bot.send_message(message.chat.id, "{0}, Вы написали: ".format(user_name) + message.text)

#получение индекса по названию города
def index(message):
    
    global data
    city=find_city(message.text,data)
    print(message.text)
    if city[1]==0:
        bot.send_message(message.chat.id, f'Найдено по запросу:\n {message.text}: {city[0][0][1]}')
        time.sleep(5)
        go(message)
    else:
        keyboard2=types.InlineKeyboardMarkup()
        for i in city[0]:
            keyboard2.add(types.InlineKeyboardButton(text=f'{i[0]}: {i[1]}',callback_data='city'))
        keyboard2.add(types.InlineKeyboardButton(text=f'Нет нужного города',callback_data='non-city'))
        bot.send_message(message.chat.id, f'Точных данных не найдено.\n Возможные запросы:\n',reply_markup=keyboard2)


#получение названия города по индексу
def city(message):
    er=True
    global data
    index_str=message.text

    city=find_index(message.text,data)
    print(message.text)
    if city[1]==0:
        bot.send_message(message.chat.id, f'Найдено по запросу:\n {message.text}: {city[0][0][0]}')
        time.sleep(5)
        go(message)
    else:
        keyboard2=types.InlineKeyboardMarkup()
        for i in city[0]:
            keyboard2.add(types.InlineKeyboardButton(text=f'{i[1]}: {i[0]}',callback_data='city'))
        keyboard2.add(types.InlineKeyboardButton(text=f'Нет нужного индекса',callback_data='non-city'))
        bot.send_message(message.chat.id, f'Точных данных не найдено.\n Возможные запросы:\n',reply_markup=keyboard2)
    


    
#Функция отлавливающая события для распределения на индекс и город
@bot.callback_query_handler(lambda call: call.data=='name' or call.data=='index')
def get_start_answer(call):
    if (call.data=="name"):
        bot.send_message(call.message.chat.id, "Введите название города")
        er=True
        er=bot.register_next_step_handler(call.message,index)
    elif (call.data=='index'):
        bot.send_message(call.message.chat.id, "Введите индекс")
        er=True
        er=bot.register_next_step_handler(call.message,city)

#Функция отлавливающая события для определения правильности доп. выбора
@bot.callback_query_handler(lambda call: call.data=='city' or call.data=='non-city')
def get_city_answer(call):
    if (call.data=='city'):
        bot.send_message(call.message.chat.id, "Мы рады, что наш бот помогла вам найти нужную информацию")
    elif (call.data=='non-city'):
        bot.send_message(call.message.chat.id, "Мы сожалеем, ничем не смогли вам помочь")
    time.sleep(5)
    go(call.message)
        
# Запускаем бота
bot.polling(none_stop=True, interval=0)

