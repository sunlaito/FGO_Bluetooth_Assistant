def battle():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始
    Current_state.WaitForBattleStart()
    # time.sleep(6)                   #等待6秒，因为礼装效果掉落暴击星会耗时
    # Turn1
    character_skill(3, 1, 1)
    character_skill(2, 1, 1)
    character_skill(1, 1)
    character_skill(1, 3, 1)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn2
    character_skill(3, 3, 1)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3, 3, 2)
    character_skill(3, 3)
    character_skill(3, 2)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn3
    character_skill(3, 1, 1)
    character_skill(2, 3, 1)
    card()