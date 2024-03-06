"""Code for the main window containing all the frames and menus of the GUI."""

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QImage, QMouseEvent, QPainter, QPixmap, QResizeEvent
from PySide6.QtWidgets import QLabel, QMainWindow, QSizeGrip


class MainWindow(QMainWindow):
    """Main window containing the image selection and visualisation."""

    def __init__(self) -> None:
        """Initialise the main window."""
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        image = QImage()
        image.load("test.jpg")
        image = image.convertToFormat(QImage.Format.Format_ARGB32)

        newImg = QImage(image.size(), QImage.Format.Format_ARGB32)
        newImg.fill(Qt.GlobalColor.transparent)
        painter = QPainter(newImg)

        painter.setOpacity(0.5)
        painter.drawImage(QRect(0, 0, image.width(), image.height()), image)
        painter.end()

        pixmap = QPixmap(newImg)
        pixmap = pixmap.scaledToHeight(300, Qt.TransformationMode.SmoothTransformation)

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        self.setCentralWidget(label)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle the resize event."""
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse press event."""
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse move event."""
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
