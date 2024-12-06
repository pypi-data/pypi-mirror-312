import ctypes
from typing import Optional, Tuple

from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget

from utils import get_image_path


class GPageWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, geometry: Optional[Tuple[int, int, int, int]] = None,
                 is_center: bool = True, is_max: bool = True, bd_color: Optional[str] = None,
                 icon_path: Optional[str] = None, title: Optional[str] = None, is_resize: bool = False) -> None:
        super().__init__(parent)

        self.parent = parent

        # 初始化几何参数
        self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry or (800, 600, 0, 0)

        self.set_geometry(geometry, is_center, is_max)      # 设置窗口几何
        self.set_icon(icon_path)    # 设置图标
        self.set_title(title)       # 设置标题
        self.set_attribute(is_resize=is_resize, bd_color=bd_color)      # 设置属性

    def set_geometry(self, geometry: Tuple[int, int, int, int] = None, is_center: bool = True,
                     is_max: bool = True) -> None:
        def get_screen_size_with_taskbar() -> Tuple[int, int]:
            """
            获取屏幕尺寸并减去任务栏高度。
            """
            user32 = ctypes.windll.user32
            _screen_width = user32.GetSystemMetrics(0)  # 屏幕宽度
            _screen_height = user32.GetSystemMetrics(1)  # 屏幕高度

            # 获取任务栏高度
            taskbar_handle = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)

            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                            ("top", ctypes.c_long),
                            ("right", ctypes.c_long),
                            ("bottom", ctypes.c_long)]

            rect = RECT()
            ctypes.windll.user32.GetWindowRect(taskbar_handle, ctypes.byref(rect))
            taskbar_height = rect.bottom - rect.top

            return _screen_width, _screen_height - taskbar_height

        if is_max:
            # 获取屏幕大小并减去任务栏高度
            screen_width, screen_height = get_screen_size_with_taskbar()
            self.gWidth = screen_width
            self.gHeight = screen_height
            self.gLT_x = 0
            self.gLT_y = 0
        elif is_center:
            # 获取屏幕大小
            screen_width, screen_height = get_screen_size_with_taskbar()

            # 计算居中位置
            self.gWidth, self.gHeight = geometry[:2] if geometry else (self.gWidth, self.gHeight)
            self.gLT_x = (screen_width - self.gWidth) // 2
            self.gLT_y = (screen_height - self.gHeight) // 2
        elif geometry:
            # 使用提供的 geometry 参数
            self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry

        self.setGeometry(self.gLT_x, self.gLT_y, self.gWidth, self.gHeight)

    def set_icon(self, icon_path: Optional[str] = None) -> None:
        if icon_path:
            self.setWindowIcon(QIcon(get_image_path(icon_path)))

    def set_title(self, title: Optional[str] = None) -> None:
        self.setWindowTitle(title if title else 'Default Title')

    def set_attribute(self, is_resize: Optional[bool] = False, bd_color: Optional[str] = None) -> None:
        if not is_resize:
            self.resize(self.gWidth, self.gHeight)

        if bd_color:
            # 设置背景颜色
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(self.backgroundRole(), QColor(bd_color))
            self.setPalette(palette)
