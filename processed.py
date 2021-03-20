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

from vk_api.utils import get_random_id
# from vk_api import VkApi


longpoll = VkLongPoll(vk_session, 90)
vk = vk_session.get_api()


# idUsers = ['147155440', '189217218', '105431859', '170735090'] 

def connectionDB():
    connect = pymysql.connect(
    
    )
    return connect

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

def update_payload(id: int, payload: str):
    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query = 'INSERT queue (payload) WHERE id=%s VALUES (%s)'
            cursor.execute(query,(id, payload))
            connect.commit()

def commit_is_processed(id: int):
    try:
        with closing(connectionDB()) as connect:
            with connect.cursor() as cursor:
                query = f'UPDATE queue SET isProcessed=1 WHERE id={id}'
                cursor.execute(query)
                connect.commit()

    except Exception as e:
        print(e)

def get_queue() -> list:
    queues = []
    
    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            query ='SELECT id, id_user, message, payload FROM queue WHERE isProcessed=0'
            cursor.execute(query)

            for row in cursor:
                queues.append(row)
                
        return queues

def commit_DB_question(id_user: int, message: str, payload: str):
    with closing(connectionDB()) as connect:
        with connect.cursor() as cursor:
            
            query = f"""UPDATE questions SET {payload}='{message}' WHERE id_user={id_user}"""
            cursor.execute(query)
            connect.commit()
 
            # queryGetCount = 'SELECT countQUE FROM countQUE'
            # cursor.execute(queryGetCount)

            # countQuestion = list(cursor)[0]['countQUE']
            # print(countQuestion)
        

queues = get_queue() 

for queue in queues:
    if queue['payload'] == 'REGcomplite':
        userInfo = vk.users.get(user_ids=queue['id_user'], fields=['first_name', 'last_name'])
        name = userInfo[0]['first_name'] +'_'+ userInfo[0]['last_name']

        commit_DB_register(queue['id_user'], name, queue['message'])
        commit_is_processed(queue['id']) 
        continue
    
    if queue['payload'] == 'REG' or queue['payload'] == 'QUE':
        commit_is_processed(queue['id'])
        continue
    
    elif queue['payload'] == 'TEXT':
        try: 
            with closing(connectionDB()) as connect:
                with connect.cursor() as cursor:
                    
                    a = queue['id_user']
                    query=f'SELECT id_user FROM questions WHERE id_user={a}'
                    
                    cursor.execute(query)
                    count = list(cursor)[0]['id_user']  
                    continue  
      
        except:
            userInfo = vk.users.get(user_ids=queue['id_user'], fields=['first_name', 'last_name'])
            name = userInfo[0]['first_name'] +'_'+ userInfo[0]['last_name']

            commit_DB_register(queue['id_user'], name, queue['message'])
            commit_is_processed(queue['id'])
            continue

                
        
    else:
        try: 
            commit_DB_question(queue['id_user'], queue['message'], queue['payload'])
            commit_is_processed(queue['id'])
            print('Обработка очереди -> [QUE] ', colored('  [OK]', 'green'))
        except Exception as e:
            
            print('Обработка очереди -> [QUE] ', colored('  [FAIL]', 'red'))
            print(traceback.format_exception(e))

# with closing(connectionDB()) as connect:
#         with connect.cursor() as cursor:
            
#             for i in range(50):
#                 query = f'ALTER TABLE questions ADD question{i} TEXT NULL'
#                 cursor.execute(query)
#                 connect.commit()

print('готово')     
    
