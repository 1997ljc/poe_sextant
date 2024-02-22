import logging
import tkinter as tk


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)


def gen_logger(log_text):
    logging.basicConfig()
    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建一个文本处理器，将日志写入文本框
    text_handler = TextHandler(log_text)
    logger.addHandler(text_handler)

    # 返回logger方便别处调用
    return logger
