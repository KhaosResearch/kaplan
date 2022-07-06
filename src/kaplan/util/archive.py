from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from kaplan.util.comparator import (
    Comparator,
    DominanceComparator
)

S = TypeVar("S")

class Archive(Generic[S], ABC):
    def __init__(self):
        self.solution_list: List[S] = []

    @abstractmethod
    def add(self, solution: S) -> bool:
        pass

    def get(self, index: int) -> S:
        return self.solution_list[index]

    def size(self) -> int:
        return len(self.solution_list)

    def get_name(self) -> str:
        return self.__class__.__name__


class NonDominatedSolutionsArchive(Archive[S]):
    def __init__(self, dominance_comparator: Comparator = DominanceComparator()):
        super(NonDominatedSolutionsArchive, self).__init__()
        self.comparator = dominance_comparator

    def add(self, solution: S) -> bool:
        is_dominated = False
        is_contained = False

        if len(self.solution_list) == 0:
            self.solution_list.append(solution)
            return True
        else:
            number_of_deleted_solutions = 0

            # New copy of list and enumerate
            for index, current_solution in enumerate(list(self.solution_list)):
                is_dominated_flag = self.comparator.compare(solution, current_solution)
                if is_dominated_flag == -1:
                    del self.solution_list[index - number_of_deleted_solutions]
                    number_of_deleted_solutions += 1
                elif is_dominated_flag == 1:
                    is_dominated = True
                    break
                elif is_dominated_flag == 0:
                    if solution.objectives == current_solution.objectives:
                        is_contained = True
                        break

        if not is_dominated and not is_contained:
            self.solution_list.append(solution)
            return True

        return False