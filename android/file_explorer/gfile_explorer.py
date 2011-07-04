#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os

class TreeViewFile:
    def __init__(self, pixbufDir, pixbufFile):
        
        self.pixbufDirectory = pixbufDir
        self.pixbufFile = pixbufFile

        self.tree_store = gtk.TreeStore(gobject.TYPE_BOOLEAN, str, int) # GOTCHA!!!
        self.tree_view = gtk.TreeView(self.tree_store)
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.add_with_viewport(self.tree_view)
        
        # TYPE
        type_col = gtk.TreeViewColumn('')
        self.tree_view.append_column(type_col)
        
        type_col_renderer_pixbuf = gtk.CellRendererPixbuf()
        type_col.pack_start(type_col_renderer_pixbuf, expand=True)
        type_col.set_cell_data_func(type_col_renderer_pixbuf, self.renderDirOrFile) # GOTCHA This must be done after the renderer is packed into the column
        #type_col.add_attribute(type_col_renderer_pixbuf, 'pixbuf', 0)

        # NAME
        name_col = gtk.TreeViewColumn('File name')
        self.tree_view.append_column(name_col)
        
        name_col_renderer_text = gtk.CellRendererText()
        name_col.pack_start(name_col_renderer_text, expand=True)
        name_col.add_attribute(name_col_renderer_text, 'text', 1)
        name_col.set_sort_column_id(1)
        self.tree_view.set_search_column(1)
        
        # SIZE
        size_col = gtk.TreeViewColumn('Size')
        self.tree_view.append_column(size_col)
        
        size_col_renderer = gtk.CellRendererText()
        size_col.pack_start(size_col_renderer, expand=True)
        size_col.add_attribute(size_col_renderer, 'text', 2)


        
        
    def renderDirOrFile(self, tree_view_column, cell, model, iter):
        isDir = model.get_value(iter, 0)
        if isDir:
            pixbuf = self.pixbufDirectory
        else:
            pixbuf = self.pixbufFile

        cell.set_property('pixbuf', pixbuf)

    def getView(self):
        return self.scrolled_window

    def loadData(self, data):

        self.tree_store.clear()

        for row in data:
            rowIter = self.tree_store.append(None, [ row['directory'], row['name'], row['size'] ])

class GFileExplorer:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)
        self.window.set_size_request(640, 480)

        self.window.connect('destroy', self.destroy)

        self.v_box = gtk.VBox(False, 0)
        self.window.add(self.v_box)

        imageDir = gtk.Image()
        imageDir.set_from_file('./icons/folder.png')
        imageFile = gtk.Image()
        imageFile.set_from_file('./icons/file.png')

        # Host and device panels
        # They're inside an HBox (which is inside the topmost VBox)
        self.h_box = gtk.HBox(False, 0)
        self.v_box.pack_start(self.h_box, True, True, 0)

        self.host_tree_view_file = TreeViewFile(imageDir.get_pixbuf(), imageFile.get_pixbuf())
        self.h_box.pack_start(self.host_tree_view_file.getView())

        self.device_tree_view_file = TreeViewFile(imageDir.get_pixbuf(), imageFile.get_pixbuf())
        self.h_box.pack_start(self.device_tree_view_file.getView())

        # Status
        self.status_frame = gtk.Frame("Status")
        
        self.status_text = gtk.TextView()
        self.status_text.set_editable(False)
        self.status_frame.add(self.status_text)
        
        self.v_box.pack_start(self.status_frame, True, True, 0)

        self.window.show_all()

        self.output("Ready")

        self.cwd = os.getcwd()
        self.host_tree_view_file.loadData(self.dirScanHost(self.cwd))
        self.device_tree_view_file.loadData(self.dirScanHost(self.cwd))

    """ Walks through a directory and return the data in a tree-style list 
        that can be used by the TreeViewFile """
    def dirScanHost(self, directory):
        output = []

        print "Scanning", directory
        root, dirs, files = next(os.walk(directory))

        dirs.sort()
        files.sort()

        for d in dirs:
            output.append({'directory': True, 'name': d, 'size': 0})

        for f in files:
            size = os.path.getsize(os.path.join(directory, f))
            output.append({'directory': False, 'name': f, 'size': size})

        return output


    def output(self, text):
        buffer = self.status_text.get_buffer()
        buffer.set_text(text)
        self.status_text.set_buffer(buffer)

    def die_callback(self, widget, data=None):
        self.destroy(widget, data)

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


if __name__ == '__main__':
    explorer = GFileExplorer()
    explorer.main()
