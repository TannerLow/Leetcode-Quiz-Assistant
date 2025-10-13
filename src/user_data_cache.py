import json
from typing import Any


class UserDataCache:

    def __init__(self, user_stats_filename: str) -> None:
        self.user_stats_filename: str = user_stats_filename
        self.stats: dict[str, Any] = {}
        self.reload_stats()


    def write_level(self, problem_name: str, level: int) -> None:
        self.stats['levels'][problem_name] = level
        
        with open(self.user_stats_filename, 'w') as file:
            json.dump(self.stats, file, indent=4)

        self.reload_stats()


    def get_level(self, problem_name: str) -> int:
        return self.stats['levels'].get(problem_name, 0)
    

    def get_levels(self, problem_list: list[str]) -> dict[str, int]:
        output: dict[str, int] = {}

        for problem_name in problem_list:
            output[problem_name] = self.get_level(problem_name)

        return output


    def reload_stats(self) -> None:
        with open(self.user_stats_filename, 'r') as file:
            self.stats = json.load(file)
