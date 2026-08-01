from __future__ import annotations

from abc import ABC, abstractmethod


class Jugada(ABC):
    """clase abstracta de la que heredan Piedra, Papel y Tijeras
    args:
      name: str

    abstractmethod:
      __str__(self) -> str:"""

    def __init__(self, name: str) -> None:
        """define la instancia del objeto
        args:
          name: str
        attributes:
          self.name"""

        self.name = name

    @abstractmethod
    def __str__(self) -> str:
        """devuelve un f str con los datos name y type del objeto"""

        return f"Name: {self.name}. Type: {type(self)}"

    @abstractmethod
    def vence_a(self, otra: Jugada) -> bool:
        """Devuelve true si el objeto Jugada vence a otra
        args:
          otra: Jugada

        return:
          bool"""
