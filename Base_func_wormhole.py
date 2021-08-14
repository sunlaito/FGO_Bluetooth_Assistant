# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:50:04 2019

@author: McLaren
"""

# import sys
# sys.path.append(r'D:\Software\FGO_Project')

import cv2 as cv
import numpy as np
# import win32api
import win32con
import win32gui
import win32ui

from Notice import sent_message_fake as sent_message
from config import device_config as config
from config import cur_device


def init_wormhole(device: str = "iPadA3"):
    hwnd = win32gui.FindWindow("Qt5QWindowIcon", config[device]["name"])  # 窗口
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top

    # put the wormhole window at the right side of the screen
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, width, height, 0)
    # win32gui.SetWindowPos(hWnd, InsertAfter, X, Y, cx, cy, Flags)
    # win32con.HWND_TOPMOST: put the window over other windows


class Fuse:
    def __init__(self):
        init_wormhole(cur_device)
        self.value = 0
        self.tolerant_time = 50  # 截取50张图片后仍未发现对应目标则报错
        # 防止程序死在死循环里

    def increase(self):
        self.value += 1

    def reset(self):
        self.value = 0

    def alarm(self):
        if self.value == self.tolerant_time:
            sent_message(text='【FGO】: Encounter a fuse error.')


fuse = Fuse()


def match_template(filename, show_switch=False, err=0.85):
    fuse.increase()
    temppath = './Template/' + filename + '.jpg'
    img = window_capture()
    # img = cv.imread(imgpath)
    player_template = cv.imread(temppath)
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    # 当图片中有与模板匹配度超过95%的部分时：
    if max_val > err:
        # 框选出目标，并标出中心点
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] + player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1] / 2), max_loc[1] + int(player_template.shape[0] / 2))

        if show_switch:
            cv.circle(img, player_spot, 10, (0, 255, 255), -1)
            cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 3)
            cv.namedWindow('FGO_MatchResult', cv.WINDOW_KEEPRATIO)
            cv.imshow("FGO_MatchResult", img)
            # 显示结果2秒钟
            k = cv.waitKey(1000)
            if k == -1:
                cv.destroyAllWindows()

        fuse.reset()
        return True, player_spot
    else:
        fuse.alarm()
        return False, 0


def window_capture():
    hwnd = win32gui.FindWindow("Qt5QWindowIcon", config[cur_device]["name"])  # 窗口
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top

    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, filename)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    # 截取出ios屏幕区域
    y0 = config[cur_device]["top_bias"]
    y1 = height - config[cur_device]["bottom_bias"]
    x0 = config[cur_device]["left_bias"]
    x1 = width - config[cur_device]["right_bias"]
    cropped = img[y0:y1, x0:x1]
    # 裁剪坐标为[y0:y1, x0:x1]
    # cv.imwrite('./Template/cropped_test.jpg', cropped)
    win32gui.DeleteObject(saveBitMap.GetHandle())  # 释放内存
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return cropped
