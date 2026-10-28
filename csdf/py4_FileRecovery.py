"""
QUESTION 4 (CSDF):
Write a program to demonstrate deleted-file recovery from a disk image
using Sleuth Kit: create an image with dd, list deleted-file inodes with
fls, inspect an inode with istat, and extract the file with icat.

HOW IT WORKS (FORENSIC WORKFLOW):
1. lsblk lists block devices so the device path is chosen correctly -
   never guess a device in forensics.
2. dd images the whole device sector by sector (bs=512) into a file.
   Work on the COPY: any mistake then damages the image, not the evidence.
3. fls -d lists DELETED-file entries with their inode numbers: deletion
   normally only unlinks the inode - the data blocks survive until they
   are overwritten, which is why recovery is possible at all.
4. istat shows the metadata (size, times, block pointers) of the chosen
   inode - tells you whether the content is intact/recoverable.
5. icat dumps the data addressed by that inode into a new normal file -
   that dump IS the recovered file.

NOTE: this practical cannot pre-create its input file - the "dataset" is
a REAL block device chosen interactively, which is the forensic point.

COMMANDS (run from the repository root):
    install dependencies : sudo apt install sleuthkit
    run the program      : python3 csdf/py4_FileRecovery.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os
import subprocess


# ============================================================
# STEP 2 : SHOW DEVICES - list block devices (the "data source"
#          here is a real device, chosen interactively)
# ============================================================
def show_devices():
    """List block devices so the device path can be picked correctly."""
    print("\nList of devices:")
    subprocess.run(["lsblk"])


# ============================================================
# STEP 3 : CREATE THE FILE - image the chosen device into a
#          disk-image file with dd (this is the file next steps use)
# ============================================================
def create_disk_image(devname, imgname):
    """dd step: copy the whole device into the image file (abort on error)."""
    print("\nCreating disk image...")
    with open(imgname, "wb") as image:
        subprocess.run(
            ["dd", "if=" + devname, "bs=512", "status=progress"],
            stdout=image,
            check=True,
        )
    print("\nDisk image created successfully.")


# ============================================================
# STEP 4 : USE THE FILE - list deleted inodes, inspect, recover
# ============================================================
def list_deleted_files(imgname):
    """fls -d: show deleted-file entries and their inode numbers."""
    print("\nShowing deleted files and inode numbers:")
    subprocess.run(["fls", "-d", imgname])


def show_inode_info(imgname, inodeno):
    """istat: metadata (size/times/blocks) of the chosen inode."""
    print("\nFile information:")
    subprocess.run(["istat", imgname, inodeno])


def recover_file(imgname, inodeno, newfile):
    """icat: dump the inode's data blocks into a new normal file."""
    with open(newfile, "wb") as recovered:
        subprocess.run(["icat", imgname, inodeno], stdout=recovered, check=True)


# ============================================================
# STEP 5 : DRIVER - devices -> image -> list -> inspect -> recover
# ============================================================
def run():
    print("----- FILE RECOVERY SCRIPT -----")

    show_devices()                                        # STEP 2
    devname = input("\nEnter device path (e.g. /dev/sdb1): ")
    imgname = input("Enter image filename: ")

    create_disk_image(devname, imgname)                   # STEP 3
    list_deleted_files(imgname)                           # STEP 4

    inodeno = input("\nEnter inode of deleted file: ")
    show_inode_info(imgname, inodeno)

    newfile = input("\nEnter recovered filename with extension: ")
    recover_file(imgname, inodeno, newfile)

    print("\nFile recovered successfully.")
    print("Recovered file:", newfile)
    print("File size:", os.path.getsize(newfile), "bytes")


if __name__ == "__main__":
    run()