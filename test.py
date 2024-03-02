import tkinter as tk

root = tk.Tk()

# 创建两个标签和两个文本框
label1 = tk.Label(root, text="Label 1")
label2 = tk.Label(root, text="Label 2")
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

# 使用grid布局放置组件
label1.grid(row=0, column=0)
entry1.grid(row=0, column=1, columnspan=2)  # entry1横跨2列
label2.grid(row=1, column=0)
entry2.grid(row=1, column=1)

root.mainloop()