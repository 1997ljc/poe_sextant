import tkinter as tk

root = tk.Tk()
entry = tk.Entry(root)
entry.insert(0, "默认值")
entry.pack()

root.mainloop()