"""Table Row element module."""

from t_page_object.base_element import BaseElement


class TableRowElement(BaseElement):
    """Class for TextElement element model."""

    def get_row_values(self) -> list[str]:
        """Get Element value."""
        row_cells = self.find_elements()
        return [cell.text for cell in row_cells]
