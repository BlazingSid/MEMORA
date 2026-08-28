from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect

from app.styles.colors import SHADOW, SHADOW_ALPHA


def apply_soft_shadow(widget, blur_radius=24, offset_y=7):
    """Add the restrained elevation used by primary shell surfaces."""

    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setOffset(0, offset_y)

    color = QColor(SHADOW)
    color.setAlpha(SHADOW_ALPHA)
    shadow.setColor(color)

    widget.setGraphicsEffect(shadow)


class GlassCard(QFrame):
    """A soft, rounded content surface with an optional subtle shadow."""

    def __init__(self, parent=None, elevated=False):
        super().__init__(parent)

        self.setObjectName("GlassCard")
        self.setProperty("elevated", elevated)

        if elevated:
            apply_soft_shadow(self)
