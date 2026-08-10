from enum import Enum


class Resultado(Enum):
    """Resultados posibles de una ronda desde la perspectiva humana."""

    VICTORIA = "Victoria"
    DERROTA = "Derrota"
    EMPATE = "Empate"

    def __str__(self) -> str:
        return self.value
