from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
)

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class VentanaDeJuego(QMainWindow):
    """Ventana principal de la aplicacion"""

    _ESTILO_BOTONES_JUGADA = """
      QPushButton {
          border: 2px solid transparent;
          border-radius: 8px;
          padding: 3px;
      }

      QPushButton:hover {
          background-color: #d8d8d8;
      }

      QPushButton:checked {
          background-color: #9aaa8c;
          border: 3px solid #607554;
      }
  """

    _ESTILO_BOTON_BO = """
      QPushButton {
          min-width: 100px;
          min-height: 52px;
          border: 2px solid #555555;
          border-radius: 10px;
          background-color: #707070;
          color: #bdbdbd;
          font-size: 22px;
          font-weight: bold;
      }

      QPushButton:enabled {
          background-color: #ff7a18;
          border-color: #ff9a4d;
          color: #ffffff;
      }

      QPushButton:enabled:hover {
          background-color: #ff9138;
          border-color: #ffc08a;
      }

      QPushButton:enabled:pressed {
          background-color: #d95c00;
          border-color: #ff7a18;
          padding-top: 3px;
          padding-left: 2px;
      }

      QPushButton:disabled {
          background-color: #4a4a4a;
          border-color: #606060;
          color: #858585;
      }
  """

    def __init__(self) -> None:
        super().__init__()

        # definir el directorio de recursos
        self._directorio_recursos = Path(__file__).resolve().parents[1] / "resources"

        # configuracion nombre y tam de la ventana
        self.setWindowTitle("Piedra, papel o tijeras")
        self.resize(600, 480)

        # jugada actual de la partida
        self._jugada_actual: TipoJugada | None = None

        # ejecutar la cascada de funciones
        self._crear_componentes()
        self._crear_layouts()
        self._conectar_eventos()
        self._configurar_estado_inicial()

    def _crear_componentes(self) -> None:
        """creacion de los distintos componentes"""

        # declarar los botones, configurarlos y aplicar estilo
        self.piedra_btn = QPushButton()
        self.piedra_btn.setIcon(
            QIcon(str(self._directorio_recursos / "btn_piedra.png"))
        )
        self.piedra_btn.setIconSize(QSize(90, 90))
        self.piedra_btn.setFixedSize(100, 100)
        self.piedra_btn.setCheckable(True)

        self.papel_btn = QPushButton()
        self.papel_btn.setIcon(QIcon(str(self._directorio_recursos / "btn_papel.png")))
        self.papel_btn.setIconSize(QSize(90, 90))
        self.papel_btn.setFixedSize(100, 100)
        self.papel_btn.setCheckable(True)

        self.tijeras_btn = QPushButton()
        self.tijeras_btn.setIcon(
            QIcon(str(self._directorio_recursos / "btn_tijeras.png"))
        )
        self.tijeras_btn.setIconSize(QSize(90, 90))
        self.tijeras_btn.setFixedSize(100, 100)
        self.tijeras_btn.setCheckable(True)

        self.bo_btn = QPushButton("bo!")
        self.bo_btn.setCheckable(False)
        self.bo_btn.setFixedSize(100, 100)

        # definir estilo botones
        self.piedra_btn.setStyleSheet(self._ESTILO_BOTONES_JUGADA)
        self.papel_btn.setStyleSheet(self._ESTILO_BOTONES_JUGADA)
        self.tijeras_btn.setStyleSheet(self._ESTILO_BOTONES_JUGADA)
        self.bo_btn.setStyleSheet(self._ESTILO_BOTON_BO)

        # agrupar los botones
        self.grupo_jugadas = QButtonGroup(self)
        self.grupo_jugadas.addButton(self.piedra_btn)
        self.grupo_jugadas.addButton(self.papel_btn)
        self.grupo_jugadas.addButton(self.tijeras_btn)
        # definir que solo un boton del grupo esté activado
        self.grupo_jugadas.setExclusive(True)

        # crear los componentes para renderizar las imagenes
        self._imagen_jugador_humano = QLabel()
        self._imagen_jugador_maquina = QLabel()
        self._imagen_resultado_jugada = QLabel()

        # crear los labels para los nombres
        self.nombre_jugador_humano = QLabel("Jugador")
        self.nombre_jugador_maquina = QLabel("Máquina")

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

        # un layout que anide jugador_humano, jugador_maquina y resultado_jugada
        self.layout_jugadas = QHBoxLayout()

        self.layout_botones_jugadas = QHBoxLayout()
        self.layout_boton_bo = QHBoxLayout()

        # 4. Añadir componentes a layouts secundarios
        self.layout_botones_jugadas.addWidget(
            self.piedra_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_botones_jugadas.addWidget(
            self.papel_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_botones_jugadas.addWidget(
            self.tijeras_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_boton_bo.addWidget(
            self.bo_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout_jugador_humano.addWidget(
            self.nombre_jugador_humano, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_jugador_humano.addWidget(
            self._imagen_jugador_humano, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout_jugador_maquina.addWidget(
            self.nombre_jugador_maquina, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_jugador_maquina.addWidget(
            self._imagen_jugador_maquina, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout_resultado_jugada.addWidget(
            self._imagen_resultado_jugada, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # 5. Anidar layouts
        self.layout_jugadas.addLayout(self.layout_jugador_humano)
        self.layout_jugadas.addLayout(self.layout_resultado_jugada)
        self.layout_jugadas.addLayout(self.layout_jugador_maquina)

        self.layout_principal.addLayout(self.layout_jugadas)
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

        # mantenter el contenedor vacio hasta que se asigne una imagen
        self._imagen_jugador_humano.clear()
        self._imagen_jugador_maquina.clear()
        self._imagen_resultado_jugada.clear()

        # configurar boton bo!
        self.bo_btn.setEnabled(False)

    def _seleccionar_y_mostrar_imagen(self, jugada: str) -> None:
        """selecciona la imagen según evento y muestra el objeto oculto"""
        pass

    def _ejectuar_ronda(self) -> None:
        # Validar que existe jugada humana
        # desactivar botones
        # solicitar ronda a Partida
        # mostrar jugada humana
        # mostrar jugada maquina
        # Programar presentacion resultado
        pass

    def _seleccion_jugada(self, tipo_jugada: TipoJugada) -> None:
        """Asigna valor al atributo y activa el botón bo!"""

        self._jugada_actual = tipo_jugada
        self.bo_btn.setEnabled(True)
