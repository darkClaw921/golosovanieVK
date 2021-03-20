import pymysql
import vk_api
import time
import traceback

from pprint import pprint
from termcolor import colored
from contextlib import closing
from threading import Thread

from pymysql.cursors import DictCursor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard 
from vk_api.utils import get_random_id
from vk_api import VkApiGroup
# from vk_api import VkApi


# vk_session = VkApiGroup(vk_session)
longpoll = VkLongPoll(vk_session, 90)
vk = vk_session.get_api()
 

# idUsers = ['147155440', '189217218', '105431859', '170735090'] 
# idUsers = ['105431859']
def connectionDB():
    connect = pymysql.connect(
      
    )
    return connect

PEOPLES = ['Маев Никита', 'Акишкин Иван', 'Стаднюк Дмитрий', 'Яньков Егор', 'Ковальчук Алексей', 'Пономарева Мария', 'Смирнов Максим']
ID_MESSAGES = []
usersId = []
adminId = []
PAYLOAD = 'TEXT'
COUNT_PEOPLES = 0
IS_REGISTER = True

def commit_DB_standUP(user_id: int, message: str, id_message: int, payload='REG'):
    try: 
        userInfo = vk.users.get(user_ids=user_id, fields=['first_name', 'last_name'])
        name = userInfo[0]['first_name'] +'_'+ userInfo[0]['last_name']

        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = 'INSERT standUP (id_user, code, voice, name, id_message) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(query,(user_id, message, 'хз', name, id_message ))
                connect.commit()
                print('Запись данных...  ', colored('[OK]', 'green'))

    except Exception as err:
        print('Запись данных...  ', colored('[Fail]', 'red'), traceback.format_exc())

def commit_DB_edit_standUP(user_id: int, message: str, payload='voice'):
    try: 
        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = f"""UPDATE standUP SET voice='{message}' WHERE id_user={user_id}"""
                cursor.execute(query)
                connect.commit()
                print('Редактирование данных...  ', colored('[OK]', 'green'))

    except Exception as err:
        print('Редактирование данных...  ', colored('[Fail]', 'red'))

def commit_DB_register(user_id: int, username: int, message: str):
    try: 
        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = 'INSERT questions (id_user, name, command) VALUES (%s, %s, %s)'
                cursor.execute(query,(user_id, username, message))
                connect.commit()
                print('Регистрация команд...  ', colored('[OK]', 'green'))

    except Exception as err:
        print('Регистрация команд...  ', colored('[Fail]', 'red'), traceback.format_exc())


def get_register_command(event):

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message='Пришлите название команды',
    )

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            userInfo = vk.users.get(user_ids=event.user_id, fields=['first_name'])
            name = userInfo[0]['first_name'] +'_'+ userInfo[0]['last_name']
            commit_DB_register(event.user_id, name, event.text)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message='Вы зарегистрированы',
    )

def get_last_payload(user_id) -> str:
    try: 
        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = 'SELECT payload FROM queue WHERE id_user=%s ORDER BY `id` DESC LIMIT 1'
                cursor.execute(query,(user_id))
                cursor = list(cursor)
                print('Полоучение последних данных...  ', colored('[OK]', 'green'))
                return cursor[0]['payload']

    except Exception as err:
        print('Полоучение последних данных...  ', colored('[Fail]', 'red'), traceback.format_exc())
        return 'FAIL'

def get_count_peoples():
    global COUNT_PEOPLES

    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query=f'SELECT countQUE FROM countQUE'
            cursor.execute(query)
            count = list(cursor)[0]['countQUE']
            
    COUNT_PEOPLES = count
            # PAYLOAD = f'question{count}'

    # time.sleep(55)

def get_id_messages() -> list:
    idsMessages=[]
    idsUsers=[]

    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query = 'SELECT id_message FROM standUP'
            cursor.execute(query)
            for row in cursor:
                idsMessages.append(row['id_message'])

            query = 'SELECT id_user FROM standUP'
            cursor.execute(query)
            for row in cursor:
                idsUsers.append(row['id_user'])

            return idsUsers, idsMessages

def get_results() -> list:
    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query='SELECT COUNT(voice) as count, voice FROM standUP GROUP BY voice ORDER BY count DESC'
            cursor.execute(query)
    
    return list(cursor)


def edit_messages(user_id: int):
    idsUsers = get_id_messages()[0]
    idMessages = get_id_messages()[1]
    
    for idUser, idMessage in zip(idsUsers, idMessages):
        time.sleep(0.05)

        vk.messages.edit(
            peer_id = idUser,
            message = f'Вы зарегистрированы',
            message_id = idMessage,
            keyboard=KEYBOARD,
        )

def next_people():
    global PAYLOAD

    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query='UPDATE countQUE SET countQUE = countQUE + 1'
            cursor.execute(query)
            connect.commit()

    # PAYLOAD = 'TEXT'

    # idMessages = []
    # i = 0
    # try: 
    #     for idUser in idUsers:
    #         mes = vk.messages.send(
    #             user_id=idUser,
    #             random_id=get_random_id(),
    #             message = "Присылайте ответ",
    #         )
    #         idMessages.append(mes)

    #     for i in range(3):
    #         time.sleep(1)
    #         for idUser, idMessage in zip(idUsers, idMessages):   
    #             vk.messages.edit(
    #                 peer_id = idUser,
    #                 message = f'Осталось времени: {60 - i} сек',
    #                 message_id = idMessage
    #             )

    #     vk.messages.edit(
    #         peer_id = idUser,
    #         message = f'Время вышло',
    #         message_id = idMessage
    #     )
    # except ApiError as e:
    #     print('apiError', e)
    #     PAYLOAD = 'TEXT'


    
    # x.join()

def keyboardCreater(*args, count: int): 
    keyboard = VkKeyboard(one_time=False)
    i = 0
    for label in args:
        if i >= count:
            break
        keyboard.add_button(label)
        keyboard.add_line()
        i+=1
   
    keyboard.add_button(label = '↑↑↑↑↑↑↑ Голосуй ↑↑↑↑↑↑↑', color='negative')        
    keyboard = keyboard.get_keyboard()
    return keyboard


def isHE(id_user):
    try:
        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = f'SELECT COUNT(*) as count FROM standUP WHERE id_user={id_user}'
                cursor.execute(query)
                if list(cursor)[0]['count'] > 0:
                    return True
                else:
                    return False
    except Exception as e:
        print('Ошибка: ', e) 

def isInt(message):
    try:
        int(message)
        return True
    except: 
        return False

# KEYBOARD = keyboardCreater(*PEOPLES, count=2)
keyboardAdmin = keyboardCreater('Следующий участник', 'Закончить голосование','Закончить регистрацию', 'Результаты', count=5)

vk.messages.send(
    user_id='105431859',
    random_id=get_random_id(),
    message = "админ [online]",
    keyboard= keyboardAdmin,
    )

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                # lastPayload = get_last_payload(event.user_id)
                text = event.text.lower()
                print(text)

                if text == 'следующий участник':
                    next_people()
                    get_count_peoples()
                    KEYBOARD = keyboardCreater(*PEOPLES, count=COUNT_PEOPLES)
                    edit_messages(event.user_id)
                    continue

                if text == 'закончить регистрацию':
                    IS_REGISTER=False
                    continue
                
                if text == 'результаты':
                    results = get_results()
                    message=''

                    for result in results:
                        voice = result['voice']
                        count = result['count']

                        message += f'{ count }    { voice } \n'
                    
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message = message,
                    )
                    continue

                if isInt(text) and IS_REGISTER:
                    if isHE(event.user_id):
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message = "Вы уже зарегистрированы",
                        )

                    else:
                        idMessage = vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message = "Вы зарегистрированы",
                        )

                        commit_DB_standUP(event.user_id, event.text, idMessage)
                    continue

                elif isInt(text) and not IS_REGISTER:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message = "Регистрация уже завершена",
                    )
                    continue


                if text == 'конец':
                    end()
                    commit_DB_queue(event.user_id, event.text, PAYLOAD) 
                    continue

                # if lastPayload == 'REG':
                #     commit_DB_queue(event.user_id, event.text, 'REGcomplite')
                #     continue

                # print(isHE(event.user_id))

                if isHE(event.user_id):
                    commit_DB_edit_standUP(event.user_id, event.text)

                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message = "Вы не можете голосовать так как не указали секретный код",
                        # keyboard= KEYBOARD,
                    )
            # commit_DB_queue(event.user_id, event.text, PAYLOAD)
    except Exception as e:
        print(e, traceback.print_exc())
        
        continue

        # with closing(connectionDB()) as connect:
        #     with connect.cursor() as cursor:
        #         for i in range(10):
        #             query = f'ALTER TABLE questions ADD question{i} TEXT NULL'
        #             cursor.execute(query)
        #             connect.commit()
                
