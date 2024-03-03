import tkinter as tk

def on_scroll(*args):
    canvas.yview(*args)  # 将滚动条与画布关联

root = tk.Tk()
root.title("垂直滚动条示例")

# 创建一个画布
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack()

# 创建一个垂直滚动条
scrollbar = tk.Scrollbar(root, orient="vertical", command=on_scroll)
scrollbar.pack(side="right", fill="y")  # 放置在右侧并填充垂直方向

# 将画布与滚动条关联
canvas.config(yscrollcommand=scrollbar.set)

# 在画布上添加一些文本
for i in range(20):
    canvas.create_text(200, 20 * i, text=f"Line {i + 1}", anchor="w")

root.mainloop()