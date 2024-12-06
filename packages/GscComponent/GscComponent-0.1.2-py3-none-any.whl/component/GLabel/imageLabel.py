from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QWidget

from component.GLabel.generalLabel import GeneralLabel
from utils import get_image_path


class ImageLabel(GeneralLabel):
    def __init__(self, image_path: Optional[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_path: Optional[str] = None

        self.set_image(image_path)

    def set_image(self, image_path: Optional[str]):
        # 验证图片路径
        validated_path = get_image_path(image_path)

        if validated_path == 'path is invalid':
            self.image_path = None
            self.set_style(border_color='#FF0000', border_width=2)  # 设置错误样式

            self.clear()    # 清空当前显示的图片
        else:
            self.image_path = validated_path
            self.set_style(border_color="#F0F0F0", border_width=0)  # 恢复样式

            self.update_pixmap()

    def update_pixmap(self) -> None:
        """
        根据当前控件大小调整并显示图片。
        """
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.size(),
                    aspectRatioMode=Qt.KeepAspectRatio,
                    transformMode=Qt.SmoothTransformation,
                )
                self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        在控件大小发生变化时，重新调整图片大小。
        """
        super().resizeEvent(event)
        self.update_pixmap()