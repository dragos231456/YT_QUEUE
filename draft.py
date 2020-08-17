from tkinter import *
import os

root = Tk()
class MainGui:
    def __init__(self, master):
        self.mypathLabel = Label(master, text="Copy and Paste your filepath here:")
        self.mypathEntry = Entry(master, bg="black", fg="white", relief=SUNKEN)
        self.mypathSaveButton = Button(master, text="Save Path", bg="black", fg="white", command=self.save_path)
        self.mypathList = Listbox(master, bg="black", fg="white")

        self.mypathLabel.pack()
        self.mypathEntry.pack()
        self.mypathSaveButton.pack()
        self.mypathList.pack()
        self.mypathList.bind("<Double-Button-1>", self.open_path)

    def save_path(self):
        fp = self.mypathEntry.get()
        self.mypathEntry.delete(0, 'end')
        self.mypathList.insert(1, fp)

    def open_path(self, event):
        list_item = self.mypathList.curselection()
        print(list_item)
        fp = self.mypathList.get(list_item[0])
        print(fp)
        try:
            with open(fp, 'r') as result:
                print(result.read())
        except Exception as e:
            print(e)    

MainGui(root)
root.mainloop()