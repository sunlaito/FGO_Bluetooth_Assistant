# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""
from typing import Any

import time
import sys
from tqdm import tqdm
import random
# sys.path.append(r'F:\FGO_Project')

# import Serial
# import Base_func
import Serial_wormhole as Serial
import Base_func_wormhole as Base_func

import Mystic_Codes
import Battle_templates

from Notice import sent_message


class state:
    def HasBackToMenu(self):
        while True:
            Flag, Position = Base_func.match_template('Menu_button')
            if Flag:
                break
            Flag, Position = Base_func.match_template('reenter_battle')
            if Flag:
                break
            time.sleep(1)

    def WaitForBattleStart(self):
        while True:
            Flag, Position = Base_func.match_template('Attack_button')
            if Flag:
                break
            time.sleep(1)

    def WaitForFriendShowReady(self):
        while True:
            Flag, Position = Base_func.match_template('friend_sign')
            if Flag:
                break
            Flag, Position = Base_func.match_template('no_friend')
            if Flag:
                break
            time.sleep(1)


def enter_battle():
    Current_state.HasBackToMenu()
    # 确认已经返回菜单界面，或检测到连续出击按键
    for enter_battle_type in ['reenter_battle', 'LastOrder_sign']:
        Flag, Position = Base_func.match_template(enter_battle_type)
        if Flag:
            break
    if Flag:
        if enter_battle_type == 'reenter_battle':
            Position = [705, 475]
        else:
            Position = [Position[0] + 230, Position[1] + 50]
    else:
        Position = [791, 155]
        enter_battle_type = 'default_pos'
    print(f' Enter battle type: {enter_battle_type}')

    while True:  # 点击战斗直到进入吃苹果或选助战界面
        Serial.touch(Position[0], Position[1])
        time.sleep(3)
        for state_type in ['AP_recover', 'Refresh_friend']:
            Flag, Position_next = Base_func.match_template(state_type)
            if Flag:
                print(' Enter battle success')
                return state_type


def apple_feed():
    # 进入吃苹果界面的逻辑已在enter_battle()中完成, 无须再判断
    global num_GoldApple_used, num_SilverApple_used
    for apple_type in ['Silver_apple', 'Gold_apple']:
        Flag, Position = Base_func.match_template(apple_type)
        if Flag:
            break
    if Flag:  # 持有银苹果或金苹果
        while True:  # 点击苹果直到进入吃苹果确认界面
            Serial.touch(709, Position[1])
            time.sleep(1.5)
            Flag, Position = Base_func.match_template('Feedapple_decide')
            if Flag:
                break

        while True:  # 点击决定吃苹果直到进入助战画面
            Serial.touch(Position[0], Position[1])
            time.sleep(1.5)
            for friend_type in ['friend_sign', 'no_friend']:
                Flag, Position = Base_func.match_template(friend_type)
                if Flag:
                    break
            if Flag:
                if apple_type == 'Silver_apple':
                    num_SilverApple_used += 1
                else:
                    num_GoldApple_used += 1
                print(' Feed {} success'.format(apple_type))
                break
    else:  # 没有苹果
        print(' No apple remain')
        Serial.touch(0, 0)
        sys.exit(0)


def find_friend(servant):
    Current_state.WaitForFriendShowReady()  # 等待助战列表载入完成

    if servant == "ALL":
        print(' Just pick the first friend')
        Serial.touch(500, 240)
        time.sleep(1.5)
        Serial.touch(1005, 570)
        print(' Start battle button pressed')
        return

    Flag, Position = Base_func.match_template(servant + '_skill_level', False, 0.9)
    time_limit_flag = 1
    # 找310servant直到找到为止
    while bool(1 - Flag):
        print(' Didn\'t find {}, retry. Attempt{}'.format(servant, time_limit_flag))
        if time_limit_flag > 1:
            time.sleep(15)
            # Flag,Position = Base_func.match_template('Refresh_friend')
        Serial.touch(710, 110)
        time.sleep(1.5)
        Flag, Position = Base_func.match_template('Refresh_decide')
        Serial.touch(Position[0], Position[1])

        Current_state.WaitForFriendShowReady()

        Flag, Position = Base_func.match_template(servant + '_skill_level', False, 0.9)
        time_limit_flag += 1

    if Flag:
        print(' Success find', servant)
        Serial.touch(Position[0], Position[1] - 60)
        time.sleep(1.5)
        Serial.touch(1005, 570)
        print(' Start battle button pressed')


def start_attack():
    # 包含状态监测的函数, 用于点击attack按钮
    fail_times = 0
    while True:  # 点击attack按钮直到进入选卡界面
        Serial.touch(960, 510)
        time.sleep(2)
        Flag, Position = Base_func.match_template('Attack_return')
        if Flag:
            print(" start attack success")
            return
        else:
            fail_times += 1
            if fail_times > 10:
                sent_message("start attack error", -1)


def Master_skill(func=Mystic_Codes.Chaldea_Combat_Uniform, *args):
    # 御主技能模块较复杂, 暂未修改
    Serial.touch(1010, 266)  # 御主技能按键
    time.sleep(1)
    func(*args)
    time.sleep(1)
    Current_state.WaitForBattleStart()
    print(' Master skill{} has pressed'.format(args[0]))
    time.sleep(1)


def character_skill(character_no, skill_no, para=None, check=False):  # 角色编号，技能编号，选人（可选）
    fail_times = 0
    while True:
        Position = (65 + (character_no - 1) * 270 + (skill_no - 1) * 80, 488)
        Serial.touch(Position[0], Position[1])
        time.sleep(3)

        Flag, Position = Base_func.match_template('SkillCancel')
        if Flag:  # 技能成功
            print(' Character{}\'s skill{} success'.format(character_no, skill_no))
            while True:  # 点击一个安全位置(御主头像), 直到退出技能确认界面
                Serial.touch(1000, 100)
                Flag, Position = Base_func.match_template('SkillCancel')
                if not Flag:
                    break
            break

        if para is not None:
            Position = (280 + (para - 1) * 250, 290)  # 选择技能对象. 此处将Y坐标取在较高位置, 防止误触发角色状态
            while True:  # 点击技能对象, 直到释放成功
                Serial.touch(Position[0], Position[1])
                time.sleep(3)  # 等待技能动画时间
                Flag, Position = Base_func.match_template('SkillAim')
                if not Flag:
                    break

        if check is False:  # check = False, 则不检查技能是否成功
            break

        # 技能失败, 注意技能成功释放后的第一次检查一定失败
        fail_times += 1
        if fail_times > 10:
            sent_message(' Character{}\'s skill{} error'.format(character_no, skill_no), -1)

    Current_state.WaitForBattleStart()


def card(TreasureDevice_no=1):
    fail_times = 0
    while True:
        start_attack()  # 点击attack按钮
        Serial.touch(350 + (TreasureDevice_no - 1) * 200, 200)  # 打手宝具,参数可选1-3号宝具位
        Card_index = random.sample(range(0, 4), 2)  # 随机两张牌
        Serial.touch(115 + (Card_index[0]) * 215, 430)
        Serial.touch(115 + (Card_index[1]) * 215, 430)
        time.sleep(10)  # 等待战斗动画播放完成

        Flag, Position = Base_func.match_template('Attack_return')
        if Flag:  # 宝具未成功释放, 卡在Attack界面, 点击返回键回到Battle界面
            fail_times += 1
            if fail_times > 10:
                sent_message(" Card error", -1)
            print(' Card {} failed, restart'.format(TreasureDevice_no))
            while True:  # 点击退出, 直到退回Battle界面
                Serial.touch(Position[0], Position[1])
                Flag, Position = Base_func.match_template('Attack_return')
                if not Flag:
                    break
            Current_state.WaitForBattleStart()
        else:  # 宝具成功释放, 进入Battle界面
            print(' Card {} success'.format(TreasureDevice_no))
            break


def budao():
    while True:
        while True:
            time.sleep(1)
            Flag, Position = Base_func.match_template('Battlefinish_sign')
            if Flag:
                break
            Flag, Position = Base_func.match_template('Attack_button')
            if Flag:
                break
        Flag, Position = Base_func.match_template('Attack_button')
        if Flag:
            start_attack()  # 点击attack按钮
            Card_index = random.sample(range(0, 4), 3)  # 随机三张牌
            Serial.touch(115 + (Card_index[0]) * 215, 430)
            Serial.touch(115 + (Card_index[1]) * 215, 430)
            Serial.touch(115 + (Card_index[2]) * 215, 430)
            print(' Card has pressed')
        else:
            break


def quit_battle():
    time.sleep(15)
    while True:
        time.sleep(1)
        Flag, Position = Base_func.match_template('Battlefinish_sign')
        if Flag:
            break
        Flag, Position = Base_func.match_template('Attack_button')
        if Flag:
            break
    Flag, Position = Base_func.match_template('Attack_button')
    if Flag:
        print(' 翻车，进入补刀程序')  # 翻车检测
        budao()
    print(' Battle finished')
    time.sleep(1)

    # # 礼装掉落检测
    # global num_Craft
    # Flag, Position = Base_func.match_template('Rainbow_box')  # 检测是否掉礼装，若掉落则短信提醒
    # if Flag:
    #     sent_message("掉落礼装!")
    #     num_Craft += 1

    Serial.touch(986, 565, 6)
    Serial.touch(235, 525, 2)  # 拒绝好友申请
    Serial.mouse_set_zero()  # 鼠标复位,防止误差累积
    print(' Quit success')
    time.sleep(1)


def FGO_process(times, servant, Battle_func):
    for i in tqdm(range(times)):
        times -= 1
        ending_state = enter_battle()
        if ending_state == 'AP_recover':
            apple_feed()
        find_friend(servant)
        Battle_func()
        quit_battle()
        print(' ')
        print(' {}times of battles remain.'.format(times))
        print(f'Used {num_GoldApple_used} GoldApples, {num_SilverApple_used} SilverApples, got {num_Craft} Crafts')


Current_state = state()
num_Craft = 0
num_GoldApple_used = 0
num_SilverApple_used = 0


def main(port_no, times, servant, battle_func):
    Serial.port_open(port_no)  # 写入通讯的串口号
    Serial.mouse_set_zero()
    FGO_process(times, servant, battle_func)
    Serial.port_close()
    print(' All done!')


if __name__ == '__main__':
    # main('com5', 50, "ALL", Battle_templates.QP)
    main('com5', 50, "ALL", Battle_templates.GoldenEgg)
    sent_message("脚本完成!", 1)
