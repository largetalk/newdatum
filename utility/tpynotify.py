#!/usr/bin/env python
#coding:UTF-8
 
import time
import pynotify
import gtk
import pygtk
from datetime import datetime
 
class Warning:
   
    def destroy(self, widget):
        gtk.main_quit()
 
    def __init__(self):
        self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(16)
        self.button=gtk.Button("保护视力，休息一下")
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.window.add(self.button)
        self.button.show()
        self.window.show()
 
    def main2(self):
        gtk.main()
 
def Notify():
    pynotify.init("DCY-Title")
    n = pynotify.Notification("DCY温馨提示：保护视力", "当前时间是%s, 休息一下，眼保健操"%datetime.now().strftime("%Y-%m-%d %H:%M"))
    n.show()
 
def main():
    while True:
        time.sleep(3600)
        Notify()
        warn = Warning()
        warn.main2()
 
if __name__ == "__main__":
    main()
