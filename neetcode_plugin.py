import json
import os
import random

from semantic_kernel.functions import kernel_function


class NeetcodePlugin:

    def __init__(self, directory: str):
        self.directory = directory

        file_path = os.path.join(self.directory, "problems.json")
        self.problem_list: str = []

        with open(file_path, "r") as file:
            file_content = file.read()
            problem_categories = json.loads(file_content)

            for _, category in problem_categories.items():
                for problem_name in category:
                    self.problem_list.append(problem_name)

    
    @kernel_function(
            name="GetNeetcode250List", 
            description="Get a list of all problem names in the Neetcode 250 set"
    )
    async def get_neetcode_250_list(self) -> list[str]:
        """Get a list of all problem names in the Neetcode 250 set"""
        return self.problem_list
    

    @kernel_function(
            name="GetRandomNeetcode250Problem", 
            description="Get a single randomly selected problem name from the Neetcode 250 set"
    )
    async def get_random_neetcode_250_problem(self) -> str:
        """Get a single randomly selected problem name from the Neetcode 250 set"""
        index = random.randint(0, len(self.problem_list))
        return self.problem_list[index]
