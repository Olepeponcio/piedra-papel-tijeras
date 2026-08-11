import sys

from PySide6.QtWidgets import QApplication

from piedra_papel_tijeras.gui.ventana_de_juego import VentanaDeJuego
from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.services.partida import Partida


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
    jugador_humano.registrar_seleccion(solicitar_tipo(nombre))
    jugador_maquina = JugadorMaquina()
    partida = Partida(jugador_humano, jugador_maquina)

    resultado = partida.jugar()
    print(f"Resultado: {resultado}")
    input("Pulsa Enter para cerrar...")


def main_pyside6() -> None:
    """inicia la interfaz grafica de la aplicacion"""
    # Crear QApplication
    aplicacion = QApplication(sys.argv)

    # Crear objetos jugador y maquina
    jugador_humano = JugadorHumano()
    jugador_maquina = JugadorMaquina()

    # crear el objeto partida
    partida = Partida(jugador_humano, jugador_maquina)

    # inyecta JugadorHumano y Partida en VentanaDeJuego
    ventana = VentanaDeJuego(jugador_humano, partida)
    # mostrar la interfaz
    ventana.show()

    # iniciar el ciclo de eventos: clics, teclado, temporizadores y cierre
    codigo_salida = aplicacion.exec()

    # comunica al SO como terminó
    sys.exit(codigo_salida)


def main() -> None:
    """ejecuta la interfaz en versiones: CLI, GUI."""
    # main_consola()
    main_pyside6()


if __name__ == "__main__":
    main()
