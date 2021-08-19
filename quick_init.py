# import win32api
import win32con
import win32gui
# import win32ui

winName = "Wormhole(sipad)"
hwnd = win32gui.FindWindow("Qt5QWindowIcon", winName)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1122, 948, 0)

left, top, right, bot = win32gui.GetWindowRect(hwnd)
width = right - left
height = bot - top

print(left, top, right, bot)
print(width, height)