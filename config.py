import os

class Path:
    def __init__(self, folder_path, subfolder_source, subfolder_destination = None):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = folder_path
        self.subfolder_source = subfolder_source
        self.subfolder_destination = subfolder_destination

    def get_source_path(self):
        return os.path.join(self.project_root, self.folder_path, self.subfolder_source)

    def get_destination_path(self):
        return os.path.join(self.project_root, self.folder_path, self.subfolder_destination)
