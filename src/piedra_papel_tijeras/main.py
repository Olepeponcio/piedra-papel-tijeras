from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.services.partida import Partida


def solicitar_tipo(nombre: str) -> TipoJugada:
    """Solicita por consola un tipo de jugada válido."""
    while True:
        entrada = input(
            f"{nombre}, elige piedra, papel o tijeras: "
        ).strip().capitalize()

        try:
            return TipoJugada(entrada)
        except ValueError:
            print("Elección no válida. Debes introducir piedra, papel o tijeras.")


def main() -> None:
    """Ejecuta una ronda de piedra, papel o tijeras por consola."""
    nombre = input("Introduce tu nombre: ").strip() or "Jugador"
    jugador_humano = JugadorHumano(
        nombre,
        selector_tipo=lambda: solicitar_tipo(nombre),
    )
    jugador_maquina = JugadorMaquina()
    partida = Partida(jugador_humano, jugador_maquina)

    resultado = partida.jugar()
    print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()
