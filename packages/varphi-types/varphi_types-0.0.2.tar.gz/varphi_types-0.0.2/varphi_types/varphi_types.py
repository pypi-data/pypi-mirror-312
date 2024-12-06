from dataclasses import dataclass
from enum import Enum, auto

class TapeCharacter(Enum):
    BLANK = auto()
    TALLY = auto()


class HeadDirection(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Instruction:
    nextState: "State"  # Quotes for forward reference
    characterToPlace: TapeCharacter
    directionToMove: HeadDirection
    lineNumber: int
    line: str


@dataclass
class State:
    name: str
    onTally: list[Instruction]
    onBlank: list[Instruction]
    references: list[tuple[int, tuple[int, int]]]  # List of (lines, (start col, end col)) of all references to this state.
    implementations: list[tuple[int, tuple[int, int]]]

    def __init__(self, name: str) -> None:
        self.name = name
        self.onTally = []
        self.onBlank = []
        self.references = []
        self.implementations = []

    def addOnTallyInstruction(self, instruction: Instruction) -> None:
        if instruction not in self.onTally:
            self.onTally.append(instruction)

    def addOnBlankInstruction(self, instruction: Instruction) -> None:
        if instruction not in self.onBlank:
            self.onBlank.append(instruction)


class Comment:
    pass
