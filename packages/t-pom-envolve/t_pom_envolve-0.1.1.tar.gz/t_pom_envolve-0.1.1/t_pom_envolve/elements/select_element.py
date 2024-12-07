"""Select element module."""
from t_page_object.base_element import BaseElement


class SelectElement(BaseElement):
    """Class to Select element model."""

    def select_options(self, options: list[str]) -> None:
        """Selects a list of options from a dropdown menu."""
        for option in options:
            self.select_from_list_by_label(option)

    def get_selected_option(self) -> str:
        """Gets the selected option."""
        value = self.find_element().text
        return value
