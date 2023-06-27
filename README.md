# nautilus-smb
![  NAUTILUS SMB Logo](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/nautilus-smb.png)

## Description

The project is a plugin for Gnome Nautilus that allows users to conveniently mount SMB shares into local folders. It utilizes GTK 4 and provides a seamless experience to open remote files in SMB shares as if they were local files.

Please note that this is an alpha version of the plugin. While we have put in our best effort to ensure its functionality, there might be some bugs and errors present. We kindly request users to report any issues they encounter to help us improve the plugin.

## Features

- Mount SMB shares into local folders
- Open remote files in SMB shares as if they were local files
- Utilizes GTK 4 for a modern and intuitive user interface

## Installation

1. Install python: `sudo dnf install python3`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Install Nautilus Python: `sudo dnf install nautilus-extensions git python3 python-requests nautilus-python python3-gobject`
4. Copy the plugin into: `~/.local/share/nautilus-python/extensions`
5. Restart Gnome Nautilus: `nautilus -q`

## Usage

1. Launch Gnome Nautilus.
2. Navigate to the folder where you want to mount the SMB share.
3. Right-click on the folder and select the "Mount SMB Share" option from the context menu.
4. Enter the required information, such as the share URL(without smb://), username, and password.
5. Click "Mount" to mount the SMB share into the selected folder.
6. You can now access remote files in the SMB share as if they were local files.

## Reporting Issues

If you encounter any bugs, errors, or have suggestions for improvements, please [create an issue](https://github.com/ginkyoOne/nautilus-smb/issues) on the GitHub repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).


## Screenshots

Mount item in the context Menu:  
![Mount item](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/01.png)

Main screen to mount the share:  
![Mount Screen](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/02.png)

Unmount item in the context Menu:  
![Unmount Item](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/03.png)
