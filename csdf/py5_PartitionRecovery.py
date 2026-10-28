"""
QUESTION 5 (CSDF):
Write a program to demonstrate partition recovery inspection: list block
devices with lsblk, show the partition table with fdisk, and scan for
lost partitions with TestDisk.

HOW IT WORKS:
1. lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS - see every connected
   device so the right one is chosen without guessing.
2. fdisk -l <device> - print the partition table the kernel currently
   sees. A "missing" partition usually appears here as unallocated
   space: the table entry was corrupted/overwritten/deleted, while the
   data sectors remain intact.
3. TestDisk <device> - interactive inspection: it scans unallocated
   space for filesystem superblocks / partition signatures and can
   RESTORE partition entries from backup boot sectors. Inspection is
   passive; only an explicit "Write" inside TestDisk changes the disk.

NOTE: this practical cannot pre-create its input file - the "dataset"
is a REAL block device chosen interactively (the forensic point).

COMMANDS (run from the repository root):
    install dependencies : sudo apt install testdisk
    run the program      : python3 csdf/py5_PartitionRecovery.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import subprocess


# ============================================================
# STEP 2 : SHOW DEVICES - list block devices (the "data source"
#          here is a real device, chosen interactively)
# ============================================================
def show_devices():
    """Step 2: list block devices with the useful identification columns."""
    print("\nList of devices:")
    subprocess.run(["lsblk", "-o", "NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS"])


# ============================================================
# STEP 3 : EXAMINE THE DEVICE - show the partition table (fdisk)
# ============================================================
def show_partition_table(devname):
    """Print the partition table the kernel currently sees."""
    print("\nShowing partition table:")
    subprocess.run(["sudo", "fdisk", "-l", devname])


# ============================================================
# STEP 4 : SCAN FOR LOST PARTITIONS - interactive TestDisk session
# ============================================================
def scan_lost_partitions(devname):
    """Launch TestDisk interactively for the lost-partition scan."""
    print("\nStarting partition recovery inspection...")
    print("TestDisk will help identify lost partitions.")
    subprocess.run(["sudo", "testdisk", devname])


# ============================================================
# STEP 5 : DRIVER - devices -> partition table -> TestDisk scan
# ============================================================
def run():
    print("----- PARTITION RECOVERY SCRIPT -----")

    show_devices()                                  # STEP 2
    devname = input("\nEnter device path (e.g. /dev/sdb): ")

    show_partition_table(devname)                   # STEP 3
    scan_lost_partitions(devname)                   # STEP 4

    print("\nPartition recovery inspection completed.")
    print("Verify partition boundaries before writing any changes.")


if __name__ == "__main__":
    run()