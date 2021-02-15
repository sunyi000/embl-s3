from Tkinter import *
import Tkinter as tk
import subprocess
import tkMessageBox
from os.path import expanduser
import os


def mount():

    home = expanduser("~")

    pass_file = home + "/.passwd-s3fs"
    mount_dir = home + "/" + bucket_entry.get()

    passwd_s3fs = open(pass_file,"w")
    passwd_s3fs.write(access_entry.get()+":" + secret_entry.get())
    passwd_s3fs.close()

    subprocess.call(['chmod','0600',pass_file])

    if os.path.ismount(mount_dir):
        tkMessageBox.showerror(title="Error", message="Bucket is already mounted")
    else:
        subprocess.call(['mkdir', '-p',mount_dir])

        p1 = subprocess.Popen(["s3fs",bucket_entry.get(), mount_dir, "-o","url=https://s3.embl.de","-o","use_path_request_style"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,err = p1.communicate()

        if err == "":
            tkMessageBox.showinfo("Success!!", "Your EMBL S3 bucket is mounted at ~/embl-s3")
            subprocess.check_call(['xdg-open', mount_dir])
        else:
            tkMessageBox.showerror("Error!!","Error mounting EMBL S3 bucket, please check your credentials and try again !")


def umount():
    bucket = bucket_entry.get()
    mount_dir = "~/" + bucket
    if os.path.ismount(mount_dir):
        subprocess.call(['fusermount', '-uqz', mount_dir])
    else:
        tkMessageBox.showerror(title="Error", message="Bucket not mounted")


master = tk.Tk()
master.title("EMBL S3 client")

tk.Label(master,text="Access Key").grid(row=0)
tk.Label(master,text="Secret Key").grid(row=1)
tk.Label(master,text="Bucket").grid(row=2)

access_entry = tk.Entry(master,width=30)
secret_entry = tk.Entry(master,width=30)
bucket_entry = tk.Entry(master,width=30)

access_entry.grid(row=0,column = 1,padx=5,pady=5)
secret_entry.grid(row=1, column=1,padx=5,pady=5)
bucket_entry.grid(row=2,column=1,padx=5,pady=5)

tk.Button(master, text='Quit',command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Mount', command=mount).grid(row=3, column=1, sticky=tk.W, pady=4)

tk.Button(master, text='Unmount', command=umount).grid(row=3, column=2, sticky=tk.W, pady=4)


master.mainloop()


