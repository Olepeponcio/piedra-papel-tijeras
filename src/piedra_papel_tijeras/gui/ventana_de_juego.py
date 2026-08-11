from pathlib import Path
from typing import ClassVar

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.resultado import Resultado
from piedra_papel_tijeras.models.resultado_ronda import ResultadoDeLaRonda
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.services.partida import Partida


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

    _ARCHIVOS_JUGADA: ClassVar[dict[TipoJugada, str]] = {
        TipoJugada.PIEDRA: "jugada_piedra.png",
        TipoJugada.PAPEL: "jugada_papel.png",
        TipoJugada.TIJERAS: "jugada_tijeras.png",
    }

    _ARCHIVOS_RESULTADO: ClassVar[dict[Resultado, str]] = {
        Resultado.VICTORIA: "resultado_victoria.png",
        Resultado.DERROTA: "resultado_derrota.png",
        Resultado.EMPATE: "resultado_empate.png",
    }

    def __init__(self, jugador_humano: JugadorHumano, partida: Partida) -> None:
        super().__init__()

        # definir el directorio de recursos
        self._directorio_recursos = Path(__file__).resolve().parents[1] / "resources"

        # definir los objetos que interactuaran con los eventos
        self._jugador_humano = jugador_humano
        self._partida = partida

        # variable para alberga estado de la ronda
        self._resultado_ronda_actual: ResultadoDeLaRonda | None = None

        # configuracion nombre y tam de la ventana
        self.setWindowTitle("Piedra, papel o tijeras")
        self.resize(600, 480)

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

        # definir tam por defecto del contenedor vacio
        self._imagen_jugador_humano.setFixedSize(180, 180)
        self._imagen_jugador_maquina.setFixedSize(180, 180)
        self._imagen_resultado_jugada.setFixedSize(90, 90)

        # centrar el contenido
        self._imagen_jugador_humano.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._imagen_jugador_maquina.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._imagen_resultado_jugada.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
            lambda: self._seleccionar_jugada(TipoJugada.PIEDRA)
        )
        self.papel_btn.clicked.connect(
            lambda checked=False: self._seleccionar_jugada(TipoJugada.PAPEL)
        )

        self.tijeras_btn.clicked.connect(
            lambda checked=False: self._seleccionar_jugada(TipoJugada.TIJERAS)
        )

        self.bo_btn.clicked.connect(self._ejecutar_ronda)

    def _configurar_estado_inicial(self) -> None:
        """prepara el entorno de juego"""

        # mantenter el contenedor vacio hasta que se asigne una imagen
        self._imagen_jugador_humano.clear()
        self._imagen_jugador_maquina.clear()
        self._imagen_resultado_jugada.clear()

        # configurar boton bo!
        self.bo_btn.setEnabled(False)

    def _mostrar_jugada(
        self,
        tipo_jugada: TipoJugada,
        contenedor: QLabel,
    ) -> None:
        nombre_archivo = self._ARCHIVOS_JUGADA[tipo_jugada]
        ruta_imagen = self._directorio_recursos / nombre_archivo

        imagen = QPixmap(str(ruta_imagen))

        if imagen.isNull():
            raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta_imagen}")

        # ajustar imagen. escalar imagen. cambiar tamaño imagen.
        imagen_ajustada = imagen.scaled(
            contenedor.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        contenedor.setPixmap(imagen_ajustada)

    def _mostrar_resultado(self) -> None:
        """asigna valor de QPixmap la variable imagen carga la imagen usando la
        ruta de _directorio_recursos / _ARCHIVOS_RESULTADO [value del diccionario],
        escala la imagen al contenedor para configurar al atributo QPixmap de clase _imagen_resultado_jugada.
        vuelve a liberar los botones de jugada
        """
        # si aún no ha habido ronda
        if self._resultado_ronda_actual is None:
            return

        # recuperamos el valor del objeto tipo ResultadoDeLaRonda
        resultado = self._resultado_ronda_actual.resultado

        # asignamos como valor .value del diccionario
        nombre_archivo = self._ARCHIVOS_RESULTADO[resultado]

        # recuperamos la ruta a resources desde variable interna
        ruta_imagen = self._directorio_recursos / nombre_archivo

        # creamos la imagen
        imagen = QPixmap(str(ruta_imagen))

        # comprobar que la variable del tipo no arroje error
        if imagen.isNull():
            raise FileNotFoundError(f"No se pudo cargar la imagen {ruta_imagen}")

        imagen_ajustada = imagen.scaled(
            self._imagen_resultado_jugada.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # asignar el valor de la configuración al atributo de clase del tipo QPixmap
        self._imagen_resultado_jugada.setPixmap(imagen_ajustada)

        # preparar los componentes para la siguiente ronda
        self._preparar_seleccion_siguiente_ronda()

    def _ejecutar_ronda(self) -> None:
        """Asigna valor al atributo invocando el metodo jugar de partida. Muestra las jugadas de los actores y el resultado
        con retardo invocando al metodo de clase _mostrar_jugada y _mostrar_resultado respectivamente
        """
        self._resultado_ronda_actual = self._partida.jugar()

        self._mostrar_jugada(
            self._resultado_ronda_actual.jugada_humana.tipo,
            self._imagen_jugador_humano,
        )

        self._mostrar_jugada(
            self._resultado_ronda_actual.jugada_maquina.tipo,
            self._imagen_jugador_maquina,
        )

        # preparar el evento retardado para mostrar resultado
        self._imagen_resultado_jugada.clear()

        # desactivar temporalmente los botones
        self.piedra_btn.setEnabled(False)
        self.papel_btn.setEnabled(False)
        self.tijeras_btn.setEnabled(False)
        self.bo_btn.setEnabled(False)

        # retardo de 1500 ms para invocar el metodo que renderiza el resultado
        QTimer.singleShot(1500, self._mostrar_resultado)

    def _seleccionar_jugada(self, tipo_jugada: TipoJugada) -> None:
        """Asigna valor al atributo y activa el botón bo!"""

        if self._resultado_ronda_actual is not None:
            self._imagen_jugador_humano.clear()
            self._imagen_jugador_maquina.clear()
            self._imagen_resultado_jugada.clear()
            self._resultado_ronda_actual = None

        # selecciona
        self._jugador_humano.registrar_seleccion(tipo_jugada)
        self.bo_btn.setEnabled(True)

    def _preparar_seleccion_siguiente_ronda(self) -> None:
        self.grupo_jugadas.setExclusive(False)

        self.piedra_btn.setChecked(False)
        self.papel_btn.setChecked(False)
        self.tijeras_btn.setChecked(False)

        self.grupo_jugadas.setExclusive(True)

        self.piedra_btn.setEnabled(True)
        self.papel_btn.setEnabled(True)
        self.tijeras_btn.setEnabled(True)

        self.bo_btn.setEnabled(False)
