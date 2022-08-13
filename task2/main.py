from tkinter import messagebox, filedialog
from tkvideo import tkvideo
import tkinter as tk
import webbrowser
import threading
import youtube_dl
import os, re

# tkinter object
root = tk.Tk()

# images and other vars
reg = re.compile("((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?")
folder_btn= tk.PhotoImage(file='media/folder.png')
mp3_radio = tk.PhotoImage(file="media/mp3.png")
mp4_radio = tk.PhotoImage(file="media/mp4.png")
mix_radio = tk.PhotoImage(file="media/video.png")
title = tk.PhotoImage(file="media/title.png")
low = tk.PhotoImage(file="media/low.png")
best = tk.PhotoImage(file="media/best.png")
github = tk.PhotoImage(file="media/github.png")
    
# functions 
def get_format(quality, format):
    if quality=="high":
        if format=="audio": return "bestaudio[ext=mp3]"
        elif format=="video": return "bestvideo[ext=mp4]"
        else: return "best[ext=mp4]"
    elif quality=="low":
        if format=="audio": return "worstaudio[ext=mp3]"
        elif format=="video": return "worstvideo[ext=mp4]"
        else: return "worst[ext=mp4]"

def update(status):
    print(status['status'])
    if status['status'] == 'finished':
        messagebox.showinfo("Success", "The content is downloaded!!")

def download(*args):
    yt_link = url.get(1.0, "end-1c")
    location = path.get(1.0, "end-1c")
    _format = format.get()
    _quality = quality.get()
    if not os.path.isdir(location): messagebox.showinfo("Error", "Not a valid location 😕"); return
    link = re.search(reg, yt_link)
    if not link: messagebox.showinfo("Error", "No Youtube links found 😕");return
    link = link.group()
    url.delete("1.0", tk.END)
    path.delete("1.0", tk.END)
    video_btn.select()
    best_quality.select()
    path.insert(tk.END, os.path.expanduser('~'))
    url.insert("end-1c", "Enter link here...")
    messagebox.showinfo("Info", "Downloading started!!!!\n")
    
    ydl_opts={
        'format': get_format(_quality, _format),
        'outtmpl':f'{location}/%(title)s.%(ext)s'
    }
    
    try:    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except youtube_dl.utils.DownloadError: 
        os.system("notify-send '{}'".format("Selected format not available!!"))
        messagebox.showinfo("Error","Format not available!")
    os.system("notify-send '{}'".format("Download completed!!"))

def path_select(*args):
    filename = filedialog.askdirectory(initialdir = os.path.expanduser('~') ,title = "Select Folder to save!")
    path.delete("1.0", tk.END)
    path.insert(tk.END, filename)

# default settings for box
root.title("Download Youtube Content")
root.geometry('550x400')
root.resizable(0, 0)

# canvas of the box
canvas = tk.Canvas(
    root,
    bg = "#000000",
    height = 390,
    width = 540,
    bd=0, 
    highlightthickness=1,
    border=4,
    highlightbackground="white",
    highlightcolor="white",
    relief = "solid"
    )
canvas.place(x = 0, y = 0)

# if "Enter" button is presesed, it will submit the inputs
root.bind('<Return>', download)

# header
canvas.create_image(275,50, image=title)

# for URL input
canvas.create_text(
    110, 100,
    text = "URL : ",
    fill = "#99ffcc",
    font = ("Roboto-Light", int(14.0)))
url = tk.Text(root, height = 1,width = 35)
url.insert("end-1c", "Enter link here...")
url.pack(padx=85,pady=70, anchor=tk.N)
url.place(x=153, y=88)

# for Folder to download input
canvas.create_text(
    100, 140,
    text = "Folder : ",
    fill = "#99ffcc",
    font = ("Roboto-Light", int(14.0)))
path = tk.Text(root, height=1, width=30)
path.insert(tk.END, os.path.expanduser('~'))
path.pack(padx=0, pady=0, anchor=tk.N) 
path.bind("<2>", path_select)
path.place(x=153, y=131)

# user can select the folder using GUI 
btn=tk.Button(root,text="Select Folder", command=path_select, font=('Verdana',6), image=folder_btn)
btn.pack()
btn.place(x=410, y=130)

# Displays Format options
canvas.create_text(
    95, 180,
    text = "Format : ",
    fill = "#99ffcc",
    font = ("Roboto-Light", int(14.0)))

format = tk.StringVar()

audio_btn=tk.Radiobutton(
        root,
        image=mp3_radio,
        text="Audio",
        value="audio",
        variable=format,
        highlightthickness=0,
        activebackground="#000000",
    )
audio_btn.pack()
audio_btn.place(x=155, y=170)
audio_btn.configure(background="#000000")

video_btn=tk.Radiobutton(
        root,
        image=mp4_radio,
        text="Video",
        value="video",
        variable=format,
        highlightthickness=0,
        activebackground="#000000",
    )
video_btn.pack()
video_btn.select()
video_btn.place(x=235, y=170)
video_btn.configure(background="#000000")

both_btn=tk.Radiobutton(
        root,
        image=mix_radio,
        text="Both",
        value="both",
        variable=format,
        highlightthickness=0,
        activebackground="#000000",
    )
both_btn.pack()
both_btn.place(x=315, y=170)
both_btn.configure(background="#000000")

# Displays Quality section
canvas.create_text(
    95, 235,
    text = "Quality : ",
    fill = "#99ffcc",
    font = ("Roboto-Light", int(14.0)))

quality = tk.StringVar()

low_quality=tk.Radiobutton(
        root,
        image=low,
        text="Low",
        value="low",
        variable=quality,
        highlightthickness=0,
        activebackground="#000000",
    )
low_quality.pack()
low_quality.place(x=145, y=210)
low_quality.configure(background="#000000")

best_quality=tk.Radiobutton(
        root,
        image=best,
        text="High",
        value="high",
        variable=quality,
        highlightthickness=0,
        activebackground="#000000",
    )
best_quality.pack()
best_quality.select()
best_quality.place(x=235, y=210)
best_quality.configure(background="#000000")


# Displays submit button
submit_btn = tk.Label(root, highlightthickness=0)
submit_btn.pack()
submit_btn.bind("<1>", lambda x:threading.Thread(target=download, daemon=True).start())
player = tkvideo(
    "media/gif.mp4", 
    submit_btn, 
    loop = 1, 
    size = (100,30)
    )
player.play()
submit_btn.place(x=360, y=300)


a=canvas.create_image(530,382, image=github)
canvas.tag_bind(a, "<1>", lambda e:webbrowser.open_new_tab("https://github.com/jainamoswal"))


if __name__ == "__main__":
    root.mainloop()