#!/usr/bin/env python3


import os
import webbrowser
import gi
import sys
gi.require_version('Gtk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw



class app():


	#called on startup, checks if folder set in config is valid
	def checkValidFolder():
		if os.path.exists(app.readConfig('Target_Path')):
			return
		else:
			app.setConfig('Target_Path', '/home')


	#opens the selected file in a webbrowser
	def openFile(file):
		longpath = app.readConfig('Target_Path')
		shortpath = '/'.join(longpath.split('/')[3:])			#gets path as string, converts it to list and deletes first 3 entrys(/home/user), puts it back together
		if file.endswith('.php') or file.endswith('.html'):
			url = 'localhost:9000/' + shortpath + '/' + file
			webbrowser.open_new_tab(url)
		elif file.endswith('.sh') or file.endswith('.py'):
			os.system('gnome-terminal -- "' + longpath + '/' + file + '"')#longpath + '/' + file)

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
		
	#gets all the files in the current directory
	def getFiles():
		path = app.readConfig('Target_Path')
		fileList = []
		with os.scandir(path) as dirs:
			for entry in dirs:
				#if not entry.name.startswith('.', 0, 1):		#hides hidden files
				if entry.is_file():					#hides folders
					if entry.name.endswith('.php') and app.readConfig('Show PhP Files') == 'True':
						fileList.append(entry.name)
					elif entry.name.endswith('.html') and app.readConfig('Show HTML Files') == 'True':
						fileList.append(entry.name)
					elif entry.name.endswith('.py') and app.readConfig('Show Python Files') == 'True':
						fileList.append(entry.name)
					elif entry.name.endswith('.sh') and app.readConfig('Show Shell Files') == 'True':
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
		with open('codey.config', 'w') as config:
			for settings in allSettings:
				config.write(': '.join(settings) + '\n')
			
			
	#reads the config
	def readConfig(setting):
		allSettings = []
		with open('codey.config', 'r') as config:
			for line in config:
				line = line.strip().split(': ')
				if setting == 'allSettings':
					allSettings.append(line)
				elif line[0] == setting:
					return(line[1])
		return(allSettings)





class window(Gtk.ApplicationWindow):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)#'Codey', 960, 540, **kwargs)

		app3 = self.get_application()
		sm = app3.get_style_manager()
		sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
		
		#window
		Gtk.Window.__init__(self, title='Codey')
		#self.set_border_width(20)
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
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 40)
		self.set_child(self.mainBox)

		#left side of Window, used for Button etc
		self.interfaceBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.mainBox.append(self.interfaceBox)
		self.box1 = Gtk.Box(spacing = 20)
		self.interfaceBox.append(self.box1)
		self.box2 = Gtk.Box(spacing = 20)
		self.interfaceBox.append(self.box2)

		#Scrollable right side of the window for the Code block
		self.scrolledWindow = Gtk.ScrolledWindow()
		self.scrolledWindow.set_vexpand(True)
		self.scrolledWindow.set_hexpand(True)
		self.mainBox.append(self.scrolledWindow)
		


		#Populate the Header Bar

		#Hamburger Menu
		#Popover and Button
		self.popover = Gtk.Popover()
		self.popover.set_position(Gtk.PositionType.BOTTOM)
		self.menuButton = Gtk.MenuButton(popover=self.popover)
		#self.menuIcon = Gtk.Image.new_from_icon_name("open-menu-symbolic")
		#self.menuButton.append(self.menuIcon)
		self.headerBar.pack_end(self.menuButton)
		#add a box to the Menu
		self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.popover.set_child(self.menuBox)
		#add Menu Items 
		self.showHidden = Gtk.CheckButton()
		self.showHidden.set_label('Show Hidden Files')
		self.showHidden.set_active(self.setCheckButton(self.showHidden.get_label()))
		self.showHidden.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showHidden)#, False, True, 10)
		self.showPhp = Gtk.CheckButton()
		self.showPhp.set_label('Show PhP Files')
		self.showPhp.set_active(self.setCheckButton(self.showPhp.get_label()))
		self.showPhp.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showPhp)#, False, True, 10)
		self.showHtml = Gtk.CheckButton()
		self.showHtml.set_label('Show HTML Files')
		self.showHtml.set_active(self.setCheckButton(self.showHtml.get_label()))
		self.showHtml.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showHtml)#, False, True, 10)
		self.showPy = Gtk.CheckButton()
		self.showPy.set_label('Show Python Files')
		self.showPy.set_active(self.setCheckButton(self.showPy.get_label()))
		self.showPy.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showPy)#, False, True, 10)
		self.showShell = Gtk.CheckButton()
		self.showShell.set_label('Show Shell Files')
		self.showShell.set_active(self.setCheckButton(self.showShell.get_label()))
		self.showShell.connect("toggled", self.onChecked)
		self.menuBox.prepend(self.showShell)#, False, True, 10)
		#add all the Menu items and show them 
		#self.menuBox.show_all()
		
		#self.setCheckButton()

		
		
		#Sourcefolder Chooser
		self.folderChooser = Gtk.Button()
		self.folderIcon = Gtk.Image.new_from_icon_name('folder-open-symbolic')#, Gtk.IconSize.MENU)
		self.folderChooser.set_child(self.folderIcon)
		self.folderChooser.connect('clicked', self.folderClicked)
		self.headerBar.pack_start(self.folderChooser)


		#Populate the Window itself

		#Dropdown to choose the file
		self.fileChooser = Gtk.ComboBoxText()
		self.box1.append(self.fileChooser)
		self.fillSelection()
		self.fileChooser.connect('changed', self.fileChanged)

		#Button to open the file
		self.submit = Gtk.Button(label = 'Open')
		self.submit.connect('clicked', self.submitClicked)
		self.box2.append(self.submit)

		#displays the code of the opened file
		self.codeLabel = Gtk.Label()
		self.codeLabel.set_wrap(False)
		self.codeLabel.set_justify(Gtk.Justification.LEFT)
		self.scrolledWindow.set_child(self.codeLabel)



	#opens dialog to choose folder to look in
	def folderClicked(self, widget):
		dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.set_transient_for(self)
		dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
		#response = 0
		dialog.connect('response', self.on_dialog_response)
		dialog.show()
		
	def on_dialog_response(self, widget, response_id):
		#print(widget)
		#print(response_id)
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
		for entry in files:
			self.fileChooser.append_text(entry)

	#submits the filechoice
	def submitClicked(self, widget):
		file = self.fileChooser.get_active_text()
		app.openFile(file)
		
	def onChecked(self, widget):
		app.setConfig(widget.get_label(), str(widget.get_active()))
		
	def setCheckButton(self, name):
		setting = app.readConfig(name)
		if setting == 'True':
			return True
		else:
			return False

class MyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect('activate', self.on_activate)

	def on_activate(self, app):
		self.win = window(application = app)
		self.win.present()
		
		
app.checkValidFolder()

#start webserver
os.system('php -S localhost:9000 -t ~/ &>/dev/null &')

#window = window()
#window.connect('delete-event', Gtk.main_quit)
#window.show_all()
#Gtk.main()
app2=MyApp(application_id='org.Unicorn.Codey')
app2.run(sys.argv)

#kill webserver
os.system('killall -9 php &>/dev/null &')



