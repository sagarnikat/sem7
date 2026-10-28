"""
PROBLEM STATEMENT : Partition Recovery Inspection (CSDF forensics)

Walk through checking WHY a filesystem is missing one or more partitions and
let TestDisk guide an inspection: lsblk to see devices, fdisk to read the
current partition table, then TestDisk to scan for lost partitions.

HOW THE PROCESS WORKS:
1. lsblk lists every connected block device with size/format/type, so the
   right device path is chosen WITHOUT guessing - picking the wrong device
   is the classic way to lose data in this domain.
2. fdisk -l <device> prints the partition table the kernel currently sees.
   A "missing" partition usually shows up here as unallocated space: the
   table entry got corrupted, overwritten (e.g. by a failed install) or
   simply deleted - while the actual data sectors remain intact.
3. TestDisk then scans the unallocated space for filesystem superblocks /
   partition signatures and offers to RESTORE the partition entries (chain
   of boot-sector backups). Only the inspection stages are passive; WRITING
   a partition table is only done deliberately inside TestDisk.

WHY PYTHON (NOT C++):
Same reasoning as FileRecovery.py: the practical is correct, deliberate
use of existing forensic tools (lsblk/fdisk/testdisk); Python's subprocess
launches them with the exact arguments, keeping the script portable and
reviewable line by line.

SAFETY NOTES:
- Invoked with sudo (fdisk -l and TestDisk need raw device access) - stick to
  inspecting; do NOT run "Write"/"Repair" inside TestDisk unless you
  intend to CHANGE the disk and hold a verified backup.
- Never experiment on a disk containing important data.
- Needs:  sudo apt install testdisk   (lsblk/fdisk ship with the base system)
- Run:    python3 "csdf/PartitionRecovery.py"
"""

import subprocess  # launching lsblk/fdisk/testdisk


def show_devices():
    """Step 1: list block devices with the useful identification columns."""
    print("\nList of devices:")
    subprocess.run(["lsblk", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS"])


def get_device():
    """Step 2a: confirm which whole disk to examine."""
    return input("\nEnter device path (e.g. /dev/sdb): ")


def show_partition_table(devname):
    """Step 2b: fdisk -l shows the partition table the kernel currently has."""
    print("\nShowing partition table:")
    subprocess.run(["sudo", "fdisk", "-l", devname])


def scan_lost_partitions(devname):
    """
    Step 3: launch TestDisk in interactive mode on the chosen device.
    The user walks the menus (Analyse -> QuickSearch) to look for lost
    partitions; nothing is written unless they choose Write.
    """
    print("\nStarting partition recovery inspection...")
    print("TestDisk will help identify lost partitions.")
    subprocess.run(["sudo", "testdisk", devname])


def run():
    """Device listing -> partition table -> TestDisk scan; main calls this."""
    print("----- PARTITION RECOVERY SCRIPT -----")

    show_devices()
    devname = get_device()

    show_partition_table(devname)
    scan_lost_partitions(devname)

    print("\nPartition recovery inspection completed.")
    print("Verify partition boundaries before writing any changes.")


if __name__ == "__main__":
    run()
