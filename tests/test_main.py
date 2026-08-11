import pytest

from piedra_papel_tijeras.main import solicitar_tipo
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


def test_solicitar_tipo_normaliza_la_entrada(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "  pApEl  ")

    resultado = solicitar_tipo("Ana")

    assert resultado is TipoJugada.PAPEL


def test_solicitar_tipo_repite_tras_una_entrada_invalida(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    entradas = iter(["lagarto", "tijeras"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = solicitar_tipo("Ana")

    assert resultado is TipoJugada.TIJERAS
    assert "Elección no válida" in capsys.readouterr().out


# def test_main_consola_ejecuta_una_partida_completa(
#     monkeypatch: pytest.MonkeyPatch,
#     capsys: pytest.CaptureFixture[str],
# ) -> None:
#     entradas = iter(["Ana", "piedra", ""])
#     monkeypatch.setattr("builtins.input", lambda _: next(entradas))
#     monkeypatch.setattr(
#         JugadorMaquina,
#         "_seleccionar_tipo",
#         lambda _: TipoJugada.TIJERAS,
#     )

#     main_consola()

#     assert "Resultado: Victoria" in capsys.readouterr().out
