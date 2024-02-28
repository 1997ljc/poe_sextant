import tencent_server_price as tsp
import global_serer_price as gsp
import tkinter as tk


#复选框选择按钮--全选
def select_all(compass_var_dir):
    for var in compass_var_dir.values():
        var.set(1)  # 设置所有复选框为选中状态


#复选框选择按钮--全不选
def deselect_all(compass_var_dir):
    for var in compass_var_dir.values():
        var.set(0)  # 设置所有复选框为未选中状态


#根复选框选择按钮--据价格进行选择
def select_special(compass_var_dir,price_compass_dir,price_above,root):
    # 预先清空一遍
    deselect_all(compass_var_dir)

    for key, var in compass_var_dir.items():
        if key in price_compass_dir.keys():
            if price_compass_dir[key] >= float(price_above):
                var.set(1)  # 设置所有复选框为选中状态
        else:
            window_error = tk.Toplevel(root)
            window_error.title("错误！")
            label_error = tk.Label(window_error, text="请联系作者！", font=("Courier", 12))
            label_error.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本
            window_error.geometry("300*400")


def gen_checkbuttons_for_all_compass(price_compass_dir,root):
    window1 = tk.Toplevel(root)
    window1.title("罗盘过滤选择！")
    window1.geometry("2000x800")  # 设置窗口大小
    location_index = 0
    #count = len(price_compass_dir)

    compass_var_dir = {}

    for key, value in price_compass_dir.items():
        # 创建坐标
        location_index_x, location_index_y = divmod(location_index, 12)
        # 创建复选框
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(window1, text=f"{key}\n价格为:{value} c", variable=var)
        # 设置复选框的位置
        checkbutton.grid(row=location_index_y, column=location_index_x)
        # 循环变量递增
        location_index = location_index + 1
        # 返回价格和复选框的字典，方便后面进行高于多少价格的判断
        compass_var_dir[key] = var

    # 创建全选和反选按钮
    select_all_button = tk.Button(window1, text="Select All", command=lambda: select_all(compass_var_dir))
    select_all_button.grid(row=14, column=2)

    deselect_all_button = tk.Button(window1, text="Deselect All", command=lambda: deselect_all(compass_var_dir))
    deselect_all_button.grid(row=14, column=3)

    deselect_all_button = tk.Button(window1, text="根据价格设置", command=lambda: select_special(compass_var_dir,price_compass_dir,5,root))
    deselect_all_button.grid(row=14, column=4)


def Global_checkbuttons(root):
    Global_TFT_Data_Url = "https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/bulk-compasses.json"
    Global_NINJA_Data_Url = "https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
    global_server_compass_data = gsp.load_TFTdata_from_github(Global_TFT_Data_Url)
    gen_checkbuttons_for_all_compass(gsp.Global_compass_data_alias(global_server_compass_data, gsp.compass_english2chinese), root)


def Tencent_checkbuttons(root):
    Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
    tencent_compass_data = tsp.Tencent_compass_data(Tencent_Server_Url)
    gen_checkbuttons_for_all_compass(tsp.Tencent_compass_data_alias(tencent_compass_data, tsp.compass_list_all), root)

# todo
def choose_server(root):
    print("TODO")

if __name__ == "__main__":
    Tencent_Server_Url = "https://gitee.com/hhzxxx/exilence-next-tx-release/raw/master/price2.txt"
    tencent_compass_data = tsp.Tencent_compass_data(Tencent_Server_Url)

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
