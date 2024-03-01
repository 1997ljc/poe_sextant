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
def select_special(compass_var_dir, price_above,root):
    # 预先清空一遍
    deselect_all(compass_var_dir)

    for key, value in compass_var_dir.items():
        if value[0] >= float(price_above):
                var = value[1]
                var.set(1)  # 设置所有复选框为选中状态


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
                print(config_data)
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
    #compass_var_dir格式为 {名称: [价格, 复选框内存地址, 复选框的值]}
    for key, value in compass_var_dir.items():
        value[2] = value[1].get()
        save_data[key] = value[2]

    if filepath:
        # 用户选择了文件名，执行保存操作
        with open(filepath, "w") as file:
            json.dump(save_data, file)


def confirm_config(compass_var_dir,root):
    global compass_list
    try:
        for key, value in compass_var_dir.items():
            value[2] = value[1].get()
            if value[2] == 1:
                compass_list.append(key)

        confirm_window = tk.Toplevel(root)
        confirm_window.title("配置成功！")
        set_window(200, 200, confirm_window, root)
        confirm_label = tk.Label(confirm_window, text="配置成功！！")
        confirm_label.pack()

    except ValueError:
        file_error_window = tk.Toplevel(root)
        file_error_window.title("配置=出错！")
        set_window(200, 200, file_error_window, root)
        file_error_label = tk.Label(file_error_window, text="请联系作者！！")
        file_error_label.pack()


def gen_checkbuttons_for_all_compass(price_compass_dir, root):
    checkbuttons_window = tk.Toplevel(root)
    checkbuttons_window.title("罗盘过滤选择！")
    checkbuttons_window.geometry("1800x800")  # 设置窗口大小
    location_index = 0
    compass_var_dir = {}

    # key是价格, value是罗盘名称
    for key, value in price_compass_dir.items():
        # 创建坐标
        location_index_x, location_index_y = divmod(location_index, 12)
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
    select_all_button = tk.Button(checkbuttons_window, text="Select All", command=lambda: select_all(compass_var_dir))
    select_all_button.grid(row=14, column=1)

    deselect_all_button = tk.Button(checkbuttons_window, text="Deselect All", command=lambda: deselect_all(compass_var_dir))
    deselect_all_button.grid(row=14, column=2)

    deselect_all_button = tk.Button(checkbuttons_window, text="根据价格设置", command=lambda: select_special(compass_var_dir, 5, root))
    deselect_all_button.grid(row=14, column=3)

    user_define_button = tk.Button(checkbuttons_window, text="读取已有设置", command=lambda: select_user_define(compass_var_dir, checkbuttons_window))
    user_define_button.grid(row=16, column=1)

    user_define_button = tk.Button(checkbuttons_window, text="保存当前设置", command=lambda: save_user_define(compass_var_dir))
    user_define_button.grid(row=16, column=2)

    confirm_button = tk.Button(checkbuttons_window, text="     确定     ", command=lambda: confirm_config(compass_var_dir, checkbuttons_window))
    confirm_button.grid(row=16, column=3)


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





# todo
def choose_server(root):

    choose_server_window = tk.Toplevel(root)
    choose_server_window.title("选择服务器")
    set_window(200, 200, choose_server_window, root)

    button_chinese = tk.ttk.Button(choose_server_window, text="国服数据", command=lambda: Tencent_checkbuttons(root,choose_server_window))
    button_chinese.place(relx=0.5, rely=0.75, anchor="center")  # 设置按钮的位置
    button_english = tk.ttk.Button(choose_server_window, text="国际服数据", command=lambda: Global_checkbuttons(root,choose_server_window))
    button_english.place(relx=0.5, rely=0.3, anchor="center")  # 设置按钮的位置


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
