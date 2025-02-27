# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 20:17:33 2020

@author: McLaren
"""
import sys
# sys.path.append(r'D:\Software\FGO_Project')

# import Serial
import Serial_wormhole as Serial
import time
import winsound

from Notice import sent_message

# 无限池抽取函数
def InfinatePool(times=100):
    Serial.port_open('com3')
    Serial.mouse_set_zero()
    Serial.mouse_move((320, 360))
    for i in range(times):
        Serial.mouse_click()
        time.sleep(0.1)


# 友情池抽取函数
def FriendPointSummon():
    Serial.port_open('com3')
    time.sleep(0.5)

    Serial.mouse_set_zero()

    Serial.touch(540, 472)

    Serial.touch(702, 480, 2)
    time.sleep(1)
    Serial.touch(647, 570, 8)

    while True:
        Serial.touch(702, 480, 1)
        time.sleep(1)
        Serial.touch(647, 570, 7)


# 搓丸子
def MakeCraftEssenceEXCard():
    Serial.port_open('com3')
    Serial.mouse_set_zero()

    while True:
        Serial.touch(720, 280)
        time.sleep(0.5)
        Serial.mouse_swipe((150, 250), (600, 600), 0.5)
        Serial.touch(990, 570, 3)
        time.sleep(0.5)
        Serial.touch(720, 507, 10)


if __name__ == '__main__':
    # FriendPointSummon()
    InfinatePool(200)
    sent_message("抽取完成!", 1)

