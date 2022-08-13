import os
import pygame
import threading
import tkinter as tk
from mutagen.id3 import ID3
from tkinter import filedialog 
from datetime import timedelta
from pygame import mixer, init


root = tk.Tk()
mixer.pre_init(44100, -16, 2, 2048)
mixer.init()
init()

root.title("MP3 player")
root.geometry('550x400')
root.resizable(0, 0)


light = tk.PhotoImage(file = "media/light.png")
dark = tk.PhotoImage(file = "media/dark.png")
on = tk.PhotoImage(file = "media/on.png")
off = tk.PhotoImage(file = "media/off.png")
play_btn = tk.PhotoImage(file = "media/play.png")
pause_btn = tk.PhotoImage(file = "media/pause.png")
next_btn = tk.PhotoImage(file = "media/next.png")
back_btn = tk.PhotoImage(file = "media/back.png")
mp3_select = tk.PhotoImage(file = "media/mp3.png")
folder_select = tk.PhotoImage(file = "media/folder.png")
mute_btn = tk.PhotoImage(file = "media/mute.png")
unmute_btn = tk.PhotoImage(file = "media/unmute.png")
meta_data_in_dark= tk.PhotoImage(file = "media/meta-data-light.png")
meta_data_in_light = tk.PhotoImage(file = "media/meta-data-dark.png")

MUSIC_DONE = pygame.event.custom_type()
pygame.mixer.music.set_endevent(MUSIC_DONE)

music_files = []
loaded = False
dark_mode = False
muted = False
music_playing = 0
# 0 == music was not played before and just started (play)
# 1 == music was played before and was paused (resume)
# 2 == music is playing and paused (pause)
pointer = 0
songprogress = tk.DoubleVar()

def reset_at_idle(*args):
    global music_playing, loaded, playing, pointer
    while True:
        if music_files: 
            played_sec = mixer.music.get_pos()/1000
            progress.set(float(played_sec*100/mixer.Sound(music_files[pointer]).get_length()))
            canvas.itemconfig(current_duration, text=timedelta(seconds=int(played_sec)))
        for event in pygame.event.get():
            if event.type == MUSIC_DONE:
                canvas.itemconfig(music_btn, image=play_btn)
                progress.set(0.0)
                if len(music_files) <= pointer+1: 
                    song_duration.delete('1.0', tk.END)
                    name.delete('1.0', tk.END)
                    next_music.delete('1.0', tk.END)
                    singer.delete('1.0', tk.END)
                    canvas.itemconfig(total_duration, text="0:00:00")
                    music_playing=0
                else:
                    pointer=pointer+1
                    music_playing=2
                    mixer.music.load(music_files[pointer])
                    load_metadata(music_files[pointer])
                    canvas.itemconfig(music_btn, image=pause_btn)
                    mixer.music.play()
                              
def load_metadata(file):
    length=mixer.Sound(file).get_length()
    canvas.itemconfig(total_duration, text=timedelta(seconds=int(length)))
    try: song_info = ID3(music_files[pointer]).get('TPE1', None)
    except: song_info=None
    singer.delete('1.0', tk.END)
    name.delete('1.0', tk.END)
    song_duration.delete('1.0', tk.END)
    name.insert("1.0", os.path.basename(music_files[pointer]).replace(".mp3", ""))
    song_duration.insert('1.0', str(timedelta(seconds=int(length))))
    if song_info: singer.insert('1.0', song_info.text)
    else: singer.insert('1.0', "Not known!")
    next_music.delete('1.0', tk.END)
    try: next_music.insert('1.0', os.path.basename(music_files[pointer+1]).replace(".mp3", ""))
    except: next_music.insert('1.0', "No song!")
    
def switch(*args):
    global dark_mode
    canvas.itemconfig(background, image=light if dark_mode else dark)
    canvas.itemconfig(btn, image = off if dark_mode else on)
    canvas.itemconfig(meta_data, image = meta_data_in_dark if dark_mode else meta_data_in_light)
    progress.config(bg="#000000" if dark_mode else "#f70a0a")
    canvas.itemconfig(current_duration, fill="#000000" if dark_mode else "#1cfc03")
    canvas.itemconfig(total_duration, fill="#000000" if dark_mode else "#1cfc03")
    dark_mode = not dark_mode 

def mute_switch(*args):
    global muted
    mixer.music.set_volume(100 if muted else 0)
    canvas.itemconfig(mute_btn_canv, image=unmute_btn if muted else mute_btn)
    muted=not muted
    
def toggle_music(*args):
    global music_playing
    if music_files and music_playing==0 and loaded: 
        mixer.music.play()
        music_playing=2
        canvas.itemconfig(music_btn, image=pause_btn)
        load_metadata(music_files[pointer])
    elif music_files and music_playing==1: 
        mixer.music.unpause()
        music_playing=2
        canvas.itemconfig(music_btn, image=pause_btn)
    elif music_files and music_playing==2: 
        mixer.music.pause()    
        music_playing=1
        canvas.itemconfig(music_btn, image=play_btn)
    
def load_files(mode):
    global music_files, loaded
    if mode == "file":
        path = filedialog.askopenfilename(initialdir="/home/jainamoswal/Music", title="Select MP3", filetypes=[("MP3 file", ["*.mp3"])])
        if path: 
            music_files.append(path)
    elif mode == "folder":
        path = filedialog.askdirectory()
        if path and os.path.isdir(path):
            music_files=[os.path.join(path, x) for x in os.listdir(path=path) if x.endswith(".mp3")]
    if path and not music_playing and not loaded:
        loaded = True
        pointer = 0
        mixer.music.load(music_files[pointer])
        load_metadata(music_files[pointer])
    
def music_switch(action):
    global pointer, music_playing, loaded
    progress.set(0.0)
    if action=="next" and len(music_files)>pointer+1:
        mixer.music.unload()
        pointer+=1
        mixer.music.load(music_files[pointer])
        load_metadata(music_files[pointer])
        loaded=True
        if music_playing==2:
            mixer.music.play()
            music_playing=1
            return
        music_playing=0
    elif action=="back" and pointer-1>=0:
        mixer.music.unload()
        pointer-=1
        mixer.music.load(music_files[pointer])
        load_metadata(music_files[pointer])
        loaded=True
        if music_playing==2:
            mixer.music.play()
            music_playing=1
            return
        music_playing=0

canvas = tk.Canvas(
    root,
    bg = "#000000",
    height = 400,
    width = 550,
    bd=0, 
    highlightthickness=0,
    border=0,
    highlightbackground="white",
    highlightcolor="white",
    relief = "solid"
    )

canvas.place(x = 0, y = 0)
background=canvas.create_image(0, 0, image=light)

music_file_btn = canvas.create_image(85, 150, image=mp3_select)
canvas.tag_bind(music_file_btn, "<1>", lambda x:load_files("file"))

folder_select_btn = canvas.create_image(85, 225, image=folder_select)
canvas.tag_bind(folder_select_btn, "<1>", lambda x:load_files("folder"))

meta_data = canvas.create_image(190, 185, image=meta_data_in_dark)

name = tk.Text(root, height=1, width=30, relief=tk.FLAT)
name.place(x=235, y=143)
singer = tk.Text(root, height=1, width=30, relief=tk.FLAT)
singer.place(x=235, y=165)
song_duration = tk.Text(root, height=1, width=30, relief=tk.FLAT)
song_duration.place(x=235, y=188)
next_music = tk.Text(root, height=1, width=30, relief=tk.FLAT)
next_music.place(x=235, y=215)

btn=canvas.create_image(510, 30, image=off)
canvas.tag_bind(btn, "<1>", switch)

music_btn=canvas.create_image(275, 340, image=play_btn)
canvas.tag_bind(music_btn, "<1>", toggle_music)

prev=canvas.create_image(225, 340, image=next_btn)
canvas.tag_bind(prev, "<1>", lambda x:music_switch("back"))

next=canvas.create_image(325, 340, image=back_btn)
canvas.tag_bind(next, "<1>", lambda x:music_switch("next"))

mute_btn_canv=canvas.create_image(370, 340, image=unmute_btn)
canvas.tag_bind(mute_btn_canv, "<1>", mute_switch)

progress = tk.Scale(
        root, 
        variable = songprogress, 
        from_ = 1, 
        to = 100, 
        orient = tk.HORIZONTAL, 
        length=400, 
        width=3, 
        tickinterval=0.1, 
        sliderlength=8, 
        showvalue=0,
        relief=tk.FLAT,
        border=0,
        bg="#000000",
        sliderrelief=tk.FLAT
    ) 
progress.pack()
progress.place(x=70, y=290)

current_duration = canvas.create_text(75, 310, text="00:00")
total_duration = canvas.create_text(475, 310, text="00:00")

if __name__ == "__main__":
    loop_1=threading.Thread(target=reset_at_idle, daemon=True)
    loop_1.start()
    root.mainloop()