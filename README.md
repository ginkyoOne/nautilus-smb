# nautilus-smb
![  NAUTILUS SMB Logo](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/nautilus-smb.png)

![PYTHON](https://img.shields.io/badge/Pyhton-%23ffff6a?style=for%20the%20badge&logo=python&logoColor=white)
![GTK](https://img.shields.io/badge/GTK-03C75A?style=for%20the%20badge&logo=gtk&logoColor=white)
![GNOME](https://img.shields.io/badge/Gnome_44-%230b49c2?style=for%20the%20badge&logo=gnome&logoColor=white)

 
## Description

The project is a plugin for Gnome Nautilus that allows users to conveniently mount SMB shares into local folders. It utilizes GTK 4 and provides a seamless experience to open remote files in SMB shares as if they were local files.

Please note that this is an alpha version of the plugin. While we have put in our best effort to ensure its functionality, there might be some bugs and errors present. We kindly request users to report any issues they encounter to help us improve the plugin.

## Features

- Mount SMB shares into local folders
- Open remote files in SMB shares as if they were local files
- Utilizes GTK 4 for a modern and intuitive user interface

## Installation

1. Clone the GitHub repository: `git clone https://github.com/ginkyoOne/nautilus-smb`
2. Enter the folder: `cd nautilus-smb`
3. Install Nautilus Python: 
    - Fedora: `sudo dnf install nautilus-extensions git python3 python-requests nautilus-python python3-gobject`
    - Ubuntu: `sudo apt-get install nautilus-extensions git python3 python3-requests python3-nautilus python3-gi`
    - openSUSE: `sudo zypper install nautilus-extensions git python3 python3-requests python3-nautilus python3-gobject`
    - Arch Linux: `sudo pacman -S nautilus-extensions git python3 python-requests python-nautilus python-gobject`
   


5. Install the required dependencies: `pip install -r requirements.txt`
6. Install plugin: `sudo install --mode=644 nautilus-mounts.py /usr/share/nautilus-python/extensions/`
7. Restart Gnome Nautilus: `nautilus -q`

## Usage

1. Launch Gnome Nautilus.
2. Navigate to the folder where you want to mount the SMB share.
3. Right-click on the folder and select the "Mount SMB Share" option from the context menu.
4. Enter the required information, such as the share URL(without smb://), username, and password.
5. Click "Mount" to mount the SMB share into the selected folder.
6. You can now access remote files in the SMB share as if they were local files.

## Reporting Issues

If you encounter any bugs, errors, or have suggestions for improvements, please [create an issue](https://github.com/ginkyoOne/nautilus-smb/issues) on the GitHub repository.


## Screenshots

Mount item in the context Menu:  
![Mount item](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/01.png)

Main screen to mount the share:  
![Mount Screen](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/02.png)

Unmount item in the context Menu:  
![Unmount Item](https://raw.githubusercontent.com/ginkyoOne/nautilus-smb/main/screenshots/03.png)


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
