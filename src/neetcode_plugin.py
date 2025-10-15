import json
import os
import random
from typing import Optional

from semantic_kernel.functions import kernel_function

from .user_data_cache import UserDataCache


class NeetcodePlugin:

    def __init__(self, data_dir: str, user_stats_filename: str):
        self.data_dir = data_dir
        self.user_data_cache: UserDataCache = UserDataCache(user_stats_filename)
        self.last_problem: Optional[str] = None
        self.last_increase: Optional[str] = None
        self.last_decrease: Optional[str] = None

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
        description=(
            "Get a single randomly selected problem name from the Neetcode 250 set."
            "Use this function for selecting the next problem to quiz the user on."
        )
    )
    async def get_random_neetcode_250_problem(self) -> str:
        """
        Get a single randomly selected problem name from the Neetcode 250 set.
        Use this function for selecting the next problem to quiz the user on.
        """
        levels: dict[str, int] = self.user_data_cache.get_levels(self.problem_list)

        weighted_problem_list: list[str] = []
        for name, level in levels.items():
            for _ in range((6 - level)**2):
                weighted_problem_list.append(name)

        index = random.randint(0, len(weighted_problem_list))
        self.last_problem = weighted_problem_list[index]

        return self.last_problem
    
    
    @kernel_function(
        name="IncreaseProblemKnowledgeLevel", 
        description="Increase the knowledge level of a problem in the database"
    )
    async def increase_problem_knowledge_level(self) -> None:
        """Increase the knowledge level of a problem in the database"""
        if self.last_problem is None or self.last_problem == self.last_increase:
            return
        
        problem_level: int = self.user_data_cache.get_level(self.last_problem)
        self.user_data_cache.write_level(self.last_problem, min(problem_level + 1, 5))


    @kernel_function(
        name="DecreaseProblemKnowledgeLevel", 
        description="Decrease the knowledge level of a problem in the database"
    )
    async def decrease_problem_knowledge_level(self) -> None:
        """Decrease the knowledge level of a problem in the database"""
        if self.last_problem is None or self.last_problem == self.last_decrease:
            return
        
        problem_level: int = self.user_data_cache.get_level(self.last_problem)
        self.user_data_cache.write_level(self.last_problem, max(problem_level - 1, 0))
    