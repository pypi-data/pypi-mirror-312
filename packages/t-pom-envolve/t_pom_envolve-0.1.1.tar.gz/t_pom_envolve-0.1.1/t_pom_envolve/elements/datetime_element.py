"""Datetime element module."""
from t_page_object.base_element import BaseElement


class DateTimeElement(BaseElement):
    """Class for Datetime element model."""

    def select_date(self, date: str) -> None:
        """Inputs a date into a date field."""
        self.input_text_when_element_is_visible(text=date)
