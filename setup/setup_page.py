class SetupPage:
    def __init__(self, path_to_html: str, path_to_css: str):
        self.path_to_html = path_to_html
        self.path_to_css = path_to_css

    def _load_page(self) -> str:
        with open(self.path_to_html, "r") as f:
            page = f.read()
        return page

    def _load_css(self) -> str:
        with open(self.path_to_css, "r") as f:
            css = f.read()
        return css

    def render(self, wifi_list: list) -> str:
        page = self._load_page()
        css = self._load_css()

        page = page.replace("{{CSS}}", f"<style>{css}</style>")
        options = "".join(
            f"<option value='{item["ssid"]}'>{item["ssid"]}</option>"
            for item in wifi_list
        )

        page = page.replace("{{OPTIONS}}", options)

        return page
