"""
This helper class represents an fstab entry that stores
 the information to be added to an fstab file.
It offers a generate_fstab_row function to build the string
 to be added to the fstab file.
"""

TAB = '\t'
ROOT_MOUNTPOINT = '/'
SQL_STRING = 'sql'
FSCK_ROOT_CHECK_OPTION = '0\t1'
BACKUP_DB_OPTION = '1\t0'
NOFSCK_NOBACKUP = '0\t0'
DEFAULT_OPTIONS = 'defaults'

class FstabEntry:
    """
    This class represents the information contained in the YAML input file
     relative to an fstab entry.
    """
    def __init__(self, device_filesystem, mount_point, export_parameter, file_system_type, options):
        self.device_filesystem = device_filesystem
        self.mount_point = mount_point
        self.export_parameter = export_parameter
        self.file_system_type = file_system_type
        self.options = options
        self.fstab_row = ''

    def generate_fstab_row(self):
        """
        This method generates the fstab row, specifying particular
         options in case of root mount point or databases entries.
        """
        device_filesystem = self.device_filesystem
        if self.export_parameter:
            device_filesystem += ':' + self.export_parameter
        fstab_row = device_filesystem + TAB + self.mount_point + TAB + self.file_system_type + TAB
        if self.options:
            fstab_options = ''
            for option in self.options:
                fstab_options += option + ','
            fstab_options = fstab_options[:-1]
            fstab_row += fstab_options + TAB
        if not self.options:
            fstab_row += DEFAULT_OPTIONS + TAB

        if self.mount_point == ROOT_MOUNTPOINT:
            fstab_row += FSCK_ROOT_CHECK_OPTION
        elif SQL_STRING in self.mount_point:
            fstab_row += BACKUP_DB_OPTION
        else:
            fstab_row += NOFSCK_NOBACKUP
        self.fstab_row = fstab_row

    def get_fstab_row(self):
        """
        This method returns the fstab row generated.
        """
        return self.fstab_row
