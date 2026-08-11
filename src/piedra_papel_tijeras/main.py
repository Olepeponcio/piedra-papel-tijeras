from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.services.partida import Partida
from piedra_papel_tijeras.gui.ventana_de_juego import VentanaDeJuego


def solicitar_tipo(nombre: str) -> TipoJugada:
    """Solicita por consola un tipo de jugada válido."""
    while True:
        entrada = (
            input(f"{nombre}, elige piedra, papel o tijeras: ").strip().capitalize()
        )

        try:
            return TipoJugada(entrada)
        except ValueError:
            print("Elección no válida. Debes introducir piedra, papel o tijeras.")


def main_consola() -> None:
    """Ejecuta una ronda mediante la interfaz histórica de consola."""
    nombre = input("Introduce tu nombre: ").strip() or "Jugador"
    jugador_humano = JugadorHumano(nombre)
    jugador_humano.seleccionar_tipo(solicitar_tipo(nombre))
    jugador_maquina = JugadorMaquina()
    partida = Partida(jugador_humano, jugador_maquina)

    resultado = partida.jugar()
    print(f"Resultado: {resultado}")
    input("Pulsa Enter para cerrar...")


def main_PySide6() -> None:
    # Crear QApplication
    # Crear objetos jugador y maquina
    jugador_humano = JugadorHumano()
    jugador_maquina = JugadorMaquina()

    # crear el objeto partida
    partida = Partida(jugador_humano, jugador_maquina)

    # crear la ventana
    # ventana = VentanaDeJuego(jugador_humano = jugador_humano, partida= partida)


def main() -> None:
    """Mantiene la consola como entrada activa durante la migración a PySide6."""
    main_consola()


if __name__ == "__main__":
    main()
