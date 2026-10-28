"""
PROBLEM STATEMENT : Deleted File Recovery from a Disk (CSDF forensics)

Demonstrate deleted-file recovery on a disk using Sleuth Kit: image the
source device with dd, list deleted-file inode entries with fls, inspect one
inode with istat, and extract the data with icat.

WHY THE WORKFLOW IS BUILT THIS WAY (forensic principles):
- NEVER work on a live/original disk for recovery: image it first and
  operate only on the copy (dd). Any read/write mistake then damages the
  image, not the evidence.
- Deleted files are usually still present on disk: deletion normally only
  unlinks the inode and frees the blocks - the CONTENT remains until
  overwritten. fls -d lists those deleted entries and their inode numbers.
- istat shows the metadata of a chosen inode (times, size, block pointers)
  which tells you whether the content is recoverable (blocks not reused).
- icat dumps the raw data addressed by that inode, overlooking the fact that
  the filesystem no longer names it - that dump IS the recovered file.

WHY PYTHON (NOT C++):
The practical is essentially safe orchestration of forensic utilities
(dd/fls/istat/icat); Python's subprocess drives exactly those tools, so the
same script works across filesystem types the toolkit supports.

SAFETY NOTES (REALLY READ THIS):
- Run only on media you own or are authorised to examine.
- double-check the device path (lsblk output) BEFORE imaging: dd prompts for
  nothing and a wrong path/destination can destroy data instantly.
- The image file and the recovered file are opened for writing and WILL
  overwrite existing files at those paths.
- Needs:  sudo apt install sleuthkit   (lsblk/dd come with any base Linux)
- Run:    python3 "csdf/FileRecovery.py"
"""

import os        # to report the recovered file's size
import subprocess  # launching lsblk/dd/fls/istat/icat


def show_devices():
    """Show block devices so the device path can be picked correctly."""
    print("\nList of devices:")
    subprocess.run(["lsblk"])


def get_paths():
    """Ask for the source device and the destination image filename."""
    devname = input("\nEnter device path (e.g. /dev/sdb1): ")
    imgname = input("Enter image filename: ")
    return devname, imgname


def create_disk_image(devname, imgname):
    """
    dd step: read the whole device sector by sector (bs=512) into the image
    file. Progress prints live; failure aborts (check=True).
    """
    print("\nCreating disk image...")
    with open(imgname, "wb") as image:
        subprocess.run(
            ["dd", "if=" + devname, "bs=512", "status=progress"],
            stdout=image,
            check=True,
        )
    print("\nDisk image created successfully.")


def list_deleted_files(imgname):
    """fls -d: walk the filesystem and list deleted-file inodes."""
    print("\nShowing deleted files and inode numbers:")
    subprocess.run(["fls", "-d", imgname])


def show_inode_info(imgname, inodeno):
    """istat: metadata (size/times/blocks) for the chosen inode."""
    print("\nFile information:")
    subprocess.run(["istat", imgname, inodeno])


def recover_file(imgname, newfile, inodeno):
    """icat: dump the inode's data blocks into a new normal file."""
    with open(newfile, "wb") as recovered:
        subprocess.run(["icat", imgname, inodeno], stdout=recovered, check=True)


def run():
    """Imaging -> listing -> inspect -> extract; main() only calls this."""
    print("----- FILE RECOVERY SCRIPT -----")

    show_devices()
    devname, imgname = get_paths()

    create_disk_image(devname, imgname)
    list_deleted_files(imgname)

    inodeno = input("\nEnter inode of deleted file: ")
    show_inode_info(imgname, inodeno)

    newfile = input("\nEnter recovered filename with extension: ")
    recover_file(imgname, newfile, inodeno)

    print("\nFile recovered successfully.")
    print("Recovered file:", newfile)
    print("File size:", os.path.getsize(newfile), "bytes")


if __name__ == "__main__":
    run()
