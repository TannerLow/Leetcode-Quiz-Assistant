import json
import os
import random

from semantic_kernel.functions import kernel_function


class NeetcodePlugin:

    def __init__(self, data_dir: str, user_stats_filename: str):
        self.data_dir = data_dir
        self.user_stats_filename = user_stats_filename
        self.last_problem = None

        file_path = os.path.join(self.data_dir, "problems.json")
        self.problem_list: list[str] = []

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
        self.last_problem = self.problem_list[index]
        return self.last_problem
    
    
    @kernel_function(
        name="IncreaseProblemKnowledgeLevel", 
        description="Increase the knowledge level of a problem in the database"
    )
    async def increase_problem_knowledge_level(self) -> None:
        """Increase the knowledge level of a problem in the database"""
        with open(self.user_stats_filename, 'r') as file:
            stats = json.load(file)

            if self.last_problem in stats['skips']:
                return

            stats['levels'][self.last_problem] = min(stats['levels'].get(self.last_problem, 0) + 1, 5)

        with open(self.user_stats_filename, 'w') as file:
            json.dump(stats, file)

    def get_problem_level(self, problem_name: str) -> int:
        """Get the user's knowledge level for a given problem"""
        with open(self.user_stats_filename, 'r') as file:
            stats = json.load(file)
            
            if problem_name in stats['levels']:
                return stats['levels'][problem_name]
            
            elif problem_name not in stats['skips']:
                stats['levels'][problem_name] = 0

            else:
                return -1
            
        with open(self.user_stats_filename, 'w') as file:
            json.dump(stats, file)

        return stats['levels'][problem_name]
