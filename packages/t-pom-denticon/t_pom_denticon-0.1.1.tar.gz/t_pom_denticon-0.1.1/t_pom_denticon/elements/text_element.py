"""TextElement element module."""
from t_page_object.base_element import BaseElement


class TextElement(BaseElement):
    """Class for TextElement element model."""

    def get_element_text(self) -> str:
        """Get Element value."""
        text = self.find_element().text
        return text
