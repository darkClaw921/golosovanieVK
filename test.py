import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from PIL import Image, ImageDraw, ImageFont

# VK API import
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload 

# OS import
import time
import os
from threading import Thread
import threading

# Help files import
# import setings
# import test 
# import viktorinaCreateSheet
# import viktorinaQ uestions
import json


# VK setings
vk_session = vk_api.VkApi(token = '') # отдел
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

people = ['Ковальчук Алексей', 'Акишкин Иван', 'Пономарева Мария', 'Стаднюк Дмитрий', 'Маев Никита', 'Смирнов Максим', 'Яньков Егор']
print(len(people))
people1 = ['1']

def keyboardCreater(*args, count: int): 
    keyboard = VkKeyboard(one_time=False)
    i = 0
    for label in args:
        if i >= count:
            break
        keyboard.add_button(label)
        keyboard.add_line()
        i+=1
   
    keyboard.add_button(label = '↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑')        
    keyboard = keyboard.get_keyboard()
    return keyboard

# keyboard1 = keyboardCreater('Ковальчук Алексей', 'Акишкин Иван', 'Пономарева Мария', 'Стаднюк Дмитрий')
keyboard1 = keyboardCreater(*people, count=2)
a = True
if a:
    print(a, 'as')
elif not a:
    print(a)
# # a = vk.messages.send(
# #     user_id='105431859',
# #     random_id=get_random_id(),
# #     message = "админ [online]",
# #     keyboard= keyboard1,
# #     )
# for i in range(8):
#     vk.messages.edit(
#             peer_id = '105431859',
#             message = f'Вы зарегистрированы',
#             message_id = 4993,
#             keyboard=keyboardCreater(*people, count=i)
#         )
    time.sleep(3)
print('[OK]')