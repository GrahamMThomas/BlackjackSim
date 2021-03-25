from enum import Enum


class BlackjackAction(Enum):
    Stay = 1
    Hit = 2
    Double = 3
    Split = 4
    Surrender = 5
    Bust = 6

    def __str__(self):
        name = self.value
        if name == self.Stay.value:
            return "St"
        elif name == self.Hit.value:
            return "Hi"
        elif name == self.Double.value:
            return "Do"
        elif name == self.Split.value:
            return "Sp"
        elif name == self.Surrender.value:
            return "FF"
        else:
            return "?"