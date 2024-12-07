"""Table element module."""
from selenium.webdriver.common.by import By
from t_page_object.base_element import BaseElement


class TableElement(BaseElement):
    """Class for table elements."""

    def get_table_data(self) -> dict:
        """Extracts data from an HTML table.

        This method locates table headers and body elements, then iterates over them to extract and structure the data
        into a dictionary.

        Returns:
            dict: A dictionary where each key is a table name and each value is another dictionary containing
            the column names and their respective values.
        """
        table_data: dict = {}
        t_headers = self.find_element().find_elements(By.XPATH, ".//thead")
        t_bodies = self.find_element().find_elements(By.XPATH, ".//tbody")
        for header, body in zip(t_headers, t_bodies):
            table_name = header.find_element(By.XPATH, ".//tr//th").text.strip()
            table_data[table_name] = {}
            for row in body.find_elements(By.XPATH, ".//tr"):
                column, column_value = row.find_elements(By.XPATH, ".//td")
                table_data[table_name][column.text.strip()] = column_value.text.strip()
        return table_data

    def get_summary_table_data(self) -> list:
        """Extracts and structures data from an HTML summary table into a list of dictionaries.

        This method locates the table headers and body rows, then iterates over them to extract the data.
        Each row of the table is represented as a dictionary.

        Returns:
            list: A list of dictionaries, where each dictionary represents a row in the table.
                Each dictionary key is a column header, and each value is the corresponding data
                from that column in the row.
        """
        table_data = []
        t_heads = self.find_element().find_elements(By.XPATH, ".//thead//tr//th")
        rows = self.find_element().find_elements(By.XPATH, ".//tbody//tr")
        for row in rows:
            row_data = {}
            t_data = row.find_elements(By.XPATH, ".//td")
            for header, data in zip(t_heads, t_data):
                row_data[header.text.strip()] = data.text.strip()
            table_data.append(row_data)

        return table_data
