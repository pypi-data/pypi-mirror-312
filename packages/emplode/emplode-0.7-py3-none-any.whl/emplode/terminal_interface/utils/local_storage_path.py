import os

import platformdirs

config_dir = platformdirs.user_config_dir("emplode")


def get_storage_path(subdirectory=None):
    if subdirectory is None:
        return config_dir
    else:
        return os.path.join(config_dir, subdirectory)
