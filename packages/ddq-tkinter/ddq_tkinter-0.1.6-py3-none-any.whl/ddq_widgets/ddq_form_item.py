import tkinter as tk
from tkinter import ttk
from typing import Optional, Literal, Any, List

# 添加 FilePicker 导入
from .ddq_file_picker import FilePicker
from .ddq_radio import Radio
from .ddq_checkbox import Checkbox
from .ddq_text import Text

class FormItem(ttk.Frame):
    """表单项组件,处理标签和输入控件的布局和对齐"""
    
    def __init__(
        self,
        master,
        label: str,
        required: bool = False,  # 添加必填参数
        widget: Optional[tk.Widget] = None,
        label_width: int = 12,
        label_anchor: Literal["w", "e"] = "e",
        layout: Literal["horizontal", "vertical"] = "horizontal",
        **kwargs
    ):
        frame_kwargs = {k: v for k, v in kwargs.items() 
                    if k not in ['mode', 'filetypes']}
        
        super().__init__(master, **frame_kwargs)
        self.pack(fill=tk.X)
        
        # 创建标签，如果是必填项则使用红色
        self.label = ttk.Label(
            self,
            text=label,
            anchor=label_anchor,
            width=label_width,
            foreground="red" if required else "black"  # 如果是必填项，文本为红色
        )
        
        # 设置输入控件
        self.widget = None
        if widget is not None:
            self.widget = self._setup_widget(widget)
            
        # 应用布局
        self._apply_layout(layout)
        
        # 添加事件回调列表
        self._change_callbacks = []
        
    def _create_label(self, label: str, width: int, anchor: str) -> ttk.Label:
        """创建并配置标签"""
        return ttk.Label(
            self,
            text=label,
            anchor=anchor,
            width=width
        )

    def _setup_widget(self, widget: tk.Widget) -> tk.Widget:
        """设置输入控件"""
        widget.master = self
        
        # 绑定变量
        if hasattr(widget, 'var'):
            self.var = widget.var
        if hasattr(widget, 'vars'):
            self.vars = widget.vars
            
        return widget
    
    def _apply_layout(self, layout: str):
        """应用布局"""
        if layout == "horizontal":
            # 水平布局：标签在左，输入控件在右
            self.label.pack(side=tk.LEFT, padx=(0, 4))
            if self.widget:
                self.widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        else:
            # 垂直布局：标签在上，输入控件在下
            self.label.pack(side=tk.TOP, anchor="w", pady=(0, 4))
            if self.widget:
                self.widget.pack(side=tk.TOP, fill=tk.X, expand=True)

    def set_state(self, state: str):
        """统一的状态设置方法"""
        if isinstance(self.widget, FilePicker):
            self.widget.set_state(state)
        elif isinstance(self.widget, (ttk.Entry, ttk.Combobox)):
            self.widget.configure(state=state)
        elif isinstance(self.widget, tk.Text):
            self.widget.configure(state='disabled' if state != 'normal' else 'normal')
        elif isinstance(self.widget, ttk.Frame):
            for child in self.widget.winfo_children():
                if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton, ttk.Button)):
                    child.configure(state=state)
        elif isinstance(self.widget, Text):
            self.widget.set_state(state)

    @classmethod
    def input(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建文本输入框"""
        item = cls(master, label, **kwargs)
        var = tk.StringVar()
        entry = ttk.Entry(item, textvariable=var)
        item.widget = item._setup_widget(entry)
        item.var = var  # 保存变量引用
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def password(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建密码输入框"""
        item = cls(master, label, **kwargs)
        var = tk.StringVar()
        entry = ttk.Entry(item, show="*", textvariable=var)
        item.widget = item._setup_widget(entry)
        item.var = var  # 保存变量引用
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def select(cls, master, label: str, options: List[str], **kwargs) -> 'FormItem':
        """创建下拉选择框"""
        item = cls(master, label, **kwargs)
        var = tk.StringVar()
        combo = ttk.Combobox(
            item,
            values=options,
            textvariable=var,
            state='readonly'
        )
        item.widget = item._setup_widget(combo)
        item.var = var  # 保存变量引用
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def textarea(cls, master, label: str, height: int = 4, **kwargs) -> 'FormItem':
        """创建多行文本框"""
        item = cls(master, label, **kwargs)
        text = tk.Text(item, height=height)
        item.widget = item._setup_widget(text)
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def radio(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建单选框表单项"""
        # 从 kwargs 中分离出 frame 的参数和 Radio 的参数
        frame_kwargs = {k: v for k, v in kwargs.items() 
                       if k not in ['options', 'default', 'layout']}
        
        # 创建表单项
        item = cls(master, label, **frame_kwargs)
        
        # 创建单选框组
        radio = Radio(
            item,
            options=kwargs.get('options', []),
            default=kwargs.get('default'),
            layout=kwargs.get('layout', 'horizontal')
        )
        item.widget = item._setup_widget(radio)
        item.var = radio.var  # 保存变量引用
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        
        # 绑定变量变化事件
        item.var.trace_add('write', item._notify_change)
        
        return item
    
    @classmethod
    def checkbox(cls, master, label: str, options: List[str], **kwargs) -> 'FormItem':
        """创建复选框组"""
        item = cls(master, label, **kwargs)
        checkbox = Checkbox(item, options=options)
        item.widget = item._setup_widget(checkbox)
        item.vars = checkbox.vars  # 保存变量引用列表
        
        # 为每个复选框变量添加 trace
        for var in item.vars:
            var.trace_add('write', item._notify_change)
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item
        
    @classmethod
    def file_picker(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建文件选择器表单项"""
        item = cls(master, label, **kwargs)
        picker = FilePicker(
            item,
            label="",
            mode=kwargs.get('mode', 'file'),
            filetypes=kwargs.get('filetypes', None),
            multiple_buttons=kwargs.get('multiple_buttons', False)
        )
        item.widget = item._setup_widget(picker)
        item.var = picker.path_var  # 保存变量引用
        
        # 直接在 FormItem 上添加 set_mode 方法
        def set_mode(mode):
            if hasattr(picker, 'set_mode'):
                picker.set_mode(mode)
        item.set_mode = set_mode
        
        item._apply_layout(kwargs.get('layout', 'horizontal'))
        return item

    @property
    def value(self) -> Any:
        """获取输入控件的值"""
        if hasattr(self, 'vars'):
            # 获取所有选中项的文本
            selected_values = []
            checkbox_frame = self.widget
            checkbuttons = [child for child in checkbox_frame.winfo_children() 
                         if isinstance(child, ttk.Checkbutton)]
            
            for var, checkbutton in zip(self.vars, checkbuttons):
                if var.get():  # 如果被选中
                    selected_values.append(checkbutton.cget('text'))
            print(f"Checkbox values: {selected_values}")  # 添加日志
            return selected_values
        if hasattr(self, 'var'):
            return self.var.get()
        if isinstance(self.widget, (ttk.Entry, tk.Entry)):
            return self.widget.get()
        elif isinstance(self.widget, (ttk.Combobox, ttk.Spinbox)):
            return self.widget.get()
        elif isinstance(self.widget, tk.Text):
            return self.widget.get("1.0", "end-1c")
        elif isinstance(self.widget, FilePicker):
            return self.widget.value
        return ""
    
    @value.setter
    def value(self, value: Any):
        """设置输入控件的值"""
        if hasattr(self, 'vars'):
            print(f"Setting checkbox value: {value}")  # 添加日志
            if isinstance(value, list):
                checkbuttons = [child for child in self.widget.winfo_children() 
                            if isinstance(child, ttk.Checkbutton)]
                # 重置所有复选框
                for var in self.vars:
                    var.set(False)
                # 设置选中项
                for text in value or []:
                    for var, btn in zip(self.vars, checkbuttons):
                        if btn.cget('text') == text:
                            print(f"Setting checkbox {text} to True")  # 添加日志
                            var.set(True)
                            break
        elif hasattr(self, 'var'):
            self.var.set(value or "")  # 添加空值处理
        elif isinstance(self.widget, (ttk.Entry, tk.Entry)):
            self.widget.delete(0, tk.END)
            self.widget.insert(0, str(value or ""))
        elif isinstance(self.widget, (ttk.Combobox, ttk.Spinbox)):
            self.widget.set(value or "")
        elif isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", tk.END)
            self.widget.insert("1.0", str(value or ""))
        elif isinstance(self.widget, FilePicker):
            # 使用 FilePicker 的 value 属性
            self.widget.value = value or ""
    
    def set_label_width(self, width: int):
        """设置标签宽度"""
        self.label.configure(width=width)
        
    def set_label_anchor(self, anchor: Literal["w", "e"]):
        """设置标签对齐方式"""
        self.label.configure(anchor=anchor)
        
    def on_change(self, callback):
        """添加变化事件回调"""
        self._change_callbacks.append(callback)
        return self
        
    def _notify_change(self, *args):
        """通知所有回调"""
        value = self.value
        for callback in self._change_callbacks:
            callback(value)