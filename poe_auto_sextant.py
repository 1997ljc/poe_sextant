import pyautogui
import time
import keyboard as kb
import random
import pyperclip
import tkinter as tk
import log_printer  #输入日志
import tencent_server_price
import sextant_filter_pkg


# 在窗口打印日志并更新
def log_print(logger, msg):
    logger.info(msg)
    root.update()


# 手动进行充能罗盘的过滤
def sextant_filter(compass_list):
    # list = ["传奇怪物掉落腐化", "地图首领由守卫守护", "盗贼", "哈尔", "阻灵", "额外的传奇", "菌潮遭遇战",
    #         "腐化的异界地图中的地图首领", "共鸣", "地图首领额外掉落一件传奇物品", "尼多", "你的魔法地图额外包含",
    #         "托沃", "索伏", "艾许", "击败后可转化", "地图的品质加成", "锈蚀", "火焰", "冰霜", "闪电",
    #         "混沌", "木桶", "回复的生命和", "物理", "你的地图的品质为", "瓦尔之灵", "张额外地图", "腐化的瓦尔怪物",
    #         "反射伤害", "抛光", "尼克", "贪婪", "驱灵"]
    # list_2 = ["精华", "额外深渊", "未鉴定的地图中"]
    flag = 0

    pyautogui.hotkey("ctrl", "c")

    content = pyperclip.paste()  # 将剪贴板中的内容取出并赋值给content

    # 对剪贴版内容进行处理
    content = content.replace("\r", '')
    content = content.replace("\n", '')
    content = content[content.find("--------") + 8:]
    content = content[content.find("--------") + 8:]
    content = content[:content.find("使用剩余")]
    content = content.replace("(enchant)", "")

    for each in compass_list:
        if each in content:
            flag = 1
            break
    else:
            flag = 0

    # 提醒使用者没有点天赋
    if "使用剩余 3 次" in content:
        print(content)
        flag = 2

    return flag, content


# 模拟鼠标在六分仪和虚空石之间的点击操作
def move_click_reuse(void_position, sextant_or_compass):
    global global_run_speed
    # 移动到六分仪处
    pyautogui.moveTo(*sextant_or_compass, duration=0.05+(2 * random.random() - 1)*(global_run_speed/500.0))
    # 右键点击六分仪
    pyautogui.click(button="right")
    # 等待一段时间
    time.sleep(0.1+(global_run_speed-1)/90.0)  # 0.1 --- 0.2
    # 移动到虚空石处
    pyautogui.moveTo(*void_position, duration=0.05+(2 * random.random() - 1)*(global_run_speed/500.0))
    # 左键点击虚空石
    pyautogui.click(button="left")

# 计算背包格子的横纵间隔
def step_cal(location_1,location_2):
    row_step = abs((location_1[0] - location_2[0]) / 11.0)
    col_step = abs((location_1[1] - location_2[1]) / 4.0)
    return row_step,col_step


def auto_save_compass():
    global global_run_speed
    (row_step, col_step) = step_cal(left_up_location,right_down_location)
    # 鼠标移动到对应仓库
    pyautogui.moveTo(*store_location, duration=0.01)
    time.sleep(0.06+(2 * random.random() - 1)*(global_run_speed/500.0))
    # 点击仓库标签进入该仓库
    pyautogui.click(button="left")
    # 按住ctrl
    pyautogui.keyDown("ctrl")
    # 依次点击背包的格子
    for i in range(60):
        if kb.is_pressed('esc'):
            log_print(logger, "结束键被按下,程序终止！！！")
            break

        i_5_a, i_5_b = divmod(i, 5)  # 前面商，后面余数
        # 鼠标移动到背包中位置
        curr_location = ((left_up_location[0] + i_5_a * row_step * 1.0 + 3 * random.random()),
                         (left_up_location[1] + i_5_b * col_step * 1.0) + 3 * random.random())
        pyautogui.moveTo(*curr_location, duration=0.01)
        # 点击鼠标左键
        pyautogui.click(button="left")
    # 松开ctrl
    pyautogui.keyUp("ctrl")
    # 回到通货仓库页
    pyautogui.keyDown("left")
    time.sleep(0.8+(2 * random.random() - 1)*(global_run_speed/500.0))
    pyautogui.keyUp("left")


# 新版运行主体
def whole_process_new(void_position, sextant_position, surveyor_compass_position, sextant_num, compass_num):
    global global_run_speed
    summary_dir = {}

    times = compass_num if (sextant_num >= compass_num) else sextant_num
    (row_step, col_step) = step_cal(left_up_location,right_down_location)

    total_compass_in_one_bag = 0  # 用于记录当前这一背包充能罗盘中的个数，每次到六十个会清零

    for i in range(int(times)):
        if kb.is_pressed('end'):
            log_print(logger, "结束键被按下,程序终止！！！")
            break
        else:
            log_print(logger, "共%d次，当前第%d次" % (int(times), (i + 1)))

            move_click_reuse(void_position, (sextant_position[0] + 5 * random.random(),
                                             sextant_position[1] + 5 * random.random()))

            flag, sextant_text = sextant_filter(sextant_filter_pkg.compass_list)

            if flag == 1:
                continue
            elif flag == 2:
                log_print(logger, "检测到3次罗盘，程序停止！")
                break
            else:
                log_print(logger, ("命中：" + sextant_text))
                if sextant_text in summary_dir.keys():
                    summary_dir[sextant_text] = summary_dir[sextant_text] + 1
                else:
                    summary_dir[sextant_text] = 1

                move_click_reuse(void_position, (surveyor_compass_position[0] + 3 * random.random(),
                                                 surveyor_compass_position[1] + 3 * random.random()))

                i_5_a, i_5_b = divmod(total_compass_in_one_bag, 5)  # 前面商，后面余数

                curr_location = ((right_down_location[0] - i_5_a * row_step * 1.0 + 3 * random.random()),
                                 (left_up_location[1] + i_5_b * col_step * 1.0) + 3 * random.random())
                # 移动到放置位置处
                pyautogui.moveTo(*curr_location, duration=0.05+(2 * random.random() - 1)*(global_run_speed/500.0))
                # 放下六分仪罗盘
                pyautogui.click(button="left")

                total_compass_in_one_bag = total_compass_in_one_bag + 1
                # 满一包了自动停止，或者这里做成自动存包
                if total_compass_in_one_bag == 60:
                    total_compass_in_one_bag = 0
                    if auto_save.get():
                        # 自动存包
                        log_print(logger, "当前背包已满，自动存包开始！")
                        auto_save_compass()
                        log_print(logger, "自动存包结束！")
                    else:
                        break
            # 等待一段时间
            time.sleep(0.05+(2 * random.random() - 1)*(global_run_speed/500.0))

    # 程序结束再存一次包
    log_print(logger, "程序结束，自动存包开始！")
    auto_save_compass()
    log_print(logger, "自动存包结束！")

    # 输出总结报告
    log_print(logger,"***********************")
    log_print(logger,"本次执行获得罗盘如下：")
    log_print(logger,"***********************")
    for key, value in summary_dir.items():
        log_print(logger,(key + "共[%d]个"%value))


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
    window1.title("设置守望石位置")
    set_window(350, 130, window1)
    label1 = tk.ttk.Label(window1, text="鼠标放到守望石位置！", style="poe_style.TLabel")
    label1.pack()

    def check_space(event):
        if event.keysym == "space":
            window1.destroy()
            x1, y1 = pyautogui.position()
            logger.info("守望石位置为: (%d,%d)" % (x1, y1))
            global void_position
            void_position = (x1, y1)

            show_window2()

    window1.bind("<Key>", check_space)
    window1.focus_force()


def show_window2():
    window2 = tk.Toplevel(root)
    window2.title("设置六分仪位置")
    set_window(350, 130, window2)
    label2 = tk.ttk.Label(window2, text="鼠标放到六分仪位置！", style="poe_style.TLabel")
    label2.pack()

    def check_space(event):
        if event.keysym == "space":
            window2.destroy()
            x2, y2 = pyautogui.position()
            logger.info("六分仪位置为: (%d,%d)" % (x2, y2))
            global sextant_position
            sextant_position = (x2, y2)
            show_window3()

    window2.bind("<Key>", check_space)
    window2.focus_force()


def show_window3():
    window3 = tk.Toplevel(root)
    window3.title("设置测绘罗盘位置")
    set_window(350, 130, window3)
    label3 = tk.ttk.Label(window3, text="鼠标放到测绘罗盘位置！", style="poe_style.TLabel")
    label3.pack()

    def check_space(event):
        if event.keysym == "space":
            window3.destroy()
            x3, y3 = pyautogui.position()
            logger.info("测绘罗盘位置为: (%d,%d)" % (x3, y3))
            global surveyor_compass_position
            surveyor_compass_position = (x3, y3)
            show_window4()

    window3.bind("<Key>", check_space)
    window3.focus_force()


def show_window4():
    window4 = tk.Toplevel(root)
    window4.title("设置背包位置")
    set_window(350,130,window4)
    label4 = tk.ttk.Label(window4, text="鼠标放到背包左上格子中间位置！", style="poe_style.TLabel")
    label4.pack()

    def check_space(event):
        if event.keysym == "space":
            window4.destroy()
            show_window5()
            x4, y4 = pyautogui.position()
            logger.info("背包左上位置为: (%d,%d)" % (x4, y4))
            global left_up_location
            left_up_location = (x4, y4)

    window4.bind("<Key>", check_space)
    window4.focus_force()


def show_window5():
    window5 = tk.Toplevel(root)
    window5.title("设置背包位置")
    set_window(350,130,window5)
    label5 = tk.ttk.Label(window5, text="鼠标放到背包右下格子中间位置！", style="poe_style.TLabel")
    label5.pack()

    def check_space(event):
        if event.keysym == "space":
            window5.destroy()
            show_window6()
            x5, y5 = pyautogui.position()
            logger.info("背包右下位置为: (%d,%d)" % (x5, y5))
            global right_down_location
            right_down_location = (x5, y5)

    window5.bind("<Key>", check_space)
    window5.focus_force()


def show_window6():
    window6 = tk.Toplevel(root)
    window6.title("设置仓库页位置")
    set_window(350,130,window6)
    label6 = tk.ttk.Label(window6, text="      鼠标放到罗盘仓库位置！\n切记将通货页移动到最最左边！", style="poe_style.TLabel")
    label6.pack()

    def check_space(event):
        if event.keysym == "space":
            window6.destroy()
            x6, y6 = pyautogui.position()
            logger.info("仓库位置为: (%d,%d)" % (x6, y6))
            global store_location
            store_location = (x6, y6)

    window6.bind("<Key>", check_space)
    window6.focus_force()


# 设置六分仪数量以及测绘罗盘的数量
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

    button_confirm = tk.ttk.Button(show_set_number_window, text="确定", command=get_input)
    button_confirm.place(relx=0.5, rely=0.7, anchor="center")  # 设置按钮在窗口中间

    show_set_number_window.focus_force()


# 绕开测试，直接确定速度挡位
def get_run_speed(entry_speed,show_set_speed_window):
    global global_run_speed
    try:
        run_speed = entry_speed.get()
        run_speed = int(run_speed)
        global_run_speed = run_speed

        if (run_speed > 10) or (run_speed < 1):
            raise ValueError
        log_print(logger, "速度挡位设置成功为：%d"%global_run_speed)
        show_set_speed_window.destroy()
    except ValueError:
        # raise Error!
        speed_error_window = tk.Toplevel(root)
        speed_error_window.title("输入错误！！！！")
        set_window(300, 300, speed_error_window)
        # 文本提示
        entry_speed_remind = tk.Label(speed_error_window, text="请输入1-10的数字！！！！",font=("Courier", 12))
        entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本


# 创建测试所用窗口
def test_run_speed(entry_speed):
    global global_run_speed
    try:
        run_speed = entry_speed.get()
        run_speed = int(run_speed)
        global_run_speed = run_speed

        if (run_speed > 10) or (run_speed < 1):
            raise ValueError

        # 创建测试用窗口
        test_speed_window = tk.Toplevel(root)
        test_speed_window.title("test_run_speed")
        set_window(700, 500, test_speed_window)

        # 文本提示
        test_remind = tk.Label(test_speed_window, text="观察鼠标移动速度！\n测试结束后此窗口自动关闭！\n过程中按住esc即可停止",
                               font=("Courier", 18))
        test_remind.place(relx=0.5, rely=0.5, anchor="center")  # 设置提示文本

        root.update()
        test_x, test_y = pyautogui.position()
        # 循环点击，测试鼠标速度
        for i in (range(10)):
            # 提前关闭窗口
            if kb.is_pressed('esc'):
                break
            else:
                pyautogui.moveTo(*(test_x, test_y), duration=0.05+(2 * random.random() - 1)*(global_run_speed/500.0))
                time.sleep(0.1*global_run_speed)
                pyautogui.moveTo(*(test_x + 200, test_y - 100), duration=0.05+(2 * random.random() - 1)*(global_run_speed/500.0))
                time.sleep(0.1*global_run_speed)
        # 本次测试结束，关闭窗口
        test_speed_window.destroy()
    except ValueError:
        # raise Error!
        speed_error_window = tk.Toplevel(root)
        speed_error_window.title("输入错误！！！！")
        set_window(300, 300, speed_error_window)
        # 文本提示
        entry_speed_remind = tk.Label(speed_error_window, text="请输入1-10的数字！！！！",font=("Courier", 12))
        entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本


def set_run_speed():

    show_set_speed_window = tk.Toplevel(root)
    show_set_speed_window.title("set_run_speed")
    set_window(350, 200, show_set_speed_window)
    # 输入框
    entry_speed = tk.Entry(show_set_speed_window, width=15, font=("Arial", 15))
    entry_speed.insert(0, "输入速度挡位")  # 设置默认文本
    entry_speed.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_speed.place(relx=0.5, rely=0.45, anchor="center")  # 输入框位置

    # 文本提示
    entry_speed_remind = tk.Label(show_set_speed_window, text="输入1(快)-10(慢)的数字选择速度挡位！", font=("Courier", 12))
    entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本
    # 创建测试按钮
    test_button = tk.ttk.Button(show_set_speed_window, text=" \n  点我测试速度  \n ", command=lambda: test_run_speed(entry_speed))
    test_button.place(relx=0.3, rely=0.75, anchor="center")  # 设置按钮的位置
    button_confirm = tk.ttk.Button(show_set_speed_window, text=" \n  确定  \n ", command=lambda: get_run_speed(entry_speed,show_set_speed_window))
    button_confirm.place(relx=0.7, rely=0.75, anchor="center")  # 设置按钮的位置


def run_it():
    # 设置基础设置窗口为置顶
    root.attributes('-topmost', True)
    # 移动到虚空石处
    whole_process_new(void_position, sextant_position, surveyor_compass_position, int(sextant_input), int(compass_input))
    # 取消基础设置窗口为置顶
    root.attributes('-topmost', False)


# 创建主窗口
root = tk.Tk()
root.title("全自动罗盘")
set_window(500, 400, root)

# 速度挡位参数
global global_run_speed
global_run_speed = 2

# 定义窗口的标签风格
style = tk.ttk.Style()
style.configure("poe_style.TLabel", font=("Times new roman", 16))

# 创建提示文本
label_remind = tk.Label(root, text="记得在舆图界面打开背包和仓库！", font=("Courier", 15))
label_remind.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本
# 创建按钮
button1 = tk.ttk.Button(root, text="点我设置坐标", command=show_window1)
button1.place(relx=0.2, rely=0.3, anchor="center")  # 设置按钮的位置
button2 = tk.ttk.Button(root, text="点击设置数量", command=set_number)
button2.place(relx=0.2, rely=0.45, anchor="center")  # 设置按钮的位置
button3 = tk.ttk.Button(root, text="设置速度挡位", command=set_run_speed)
button3.place(relx=0.2, rely=0.6, anchor="center")  # 设置按钮的位置
button4 = tk.ttk.Button(root, text="点击运行", command=run_it)
button4.place(relx=0.2, rely=0.75, anchor="center")  # 设置按钮的位置
button5 = tk.ttk.Button(root, text=" \n  设置罗盘过滤  \n ", command=lambda: sextant_filter_pkg.choose_server(root))
button5.place(relx=0.5, rely=0.3, anchor="center")  # 设置按钮的位置
# 创建复选框，用于选择是否开启自动存包功能
auto_save = tk.IntVar()
checkbutton1 = tk.Checkbutton(root, text="自动存包", variable=auto_save)
checkbutton1.place(relx=0.8, rely=0.3, anchor="center")  # 设置复选框的位置
# 创建日志框
sextant_log = tk.Text(root, wrap=tk.WORD, height=10, width=40)
sextant_log.place(relx=0.65, rely=0.6, anchor="center") # 设置日志框的位置
# 创建日志记录器
logger = log_printer.gen_logger(sextant_log)

# 进入主事件循环
root.mainloop()
