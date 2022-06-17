#!/usr/bin/env python3

# Codey, Display and launch various code.
#     Copyright (C) 2022  UnicornyRainbow
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import gi
import sys
import subprocess
gi.require_version('Gtk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
import xdg

class app():

	def checkValidConfig():
		try:
			if os.path.exists(app.readConfig('Target_Path')):
				return
			else:
				app.setConfig('Target_Path', os.path.expanduser('~'))
		except Exception as e:
			if type(e) == FileNotFoundError:
				with open((xdg.xdg_config_home().__str__()+'/codey.config'), "a+") as file:
					file.write(
						"Target_Path: " + os.path.expanduser('~') + "\nShow Hidden Files: False\nShow PhP Files: True\nShow HTML Files: True\nShow all Files: False\nStart MariaDB Database: False")

	#opens the selected file in a webbrowser
	def openFile(file, action):
		longpath = app.readConfig('Target_Path')
		shortpath = '/'.join(longpath.split('/')[3:])			#gets path as string, converts it to list and deletes first 3 entrys(/home/user), puts it back together
		if action == 'Run':
			url = 'http://localhost:9000/' + shortpath + '/' + file
			process = subprocess.Popen(['xdg-open', url])
		elif action == 'Open':
			path = longpath + '/' + file
			process = subprocess.Popen(['xdg-open', path])

	#gets the code of the given file
	def getCode(file):
		path = app.readConfig('Target_Path')
		if file == None:
			code = ''				#to avoid errors: after changing directory, the currently displayed file becomes None
		else:
			file = path + '/' + file
			with open(file, 'r') as contents:
				code = contents.read()
		return code

	def setCode(file, code):
		path = app.readConfig('Target_Path')
		file = path + "/" + file
		with open(file, 'w') as contents:
			contents.write(code)

	#gets all the files in the current directory
	def getFiles():
		path = app.readConfig('Target_Path')
		fileList = []
		with os.scandir(path) as dirs:
			for entry in dirs:
				if entry.is_file():					#hides folders
					if app.readConfig('Show all Files') == 'True':
						fileList.append(entry.name)
					else:
						if entry.name.endswith('.php') and app.readConfig('Show PhP Files') == 'True':
							fileList.append(entry.name)
						elif entry.name.endswith('.html') and app.readConfig('Show HTML Files') == 'True':
							fileList.append(entry.name)
		if app.readConfig('Show Hidden Files') == 'False':
			for entry in fileList:
				if entry.startswith('.'):
					fileList.remove(entry)

		return fileList

	#writes the config
	def setConfig(setting, content):
		allSettings = app.readConfig('allSettings')
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
		with open(xdg.xdg_config_home().__str__()+'/codey.config', 'w') as config:
			for settings in allSettings:
				config.write(': '.join(settings) + '\n')


	#reads the config
	def readConfig(setting):
		allSettings = []
		with open(xdg.xdg_config_home().__str__()+'/codey.config', 'r') as config:
			for line in config:
				line = line.strip().split(': ')
				if setting == 'allSettings':
					allSettings.append(line)
				elif line[0] == setting:
					return(line[1])
		return(allSettings)





class window(Gtk.ApplicationWindow):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		app3 = self.get_application()
		sm = app3.get_style_manager()

		self.spacing = 10

		#window
		Gtk.Window.__init__(self, title='Codey')
		self.set_default_size(960, 540)


		#Define the General structure of the Window

		#Header Bar
		self.headerBar = Gtk.HeaderBar()
		self.set_titlebar(self.headerBar)
		self.headerBar.set_show_title_buttons(True)
		self.title = Gtk.Label()
		self.title.set_label('Codey')
		self.headerBar.set_title_widget(self.title)

		#Setup general window Structure
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = (self.spacing * 4))
		self.mainBox.set_margin_start(self.spacing)
		self.mainBox.set_margin_top(self.spacing)
		self.mainBox.set_margin_bottom(self.spacing)
		self.set_child(self.mainBox)

		#left side of Window, used for Button etc
		self.interfaceBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.mainBox.append(self.interfaceBox)
		self.interfaceEditBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)

		#Scrollable right side of the window for the Code block
		self.scrolledWindow = Gtk.ScrolledWindow()
		self.scrolledWindow.set_vexpand(True)
		self.scrolledWindow.set_hexpand(True)
		self.mainBox.append(self.scrolledWindow)



		#Populate the Header Bar

		#Hamburger Menu
		#Popover and Button
		self.popover = Gtk.Popover(position = Gtk.PositionType.BOTTOM, has_arrow = True)
		self.menuButton = Gtk.MenuButton(popover=self.popover, icon_name = "open-menu-symbolic", primary = True)
		self.headerBar.pack_end(self.menuButton)
		#add a box to the Menu
		self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)
		self.popover.set_child(self.menuBox)
		#add Menu Items
		self.showHidden = Gtk.CheckButton()
		self.showHidden.set_label('Show Hidden Files')
		self.showHidden.set_active(self.setCheckButton(self.showHidden.get_label()))
		self.showHidden.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showHidden)
		self.showPhp = Gtk.CheckButton()
		self.showPhp.set_label('Show PhP Files')
		self.showPhp.set_active(self.setCheckButton(self.showPhp.get_label()))
		self.showPhp.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showPhp)
		self.showHtml = Gtk.CheckButton()
		self.showHtml.set_label('Show HTML Files')
		self.showHtml.set_active(self.setCheckButton(self.showHtml.get_label()))
		self.showHtml.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showHtml)
		self.showAll = Gtk.CheckButton()
		self.showAll.set_label('Show all Files')
		self.showAll.set_active(self.setCheckButton(self.showAll.get_label()))
		self.showAll.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showAll)
		self.maria = Gtk.CheckButton()
		self.maria.set_label("Start MariaDB Database")
		self.maria.set_active(self.setCheckButton(self.maria.get_label()))
		self.maria.connect("toggled", self.mariaChecked)
		self.menuBox.append(self.maria)
		self.about = Gtk.Button(label = 'About', has_frame = False)
		self.about.connect('clicked', self.aboutClicked)
		self.menuBox.append(self.about)
  
  
  
		#Sourcefolder Chooser
		self.folderChooser = Gtk.Button()
		self.folderIcon = Gtk.Image.new_from_icon_name('folder-open-symbolic')
		self.folderChooser.set_child(self.folderIcon)
		self.folderChooser.connect('clicked', self.folderClicked)
		self.headerBar.pack_start(self.folderChooser)


		#Populate the Window itself

		#Dropdown to choose the file
		self.fileChooser = Gtk.ComboBoxText()
		self.interfaceBox.append(self.fileChooser)
		self.fillSelection()
		self.fileChooser.connect('changed', self.fileChanged)

		#Buttons to open the file
		self.submit = Gtk.Button(label = 'Run')
		self.submit.connect('clicked', self.submitClicked)
		self.interfaceBox.append(self.submit)

		self.open = Gtk.Button(label = 'Open')
		self.open.connect('clicked', self.submitClicked)
		self.interfaceBox.append(self.open)

		self.edit = Gtk.Button(label = "Edit")
		self.edit.connect("clicked", self.editClicked)
		self.interfaceBox.append(self.edit)

		self.save = Gtk.Button(label = "Save")
		self.save.connect("clicked", self.saveClicked)
		self.interfaceEditBox.append(self.save)

		self.cancel = Gtk.Button(label = "Cancel")
		self.cancel.connect("clicked", self.cancelClicked)
		self.interfaceEditBox.append(self.cancel)

		#displays the code of the opened file
		self.codeLabel = Gtk.Label()
		self.codeLabel.set_wrap(False)
		self.codeLabel.set_justify(Gtk.Justification.LEFT)
		self.scrolledWindow.set_child(self.codeLabel)
		self.codeEditor = Gtk.TextView(vexpand = True, left_margin = 5, right_margin = 5, accepts_tab = True)
		self.codeEditor.set_wrap_mode(2)
		#self.scrolledWindow.set_child(self.codeEditor)


	def cancelClicked(self, widget):
		self.mainBox.remove(self.mainBox.get_first_child())
		self.mainBox.prepend(self.interfaceBox)
		self.scrolledWindow.set_child(self.codeLabel)

	def saveClicked(self, widget):
		file = self.fileChooser.get_active_text()
		code = self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), False)
		app.setCode(file, code)
		self.mainBox.remove(self.mainBox.get_first_child())
		self.mainBox.prepend(self.interfaceBox)
		self.scrolledWindow.set_child(self.codeLabel)
		self.codeLabel.set_label(app.getCode(file))

	#make File editable
	def editClicked(self, widget):
		#self.scrolledWindow.rem
		self.scrolledWindow.set_child(self.codeEditor)
		file = self.fileChooser.get_active_text()
		self.text = Gtk.TextBuffer()
		self.text.set_text(app.getCode(file))
		self.codeEditor.set_buffer(self.text)
		self.mainBox.remove(self.mainBox.get_first_child())
		self.mainBox.prepend(self.interfaceEditBox)

	#opens dialog to choose folder to look in
	def folderClicked(self, widget):
		dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.set_transient_for(self)
		dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
		dialog.connect('response', self.on_dialog_response)
		dialog.show()

	def on_dialog_response(self, widget, response_id):
		if response_id == Gtk.ResponseType.OK:
			app.setConfig('Target_Path', widget.get_file().get_path())
		self.fileChooser.remove_all()					#removes all old file entries in dropdown
		self.fillSelection()							#gets new entries for dropdown
		widget.destroy()

	#updates the code segment when file is changed
	def fileChanged(self, widget):
		file = widget.get_active_text()
		self.codeLabel.set_label(app.getCode(file))

	#fills files from current directory into dropdown
	def fillSelection(self):
		files = app.getFiles()
		files.sort()
		for entry in files:
			self.fileChooser.append_text(entry)

	#submits the filechoice
	def submitClicked(self, widget):
		file = self.fileChooser.get_active_text()
		app.openFile(file, widget.get_label())

	def onChecked(self, widget):
		app.setConfig(widget.get_label(), str(widget.get_active()))
		self.fileChooser.remove_all()
		self.fillSelection()

	def mariaChecked(self, widget):
		app.setConfig(widget.get_label(), str(widget.get_active()))
		if widget.get_active() == False:
			subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])
		elif widget.get_active() == True:
			subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'start', 'mariadb'])

	def setCheckButton(self, name):
		setting = app.readConfig(name)
		if setting == 'True':
			return True
		else:
			return False

	def aboutClicked(self, widget):
	    self.dialog = Gtk.AboutDialog(authors = ['UnicornyRainbow'], artists= ['UnicornyRainbow'], comments = 'Display and launch various code using the Php webserver.', license_type = Gtk.License.GPL_3_0_ONLY, program_name = 'Codey', version = '1.0.0', website_label = 'Website', website = 'https://unicornyrainbow.github.io/Codey/')
	    self.dialog.set_logo_icon_name('codey')
	    self.dialog.show()

class MyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect('activate', self.on_activate)

	def on_activate(self, app):
		self.win = window(application = app)
		self.win.present()
		

app.checkValidConfig()

#start webserver and maybe mariadb
subprocess.Popen(['flatpak-spawn', '--host', 'php', '-S', '0.0.0.0:9000', '-t', os.path.expanduser('~')])
if app.readConfig("Start MariaDB Database") == "True":
	subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'start', 'mariadb'])

app2=MyApp(application_id='io.github.unicornyrainbow.codey')
app2.run(sys.argv)
 
#kill webserver and maybe mariadb
subprocess.Popen(['flatpak-spawn', '--host', 'killall', '-9', 'php'])
if app.readConfig("Start MariaDB Database") == "True":
	subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])