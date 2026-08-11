import sys

from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

from piedra_papel_tijeras.gui.ventana_principal import VentanaPrincipal

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


# def main() -> None:
#     """Ejecuta una ronda de piedra, papel o tijeras por consola."""
#     nombre = input("Introduce tu nombre: ").strip() or "Jugador"
#     jugador_humano = JugadorHumano(
#         nombre,
#         selector_tipo=lambda: solicitar_tipo(nombre),
#     )
#     jugador_maquina = JugadorMaquina()
#     partida = Partida(jugador_humano, jugador_maquina)

#     resultado = partida.jugar()
#     print(f"Resultado: {resultado}")
#     input("Pulsa Enter para cerrar...")


def main() -> None:
    """ejecuta la logica principal de la aplicación.
    interfaz principal con PySide6"""
    aplicacion = QApplication(sys.argv)

    ventana = QWidget()
    ventana.setWindowTitle("Ejemplo del ciclo de eventos")

    mensaje = QLabel("La aplicación está ejecutándose")
    boton_cerrar = QPushButton("Cerrar")

    # Cuando se pulse el botón, Qt terminará su ciclo de eventos.
    boton_cerrar.clicked.connect(aplicacion.quit)

    layout = QVBoxLayout()
    layout.addWidget(mensaje)
    layout.addWidget(boton_cerrar)

    ventana.setLayout(layout)
    ventana.show()

    print("Antes de exec(): comienza el ciclo de eventos")

    codigo_salida = aplicacion.exec()

    # Esta línea no se ejecuta hasta que la aplicación se cierre.
    print(f"Después de exec(): código recibido = {codigo_salida}")

    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()
