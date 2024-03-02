import tencent_server_price as tsp
import global_serer_price as gsp
import tkinter as tk
import tkinter.filedialog as tkf
import json
import os


def set_window(width, height, window, root):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置和大小
    window.geometry(f"{width}x{height}+{x}+{y}")


# 复选框选择按钮--全选
def select_all(compass_var_dir):
    for value in compass_var_dir.values():
        var = value[1]
        var.set(1)  # 设置所有复选框为选中状态


# 复选框选择按钮--全不选
def deselect_all(compass_var_dir):
    for value in compass_var_dir.values():
        var = value[1]
        var.set(0)  # 设置所有复选框为未选中状态


# 复选框选择按钮--根据价格进行选择
def select_special(compass_var_dir, root):
    # 预先清空一遍
    deselect_all(compass_var_dir)
    select_special_window = tk.Toplevel(root)
    select_special_window.title("设置最低价格！")
    set_window(200, 200,  select_special_window, root)

    select_special_label = tk.Label(select_special_window, text="请输入最低价格，C为单位")
    select_special_label.place(relx=0.5, rely=0.1, anchor="center")  # 设置提示文本

    entry_price = tk.Entry(select_special_window)
    entry_price.insert(0, "10")  # 设置默认文本
    entry_price.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_price.place(relx=0.5, rely=0.3, anchor="center")  # 将输入框添加到窗口中

    def get_input():
        global price_above
        price_above = entry_price.get()

        try:
            price_above = float(price_above)
        except ValueError:
            # raise Error!
            price_error_window = tk.Toplevel(root)
            price_error_window.title("输入错误！！！！")
            set_window(300, 300, price_error_window, root)
            # 文本提示
            price_error_remind = tk.Label(price_error_window, text="请输入数字！！！！", font=("Courier", 12))
            price_error_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本

        for key, value in compass_var_dir.items():
            if value[0] >= price_above:
                var = value[1]
                var.set(1)  # 设置所有复选框为选中状态
        select_special_window.destroy()

    price_button = tk.Button(select_special_window, text="确定", command=get_input)
    price_button.place(relx=0.5, rely=0.5, anchor="center")  # 设置按钮的位置


# 复选框选择按钮--读取用户自定义配置
def select_user_define(compass_var_dir, root):
    # 预先清空一遍
    deselect_all(compass_var_dir)
    # 弹出保存文件对话框
    filepath = tkf.askopenfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="compass.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="读取配置文件",  # 对话框标题
    )

    if filepath.strip() == '':
        print("用户取消了保存操作。")
    else:
        # 从配置文件加载状态
        try:
            with open(filepath, "r") as config_file:
                config_data = json.load(config_file)
                #print(config_data)
                for compass_in_config, switch_in_config in config_data.items():
                    for compass, data in compass_var_dir.items():
                        if compass == compass_in_config:
                            var = data[1]
                            var.set(switch_in_config)
        except FileNotFoundError:
            file_error_window = tk.Toplevel(root)
            file_error_window.title("配置读取出错！")
            set_window(200, 200, file_error_window, root)
            file_error_label = tk.Label(file_error_window, text="配置文件不存在！！")
            file_error_label.pack()


# 复选框选择按钮--存储用户自定义配置
def save_user_define(compass_var_dir):
    # 弹出保存文件对话框
    filepath = tkf.asksaveasfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="compass.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="保存配置文件",  # 对话框标题
    )

    save_data = {}

    # compass_var_dir格式为 {名称: [价格, 复选框内存地址, 复选框的值]}
    for key, value in compass_var_dir.items():
        value[2] = value[1].get()
        save_data[key] = value[2]

    if filepath:
        # 用户选择了文件名，执行保存操作
        with open(filepath, "w") as file:
            json.dump(save_data, file)


def confirm_config(compass_var_dir, root):
    global compass_list
    try:
        for key, value in compass_var_dir.items():
            value[2] = value[1].get()
            if value[2] == 1:
                compass_list.append(key)

        confirm_window = tk.Toplevel(root)
        confirm_window.title("配置成功！")
        # 设置基础设置窗口为置顶
        confirm_window.attributes('-topmost', True)
        set_window(200, 200, confirm_window, root)
        confirm_label = tk.Label(confirm_window, text="配置成功！！")
        confirm_label.pack()

    except ValueError:
        file_error_window = tk.Toplevel(root)
        file_error_window.title("配置出错！")
        set_window(200, 200, file_error_window, root)
        file_error_label = tk.Label(file_error_window, text="请联系作者！！")
        file_error_label.pack()


def gen_checkbuttons_for_all_compass(price_compass_dir, root):
    checkbuttons_window = tk.Toplevel(root)
    checkbuttons_window.title("罗盘过滤选择！")
    checkbuttons_window.geometry("1700x1000")  # 设置窗口大小

    location_index = 0
    compass_var_dir = {}

    # key是价格, value是罗盘名称
    for key, value in price_compass_dir.items():
        # 创建坐标
        location_index_x, location_index_y = divmod(location_index, 14)
        # 创建复选框
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(checkbuttons_window, text=f"{key}\n价格为:{value} c", variable=var)
        # 设置复选框的位置
        checkbutton.grid(row=location_index_y, column=location_index_x)
        # 循环变量递增
        location_index = location_index + 1
        # 返回价格,罗盘和复选框的字典，方便后面进行高于多少价格的判断，格式为{名称:[价格,复选框内存地址,复选框的值]}
        compass_var_dir[key] = [value, var, var.get()]

    # 创建全选和反选按钮
    select_all_button = tk.Button(checkbuttons_window, text=" \n        全选        \n ", command=lambda: select_all(compass_var_dir))
    select_all_button.grid(row=14, column=1)

    deselect_all_button = tk.Button(checkbuttons_window, text=" \n      全不选      \n ", command=lambda: deselect_all(compass_var_dir))
    deselect_all_button.grid(row=14, column=2)

    price_config_button = tk.Button(checkbuttons_window, text=" \n  根据价格配置  \n ", command=lambda: select_special(compass_var_dir, checkbuttons_window))
    price_config_button.grid(row=14, column=3)

    load_config_button = tk.Button(checkbuttons_window, text=" \n  读取已有配置  \n ", command=lambda: select_user_define(compass_var_dir, checkbuttons_window))
    load_config_button.grid(row=15, column=1)

    save_config_button = tk.Button(checkbuttons_window, text=" \n  保存当前配置  \n ", command=lambda: save_user_define(compass_var_dir))
    save_config_button.grid(row=15, column=2)

    confirm_button = tk.Button(checkbuttons_window, text=" \n        确定        \n ", command=lambda: confirm_config(compass_var_dir, checkbuttons_window))
    confirm_button.grid(row=15, column=3)

    # 创建相关说明文本
    show_text = "\n\n国服数据来源易刷E-farm\nE-farm在线人数越多,价格越精确\n请多多支持！\n\n国际服数据来源TFT！\n\n"
    label_show_text = tk.Label(checkbuttons_window, text=show_text, font=("Courier", 15))
    label_show_text.grid(row=17, column=2)  # 设置提示文本


def Global_checkbuttons(root, choose_server_window):

    Global_TFT_Data_Url = "https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/bulk-compasses.json"
    Global_NINJA_Data_Url = "https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
    global_server_compass_data = gsp.load_TFTdata_from_github(Global_TFT_Data_Url)
    choose_server_window.destroy()
    gen_checkbuttons_for_all_compass(gsp.Global_compass_data_alias(global_server_compass_data, gsp.compass_english2chinese), root)


def Tencent_checkbuttons(root, choose_server_window):

    Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
    tencent_compass_data = tsp.Tencent_compass_data(Tencent_Server_Url)
    choose_server_window.destroy()
    gen_checkbuttons_for_all_compass(tsp.Tencent_compass_data_alias(tencent_compass_data, tsp.compass_list_all), root)


def None_checkbuttons(root, choose_server_window):

    null_compass_price_dir = {}
    choose_server_window.destroy()
    for english, chinese in gsp.compass_english2chinese.items():
        null_compass_price_dir[chinese] = 0
    gen_checkbuttons_for_all_compass(null_compass_price_dir, root)


# todo
def choose_server(root):

    choose_server_window = tk.Toplevel(root)
    choose_server_window.title("选择服务器")
    set_window(300, 300, choose_server_window, root)

    button_chinese = tk.Button(choose_server_window, text="国服数据", command=lambda: Tencent_checkbuttons(root,choose_server_window))
    button_chinese.place(relx=0.5, rely=0.8, anchor="center")  # 设置国服按钮的位置
    button_english = tk.Button(choose_server_window, text="国际服数据", command=lambda: Global_checkbuttons(root,choose_server_window))
    button_english.place(relx=0.5, rely=0.3, anchor="center")  # 设置国际服按钮的位置
    button_league_start = tk.Button(choose_server_window, text="赛季初没数据点我", command=lambda: None_checkbuttons(root,choose_server_window))
    button_league_start.place(relx=0.5, rely=0.55, anchor="center")  # 设置不带价格的按钮位置

# 最终得到的将要被保留的罗盘列表 全局变量
compass_list=[]


if __name__ == "__main__":
    Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
    #tencent_compass_data = tsp.Tencent_compass_data(Tencent_Server_Url)


    Global_TFT_Data_Url = "https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/bulk-compasses.json"
    Global_NINJA_Data_Url = "https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
    global_server_compass_data = gsp.load_TFTdata_from_github(Global_TFT_Data_Url)

    #tsp.Tencent_compass_data_alias(tencent_compass_data, tsp.sextant_list_all)

    root = tk.Tk()
    root.title("Checkbutton Example")
    root.geometry("300x400")  # 设置窗口大小
    gen_checkbuttons_for_all_compass(gsp.Global_compass_data_alias(global_server_compass_data, gsp.compass_english2chinese), root)
#   gen_checkbuttons_for_all_compass(tsp.Tencent_compass_data_alias(tencent_compass_data, tsp.compass_list_all), root)
    root.mainloop()
