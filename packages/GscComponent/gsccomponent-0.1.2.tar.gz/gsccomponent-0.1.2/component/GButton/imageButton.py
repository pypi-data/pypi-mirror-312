from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from component.GButton.generalButton import GeneralButton
from utils import get_image_path


class ImageButton(GeneralButton):
    def __init__(self,image_path: Optional[str] = None, is_check_button: bool = False,):
        super().__init__()

        self.leave_image_path: Optional[str] = None
        self.hover_image_path: Optional[str] = None
        self.unable_image_path: Optional[str] = None

        # 是否为切换按钮
        self.is_check_button: bool = is_check_button
        self.is_checked: bool = False

        self.set_image_path(image_path)
        self.set_default_image()  # 设置初始图像

    def set_image_path(self, image_path: Optional[str] = None):
        """
        设置按钮的图像路径，并生成其他状态的图像路径（悬停、不可用）。
        如果图像路径无效，清空所有图像路径。
        """
        validated_path = get_image_path(image_path)
        if validated_path == 'path is invalid':
            self.leave_image_path = None
            self.hover_image_path = None
            self.unable_image_path = None
        else:
            base_path, ext = validated_path.rsplit('.', 1)
            self.leave_image_path = validated_path
            self.hover_image_path = f"{base_path}_hover.{ext}"
            self.unable_image_path = f"{base_path}_unable.{ext}"

    def set_image(self, image_path: Optional[str] = None):
        """
        根据指定的图像路径设置按钮的图标。
        如果路径无效，不设置图像。
        """
        if not image_path or image_path == 'path is invalid':
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return  # 无效图像，直接返回

        pixmap = pixmap.scaled(
            self.size(),
            aspectRatioMode=Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation
        )
        self.setIcon(QIcon(pixmap))
        self.setIconSize(self.size())

    def update_image(self) -> None:
        """
        根据按钮状态更新图像。
        """
        if not self.isEnabled() and self.unable_image_path:
            self.set_image(self.unable_image_path)
        elif self.is_checked and self.hover_image_path:
            self.set_image(self.hover_image_path)
        elif self.leave_image_path:
            self.set_image(self.leave_image_path)

    def enterEvent(self, event) -> None:
        """
        鼠标进入按钮区域时切换到悬停状态图像。
        """
        if self.isEnabled() and not self.is_checked and self.hover_image_path:
            self.set_image(self.hover_image_path)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """
        鼠标离开按钮区域时，如果是切换按钮且已按下，不恢复默认图像。
        """
        if self.isEnabled() and (not self.is_check_button or not self.is_checked):
            self.update_image()
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        """
        鼠标点击时，切换按钮状态（如果是切换按钮）。
        """
        if self.is_check_button:
            if not self.is_checked:
                self.is_checked = True
                self.setEnabled(False)  # 禁用按钮点击
                self.update_image()
        else:
            super().mousePressEvent(event)

    def reset_state(self) -> None:
        """
        手动恢复按钮状态，用于切换按钮的重置。
        """
        self.is_checked = False
        self.setEnabled(True)
        self.update_image()

    def setEnabled(self, enabled: bool) -> None:
        """
        重写 setEnabled 方法，处理不可用状态图像。
        """
        super().setEnabled(enabled)
        self.update_image()