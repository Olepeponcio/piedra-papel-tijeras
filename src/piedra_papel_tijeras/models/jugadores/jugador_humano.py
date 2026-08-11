from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class JugadorHumano(Jugador):
    """Representa a la entidad jugador humano. Obtiene tipo de jugada de la ventana_juego
    por evento disparado."""

    def __init__(self, nombre: str = "Jugador") -> None:
        super().__init__(nombre)

        self._tipo_seleccionado: TipoJugada | None = None

    def registrar_seleccion(self, tipo: TipoJugada) -> None:
        """Registra temporalmente el tipo elegido por la interfaz activa."""
        if not isinstance(tipo, TipoJugada):
            raise TypeError("Tipo debe ser una instancia de TipoJugada")

        self._tipo_seleccionado = tipo

    def _seleccionar_tipo(self) -> TipoJugada:
        """Consume y devuelve el tipo previamente registrado."""
        if self._tipo_seleccionado is None:
            raise RuntimeError("El jugador todavía no ha seleccionado una jugada")

        tipo_seleccionado = self._tipo_seleccionado
        self._tipo_seleccionado = None
        return tipo_seleccionado

    # hereda metodo elegir_jugada que usa _seleccionar_tipo
