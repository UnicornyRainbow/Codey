# Codey
A simple application to preview and run code files, primarily intended for webdevelopment.

![codey-screenshot-1](https://i.postimg.cc/SxBKTW2w/Codey-Screenshot.png)

# Installation
First make sure you have the following dependencies installed:
* flatpak
* flathub beta repo
```commandline
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo
```
then install via a graphical software center or run
```commandline
flatpak install unicorn.flatpak
```

# Build it from source
You need the gnome 42 beta runtime
You need to download the zip from github or run
```commandline
git clone https://github.com/blackmoonboy/codey
```
then build it with(you can edid the arguments to your needs)
```commandline
cd Codey & chmod +x flatpak_build.sh & flatpak_build.sh -i
```

# Run it from source
You need Pygobject, xdg, gtk 4, libadwaita 1
You need to download the zip from github or run
```commandline
git clone https://github.com/blackmoonboy/codey
```
Then you need to comment/uncomment some of the last lines according to the comments
Run codey.py:
```commandline
cd Codey & python3 codey.py
```
