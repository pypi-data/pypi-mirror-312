import tkinter as tk
from tkinter import ttk

from ddq_widgets import Form, Card

class FilePickerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("FilePicker 组件示例")
        self.root.geometry("500x300")
        
        # 创建主表单
        self.form = Form(root)
        
        # 创建文件选择分区
        self.file_section = self.form.section("文件选择")
        
        # 添加文件选择器，确保标签在左侧
        self.file_section.file_picker(
            "file",
            "简历文件:",  # 标签文本
            mode="file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        
        # 创建数据显示卡片
        self.data_card = Card(root, title="选择结果")
        self.data_card.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建文本显示区域
        self.data_text = ttk.Label(
            self.data_card.content,
            text="未选择文件",
            wraplength=400,
            justify=tk.LEFT
        )
        self.data_text.pack(fill=tk.X, padx=5, pady=5)
        
        # 设置表单变化回调
        self.form.on_change(self._handle_change)
        
        # 设置默认值
        self.form.set_defaults({
            "file": ""
        })
        
    def _handle_change(self, values):
        """处理表单值变化"""
        file_path = values.get('file', '')
        display_text = f"选择的文件: {file_path if file_path else '未选择'}"
        self.data_text.config(text=display_text)

def main():
    root = tk.Tk()
    app = FilePickerDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 