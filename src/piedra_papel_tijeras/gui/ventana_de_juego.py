from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class VentanaDeJuego(QMainWindow):
    """Ventana principal de la aplicacion"""

    def __init__(self) -> None:
        super().__init__()

        # configuracion nombre y tam de la ventana
        self.setWindowTitle("Piedra, papel o tijeras")
        self.resize(600, 480)

        # jugada actual de la partida
        self._jugada_actual: TipoJugada

        # imagenes permanecerán en el contenedor superpuestas y ocultas hasta evento
        self.imagen_jugador_humano = ""
        self.imagen_jugador_maquina = ""
        self.imagen_resultado_jugada = ""

        # ejecutar la cascada de funciones
        self._crear_componentes()
        self._crear_layouts()
        self._conectar_eventos()
        self._configurar_estado_inicial()

    def _crear_componentes(self) -> None:
        """creacion de los distintos componentes"""

        self.piedra_btn = QPushButton(self._seleccion_jugada("Piedra"))
        self.papel_btn = QPushButton(self._seleccion_jugada("Papel"))
        self.tijeras_btn = QPushButton(self._seleccion_jugada("Tijeras"))
        self.bo_btn = QPushButton("bo!")

    def _seleccion_jugada(self, jugada: str) -> None:
        self._jugada_actual = TipoJugada(jugada)

    def _crear_layouts(self) -> None:
        """crea ventana principal y anida ventanas para albergar
        los componentes"""

        # 1. Widget central del QMainWindow
        self.widget_central = QWidget()

        # 2. Layout principal
        self.layout_principal = QVBoxLayout()

        # 3. Layouts secundarios
        self.layout_jugador_humano = QVBoxLayout()
        self.layout_jugador_maquina = QVBoxLayout()
        self.layout_resultado_jugada = QVBoxLayout()
        self.layout_botones_jugadas = QHBoxLayout()
        self.layout_boton_bo = QVBoxLayout()

        # 4. Añadir componentes a layouts secundarios
        self.layout_botones_jugadas.addWidget(self.piedra_btn)
        self.layout_botones_jugadas.addWidget(self.papel_btn)
        self.layout_botones_jugadas.addWidget(self.tijeras_btn)
        self.layout_boton_bo.addWidget(self.bo_btn)

        # 5. Anidar layouts
        self.layout_principal.addChildLayout(self.layout_jugador_humano)
        self.layout_principal.addChildLayout(self.layout_jugador_maquina)
        self.layout_principal.addChildLayout(self.layout_resultado_jugada)
        self.layout_principal.addChildLayout(self.layout_botones_jugadas)
        self.layout_principal.addChildLayout(self.layout_boton_bo)

        # 6. Layout principal → QWidget
        self.widget_central.setLayout(self.layout_principal)

        # 7. QWidget → QMainWindow
        self.setCentralWidget(self.widget_central)

    def _conectar_eventos(self) -> None:
        """genera todos los eventos disparados por los botones"""
        # seleccion de jugada mediante boton
        # si btn jugada está presionado, y se pulsa btn bo! descubrir imagen correspondiente a tipoJugada
        self.bo_btn.clicked.connect(self._mostrar_imagen)
        pass

    def _configurar_estado_inicial(self) -> None:
        """prepara el entorno de juego"""
        pass

    def _mostrar_imagen(self, jugada: str) -> None:
        pass
