import cv2
from PyQt5.QtGui import QImage, QPixmap

def cv_to_pixmap(frame):
    """Convert an OpenCV BGR image to QPixmap."""
    if frame is None:
        return QPixmap()

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)
