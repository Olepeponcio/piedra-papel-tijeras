import pytest

from piedra_papel_tijeras.models.resultado import Resultado


@pytest.mark.parametrize(
    ("resultado", "texto"),
    [
        (Resultado.VICTORIA, "Victoria"),
        (Resultado.DERROTA, "Derrota"),
        (Resultado.EMPATE, "Empate"),
    ],
)
def test_resultado_conserva_su_texto(resultado: Resultado, texto: str) -> None:
    assert resultado.value == texto
    assert str(resultado) == texto
