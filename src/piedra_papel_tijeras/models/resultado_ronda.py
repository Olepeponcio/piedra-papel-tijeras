from dataclasses import dataclass

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.resultado import Resultado


@dataclass(frozen=True)
class ResultadoDeLaRonda:
    """recoge y representa las jugadas aplicadas por maquina y humano y el resultado del enfrentamiento
    para el jugador_humano"""

    jugada_humana: Jugada
    jugada_maquina: Jugada
    resultado: Resultado


# frozen asegura que no sea mutable una vez creado el objeto.
