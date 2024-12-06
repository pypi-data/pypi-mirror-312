from typing import Optional

from PyQt5.QtCore import Qt

from component.GLabel.generalLabel import GeneralLabel


class TextLabel(GeneralLabel):
    def __init__(self, text: Optional[str] = None,
                 font_family: Optional[str] = 'Arial',
                 font_size: Optional[int] = 12,
                 font_color: Optional[str] = '#000000',
                 alignment: Optional[str] = 'center',
                 *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.text: Optional[str] = text
        self.font_family: Optional[str] = font_family
        self.font_size: Optional[int] = font_size
        self.font_color: Optional[str] = font_color
        self.alignment: Optional[str] = alignment

        # 设置初始文本样式和内容
        self.apply_text_styles()
        self.setText(self.text or "")
        
        # 设置对齐方式（如果未指定，则使用默认对齐）
        self.set_alignment(self.alignment or "center")

    def set_text(self, text: Optional[str]) -> None:
        """
        设置文本内容并更新显示。
        """
        self.text = text
        self.setText(self.text or "")
        self.update()

    def set_font(self, font_family: Optional[str] = None,
                 font_size: Optional[int] = None,
                 font_color: Optional[str] = None) -> None:
        """
        更新字体样式，包括字体类型、大小和颜色。
        """
        updated = False
        if font_family is not None and font_family != self.font_family:
            self.font_family = font_family
            updated = True
        if font_size is not None and font_size != self.font_size:
            self.font_size = font_size
            updated = True
        if font_color is not None and font_color != self.font_color:
            self.font_color = font_color
            updated = True

        if updated:
            self.apply_text_styles()

    def set_alignment(self, alignment: Optional[str]) -> None:
        """
        设置文本对齐方式。
        支持 "left", "right", "center", "justify"。
        """
        alignment_map = {
            "left": Qt.AlignLeft | Qt.AlignVCenter,
            "right": Qt.AlignRight | Qt.AlignVCenter,
            "center": Qt.AlignCenter,
            "justify": Qt.AlignJustify,
        }
        if alignment and alignment.lower() in alignment_map:
            self.alignment = alignment.lower()
            self.setAlignment(alignment_map[self.alignment])
        else:
            self.setAlignment(Qt.AlignCenter)

    def apply_text_styles(self) -> None:
        """
        应用字体样式，包括字体类型、大小、颜色等。
        """
        self.setStyleSheet(f"""
            QLabel {{
                font-family: {self.font_family};
                font-size: {self.font_size}px;
                color: {self.font_color};
            }}
        """)
