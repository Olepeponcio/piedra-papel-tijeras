from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Piedra, papel o tijeras")
        self.resize(600, 480)

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        """Crea y distribuye los componentes visuales."""

        # self.etiqueta_mensaje = QLabel("Ventana preparada")
        self.boton_prueba = QPushButton("Probar evento")

        self.boton_prueba.clicked.connect(self._mostrar_mensaje)

        layout_principal = QVBoxLayout()
        # layout_principal.addWidget(self.etiqueta_mensaje)
        layout_principal.addWidget(self.boton_prueba)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)

        self.setCentralWidget(contenedor)

    @Slot()
    def _mostrar_mensaje(self) -> None:
        """Responde a la pulsación del botón."""

        self.etiqueta_mensaje.setText("El botón funciona correctamente")
