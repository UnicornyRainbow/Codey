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
#import xdg
gi.require_version('Gtk','4.0')
gi.require_version('Gdk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, Gio

class app():

    def checkValidConfig():
        configfolder = os.environ.get("XDG_CONFIG_HOME")
        try:
            if os.path.exists(app.readConfig('Target_Path')):
                return
            else:
                app.setConfig('Target_Path', os.path.expanduser('~'))
        except Exception as e:
            if type(e) == FileNotFoundError:
                #with open((xdg.xdg_config_home().__str__() + '/codey.config'), "a+") as file:
                with open((configfolder + '/codey.config'), "a+") as file:
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
        configfolder = os.environ.get("XDG_CONFIG_HOME")
        allSettings = app.readConfig('allSettings')
        for settings in allSettings:
            if settings[0] == setting:
                settings[1] = content
        #with open(xdg.xdg_config_home().__str__() + '/codey.config', 'w') as config:
        with open(configfolder + '/codey.config', 'w') as config:
            for settings in allSettings:
                config.write(': '.join(settings) + '\n')


    #reads the config
    def readConfig(setting):
        configfolder = os.environ.get("XDG_CONFIG_HOME")
        allSettings = []
        #with open(xdg.xdg_config_home().__str__() + '/codey.config', 'r') as config:
        with open(configfolder + '/codey.config', 'r') as config:
            for line in config:
                line = line.strip().split(': ')
                if setting == 'allSettings':
                    allSettings.append(line)
                elif line[0] == setting:
                    return(line[1])
        return(allSettings)

@Gtk.Template(filename="/app/bin/codey.ui") #for flatpak
#@Gtk.Template(filename="codey.ui")           #for debug
class main_window(Gtk.Window):
    __gtype_name__ = "main_window"

    mainBox = Gtk.Template.Child()

    interfaceBox = Gtk.Template.Child()
    fileChooser = Gtk.Template.Child()

    interfaceEditBox = Gtk.Template.Child()

    scrolledWindow = Gtk.Template.Child()
    codeLabel = Gtk.Template.Child()
    codeEditor = Gtk.Template.Child()

    popover = Gtk.Template.Child()
    popoverBox = Gtk.Template.Child()
    showAll = Gtk.Template.Child()
    showHtml = Gtk.Template.Child()
    showPhp = Gtk.Template.Child()
    showHidden = Gtk.Template.Child()
    maria = Gtk.Template.Child()

    aboutDialog = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def aboutClicked(self, *args):
        self.aboutDialog.set_logo_icon_name("io.github.unicornyrainbow.codey")
        self.aboutDialog.show()

    @Gtk.Template.Callback()
    def onChecked(self, widget):
        app.setConfig(widget.get_label(), str(widget.get_active()))
        self.fileChooser.remove_all()
        self.fillSelection()

    @Gtk.Template.Callback()
    def mariaChecked(self, widget):
        app.setConfig(widget.get_label(), str(widget.get_active()))
        if widget.get_active() == False:
            subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])
        elif widget.get_active() == True:
            subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'start', 'mariadb'])

    @Gtk.Template.Callback()
    def cancelClicked(self, widget):
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceBox)
        self.scrolledWindow.set_child(self.codeLabel)

    @Gtk.Template.Callback()
    def saveClicked(self, widget):
        file = self.fileChooser.get_active_text()
        code = self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), False)
        app.setCode(file, code)
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceBox)
        self.scrolledWindow.set_child(self.codeLabel)
        self.codeLabel.set_label(app.getCode(file))

    #make File editable
    @Gtk.Template.Callback()
    def editClicked(self, widget):
        self.scrolledWindow.set_child(self.codeEditor)
        file = self.fileChooser.get_active_text()
        self.text = Gtk.TextBuffer()
        self.text.set_text(app.getCode(file))
        self.codeEditor.set_buffer(self.text)
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceEditBox)

    #opens dialog to choose folder to look in
    @Gtk.Template.Callback()
    def folderClicked(self, widget):
        dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_transient_for(self)
        dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
        dialog.connect('response', self.on_dialog_response)
        dialog.show()

    #updates the code segment when file is changed
    @Gtk.Template.Callback()
    def fileChanged(self, widget):
        file = widget.get_active_text()
        self.codeLabel.set_label(app.getCode(file))

    #submits the filechoice
    @Gtk.Template.Callback()
    def submitClicked(self, widget):
        file = self.fileChooser.get_active_text()
        app.openFile(file, widget.get_label())

    def setCheckButton(self, name):
        setting = app.readConfig(name)
        if setting == 'True':
            return True
        else:
            return False

    #fills files from current directory into dropdown
    def fillSelection(self):
        files = app.getFiles()
        files.sort()
        for entry in files:
            self.fileChooser.append_text(entry)

    def on_dialog_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            app.setConfig('Target_Path', widget.get_file().get_path())
        self.fileChooser.remove_all()					#removes all old file entries in dropdown
        self.fillSelection()							#gets new entries for dropdown
        widget.destroy()

    def do_activate(self):
        self.showAll.set_active(self.setCheckButton(self.showAll.get_label()))
        self.showHtml.set_active(self.setCheckButton(self.showHtml.get_label()))
        self.showPhp.set_active(self.setCheckButton(self.showPhp.get_label()))
        self.showHidden.set_active(self.setCheckButton(self.showHidden.get_label()))
        self.maria.set_active(self.setCheckButton(self.maria.get_label()))

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = main_window(application = self)

        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)
        window.do_activate()
        window.mainBox.remove(window.mainBox.get_first_child())
        window.fillSelection()

        window.present()


app.checkValidConfig()

#start webserver and maybe mariadb
subprocess.Popen(['flatpak-spawn', '--host', 'php', '-S', '0.0.0.0:9000', '-t', os.path.expanduser('~')])

app2=MyApp(application_id='io.github.unicornyrainbow.codey')
app2.run(sys.argv)

#kill webserver and maybe mariadb
subprocess.Popen(['flatpak-spawn', '--host', 'killall', '-9', 'php'])
if app.readConfig("Start MariaDB Database") == "True":
    subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])
