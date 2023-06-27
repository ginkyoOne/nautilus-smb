#Alpha version 1.0.0
from gi import require_version

require_version('Nautilus', '4.0')
require_version('Gtk', '4.0')

import os
import socket
import subprocess
import tempfile
from threading import Thread

import psutil
from gi.repository import Gdk, Gio, GLib, GObject, Gtk, Nautilus


class SmbMountMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    window = None
    
    def __init__(self):
        pass

        
    def get_smb_shares(self):
        shares = []

        def scan_hosts(ip_prefix):
            hosts = []
            for i in range(1, 255):
                ip = f"{ip_prefix}.{i}"
                try:
                    socket.gethostbyaddr(ip)
                    hosts.append(ip)
                except (socket.herror, socket.gaierror, socket.timeout):
                    pass
            return hosts

        def get_shares_for_host(ip):
            cmd = ['smbclient', '-L', f"//{ip}", '-U', 'guest%', '-N']
            host_shares = []

            try:
                smb_output = subprocess.check_output(cmd).decode('utf-8')

                for line in smb_output.splitlines():
                    if 'Disk' in line:
                        share = line.split()[0]
                        host_shares.append(share)
            except subprocess.CalledProcessError as e:
                print(
                    f"Error: {e}. Could not fetch SMB shares for host {ip} using 'smbclient' command.")

            return host_shares


        # Get the active interface IP address
        hosts = scan_hosts('192.168.1')

        for host in hosts:
            host_shares = get_shares_for_host(host)
            shares.extend(host_shares)

        return shares
    
    def is_file_path_in_fstab_or_mount(self, file_path):
    # Check if the file path is already in the fstab file
        result = subprocess.run(['grep', file_path, '/etc/fstab'], capture_output=True, text=True)
        fstab_content = len(result.stdout) > 0
        
        # Run the `mount` command and capture the output
        result = subprocess.run(['mount'], capture_output=True, text=True)
        mount_content = file_path in result.stdout

        
        return fstab_content or mount_content
    
    
    def show_message_dialog(self, message, message_type=Gtk.MessageType.INFO ) :
        dialog = Gtk.MessageDialog(
            message_type=message_type,
            buttons=Gtk.ButtonsType.CLOSE,
            text=message,
        )        
        dialog.set_transient_for(self.window)
        dialog.set_modal(self.window)
        
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()
    
    def get_file_items(self,files):
        
        # Get the Nautilus application
        gtk_app = Gtk.Application.get_default()

        # Get the active window from the application
        active_window = gtk_app.get_active_window()
        self.window = active_window
        
        
        # Check if the file is a directory
        if len(files) == 1 & files[0].is_directory():
            file = files[0]
        else:
            return



        # Create a menu item for the mount command            
        smb_mount_item = Nautilus.MenuItem(
            name="SmbMountMenuProvider::Mount",
            label="Mount SMB Share",
            tip="Mount a remote SMB share to this folder",
        )
        smb_mount_item.connect("activate", self.mount_smb_share, file)


        # Create a spliter to separate the menu items
        separator = Nautilus.MenuItem(name='MyMenuProvider::Separator', label='-', sensitive=False)
        


        # Create a menu item for the unmount command
        smb_unmount_item = Nautilus.MenuItem(
            name="SmbMountMenuProvider::Unmount",
            label="Unmount SMB Share",
            tip="Unmount a mounted SMB share from this folder",
        )
        smb_unmount_item.connect("activate", self.unmount_smb_share, file)

        # Check if the file path is already in the fstab file or is already mounted
        file_path = file.get_location().get_path()
        exists_in_fstab = self.is_file_path_in_fstab_or_mount(file_path)

        
        # Return the menu items depending if the file path is already in the fstab file or is already mounted
        if exists_in_fstab:
            return [smb_unmount_item]
        else:
            return [smb_mount_item]





    def mount_smb_share(self, menuItem, file):

        window = Gtk.Window().get_focus()
        dialog = Gtk.Dialog(title='Mount SMB Share',
                            transient_for=window,
                            modal=True,
                            destroy_with_parent=True)

        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.set_modal(True)

        grid = Gtk.Grid(column_spacing=6, row_spacing=6)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        box.set_spacing(10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(15)
        box.set_margin_end(15)
        
        box.append(grid)
        dialog.get_content_area().append(box)  # Updated line
        
        
        
        
        manual_entry_label = Gtk.Label(label="SMB share path:")
        grid.attach(manual_entry_label, 0, 1, 1, 1)

        manual_entry = Gtk.Entry()
        grid.attach(manual_entry, 1, 1, 1, 1)
        
        user_label = Gtk.Label(label="Username:")
        grid.attach(user_label, 0, 2, 1, 1)
        
        user_entry = Gtk.Entry()
        grid.attach(user_entry, 1, 2, 1, 1)

        password_label = Gtk.Label(label="Password:")
        grid.attach(password_label, 0, 3, 1, 1)

        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        password_entry.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        grid.attach(password_entry, 1, 3, 1, 1)
        

        persist_checkbox = Gtk.CheckButton(label="Make mount persistent")
        grid.attach(persist_checkbox, 0, 4, 3, 1)









        def open_response(dialog, response):
            #set result to False
            result = False
            
            #if user clicked ok, mount the share
            if response == Gtk.ResponseType.OK:
                
                #get input from dialog
                selected_share = manual_entry.get_text()
                username = user_entry.get_text()
                password = password_entry.get_text()
                persistent = persist_checkbox.get_active()
                
                #print some debug info
                print('folder', file.get_location().get_path());
                print('selected_share: ', selected_share);
                
                #mount the share
                result = self.mount_share(file, selected_share, username, password, persistent)
                
                #if mount failed, rollback and unmount
                if(result == False):
                    self.unmount_smb_share(self, file, False)
            
            else:
                dialog.destroy()
                
            #destroy dialog if result is True
            if (result == True): dialog.destroy()
        
        
        #connect the response signal to open_response function
        dialog.connect("response", open_response)
        
        #show dialog attached to nautilus window as modal
        dialog.set_transient_for(self.window)
        dialog.set_modal(self.window)
        
        #show dialog
        dialog.show()
    
    def mount_share(self, file, share, username, password , persistent=False):
        try:
            # Get the local folder path
            local_folder = file.get_location().get_path()
            
            # Get the current user's UID and GID
            uid = os.getuid()
            gid = os.getgid()

            mount_options = f'rw,username={username},password={password},uid={uid},gid={gid}'

            # Construct the mount command
            mount_cmd = f'mount -t cifs {share} {local_folder} -o {mount_options}'

            # Construct the command to add the entry to /etc/fstab
            fstab_entry_cmd = f'echo "{share}\t{local_folder}\tcifs\t{mount_options}\t0\t0" >> /etc/fstab'

            # Combine the mount command and fstab entry command into a single pkexec command
            pkexec_cmd = ['pkexec', 'sh', '-c', f'{mount_cmd} && {fstab_entry_cmd}']

            # Execute the pkexec command
            result = subprocess.run(pkexec_cmd,capture_output=True)

            # Check if the mount command was successful
            if result.returncode != 0:
                # Display an error dialog box for mount command errors
                if result.stderr:
                    error_msg = f"Error mounting SMB share and adding entry to /etc/fstab: {result.stderr.decode('utf-8')}"                
                else:
                    error_msg = f"Error mounting SMB share and adding entry to /etc/fstab: Unknown error occurred"

                self.show_message_dialog(error_msg, Gtk.MessageType.ERROR)
            
                return False
            
            else:
                # return True if the mount command was successful
                success_msg = f"SMB share {share} mounted successfully to {local_folder}"
                self.show_message_dialog(success_msg, Gtk.MessageType.INFO)
                
                return True

        except subprocess.CalledProcessError as e:
            # Display an error dialog box for mount command errors
            error_msg = f"Error mounting SMB share: {str(e).replace(password, '********')}"
            self.show_message_dialog(error_msg, Gtk.MessageType.ERROR)
        
            #return False if the mount command failed and keep the dialog open
            return False
        
            
        except Exception as e:
            # Display a generic error dialog box for other exceptions
            error_msg = f"An error occurred: {str(e).replace(password, '********')}"
            self.show_message_dialog(error_msg, Gtk.MessageType.ERROR)
            
            #return False if the mount command failed and keep the dialog open
            return False

    def unmount_smb_share(self, menu, file, show_dialog=True):
        try: 
            
            local_folder = file.get_location().get_path()
            clean_path = local_folder.replace('/', '\\/')
            
            pkexec_cmd = [
                'pkexec', 'sh', '-c',
                f"grep -vE '{clean_path}' /etc/fstab | tee /etc/fstab.tmp && mv /etc/fstab.tmp /etc/fstab; umount {local_folder}"
            ]
            
            result = subprocess.run(pkexec_cmd, capture_output=True, text=True)

            # Check the result
            if result.returncode == 0:
                if(show_dialog == True):
                    success_msg = f"SMB share {local_folder} unmounted successfully"
                    self.show_message_dialog(success_msg, Gtk.MessageType.INFO)
                    
            else:
                if result.stderr:
                    error_msg = f"An error occurred: {result.stderr}"                
                else:
                    error_msg = f"An error occurred: Unknown error occurred"
                    
                self.show_message_dialog(error_msg, Gtk.MessageType.ERROR)

                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.show_message_dialog(error_msg, Gtk.MessageType.ERROR)
            