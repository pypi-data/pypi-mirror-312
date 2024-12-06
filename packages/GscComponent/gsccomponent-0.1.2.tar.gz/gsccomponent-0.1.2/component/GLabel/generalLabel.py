from typing import Optional, Tuple

from PyQt5.QtWidgets import QLabel, QWidget


class GeneralLabel(QLabel):
    def __init__(self, parent: Optional[QWidget] = None, geometry: Optional[Tuple[int, int, int, int]] = None,
                 bd_color: str = "#F0F0F0",
                 border_color: str = "#F0F0F0",
                 border_width: int = 0,
                 border_radius: int = 0,
                 border_style: str = "solid"
                 ):
        super().__init__(parent)

        self.parent = parent

        self.bd_color = bd_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_style = border_style

        # 初始化几何和样式参数
        self.geometry_defined = geometry is not None
        self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry or (100, 25, 0, 0)

        self.set_geometry(geometry)
        self.apply_styles()

    def set_geometry(self, geometry: Tuple[int, int, int, int]) -> None:
        if geometry:
            self.gWidth, self.gHeight, self.gLT_x, self.gLT_y = geometry
            self.geometry_defined = True
        else:
            self.geometry_defined = False

        self.setGeometry(self.gLT_x, self.gLT_y, self.gWidth, self.gHeight)

    def set_style(self,
                  bd_color: Optional[str] = None,
                  border_color: Optional[str] = None,
                  border_width: Optional[int] = None,
                  border_radius: Optional[int] = None,
                  border_style: Optional[str] = None,) -> None:
        """
        更新样式参数，并重新应用样式。
        """
        updated = False
        if bd_color is not None and bd_color != self.bd_color:
            self.bd_color = bd_color
            updated = True
        if border_color is not None and border_color != self.border_color:
            self.border_color = border_color
            updated = True
        if border_width is not None and border_width != self.border_width:
            self.border_width = border_width
            updated = True
        if border_radius is not None and border_radius != self.border_radius:
            self.border_radius = border_radius
            updated = True
        if border_style is not None and border_style != self.border_style:
            self.border_style = border_style
            updated = True

        if updated:
            self.apply_styles()

    def apply_styles(self) -> None:
        """
        根据当前的样式参数生成并应用样式表。
        如果几何信息未定义，边框颜色设置为红色。
        """
        effective_border_color = "#FF0000" if not self.geometry_defined else self.border_color
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.bd_color};
                border: {self.border_width}px {self.border_style} {effective_border_color};
                border-radius: {self.border_radius}px;
            }}
        """)
