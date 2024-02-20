import pyautogui
import time
import keyboard as kb
import random
import pyperclip
import tkinter as tk


# 手动进行充能罗盘的过滤
def sextant_filter():
    list = ["传奇怪物掉落腐化", "地图首领由守卫守护", "盗贼", "哈尔", "阻灵", "额外的传奇", "菌潮遭遇战",
            "腐化的异界地图中的地图首领", "共鸣", "地图首领额外掉落一件传奇物品", "尼多", "你的魔法地图额外包含",
            "托沃", "索伏", "艾许", "击败后可转化", "地图的品质加成", "锈蚀", "火焰", "冰霜", "闪电",
            "混沌", "木桶", "回复的生命和", "物理", "你的地图的品质为", "瓦尔之灵", "张额外地图", "腐化的瓦尔怪物",
            "反射伤害", "抛光"]
    list_2 = ["精华", "额外深渊", "未鉴定的地图中"]
    flag = 0

    pyautogui.hotkey("ctrl", "c")

    content = pyperclip.paste()  # 将剪贴板中的内容取出并赋值给content
    for each in list:
        if each in content:
            flag = 1
            print(each)
            break
        else:
            flag = 0

    return flag


# 模拟鼠标在六分仪和虚空石之间的点击操作
def move_click_reuse(void_position, sextant_or_compass):
    # 移动到六分仪处
    pyautogui.moveTo(*sextant_or_compass, duration=0.05)
    # 右键点击六分仪
    pyautogui.click(button="right")
    # 等待一段时间
    time.sleep(0.1)
    # 移动到虚空石处
    pyautogui.moveTo(*void_position, duration=0.05)
    # 左键点击虚空石
    pyautogui.click(button="left")


# 整个程序的运行主体
def whole_process(void_position, sextant_location, compass_location, full_compass_start_location, sextant_num,
                  compass_num, row_step, col_step):
    times = compass_num if (sextant_num >= compass_num) else sextant_num

    for i in range(int(times)):
        if kb.is_pressed('space'):
            print("空格键被按下！")
            break
        else:
            i_10_a, i_10_b = divmod(i, 10)  # 前面商，后面余数
            i_5_a, i_5_b = divmod(i, 5)
            move_click_reuse(void_position, (sextant_location[0] + 3 * random.random(),
                                             sextant_location[1] + col_step * i_10_a * 1.0 + 3 * random.random()))

            flag = sextant_filter();

            if (flag == 1):
                continue
            else:
                move_click_reuse(void_position, (compass_location[0] + 3 * random.random(),
                                                 compass_location[1] + col_step * i_10_a * 1.0 + 3 * random.random()))
                curr_location = ((full_compass_start_location[0] - i_5_a * row_step * 1.0 + 3 * random.random()),
                                 (full_compass_start_location[1] + col_step * i_5_b * 1.0) + 3 * random.random())
                # 移动到放置位置处
                # pyautogui.moveTo(*left_up_location, duration=0.2)
                pyautogui.moveTo(*curr_location, duration=0.05)
                # 放下六分仪罗盘
                pyautogui.click(button="left")
            # 等待一段时间
            time.sleep(0.05)


def whole_process_new(void_position, sextant_position, surveyor_compass_position, sextant_num, compass_num):

    times = compass_num if (sextant_num >= compass_num) else sextant_num
    row_step = abs((left_up_location[0] - right_down_location[0]) / 11.0)
    col_step = abs((left_up_location[1] - right_down_location[1]) / 4.0)
    total_compass_in_one_bag = 0  # 用于记录当前这一背包充能罗盘中的个数，每次到六十个会清零

    for i in range(int(times)):
        if kb.is_pressed('esc'):
            print("结束键被按下！")
            break
        else:
            move_click_reuse(void_position, (sextant_position[0] + 3 * random.random(),
                                             sextant_position[1] + 3 * random.random()))

            flag = sextant_filter()

            if flag == 1:
                continue
            else:
                move_click_reuse(void_position, (surveyor_compass_position[0] + 3 * random.random(),
                                                 surveyor_compass_position[1] + 3 * random.random()))

                i_5_a, i_5_b = divmod(total_compass_in_one_bag, 5)  # 前面商，后面余数

                curr_location = ((right_down_location[0] - i_5_a * row_step * 1.0 + 3 * random.random()),
                                 (left_up_location[1] + i_5_b * col_step * 1.0) + 3 * random.random())
                # 移动到放置位置处
                pyautogui.moveTo(*curr_location, duration=0.05)
                # 放下六分仪罗盘
                pyautogui.click(button="left")

                total_compass_in_one_bag = total_compass_in_one_bag + 1
                # 满一包了自动停止，或者这里做成自动存包
                if total_compass_in_one_bag == 20:
                    total_compass_in_one_bag = 0
                    break
                    # function自动存包

            # 等待一段时间
            time.sleep(0.05)


def set_window(width, height, window):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置和大小
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_window1():
    window1 = tk.Toplevel(root)
    window1.title("Window 1")
    set_window(300, 200, window1)
    label1 = tk.ttk.Label(window1, text="鼠标放到守望石位置！")
    label1.pack()

    def check_space(event):
        if event.keysym == "space":
            window1.destroy()
            x1, y1 = pyautogui.position()
            global void_position
            void_position = (x1, y1)
            show_window2()

    window1.bind("<Key>", check_space)
    window1.focus_force()


def show_window2():
    window2 = tk.Toplevel(root)
    window2.title("Window 2")
    set_window(300, 200, window2)
    label2 = tk.ttk.Label(window2, text="鼠标放到六分仪位置！")
    label2.pack()

    def check_space(event):
        if event.keysym == "space":
            window2.destroy()
            x2, y2 = pyautogui.position()
            global sextant_position
            sextant_position = (x2, y2)
            show_window3()

    window2.bind("<Key>", check_space)
    window2.focus_force()


def show_window3():
    window3 = tk.Toplevel(root)
    window3.title("Window 3")
    set_window(300, 200, window3)
    label3 = tk.ttk.Label(window3, text="鼠标放到测绘罗盘位置！")
    label3.pack()

    def check_space(event):
        if event.keysym == "space":
            window3.destroy()
            x3, y3 = pyautogui.position()
            global surveyor_compass_position
            surveyor_compass_position = (x3, y3)
            show_window4()

    window3.bind("<Key>", check_space)
    window3.focus_force()


def show_window4():
    window4 = tk.Toplevel(root)
    window4.title("Window 4")
    set_window(300,200,window4)
    label4 = tk.ttk.Label(window4, text="鼠标放到背包左上格子中间位置！")
    label4.pack()

    def check_space(event):
        if event.keysym == "space":
            window4.destroy()
            show_window5()
            x4, y4 = pyautogui.position()
            global left_up_location
            left_up_location = (x4, y4)

    window4.bind("<Key>", check_space)
    window4.focus_force()


def show_window5():
    window5 = tk.Toplevel(root)
    window5.title("Window 4")
    set_window(300,200,window5)
    label5 = tk.ttk.Label(window5, text="鼠标放到背包右下格子中间位置！")
    label5.pack()

    def check_space(event):
        if event.keysym == "space":
            window5.destroy()
#            root.destroy()
            x5, y5 = pyautogui.position()
            global right_down_location
            right_down_location = (x5, y5)

    window5.bind("<Key>", check_space)
    window5.focus_force()


def set_number():
    show_set_number_window = tk.Toplevel(root)
    show_set_number_window.title("set_number_window")
    set_window(300, 200, show_set_number_window)

    entry_sextant = tk.Entry(show_set_number_window)
    entry_sextant.insert(0, "输入六分仪数量")  # 设置默认文本
    entry_sextant.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_sextant.pack()  # 将输入框添加到窗口中
    entry_compass = tk.Entry(show_set_number_window)
    entry_compass.insert(0, "输入罗盘数量")  # 设置默认文本
    entry_compass.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_compass.pack()  # 将输入框添加到窗口中

    def get_input():
        global sextant_input
        global compass_input
        sextant_input = entry_sextant.get()
        compass_input = entry_compass.get()
        show_set_number_window.destroy()
        root.attributes('-topmost', True)

    button_confirm = tk.ttk.Button(show_set_number_window, text="确定", command=get_input)
    button_confirm.place(relx=0.5, rely=0.7, anchor="center")  # 设置按钮在窗口中间

    show_set_number_window.focus_force()


def run_it():

    # 移动到虚空石处
    whole_process_new(void_position, sextant_position, surveyor_compass_position, int(sextant_input), int(compass_input))


# 创建主窗口
root = tk.Tk()
root.title("全自动罗盘")
set_window(300, 200, root)


# 创建提示文本
label_remind = tk.Label(root, text="记得在舆图界面打开背包和仓库！", font=("Courier", 12))
label_remind.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本
# 创建按钮
button1 = tk.ttk.Button(root, text="点我设置坐标", command=show_window1)
button1.place(relx=0.5, rely=0.3, anchor="center")  # 设置按钮在窗口中间
button2 = tk.ttk.Button(root, text="点击设置数量", command=set_number)
button2.place(relx=0.5, rely=0.5, anchor="center")  # 设置按钮在窗口中间
button3 = tk.ttk.Button(root, text="点击运行", command=run_it)
button3.place(relx=0.5, rely=0.7, anchor="center")  # 设置按钮在窗口中间

# 进入主事件循环
root.mainloop()
