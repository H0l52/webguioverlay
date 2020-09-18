# Web Gui Overlay by H0l52
A easily customize-able GUI overlay that goes over the computer desktop. 

This project uses the pywin32 library (go check them out [HERE](https://github.com/mhammond/pywin32)!)
And it uses the pyqt5 libraries. To install these do `pip install PyQt5 PyQtWebEngine`.

It uses Tkinter for the `run` command.

## Downloads

To get a pre-combiled binary (made with pyinstaller), go to the [releases tab in GitHub.](https://github.com/H0l52/webguioverlay/releases)

Otherwise you can clone the repository and build it for yourself!

Installer command is `pyinstaller webguioverlay.py --onefile --hidden-import=pywintypes`

## HowTo

Make a folder in the directory of the program, and call it `gui`.

Run the program.

In the command line type `addelement`

Run through the setup process.

Type `help` to see the other commands

Example:

I went to [streamkit.discord.com/overlay](https://streamkit.discord.com/overlay)
and choose OBS.

I then configured the voice widget to my liking and grabbed the link.

In the Web Gui Overlay program i run `addelement` and I choose `topleft` as my position
Then I enter the link I got from the discord streamkit.
Then I choose a SizeX of 312
And I choose a SizeY of 600

Now when I join the voice chat I setup in the discord streamkit, I can see who is speaking as an overlay on my screen.
