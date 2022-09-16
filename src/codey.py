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

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw#, Gdk, Gio


class App():

    def check_valid_config():
        if __debug__:
            configfolder = "src/res"
        else:
            if os.path.exists(os.path.expanduser("~") + "/.config"):
                configfolder = os.path.expanduser("~") + "/.config"
            else:
                configfolder = os.environ.get("XDG_CONFIG_HOME")
        try:
            if os.path.exists(App.read_config('Target_Path')):
                return
            else:
                App.set_config('Target_Path', os.path.expanduser('~'))
        except Exception as e:
            if type(e) == FileNotFoundError:
                with open((configfolder + '/codey.config'), "w") as file:
                    file.write(
                        "Target_Path: " + os.path.expanduser(
                            '~') + "\nShow Hidden Files: False\nShow PhP Files: True\nShow HTML Files: True\nShow all Files: False\nStart MariaDB Database: False")

    # opens the selected file in a webbrowser
    def open_file(file: str, action: str):
        longpath = App.read_config('Target_Path')
        shortpath = '/'.join(longpath.split('/')[
                             3:])  # gets path as string, converts it to list and deletes first 3 entrys(/home/user), puts it back together
        if action == 'Run':
            url = 'http://localhost:9000/' + shortpath + '/' + file
            process = subprocess.Popen(['xdg-open', url])
        elif action == 'Open':
            path = longpath + '/' + file
            process = subprocess.Popen(['xdg-open', path])

    # gets the code of the given file
    def get_code(file: str):
        path = App.read_config('Target_Path')
        if file is None:
            code = ''  # to avoid errors: after changing directory, the currently displayed file becomes None
        else:
            file = path + '/' + file
            with open(file, 'r') as contents:
                code = contents.read()
        return code

    def set_code(file: str, code: str):
        path = App.read_config('Target_Path')
        file = path + "/" + file
        with open(file, 'w') as contents:
            contents.write(code)

    # gets all the files in the current directory
    def get_files():
        path = App.read_config('Target_Path')
        filelist = []
        with os.scandir(path) as dirs:
            for entry in dirs:
                if entry.is_file():  # hides folders
                    if App.read_config('Show all Files') == 'True':
                        filelist.append(entry.name)
                    else:
                        if entry.name.endswith('.php') and App.read_config('Show PhP Files') == 'True':
                            filelist.append(entry.name)
                        elif entry.name.endswith('.html') and App.read_config('Show HTML Files') == 'True':
                            filelist.append(entry.name)
        if App.read_config('Show Hidden Files') == 'False':
            for entry in filelist:
                if entry.startswith('.'):
                    filelist.remove(entry)
        return filelist

    # writes the config
    def set_config(setting: str, content: str):
        if __debug__:
            configfolder = "src/res"
        else:
            if os.path.exists(os.path.expanduser("~") + "/.config"):
                configfolder = os.path.expanduser("~") + "/.config"
            else:
                configfolder = os.environ.get("XDG_CONFIG_HOME")
        allsettings = App.read_config('allSettings')
        for settings in allsettings:
            if settings[0] == setting:
                settings[1] = content
        with open(configfolder + '/codey.config', 'w') as config:
            for settings in allsettings:
                config.write(': '.join(settings) + '\n')

    # reads the config
    def read_config(setting: str):
        if __debug__:
            configfolder = "src/res"
        else:
            if os.path.exists(os.path.expanduser("~") + "/.config"):
                configfolder = os.path.expanduser("~") + "/.config"
            else:
                configfolder = os.environ.get("XDG_CONFIG_HOME")
        allsettings = []
        with open(configfolder + '/codey.config', 'r') as config:
            for line in config:
                line = line.strip().split(': ')
                if setting == 'allSettings':
                    allsettings.append(line)
                elif line[0] == setting:
                    return line[1]
        return allsettings


if __debug__:
    uipath = "src/res/codey.ui"
else:
    uipath = "/app/bin/codey.ui"


@Gtk.Template(filename=uipath)
class MainWindow(Gtk.Window):
    __gtype_name__ = "MainWindow"

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

    text = Gtk.TextBuffer()

    @Gtk.Template.Callback()
    def about_clicked(self, *args):
        self.aboutDialog.set_logo_icon_name("io.github.unicornyrainbow.codey")
        self.aboutDialog.show()

    @Gtk.Template.Callback()
    def on_checked(self, widget):
        App.set_config(widget.get_label(), str(widget.get_active()))
        self.fileChooser.remove_all()
        self.fill_selection()

    @Gtk.Template.Callback()
    def maria_checked(self, widget):
        App.set_config(widget.get_label(), str(widget.get_active()))
        if not widget.get_active():
            if __debug__:
                subprocess.Popen(['pkexec', 'systemctl', 'stop', 'mariadb'])
            else:
                subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])
        elif widget.get_active():
            if __debug__:
                subprocess.Popen(['pkexec', 'systemctl', 'start', 'mariadb'])
            else:
                subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'start', 'mariadb'])

    @Gtk.Template.Callback()
    def cancel_clicked(self, widget):
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceBox)
        self.scrolledWindow.set_child(self.codeLabel)

    @Gtk.Template.Callback()
    def save_clicked(self, widget):
        file = self.fileChooser.get_active_text()
        code = self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), False)
        App.set_code(file, code)
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceBox)
        self.scrolledWindow.set_child(self.codeLabel)
        self.codeLabel.set_label(App.get_code(file))

    # make File editable
    @Gtk.Template.Callback()
    def edit_clicked(self, widget):
        self.scrolledWindow.set_child(self.codeEditor)
        file = self.fileChooser.get_active_text()
        self.text.set_text(App.get_code(file))
        self.codeEditor.set_buffer(self.text)
        self.mainBox.remove(self.mainBox.get_first_child())
        self.mainBox.prepend(self.interfaceEditBox)

    # opens dialog to choose folder to look in
    @Gtk.Template.Callback()
    def folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_transient_for(self)
        dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
        dialog.connect('response', self.on_dialog_response)
        dialog.show()

    # updates the code segment when file is changed
    @Gtk.Template.Callback()
    def file_changed(self, widget):
        file = widget.get_active_text()
        self.codeLabel.set_label(App.get_code(file))

    # submits the filechoice
    @Gtk.Template.Callback()
    def submit_clicked(self, widget):
        file = self.fileChooser.get_active_text()
        App.open_file(file, widget.get_label())

    @staticmethod
    def set_check_button(name: str):
        setting = App.read_config(name)
        if setting == 'True':
            return True
        else:
            return False

    # fills files from current directory into dropdown
    def fill_selection(self):
        self.fileChooser.remove_all()
        files = App.get_files()
        files.sort()
        for entry in files:
            self.fileChooser.append_text(entry)

    def on_dialog_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            App.set_config('Target_Path', widget.get_file().get_path())
        self.fileChooser.remove_all()  # removes all old file entries in dropdown
        self.fill_selection()  # gets new entries for dropdown
        widget.destroy()

    def do_activate(self):
        self.showAll.set_active(self.set_check_button(self.showAll.get_label()))
        self.showHtml.set_active(self.set_check_button(self.showHtml.get_label()))
        self.showPhp.set_active(self.set_check_button(self.showPhp.get_label()))
        self.showHidden.set_active(self.set_check_button(self.showHidden.get_label()))
        self.maria.set_active(self.set_check_button(self.maria.get_label()))


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = MainWindow(application=self)

        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)
        window.do_activate()
        window.mainBox.remove(window.mainBox.get_first_child())
        window.fill_selection()

        window.present()


App.check_valid_config()

# start webserver and maybe mariadb
if __debug__:
    subprocess.Popen(['php', '-S', '0.0.0.0:9000', '-t', os.path.expanduser('~')])
else:
    subprocess.Popen(['flatpak-spawn', '--host', 'php', '-S', '0.0.0.0:9000', '-t', os.path.expanduser('~')])

app = MyApp(application_id='io.github.unicornyrainbow.codey')
app.run(sys.argv)

# kill webserver and maybe mariadb
if __debug__:
    subprocess.Popen(['killall', '-9', 'php'])
else:
    subprocess.Popen(['flatpak-spawn', '--host', 'killall', '-9', 'php'])

if App.read_config("Start MariaDB Database") == "True":
    if __debug__:
        subprocess.Popen(['pkexec', 'systemctl', 'stop', 'mariadb'])
    else:
        subprocess.Popen(['flatpak-spawn', '--host', 'pkexec', 'systemctl', 'stop', 'mariadb'])
