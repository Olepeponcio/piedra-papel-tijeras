from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
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
        self._jugada_actual: TipoJugada | None = None

        # imagenes permanecerán en el contenedor superpuestas y ocultas hasta evento
        self.imagen_jugador_humano: QLabel | None = None
        self.imagen_jugador_maquina: QLabel | None = None
        self.imagen_resultado_jugada: QLabel | None = None

        # ejecutar la cascada de funciones
        self._crear_componentes()
        self._crear_layouts()
        self._conectar_eventos()
        self._configurar_estado_inicial()

    def _crear_componentes(self) -> None:
        """creacion de los distintos componentes"""

        # declarar los botones, activar setCheckable
        self.piedra_btn = QPushButton("Piedra")
        self.piedra_btn.setCheckable(True)

        self.papel_btn = QPushButton("Papel")
        self.papel_btn.setCheckable(True)

        self.tijeras_btn = QPushButton("Tijeras")
        self.tijeras_btn.setCheckable(True)

        # agrupar los botones
        self.grupo_jugadas = QButtonGroup()
        self.grupo_jugadas.addButton(self.piedra_btn)
        self.grupo_jugadas.addButton(self.papel_btn)
        self.grupo_jugadas.addButton(self.tijeras_btn)
        # definir que solo un boton del grupo esté activado
        self.grupo_jugadas.setExclusive(True)

        self.bo_btn = QPushButton("bo!")
        self.bo_btn.setCheckable(False)
        self.bo_btn.setEnabled(False)

        # inicializar las imagenes y añadir ruta
        self.imagen_jugador_humano = QLabel()
        self.imagen_jugador_humano.setPixmap(
            "src\piedra_papel_tijeras\resources\btn_piedra.png"
        )
        self.imagen_jugador_maquina = QLabel()
        self.imagen_resultado_jugada = QLabel()

    def _crear_layouts(self) -> None:
        """crea ventana principal y anida ventanas para albergar
        los componentes"""

        # 1. Widget central del QMainWindow
        self.widget_central = QWidget()

        # 2. Layout principal
        self.layout_principal = QVBoxLayout()

        # 3. Layouts secundarios
        self.layout_jugador_humano = QHBoxLayout()
        self.layout_jugador_maquina = QHBoxLayout()
        self.layout_resultado_jugada = QHBoxLayout()
        
        #un layout que anide jugador_humano, jugador_maquina y resultado_jugada
        self.layout_jugadas = QHBoxLayout()
        
        
        self.layout_botones_jugadas = QHBoxLayout()
        self.layout_boton_bo = QHBoxLayout()

        # 4. Añadir componentes a layouts secundarios
        self.layout_botones_jugadas.addWidget(self.piedra_btn)
        self.layout_botones_jugadas.addWidget(self.papel_btn)
        self.layout_botones_jugadas.addWidget(self.tijeras_btn)
        self.layout_boton_bo.addWidget(self.bo_btn)

        # 5. Anidar layouts
        self.layout_jugadas.addLayout(self.layout_jugador_humano)
        self.layout_jugadas.addLayout(self.layout_jugador_maquina)
        self.layout_jugadas.addLayout(self.layout_resultado_jugada)
        
        # self.layout_principal.addLayout(self.layout_jugador_humano)
        # self.layout_principal.addLayout(self.layout_jugador_maquina)
        self.layout_principal.addLayout(self.layout_jugadas)
        # self.layout_principal.addLayout(self.layout_resultado_jugada)
        self.layout_principal.addLayout(self.layout_botones_jugadas)
        self.layout_principal.addLayout(self.layout_boton_bo)

        # 6. Layout principal → QWidget
        self.widget_central.setLayout(self.layout_principal)

        # 7. QWidget → QMainWindow
        self.setCentralWidget(self.widget_central)

    def _conectar_eventos(self) -> None:
        """genera todos los eventos disparados por los botones"""
        # seleccion de jugada mediante boton
        # si btn jugada está presionado, y se pulsa btn bo! descubrir imagen correspondiente a tipoJugada
        self.piedra_btn.clicked.connect(
            lambda: self._seleccion_jugada(TipoJugada.PIEDRA)
        )
        self.papel_btn.clicked.connect(lambda: self._seleccion_jugada(TipoJugada.PAPEL))

        self.tijeras_btn.clicked.connect(
            lambda: self._seleccion_jugada(TipoJugada.TIJERAS)
        )

        self.bo_btn.clicked.connect(lambda: self._ejectuar_ronda())

    def _configurar_estado_inicial(self) -> None:
        """prepara el entorno de juego"""

        # ocultar imagenes
        # self.imagen_jugador_humano.hide()

        # marcar botones como

    def _mostrar_imagen(self, jugada: str) -> None:
        pass

    def _ejectuar_ronda(self) -> None:
        #Validar que existe jugada humana
        #desactivar botones
        #solicitar ronda a Partida
        #mostrar jugada humana
        #mostrar jugada maquina
        #Programar presentacion resultado
        

    def _seleccion_jugada(self, tipo_jugada: TipoJugada) -> None:
        """Asigna valor al atributo y activa el botón bo!"""

        self._jugada_actual = tipo_jugada
        self.bo_btn.setEnabled(True)
        self.bo_btn.setCheckable(True)
