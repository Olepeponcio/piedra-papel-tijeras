from .jugada import Jugada


class Papel(Jugada):
    """clase del tipo Jugada
    args:
      name

    def:
      __str__()
      vence_a()
    """

    def __init__(self, name: str = "Papel") -> None:
        """inicializa los atributos de la instancia de clase heredada"""

        super().__init__(name)

    def __str__(self) -> str:
        return f"Jugada: {self.name}"

    def vence_a(self, otra: Jugada) -> bool:
        """devuelve true si el nombre de la otra jugada es piedra
        return: bool"""
        return otra.__str__ == "Piedra"
