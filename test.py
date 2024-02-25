import tkinter as tk

def select_all():
    for var in checkbox_vars:
        var.set(1)  # 设置所有复选框为选中状态

def deselect_all():
    for var in checkbox_vars:
        var.set(0)  # 设置所有复选框为未选中状态

root = tk.Tk()
root.title("Select All Checkboxes Example")

# 创建50个复选框
checkbox_vars = []  # 存储复选框的变量
for i in range(50):
    var = tk.IntVar()
    checkbox_vars.append(var)
    checkbutton = tk.Checkbutton(root, text=f"Option {i+1}", variable=var)
    checkbutton.grid(row=i // 5, column=i % 5, sticky="w")

# 创建全选和反选按钮
select_all_button = tk.Button(root, text="Select All", command=select_all)
select_all_button.grid(row=10, column=0)

deselect_all_button = tk.Button(root, text="Deselect All", command=deselect_all)
deselect_all_button.grid(row=10, column=1)

root.mainloop()