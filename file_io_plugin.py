import os
from semantic_kernel.functions import kernel_function


class FileIOPlugin:
    def __init__(self, directory: str):
        self._directory = directory

    @kernel_function(name="ReadFile", description="Get the contents of a file given its name")
    async def read_file(self, file_name: str) -> str:
        """Reads the contents of a file."""
        file_path = os.path.join(self._directory, file_name)
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "File not found"
        except Exception as e:
            return "Error: " + str(e)

    @kernel_function(name="WriteFile", description="Write the contents of a file")
    async def write_file(self, file_name: str, content: str) -> str:
        """Writes the contents to a file."""
        file_path = os.path.join(self._directory, file_name)
        try:
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(file_path, "w") as file:
                file.write(content)
                return "File written successfully"
        except Exception as e:
            return "Error: " + str(e)
        
    @kernel_function(name="GetFileList", description="Get a list of files in the directory")
    async def get_file_list(self) -> list[str]:
        """Gets a list of files in the directory."""
        return os.listdir(self._directory)