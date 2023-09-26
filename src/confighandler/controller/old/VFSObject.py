import os
from abc import ABC

class VFSObject(ABC):
    def __init__(self, file_system_obj: str = None, pref_folder: str = None, keywords: dict = None):
        super().__init__()

        self._raw_file_system_obj = file_system_obj
        self.keywords = keywords

        if file_system_obj is None or file_system_obj == "":
            raise ValueError("File input can't be None or empty. No file given")

        if pref_folder is None or pref_folder == "":
            self.pref_folder = "./"
        else:
            self.pref_folder = pref_folder

        self.set_obj(file_system_obj=self._raw_file_system_obj, keywords=keywords)

    @property
    def filename(self):
        return self._raw_file_system_obj

    @property
    def absolute(self):
        return self._abs

    @property
    def relative(self):
        return self._rel

    def setup_folder(self):
        # Check if the given argument is a file
        if os.path.isfile(self.absolute) or "." in self.absolute:
            folder = os.path.split(self.absolute)[0]
            # joind the splitted string
            folder = os.path.join(folder)
        else:
            folder = self.absolute

        if "{" in folder:
            print(self.absolute)
            raise Exception("Can't set folder for file with keywords in path.")

        # Try creating the output directory
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as exc:
                print(f"Could not create folder {folder}. Exception: {exc}")
                raise exc

        # check if the folder exists
        try:
            if not os.path.exists(folder):
                raise FileNotFoundError(f"Folder {folder} does not exist")
        except Exception as exc:
            print(f"Could not check if folder {folder} exists. Exception: {exc}")

        self._folder_set = True
        print(f"Folder created: {folder} for "
              f" -> \n{self.absolute}\n")
        return folder

    def create_object(self):
        if self._folder_set:
            return self
        else:
            return self.setup_folder()

    def set_obj(self, file_system_obj: str = None, keywords: dict = None, pref_folder: str = None):
        # Now replace all keywords
        if keywords is not None:
            self.keywords = {**self.keywords, **keywords}

        if file_system_obj is not None:
            self._raw_file_system_obj = file_system_obj

        if pref_folder is not None:
            self.pref_folder = pref_folder
        # print(f"Setting pref_folder to {self.pref_folder} for {self.filename}")

        self.file_system_obj = self._raw_file_system_obj

        self._folder_set = False

        self._file = self.file_system_obj

        self._file_full = os.path.join(self.pref_folder, self._file)

        self._abs = os.path.abspath(self._file_full)

        try:
            self._rel = os.path.relpath(self._file_full, os.getcwd())
        except:
            self._rel = self._abs

    def __str__(self):
        return self.relative

    def __repr__(self):
        return f"{type(self)}: {self.relative}"
