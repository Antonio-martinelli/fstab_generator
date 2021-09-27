# YAML to fstab converter

This Python utility takes in input an `input.yaml` file and mounts the file system configuration listed in it.

Assuming we have:

- all the disks available to the system, 
- `sudo` rights for the user executing the script,
- routing well configured with `192.168.4.5` (or any other IP from the private network),

the utility takes care of: 

- appending the content of the input to `/etc/fstab` ,
- creating (if not present) the mount point directories and adjusting their permissions (#TODO check),
- installing `nfs-common` as requirement for mounting `xfs` disks,
- mounting the new devices (this requires no collision or redundance with previously mounted devices),
- reserving percentages of disk space for mountpoints required with `root-reserve` option using `tune2fs` command as not specifiable in `fstab` file.

The utility generates a `requirements.txt` file with cli commands to be executed in order to install the requirements, mount the `fstab` file and reserve filesystem blocks.

NOTE: the commands in `requirements.txt` will be launched only if the script is called with parameter `install-requirements`, otherwise they will just be written to the file. This in order to possibly review the commands generated before actually executing them, as they will run with sudo.

# Usage

Import the files `input.yaml`, `fstab_generator.py` and `fstab_entry.py` in a directory accessible by the sudoer user, and launch it with the command:

- `python fstab_generator.py`
 to append to `/etc/fstab` and review the commands in `requirements.txt` before executing them,

or

- `python fstab_generator.py install-requirements` 
to append to `/etc/fstab` and execute the required cli commands to have the file system configured according to the input file.