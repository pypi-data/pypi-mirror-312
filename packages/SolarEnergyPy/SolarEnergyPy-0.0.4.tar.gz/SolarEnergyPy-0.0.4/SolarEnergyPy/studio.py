__author__ = 'He Liqun'
'''
     studio for general purpose
     2024/9/1 
'''
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
import re
import os 
# import os.path
# from os import path
# 打印 Python 的搜索路径
import sys

# 获取当前文件所在的目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))
# 获取当前目录的父目录路径
parent_directory = os.path.dirname(current_directory)
# 将父目录路径添加到 sys.path 中
sys.path.append(parent_directory)

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


### small functions
def get_user_input(prompt):  
    # 创建一个隐藏的主窗口  
    root = tk.Tk()  
    root.withdraw()  # 隐藏主窗口  

    # 弹出输入对话框  
    user_input = simpledialog.askstring("输入", prompt)  

    # 销毁主窗口  
    root.destroy()  

    return user_input 

def popup(root, options, default, callback=None):  
    def on_select():  
        selected_option = option_var.get()   
        print(f"selected : {selected_option}")   
        if callback:  # 仅在回调函数不为 None 时调用  
            callback(selected_option)  
        popup_window.after(1000, popup_window.destroy)  # 1秒后关闭弹出窗口  

    # 创建弹出窗口   
    popup_window = tk.Toplevel(root)  
    popup_window.title("Select an Option")   
    
    option_var = tk.StringVar(value=default)  
    
    for option in options:  
        rb = tk.Radiobutton(popup_window, text=option, variable=option_var, value=option)  
        rb.pack(anchor=tk.W)  
    
    confirm_button = tk.Button(popup_window, text="Confirm", command=on_select)  
    confirm_button.pack()


### studio
def _get_position(start,end,string):
    srow=string[:start].count('\n')+1 # starting row
    scolsplitlines=string[:start].split('\n')
    if len(scolsplitlines)!=0:
        scolsplitlines=scolsplitlines[len(scolsplitlines)-1]
    scol=len(scolsplitlines)# Ending Column
    lrow=string[:end+1].count('\n')+1
    lcolsplitlines=string[:end].split('\n')
    if len(lcolsplitlines)!=0:
        lcolsplitlines=lcolsplitlines[len(lcolsplitlines)-1]
    lcol=len(lcolsplitlines)+1# Ending Column
    return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)#, (lrow, lcol)

def find_pattern_position(pattern, string, txt):
    line=string.splitlines()
    start=string.find(pattern)  # Here Pattern Word Start
    end=start+len(pattern) # Here Pattern word End
    srow=string[:start].count('\n')+1 # starting row
    scolsplitlines=string[:start].split('\n')
    if len(scolsplitlines)!=0:
        scolsplitlines=scolsplitlines[len(scolsplitlines)-1]
    scol=len(scolsplitlines)# Ending Column
    lrow=string[:end+1].count('\n')+1
    lcolsplitlines=string[:end].split('\n')
    if len(lcolsplitlines)!=0:
        lcolsplitlines=lcolsplitlines[len(lcolsplitlines)-1]
    lcol=len(lcolsplitlines)# Ending Column
    return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)#, (lrow, lcol)


class mainWindow():
    def __init__(self, parser, master=None, title = 'network', size = '900x500'):
        self.master = master
        self.stdout = sys.stdout
        self.init_window(parser, title = title, size = size)

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stdout

    #Creation of init_window
    def init_window(self, parser, title = 'studio', size = '900x500'):
        # changing the title of our master widget      
        self.master.title(title)
        self.master.geometry(size)
        # allowing the widget to take the full space of the root window

        menu = Menu(self.master) 
        self.master.config(menu=menu) 

        project_menu = Menu(menu) 
        menu.add_cascade(label='Project', menu=project_menu) 
        project_menu.add_command(label='New File', command=self.new_file) 
        project_menu.add_command(label='Open File...', command=self.open_file) 
        project_menu.add_command(label='Save File as...', command=self.save_file) 
        project_menu.add_separator() 
        project_menu.add_command(label='Exit', command=self.master.quit) 
        self.project_menu = project_menu

        helpmenu = Menu(menu) 
        menu.add_cascade(label='Help', menu=helpmenu) 
        helpmenu.add_command(label='About')

        topLeft, topRight, bottomframe = FrameLayout(self.master).frames()
 
        self._display = displayFrame(topRight)
        self._output  = outputFrame(bottomframe)
        sys.stdout = StdoutRedirector(self._output.outputWindow)
        sys.stderr =  StdoutRedirector(self._output.outputWindow)

        self._input   = inputFrame(parser, topLeft, display = self._display, output = self._output) 
        # self._input.focus()

    def new_file(self):
        self.input.clear()

    def open_file(self):
        self.filename =  filedialog.askopenfilename(initialdir = "/",  title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
        if self.filename:
            self.input.load_file(self.filename)

    def save_file(self):
        if not self.input.content :
            messagebox.showinfo("Warning", "There is no content to save !!!")
            return

        filename = filedialog.asksaveasfilename(initialdir = "/", initialfile = self.filename, 
            title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
        if not filename.endswith('.txt'):
            messagebox.showinfo("Visualizer error", "Filetype must be a .txt")
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.input.content)

    def close_file(self):
        self.input.close_file()

    def configure(self,keywords=[]):
        self.input.configure(keywords = keywords ) #, output=self.input.output, display = self.input.display)

    @property
    def input(self):
        return self._input

    @property
    def display(self):
        return self._display
    
    @property
    def output(self):
        return self._output
    
    @input.setter
    def input(self,value):
        self._input = value

    @display.setter
    def display(self,value):
        self._display = value

    @output.setter
    def output(self,value):
        self._output = value

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        pass

class inputFrame():  
    def __init__(self, parser, master=None, height=25, width=40, tab_title='Filename', tab_subtitle='Content',  
                 output=None, display=None):  
        self.parser = parser  # 指定的解析函数  
        self.master = master  
        self.notebook = None  
        self.height = height  
        self.width = width  
        self.btnAction = None  

        self.tab = None  
        self.tab_title = tab_title  
        self.tab_subtitle = tab_subtitle  

        self.tabs = []  # 用于存储打开的文件标签 

        self._output = output  
        self._display = display  

        self._content = ''  
        self._hightlight_words = []  
        self.chars = []  

        self.createLayout()  

    def __str__(self):  
        return '{}()'.format(self.__class__.__name__)  

    def createLayout(self):  
        # 建立活页夹
        self.notebook = Notebook(self.master)  
        self.notebook.pack(side=LEFT, expand=True, fill=BOTH)  

    def add_file_tab(self, file, parser_name='Parse', parser_function=None):  
        if file is None or not os.path.isfile(file) or not os.access(file, os.R_OK):  
            raise RuntimeError("Either the file is missing or not readable!")  

        # 创建新页  
        tab = Frame(self.notebook, borderwidth=4)  
        tab.pack(expand=True, fill=BOTH)  

        # 添加标签页到 Notebook  
        self.notebook.add(tab, text=os.path.basename(file)) 
        self.tabs.append(file)  # 将文件名添加到列表中  

        # 加线框，带子标题  
        topframe = LabelFrame(tab, text=self.tab_subtitle, borderwidth=4)  
        topframe.pack(expand=True, fill=BOTH)  

        # 增加文本输入编辑器，可以滚页
        inputText = scrolledtext.ScrolledText(topframe, width=self.width, height=self.height, wrap=WORD)  
        inputText.pack(expand=True, fill=BOTH)  

        # 读取文件内容至文本编辑器，并显示  
        with open(file, 'r', encoding='utf-8') as f:  
            content = f.read()  
            inputText.insert(END, content)  
    
        # 设置当前活动页为刚刚添加的标签页  
        self.notebook.select(tab)
                
        # 添加解析按钮  
        if parser_function is None :
            command = lambda: self.parse_file_content(inputText.get("1.0", END))  
        else :
            command = parser_function

        Button(tab, text=parser_name, command=command).pack(side=LEFT)  

    def load_file(self, file, parser_name='Parse', parser_function=None ):
        self.add_file_tab(file, parser_name, parser_function)

    def close_file(self):
        # 关闭文件的逻辑  
        if self.tabs:  
            current_index = self.notebook.index(self.notebook.select())  # 获取当前活动标签的索引  
            if current_index != -1:  
                # 关闭当前活动标签  
                file_name = self.tabs[current_index]  
                self.notebook.forget(current_index)  # 从标签页中删除  
                del self.tabs[current_index]  # 从列表中删除  
                print(f"Closed file: {file_name}")  # 示例输出  

                # 如果还有其他标签，选择下一个标签  
                if self.tabs:  
                    next_index = current_index if current_index < len(self.tabs) else len(self.tabs) - 1  
                    self.notebook.select(next_index)  # 选择下一个标签  
            else:  
                print("No active file to close.")  # 如果没有活动标签  
        else:  
            print("No files to close.")  # 如果没有文件打开

    def load_files(self, files):  
        for i,file in enumerate(files):  
            self.load_file(file)  

    def close_files(self):
        while self.tab :
            self.close_file()

    def parse_file_content(self, content):  
        # 使用指定的解析函数进行解析  
        if self.parser:  
            result = self.parser(content)  
            print("Parsing result:")  
            print(result)  # 打印解析结果，实际应用中可以根据需要处理结果  

    def get_active_tab_frame(self):
        current_tab_index = self.notebook.index(self.mainFrame.select())  
        current_tab = self.notebook.tabs()[current_tab_index]  
        current_tab_frame = self.notebook.nametowidget(current_tab) 
        return current_tab_frame       

    def get_active_tab_text_widget(self):  
        current_tab_frame = self.get_active_tab_frame()  
        return current_tab_frame.winfo_children()[0]  

    def clear_active_tab(self):  
        inputText = self.get_active_tab_text_widget()  
        inputText.delete('1.0', END)  

    def save_active_tab_content(self, file):  
        inputText = self.get_active_tab_text_widget()  
        content = inputText.get('1.0', END)  
        with open(file, 'w', encoding='utf-8') as f:  
            f.write(content)  

    def configure(self, output=None, display=None, keywords=[]):  
        if output is not None: self._output = output  
        if display is not None: self._display = display  
        if len(keywords): self._hightlight_words = keywords  

    def frame(self):  
        return self.mainFrame  

    @property  
    def content(self):  
        return self._content  

    @property  
    def output(self):  
        return self._output  

    @property  
    def display(self):  
        return self._display  

    @property  
    def hightlight_words(self):  
        return self._hightlight_words  

    @content.setter  
    def content(self, text=''):  
        self._content = text  
        self.inputText.insert(END, self._content)  

    @output.setter  
    def output(self, value=None):  
        self._output = value  

    @display.setter  
    def display(self, value=None):  
        self._display = value  

    @hightlight_words.setter  
    def hightlight_words(self, value=[]):  
        self._hightlight_words = value  

    def add_hightlight_word(self, value):  
        self._hightlight_words.append(value)  

    def clear(self):  
        self.chars = []  
        self.content = ''  
        self.inputText.delete('1.0', END)  

    def validate(self):  
        if len(self.content):  
            # 这里可以添加验证逻辑  
            pass  
        else:  
            messagebox.showinfo("Error", "There is no definition to show !!!")  

    def run(self):  
        code = self.inputText.get("1.0", END)  
        if len(code):  
            exec(code)  
        else:  
            messagebox.showinfo("Error", "There is no code to run !!!")  

    def focus(self):  
        self.inputText.focus_set()  

    def print(self, line=''):  
        if not self.output is None:  
            self.output.print(line)  

    def set_color_tags(self, text, color='blue'):  
        if len(self.hightlight_words) == 0:  
            return  

        words = tuple(self.hightlight_words)  
        tags = ["tg" + str(k) for k in range(len(words))]  
        pattern = re.compile('(' + '|'.join(words) + ')', re.IGNORECASE)  
        length = 0  

        for i in pattern.finditer(text):  
            start = i.start()  
            end = i.end()  
            word = i.groups()[0]  
            k = words.index(word) - 1  
            size = len(word)  
            self.set_color_tag(start, end, tags[k], word, color)  

    def set_color_tag(self, start, end, text, tag, word, fg_color='black', bg_color='white'):  
        index = _get_position(start, end, string)  
        end_index = index[0]  
        begin_index = index[1]  
        self.inputText.tag_add(tag, begin_index, end_index)  
        self.inputText.tag_config(tag, foreground=fg_color, background=bg_color)  

class displayFrame(Frame):
    def __init__(self, master = None, width=600, height=350, bg='gray'):
        super().__init__(master)

        # 创建一个画布
        # self.fig, self.ax = plt.subplots()
        # self.canvas = FigureCanvasTkAgg(self.fig, self)
        # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        canvas = Canvas(master, width= width, height=height, bg=bg)
        canvas.pack(expand=True, side = RIGHT, fill = BOTH ) 
        xBar = Scrollbar(master, orient="horizontal", command=canvas.xview)
        yBar = Scrollbar(master, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=yBar.set, xscrollcommand=xBar.set)

        self.canvas = canvas

    def frame(self):
    	return self.canvas

class outputFrame():
    def __init__(self, master = None, width=120, height=5):

        # yBar = Scrollbar(master) 
        # yBar.pack( side = RIGHT, fill = Y ) 
        # xBar = Scrollbar(master, orient = HORIZONTAL) 
        # xBar.pack( side = BOTTOM, fill = X )
        
        outputWindow = scrolledtext.ScrolledText(master, width=width,height=height, wrap=WORD)
            # xscrollcommand = xBar.set,
            # yscrollcommand = yBar.set) 
        outputWindow.pack(  expand=True,fill = BOTH, side = BOTTOM )
        self.outputWindow = outputWindow

        '''
        outputWindow.insert(1, 'Python................................') 
        outputWindow.insert(2, 'Java') 
        outputWindow.insert(3, 'C++') 
        outputWindow.insert(4, 'Any other')
        for line in range(100): 
           outputWindow.insert(END, 'This is line number' + str(line))  
        '''
         
        # yBar.config(command=outputWindow.yview)
        # xBar.config(command=outputWindow.xview) 

    def frame():
        return self.outputWindow

    def print(self, line = ''):
        self.outputWindow.insert(END, str(line))
        self.outputWindow.see(END)

class FrameLayout():
    def __init__(self, master = None):

        m = Panedwindow(master, orient=VERTICAL)
        m.pack(fill=BOTH, expand=True)  

        self.topframe = Panedwindow(m, orient=HORIZONTAL)
        self.topframe.pack( expand=True,side = TOP, fill = BOTH )

        self.topLeft  = Frame(self.topframe,borderwidth=4, width=100,height=400 )
        self.topLeft.pack( side = LEFT , fill = BOTH, expand=True )
        self.topRight = Frame(self.topframe,width=400,height=400 )
        self.topRight.pack( side = RIGHT, fill = BOTH, expand=True )  

        self.topframe.add(self.topLeft,weight=1)
        self.topframe.add(self.topRight,weight=4)

        self.bottomframe = Frame(m,borderwidth = 4, width=500,height=100)
        self.bottomframe.pack( side = BOTTOM, fill = BOTH ) 

        m.add(self.topframe,weight=4)
        m.add(self.bottomframe,weight=1)

    def frames(self):
    	return self.topLeft, self.topRight, self.bottomframe



def main():
    rootWindow = Tk()

    H = 500
    W = 900
    size = '{}x{}'.format(W,H)
    my = mainWindow(rootWindow, size = size)

    rootWindow.mainloop() 

if __name__ == '__main__':
	main()
