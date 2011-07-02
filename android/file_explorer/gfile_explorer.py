#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os


class GFileExplorer:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)

        self.window.connect('destroy', self.destroy)

        self.v_box = gtk.VBox(False, 0)
        self.window.add(self.v_box)

        # Host and device panels
        # They're inside an HBox (which is inside the topmost VBox)
        self.h_box = gtk.HBox(False, 0)
        self.h_box.show()
        self.v_box.pack_start(self.h_box, True, True, 0)
        
        self.host_file_chooser = gtk.FileChooserWidget()
        self.host_file_chooser.show()
        self.host_file_chooser.set_select_multiple(True)
        self.h_box.pack_start(self.host_file_chooser)

        # Status
        self.status_frame = gtk.Frame("Status")
        self.status_frame.show()
        
        self.status_text = gtk.TextView()
        self.status_text.set_editable(False)
        self.status_text.show()
        self.status_frame.add(self.status_text)
        
        self.v_box.pack_start(self.status_frame, True, True, 0)


        self.v_box.show()

        self.window.show()

        self.output("Ready")

        self.cwd = os.getcwd()

    def output(self, text):
        buffer = self.status_text.get_buffer()
        buffer.set_text(text)
        self.status_text.set_buffer(buffer)

    def die_callback(self, widget, data=None):
        self.destroy(widget, data)

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        print 'this is main'
        gtk.main()


if __name__ == '__main__':
    explorer = GFileExplorer()
    explorer.main()
