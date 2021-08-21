# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""
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
        Flag, Position = Base_func.match_template('Menu_button')
        while bool(1 - Flag):
            time.sleep(1)
            Flag, Position = Base_func.match_template('Menu_button')
            if Flag:
                break
            Flag, Position = Base_func.match_template('reenter_battle')
            if Flag:
                break

    def WaitForBattleStart(self):
        Flag, Position = Base_func.match_template('Attack_button')
        while bool(1 - Flag):
            time.sleep(1)
            Flag, Position = Base_func.match_template('Attack_button')

    def WaitForFriendShowReady(self):
        Flag, Position = Base_func.match_template('friend_sign')
        while bool(1 - Flag):
            time.sleep(1)
            Flag, Position = Base_func.match_template('friend_sign')
            if Flag:
                break
            Flag, Position = Base_func.match_template('no_friend')
            if Flag:
                break


Current_state = state()

num_Craft = 0
num_GoldApple_used = 0
num_SilverApple_used = 0


def enter_battle():
    Current_state.HasBackToMenu()
    # 确认已经返回菜单界面，或检测到连续出击按键
    Flag, Position = Base_func.match_template('reenter_battle')
    if Flag:
        Serial.touch(705, 475)
        print(' ')
        print(' Reenter battle success')
        return

    Flag, Position = Base_func.match_template('LastOrder_sign')
    if Flag:
        Serial.touch(Position[0] + 230, Position[1] + 50)
        print(' ')
        print(' Enter battle success')
    else:
        Serial.touch(791, 155)
        print(' ')
        print(' Enter battle by clicking the default position')


def apple_feed():
    global num_GoldApple_used, num_SilverApple_used
    time.sleep(1.5)
    Flag, Position = Base_func.match_template('AP_recover')
    if Flag:
        Flag, Position = Base_func.match_template('Silver_apple')
        if Flag:
            Serial.touch(709, Position[1])
            time.sleep(1.5)
            Flag, Position = Base_func.match_template('Feedapple_decide')
            if Flag:
                Serial.touch(Position[0], Position[1])
                num_SilverApple_used += 1
                print(' Feed silver apple success')
            else:
                sent_message(" Feed silver apple error", -1)
        else:
            Flag, Position = Base_func.match_template('Gold_apple')
            if Flag:
                Serial.touch(709, Position[1])
                time.sleep(1.5)
                Flag, Position = Base_func.match_template('Feedapple_decide')
                if Flag:
                    Serial.touch(Position[0], Position[1])
                    num_GoldApple_used += 1
                    print(' Feed gold apple success')
                else:
                    sent_message(" Feed gold apple error", -1)
            else:
                print(' No apple remain')
                Serial.touch(0, 0)
                sys.exit(0)
    else:
        print(' No need to feed apple')


def find_friend(servant):
    Current_state.WaitForFriendShowReady()

    if servant == "ALL":
        print(' Just pick the first friend')
        Serial.touch(500, 240)
        time.sleep(1.5)
        Serial.touch(1005, 570)
        print(' Start battle button pressed')
        return

    Flag, Position = Base_func.match_template(servant + '_skill_level', False, 0.9)
    time_limit_flag = 1
    # 找310CBA直到找到为止
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
    while True:
        Serial.touch(960, 510)  # 点击attack按钮
        time.sleep(2)
        Flag, Position = Base_func.match_template('Attack_return')
        if Flag:
            print(" start attack success")
            return
        else:
            fail_times += 1
            if fail_times > 10:
                sent_message("start attack error", -1)


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


def Master_skill(func=Mystic_Codes.Chaldea_Combat_Uniform, *args):
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
            Serial.touch(1000, 100)  # 点击一个安全位置(御主头像), 退出技能确认界面
            break

        if para is not None:
            Position = (280 + (para - 1) * 250, 290)  # 技能选人, 点击的Y坐标取较高位置, 防止误触发角色状态
            Serial.touch(Position[0], Position[1])
            time.sleep(3)  # 等待技能动画时间

        if check is False:
            break  # 不检查技能

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

        time.sleep(10) # 等待战斗动画播放完成
        Flag, Position = Base_func.match_template('Attack_return')
        if Flag:  # 宝具未成功释放, 卡在Attack界面, 点击返回键回到Battle界面
            fail_times += 1
            if fail_times > 10:
                sent_message(" Card error", -1)
            print(' Card {} failed, restart'.format(TreasureDevice_no))
            Serial.touch(Position[0], Position[1])
            Current_state.WaitForBattleStart()
        else:  # 宝具成功释放, 进入Battle界面
            print(' Card {} success'.format(TreasureDevice_no))
            break




def FGO_process(times, servant, Battle_func):
    for i in tqdm(range(times)):
        times -= 1
        enter_battle()
        apple_feed()
        find_friend(servant)
        Battle_func()
        quit_battle()
        print(' ')
        print(' {}times of battles remain.'.format(times))
        print('Currently {} Gold Apples, {} Silver Apples used, {} Crafts dropped.'.format(num_GoldApple_used,
                                                                                           num_SilverApple_used,
                                                                                           num_Craft))


def main(port_no, times, servant, battle_func):
    Serial.port_open(port_no)  # 写入通讯的串口号
    Serial.mouse_set_zero()
    FGO_process(times, servant, battle_func)
    Serial.port_close()
    print(' All done!')


if __name__ == '__main__':
    main('com5', 50, "ALL", Battle_templates.QP)
    # main('com5', 50, "ALL", Battle_templates.GoldenEgg)
    sent_message("脚本完成!", 1)
