import vk_api
import time
import traceback
import sqlite3
from localDataBase import SqlLite
from vk_api import keyboard


from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard 
from vk_api.utils import get_random_id
from loguru import logger

vk_session = vk_api.VkApi(token = '') # отдел
longpoll = VkLongPoll(vk_session, 90)
vk = vk_session.get_api()


sql = SqlLite('golos.db', """
        CREATE TABLE golos(
            id INTEGER PRIMARY KEY,
            id_user INT UNIQUE,
            payload TEXT DEFAULT '0',
            goloss TEXT);""")


def keyboardCreater(*args, count: int): 
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(args[0])
    args[1:]
    
    for label in args[1:]:
        
        keyboard.add_line()
        keyboard.add_button(label)
        
    keyboard = keyboard.get_keyboard()
    return keyboard



vk.messages.send(
    user_id='105431859',
    random_id=get_random_id(),
    message = "админ [online]",
    # keyboard= keyboardAdmin,
    )

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                # lastPayload = get_last_payload(event.user_id)
                text = event.text.lower()
                # print(text)
                if text == 'победитель':
                    winers = sql.get("""
                        SELECT goloss,COUNT(*) AS total 
                        FROM golos 
                        GROUP BY goloss 
                        ORDER BY total 
                        DESC LIMIT 5""")

                    strWin = 'На данный момент следующие победители: '
                    for winer in winers:
                        strWin += f"\n{winer}"


                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message = strWin,
                    )


                if text == 'шутка':
                    payload = sql.get(f'select payload from golos where id={event.user_id}')
                   

                    if sql.isHe(event.user_id):
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message='Вы уже голосовали',
                         )
                        continue
                    else:
                        payload='REG'
                        values = [event.user_id, payload, 0]
                        sql.send_values('insert into golos (id_user, payload, goloss) ', values)
                        
                     
                    vk.messages.send(
                         user_id=event.user_id,
                         random_id=get_random_id(),
                         message=f"""Отправте только номер участника.\nНапример: 3""",
                     ) 
                    vk.messages.send(
                         user_id=event.user_id,
                         random_id=get_random_id(),
                         message=f"""1. Михаил Секретов \n2. Михаил Семенов \n3. Андрей Власов\n4. Андрей Балунов\n5. Никита Андропов\n 6. Илья Ванюхин""",
                     ) 
                    continue

                if sql.isHe(event.user_id):
                    lastPayload = sql.get_last_payload(event.user_id)
                    if lastPayload == 'REG':
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message = f"""Спасибо что проголосовали =)"""
                        )
                        payload = 'EXIT'
                        sql.update(f"update golos set payload = '{payload}', goloss = {text} where id_user = {event.user_id}")
                    
                      
                else:
                #    Если человека нет

                    continue


            # commit_DB_queue(event.user_id, event.text, PAYLOAD)
    except Exception as e:
        print(e, traceback.print_exc())
        vk.messages.send(
            user_id='105431859',
            random_id=get_random_id(),
            message = "админ [offline]",
            )
        vk.messages.send(
            user_id='105431859',
            random_id=get_random_id(),
            message = (e, traceback.print_exc()),
            )
        
        continue



