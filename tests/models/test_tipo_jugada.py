from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


# El enumerado define los tipos piedra, papel y tijeras.
def test_clase_enum_define_tipos_piedra_papel_tijeras() -> None:
    assert set(TipoJugada) == {TipoJugada.PIEDRA, TipoJugada.PAPEL, TipoJugada.TIJERAS}
