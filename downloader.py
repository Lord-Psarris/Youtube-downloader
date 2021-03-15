import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import os
import threading


class YoutubeDownloader:
    root = Tk()
    root.geometry("600x500")
    root.title("Psarris' youtube downloader")
    root.resizable(False, False)

    def __init__(self):
        self.master = YoutubeDownloader.root
        self.location = ''

        Label(self.master, text="Paste link here").place(x=40, y=30)
        self.link = Entry(self.master, width=60)
        self.link.place(x=40, y=60, height=30)

        var = IntVar()

        video = Radiobutton(self.master, text="Download video", padx=20, variable=var, value=2)
        video.place(x=30, y=120, anchor='w')

        audio = Radiobutton(self.master, text="Download audio", padx=20, variable=var, value=1)
        audio.place(x=30, y=145, anchor='w')

        self.download = Button(self.master, text='Download', width=15, height=2, command=self.download_)
        self.download.place(x=41, y=190)

        self.var = var
        self.success = ttk.Label(self.master, text="")
        self.success.place(x=40, y=260)
        self.location_label = ttk.Label(self.master, text="")
        self.location_label.place(x=40, y=280)

        self.master.mainloop()

    def set_location(self):
        filename_path = filedialog.askdirectory()
        self.location = filename_path + '/'

    def download_mp4(self, url):
        self.success.config(text='')
        self.location_label.config(text='')
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()
        ys.download(self.location)
        _filename = self.location + yt.title
        self.success.config(text=f'Download finished ({yt.title}.mp4)')
        self.location_label.config(text=f'File saved in {self.location}')
        self.download.config(state='normal')
        print('downloaded')

    def download_mp3(self, url):
        self.success.config(text='')
        self.location_label.config(text='')
        yt = YouTube(url)
        _filename = self.location + yt.title
        ys = yt.streams.get_highest_resolution()
        ys.download(self.location)
        print(_filename)
        with VideoFileClip(os.path.join(_filename + '.mp4')) as video:
            video.audio.write_audiofile(os.path.join(f"{self.location}{yt.title}.mp3"))
        os.remove(_filename + ".mp4")
        self.success.config(text=f'Download finished ({yt.title}.mp3)')
        self.location_label.config(text=f'File saved in {self.location}')
        self.download.config(state='normal')
        print('converted')

    def download_(self):
        self.set_location()
        var = self.var.get()
        url = self.link.get()
        self.download.config(state='disabled')
        if var == 1:
            t = threading.Thread(target=self.download_mp3, args=(url,))
            t.start()
        else:
            t1 = threading.Thread(target=self.download_mp4, args=(url,))
            t1.start()


if __name__ == "__main__":
    YoutubeDownloader()
