"""
This utily takes in input a local INPUT_FILENAME and
 appends fstab entries to OUTPUT_FILENAME based on the input file.
It also generates a REQUIREMENTS_FILENAME with the cli commands needed
 to resolve the dependencies of using
the particular configuration, in terms of
 mount point directories, modules, and reserved space needed for a particular fs.
If argument install-requirements is given in the cli while calling the script,
 the commands generated in REQUIREMENTS_FILENAME will also be executed.
"""

import os
import sys
import yaml
from fstab_entry import FstabEntry

INPUT_FILENAME = 'input.yaml'
OUTPUT_FILENAME = 'fstab'
REQUIREMENTS_FILENAME = 'requirements.txt'

MOUNT_KEY = 'mount'
EXPORT_KEY = 'export'
TYPE_KEY = 'type'
XFS_FILE_SYSTEM_TYPE = 'xfs'
ROOT_RESERVE_KEY = 'root-reserve'
OPTIONS_KEY = 'options'

NEW_LINE = '\n'

def create_fstab_file():
    """
    This is the main function of the utility, that will be called
    executing the .py file. It will append to OUTPUT_FILENAME
     the resulting FstabEntry,
     create (if not present) the directory for the mount point,
     write to REQUIREMENTS_FILENAME the dependencies,
     the mount command and finally the command to reserve bytes
     in particular file systems.
    """
    with open(INPUT_FILENAME, encoding='utf-8', mode='r') as input_file:
        with open(OUTPUT_FILENAME, encoding='utf-8', mode='w') as output_file, open(
            REQUIREMENTS_FILENAME, encoding='utf-8', mode='w') as requirements_file:
            try:
                json_dict = convert_yaml_to_json(input_file)
                reserved_bytes_dict = {}

                for device_filename, device_parameters in json_dict.items():
                    device_filesystem = device_filename
                    mount_point = device_parameters.get(MOUNT_KEY)
                    export_parameter = device_parameters.get(EXPORT_KEY)
                    file_system_type = device_parameters.get(TYPE_KEY)
                    reserved_bytes = device_parameters.get(ROOT_RESERVE_KEY)
                    options = device_parameters.get(OPTIONS_KEY)

                    fstab_entry = FstabEntry(device_filesystem, mount_point, export_parameter,
                        file_system_type, options)
                    fstab_entry.generate_fstab_row()
                    fstab_row = fstab_entry.get_fstab_row()
                    requirements_file.write("sudo mkdir -p " + fstab_entry.mount_point)
                    requirements_file.write(NEW_LINE)

                    if file_system_type == XFS_FILE_SYSTEM_TYPE:
                        requirements_file.write("sudo apt install nfs-common")
                        requirements_file.write(NEW_LINE)

                    if reserved_bytes:
                        reserved_bytes_dict[device_filename] = reserved_bytes

                    output_file.write(fstab_row)
                    output_file.write(NEW_LINE)

                requirements_file.write("sudo mount -a")
                requirements_file.write(NEW_LINE)

                if reserved_bytes_dict:
                    for device, reserved_percentage in reserved_bytes_dict.items():
                        requirements_file.write("sudo tune2fs -m" +
                            reserved_percentage[:-1] + " " + device)
                        requirements_file.write(NEW_LINE)

            except yaml.YAMLError as exc:
                print(exc)

    if len(sys.argv) > 1:
        if sys.argv[1] == 'install-requirements':
            install_requirements()

def convert_yaml_to_json(input_file):
    """This method takes in input the file path of a YAML file
     and returns a json dictionary of the given file"""
    yaml_json = yaml.safe_load(input_file)
    fstab_root_key = list(yaml_json.keys())[0]
    json_dict = yaml_json[fstab_root_key]
    return json_dict

def install_requirements():
    """This method reads from REQUIREMENTS_FILENAME
     and launches the commands in the cli"""
    with open(REQUIREMENTS_FILENAME, encoding='utf-8', mode='r') as requirements_list:
        for requirement in requirements_list:
            os.system(requirement)

if __name__ == '__main__':
    create_fstab_file()
