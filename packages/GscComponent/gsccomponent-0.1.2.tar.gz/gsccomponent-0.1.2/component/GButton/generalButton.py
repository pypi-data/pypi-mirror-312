from typing import Optional, Tuple

from PyQt5.QtWidgets import QPushButton, QWidget


class GeneralButton(QPushButton):
    def __init__(self, parent: Optional[QWidget] = None, geometry: Optional[Tuple[int, int, int, int]] = None,
                 tooltip: Optional[str] = None, is_show: bool = True, is_enabled: bool = True,
                 click_command: Optional[callable] = None) -> None:
        super().__init__(parent)

        self.parent = parent

        # 初始化几何和样式参数
        self.geometry_defined = geometry is not None
        self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry or (200, 40, 0, 0)

        self.tooltip: Optional[str] = tooltip
        self.is_show = is_show
        self.is_enabled = is_enabled

        self.set_geometry(geometry)
        self.apply_button_state()
        self.set_tooltip(tooltip)
        self.set_click_command(click_command)

    def set_geometry(self, geometry: Tuple[int, int, int, int] = None) -> None:
        """
        设置几何信息。如果未提供几何信息，则标记为未定义。
        """
        if geometry:
            self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry
            self.geometry_defined = True
        else:
            self.geometry_defined = False

        self.setGeometry(self.gLT_x, self.gLT_y, self.gWidth, self.gHeight)

    def update_state(self, is_show: Optional[bool] = None, is_enabled: Optional[bool] = None) -> None:
        """
        更新按键状态，包括是否可见、是否可用。
        """
        if is_show is not None:
            self.is_show = is_show
        if is_enabled is not None:
            self.is_enabled = is_enabled

        self.apply_button_state()

    def apply_button_state(self) -> None:
        """
        应用按钮的显示和可用状态
        """
        self.setVisible(self.is_show)
        self.setEnabled(self.is_enabled)

    def set_tooltip(self, tooltip: Optional[str] = None) -> None:
        """
        设置按钮的工具提示。
        """
        self.tooltip = tooltip
        if self.tooltip:
            self.setToolTip(self.tooltip)

    def set_click_command(self, click_command: Optional[callable] = None) -> None:
        """
        设置按钮的点击事件处理函数。
        """
        if click_command:
            self.clicked.connect(click_command)