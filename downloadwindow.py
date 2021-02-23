import tkinter as tk
import GetMusicInfo as private

search_user_input = ""
next_or_before = ""
a = {}
loading_page = -1
show_music_info_list = []
checkbuttonval = {}
start_number = 0
s = 0
times = 0



# 用户点击搜索按钮时执行的函数
def search_f():
    height = -1
    global loading_page,page,music_url_list,show_music_info_list,search_user_input,times,start_number,s
    download_name = searchval.get()

    # 如果不是初次搜索 则将上一次所搜索的内容摧毁
    if search_user_input == download_name:
        start_number = s
        if next_or_before == "next":
            for i in range(15*(times-1),15*times):
                a[i].destroy()
        elif next_or_before == "before":
            for i in range(15*(times+1),15*(times+2)):
                a[i].destroy()
    # 如果是新的搜索关键词，则从0开始遍历
    else:
        # 重新搜索时，摧毁前一次搜索显示的checkbutton
        try:
            for i in range(15*times,15*(times+1)):
                a[i].destroy()
        except:
            pass
        private.search_music_url_all = []
        start_number = 0
        private.show_music_info_list = []
        times = 0
        page = 0
        loading_page = -1

    # 列表中的数据可供循环两次，循环两次后重新获取新数据
    if times % 2 == 0 and times > loading_page:
        page += 1
        music_url_list = private.music_get_url(download_name,page)
        private.out(music_url_list,start_number)
    show_music_info_list = private.show_music_info_list

    # 记录加载到的页数，在此页之前的数据翻页时不用重新获取
    if times > loading_page:
        loading_page = times

    # 更新用户搜索的关键词，用于比较是否是新的搜索关键词
    search_user_input = download_name


    # 动态生成check button按钮
    for i in range(15*times,15*(times+1)):
        s = 15*(times+1)
        height += 1
        checkbuttonval[i] = tk.IntVar()
        a[i] = tk.Checkbutton(window, text=show_music_info_list[i], onvalue=i+1, offvalue=0, variable=checkbuttonval[i],font=(12))
        if height == 0:
            a[i].place(x=20,y=100)
        else:
            a[i].place(x=20,y=100+height*30)

# 点击下一页执行的函数
def next_page():
    global times
    global next_or_before
    next_or_before = "next"
    times += 1
    search_f()

# 点击上一页执行的函数
def before_page():
    global times
    global next_or_before
    next_or_before = "before"
    times -= 1
    search_f()

# 点击下载按钮执行的函数
b = {}
def download_button_f():
    all_url_list = private.search_music_url_all
    for i in range(15*times,15*(times+1)):
        b[i] = checkbuttonval[i].get()
        if(b[i] != 0):
            download_info_text.insert("end","正在下载 "+show_music_info_list[b[i]-1]+"\n")
            result = private.Preservation(all_url_list[b[i]-1],"D:/111/") + "\n"
            download_info_text.insert("end",result)

def main():
    global window
    global searchval
    global download_info_text
    # 主界面
    window = tk.Tk()
    window.title("Music Download System")
    window.geometry("900x700")

    # 搜索输入框
    searchval = tk.StringVar()
    search_entry = tk.Entry(window,textvariable=searchval,font=(60),width=40)
    search_entry.place(x=150,y=35)

    # 搜索按钮
    search_button = tk.Button(window,text="搜索",font=(40),command=search_f)
    search_button.place(x=500,y=30)

    # 下载按钮
    download_button = tk.Button(window,text="下载",command=download_button_f)
    download_button.place(x=300,y=600)

    # 下一页按钮
    next_page_button = tk.Button(window,text="下一页",command=next_page)
    next_page_button.place(x=400,y=600)

    # 上一页按钮
    before_page_button = tk.Button(window,text="上一页",command=before_page)
    before_page_button.place(x=200,y=600)

    # 音乐下载提示框
    download_info_text = tk.Text(window,width=37,height=50)
    download_info_text.insert("end","音乐下载提示\n")
    download_info_text.place(x=620,y=30)

    window.mainloop()
