#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import file_explorer
import re

""" A sort of TreeView container that serves for showing file listings """
class TreeViewFile:
	def __init__(self, pixbufDir, pixbufFile):
		
		self.pixbufDirectory = pixbufDir
		self.pixbufFile = pixbufFile
		# GOTCHA: Number of columns in the store *MUST* match the number of values
		# added in loadData
		self.tree_store = gtk.TreeStore(gobject.TYPE_BOOLEAN, str, int)
		self.tree_view = gtk.TreeView(self.tree_store)
		self.tree_view.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		self.scrolled_window = gtk.ScrolledWindow()
		self.scrolled_window.add_with_viewport(self.tree_view)
		
		# TYPE
		type_col = gtk.TreeViewColumn('')
		self.tree_view.append_column(type_col)
		
		type_col_renderer_pixbuf = gtk.CellRendererPixbuf()
		type_col.pack_start(type_col_renderer_pixbuf, expand=True)
		# GOTCHA Func must be set AFTER the renderer is packed into the column
		type_col.set_cell_data_func(type_col_renderer_pixbuf, self.renderDirOrFile)

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
		size_col.set_sort_column_id(2)


	def renderDirOrFile(self, tree_view_column, cell, model, iter):
		isDir = model.get_value(iter, 0)
		if isDir:
			pixbuf = self.pixbufDirectory
		else:
			pixbuf = self.pixbufFile

		cell.set_property('pixbuf', pixbuf)


	def getView(self):
		return self.scrolled_window

	def getTree(self):
		return self.tree_view


	def loadData(self, data):
		self.tree_store.clear()

		for row in data:
			rowIter = self.tree_store.append(None, [ row['directory'], row['name'], row['size'] ])



class GFileExplorer:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("interface.xml")
		builder.connect_signals({ "on_window_destroy" : gtk.main_quit })
		self.window = builder.get_object("window")

		basedir = os.path.dirname(os.path.abspath(__file__))

		imageDir = gtk.Image()
		imageDir.set_from_file(os.path.join(basedir, 'icons/folder.png'))
		imageFile = gtk.Image()
		imageFile.set_from_file(os.path.join(basedir, './icons/file.png'))

		# Host and device TreeViews
		self.host_treeViewFile = TreeViewFile(imageDir.get_pixbuf(), imageFile.get_pixbuf())
		self.host_treeViewFile.getTree().connect('row-activated', self.host_navigate_callback)
		hostFrame = builder.get_object('frameHost')
		hostFrame.get_child().add(self.host_treeViewFile.getView())

		self.device_treeViewFile = TreeViewFile(imageDir.get_pixbuf(), imageFile.get_pixbuf())
		self.device_treeViewFile.getTree().connect('row-activated', self.device_navigate_callback)
		deviceFrame = builder.get_object('frameDevice')
		deviceFrame.get_child().add(self.device_treeViewFile.getView())

		# Copy from/to device buttons
		btnCopyFromDevice = builder.get_object('btnCopyFromDevice')
		btnCopyFromDevice.connect('clicked', self.copy_from_device_callback, None)
		btnCopyToDevice = builder.get_object('btnCopyToDevice')
		btnCopyToDevice.connect('clicked', self.copy_to_device_callback, None)

		# Device specific buttons
		btnDeviceCreateDirectory = builder.get_object('btnDeviceCreateDirectory')
		btnDeviceCreateDirectory.connect('clicked', self.device_create_directory_callback, None)
		btnDeviceDeleteItem = builder.get_object('btnDeviceDeleteItem')
		btnDeviceDeleteItem.connect('clicked', self.device_delete_item_callback, None)

		# Progress bar
		self.progress_bar = builder.get_object('progressBar')

		# Some more subtle details...
		self.window.set_title("Android file explorer")
		self.adb = 'adb'
		self.host_cwd = os.getcwd()
		self.device_cwd = '/mnt/sdcard/'

		self.refreshHostFiles()
		self.refreshDeviceFiles()

		# And we're done!
		self.window.show_all()


	def refreshHostFiles(self):
		self.host_treeViewFile.loadData(self.dirScanHost(self.host_cwd))

	def refreshDeviceFiles(self):
		self.device_treeViewFile.loadData(self.dirScanDevice(self.device_cwd))

	""" Walks through a directory and return the data in a tree-style list 
		that can be used by the TreeViewFile """
	def dirScanHost(self, directory):
		output = []

		root, dirs, files = next(os.walk(directory))

		dirs.sort()
		files.sort()

		output.append({'directory': True, 'name': '..', 'size': 0})

		for d in dirs:
			output.append({'directory': True, 'name': d, 'size': 0})

		for f in files:
			size = os.path.getsize(os.path.join(directory, f))
			output.append({'directory': False, 'name': f, 'size': size})

		return output

	""" Like dirScanHost, but in the connected Android device """
	def dirScanDevice(self, directory):
		output = []
		
		entries = file_explorer.parse_device_list(file_explorer.device_list(self.adb, directory))

		dirs = []
		files = []

		for filename, entry in entries.iteritems():
			if entry['is_directory']:
				dirs.append(filename)
			else:
				files.append(filename)

		dirs.sort()
		files.sort()

		output.append({'directory': True, 'name': '..', 'size': 0})

		for d in dirs:
			output.append({'directory': True, 'name': d, 'size': 0})

		for f in files:
			size = int(entries[f]['size'])
			output.append({'directory': False, 'name': f, 'size': size})

		return output

	# The 'tasks' in the following functions are so that the GUI keeps
	# being updated, even if we're 'blocking' when copying files
	# See: http://stackoverflow.com/questions/496814/progress-bar-not-updating-during-operation 

	def copy_to_device_callback(self, widget, data=None):
		model, rows = self.host_treeViewFile.getTree().get_selection().get_selected_rows()

		task = self.copy_to_device_task(model, rows)
		gobject.idle_add(task.next)

	
	def copy_to_device_task(self, model, rows):
		completed = 0
		total = len(rows)

		self.update_progress()

		while completed < total:
			row = rows[completed]
			iter = model.get_iter(row)
			filename = model.get_value(iter, 1)
			full_host_path = os.path.join(self.host_cwd, filename)

			if os.path.isfile(full_host_path):
				full_device_path = self.device_cwd
			else:
				full_device_path = os.path.join(self.device_cwd, filename)

			file_explorer.action_copy_from_host(self.adb, full_host_path, full_device_path)
			completed = completed + 1
			self.refreshDeviceFiles()
			self.update_progress(completed * 1.0 / total)

			yield True

		yield False

	
	def copy_from_device_callback(self, widget, data=None):
		model, rows = self.device_treeViewFile.getTree().get_selection().get_selected_rows()

		task = self.copy_from_device_task(model, rows)
		gobject.idle_add(task.next)

	def copy_from_device_task(self, model, rows):
		completed = 0
		total = len(rows)

		self.update_progress()

		while completed < total:
			row = rows[completed]
			iter = model.get_iter(row)
			filename = model.get_value(iter, 1)
			full_device_path = os.path.join(self.device_cwd, filename)
			full_host_path = os.path.join(self.host_cwd, filename)
			file_explorer.action_copy_from_device(self.adb, full_device_path, full_host_path)
			completed = completed + 1
			self.refreshHostFiles()
			self.update_progress(completed * 1.0 / total)

			yield True

		yield False

	def update_progress(self, value = None):
		if value is None:
			self.progress_bar.set_fraction(0)
			self.progress_bar.set_text("")
			self.progress_bar.pulse()
		else:
			self.progress_bar.set_fraction(value)

			self.progress_bar.set_text("%d%%" % (value * 100))

		if value >= 1:
			self.progress_bar.set_text("Done")
			self.progress_bar.set_fraction(0)
	
	def host_navigate_callback(self, widget, path, view_column):
		
		row = path[0]
		model = widget.get_model()
		iter = model.get_iter(row)
		is_dir = model.get_value(iter, 0)
		name = model.get_value(iter, 1)

		if is_dir:
			self.host_cwd = os.path.normpath(os.path.join(self.host_cwd, name))
			self.refreshHostFiles()

	def device_navigate_callback(self, widget, path, view_column):

		row = path[0]
		model = widget.get_model()
		iter = model.get_iter(row)
		is_dir = model.get_value(iter, 0)
		name = model.get_value(iter, 1)

		if is_dir:
			self.device_cwd = os.path.normpath(os.path.join(self.device_cwd, name))
			self.refreshDeviceFiles()
	
	
	def device_delete_item_callback(self, widget, data=None):
		model, rows = self.device_treeViewFile.getTree().get_selection().get_selected_rows()
		print 'delete', len(rows)

		if len(rows) > 0:
			items = []
			for r in rows:
				iter = model.get_iter(r)
				filename = model.get_value(iter, 1)
				items.append(filename)

			result = self.dialog_device_delete_confirmation(items)
	
	def dialog_device_delete_confirmation(self, items):
		items.sort()
		joined = ', '.join(items)
		print joined
		dialog = gtk.MessageDialog(
			parent = None,
			flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			type = gtk.MESSAGE_QUESTION,
			buttons = gtk.BUTTONS_OK_CANCEL,
			message_format = "Are you sure you want to delete %d items?" % len(items)
		)
		dialog.format_secondary_markup('%s will be deleted. This action cannot be undone.' % joined)
		dialog.show_all()
		result = dialog.run()
		
		dialog.destroy()
		
		if result == gtk.RESPONSE_OK:
			for item in items:
				full_item_path = os.path.join(self.device_cwd, item)
				file_explorer.action_device_delete_item(self.adb, full_item_path)
				self.refreshDeviceFiles()
		else:
			print 'no no'
		

	def device_create_directory_callback(self, widget, data=None):
		directory_name = self.dialog_get_directory_name()
		pattern = re.compile(r'(\w|_|-)+')

		if pattern.match(directory_name):
			full_path = os.path.join(self.device_cwd, directory_name)
			file_explorer.action_device_make_directory(self.adb, full_path)
			self.refreshDeviceFiles()
		else:
			print 'invalid directory name', directory_name

	def dialog_get_directory_name(self):
		dialog = gtk.MessageDialog(
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_QUESTION,
			gtk.BUTTONS_OK,
			None)

		dialog.set_markup('Please enter new directory name:')

		entry = gtk.Entry()
		entry.connect('activate', self.dialog_response, dialog, gtk.RESPONSE_OK)

		hbox = gtk.HBox()
		hbox.pack_start(gtk.Label('Name:'), False, 5, 5)
		hbox.pack_end(entry)

		dialog.vbox.pack_end(hbox, True, True, 0)
		dialog.show_all()

		dialog.run()

		text = entry.get_text()
		dialog.destroy()
		return text

	def dialog_response(self, entry, dialog, response):
		dialog.response(response)

	def die_callback(self, widget, data=None):
		self.destroy(widget, data)

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def main(self):
		gtk.main()


if __name__ == '__main__':
	explorer = GFileExplorer()
	explorer.main()
