import tkinter as tk
from tkinter import ttk

from ddq_widgets import FormItem
from ddq_widgets.ddq_text import Text  # 确保导入 ddq_text 组件

class FormItemDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("FormItem 组件示例")
        self.root.geometry("800x600")  # 调整窗口大小以适应分栏
        
        # 创建左右分栏
        self.paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧表单容器
        self.left_frame = ttk.Frame(self.paned)
        self.paned.add(self.left_frame)
        
        # 右侧实时数据显示
        self.right_frame = ttk.Frame(self.paned)
        self.paned.add(self.right_frame)
        
        # 创建一个容器 Frame，用于测试 FormItem 的自适应性
        self.container = ttk.Frame(self.left_frame)
        self.container.pack(fill=tk.X, padx=20, pady=20)
        
        # 创建各种类型的输入控件
        # 1. 文本输入框
        self.input_item = FormItem.input(
            self.container,
            "用户名:"
        )
        
        # 2. 密码输入框
        self.password_item = FormItem.password(
            self.container,
            "密码:"
        )
        
        # 3. 下拉选择框
        self.select_item = FormItem.select(
            self.container,
            "类型:",
            options=["选项1", "选项2", "选项3"]
        )
        
        # 4. 单选框组
        self.radio_item = FormItem.radio(
            self.container,
            "性别:",
            options=["男", "女"]
        )
        
        # 5. 复选框组
        self.checkbox_item = FormItem.checkbox(
            self.container,
            "爱好:",
            options=["阅读", "音乐", "运动"]
        )
        
        # 6. 多行文本框
        self.textarea_item = FormItem.textarea(
            self.container,
            "描述:",
            height=3
        )
        
        # 7. 文件选择器 - 单个文件
        self.file_item = FormItem.file_picker(
            self.container,
            "选择文件:",
            mode="file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        # 8. 文件选择器 - 文件夹
        self.folder_item = FormItem.file_picker(
            self.container,
            "选择目录:",
            mode="folder"
        )
        
        # 9. 文件选择器 - 多按钮模式
        self.multi_item = FormItem.file_picker(
            self.container,
            "多选模式:",
            multiple_buttons=True
        )
        
        # 创建右侧实时数据显示区域
        self.create_data_display()
        
        # 绑定所有表单项的变化事件
        self.bind_change_events()
        
    def create_data_display(self):
        """创建右侧实时数据显示区域"""
        # 标题
        ttk.Label(self.right_frame, text="实时数据", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # 创建文本框用于显示数据
        self.data_display = Text(self.right_frame, wraplength=300)  # 设置合适的 wraplength
        self.data_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
    def bind_change_events(self):
        """绑定所有表单项的变化事件"""
        # 文本输入框
        self.input_item.var.trace_add('write', lambda *args: self.update_display())
        
        # 密码输入框
        self.password_item.var.trace_add('write', lambda *args: self.update_display())
        
        # 下拉选择框
        self.select_item.var.trace_add('write', lambda *args: self.update_display())
        
        # 单选框组
        self.radio_item.var.trace_add('write', lambda *args: self.update_display())
        
        # 复选框组
        for var in self.checkbox_item.vars:
            var.trace_add('write', lambda *args: self.update_display())
        
        # 多行文本框 - 使用定时器检查变化
        self.textarea_item.widget.bind('<KeyRelease>', lambda e: self.update_display())
        
        # 文件选择器
        self.file_item.var.trace_add('write', lambda *args: self.update_display())
        self.folder_item.var.trace_add('write', lambda *args: self.update_display())
        self.multi_item.var.trace_add('write', lambda *args: self.update_display())
        
    def update_display(self):
        """更新右侧数据显示"""
        # 获取所有表单项的值
        values = {
            "用户名": self.input_item.value,
            "密码": self.password_item.value,
            "类型": self.select_item.value,
            "性别": self.radio_item.value,
            "爱好": self.checkbox_item.value,
            "描述": self.textarea_item.value,
            "选择文件": self.file_item.value,
            "选择目录": self.folder_item.value,
            "多选模式": self.multi_item.value
        }
        
        # 格式化显示
        display_text = ""
        for key, value in values.items():
            display_text += f"{key}:\n{value}\n\n"
        
        # 使用 set_text 方法更新显示内容
        self.data_display.set_text(display_text)

def main():
    root = tk.Tk()
    app = FormItemDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()