import ure


class HTMLPreprocessor:
    """
    A class to preprocess HTML templates.
    This class is responsible for parsing and rendering HTML templates with dynamic content.
    Allows:
    - {{ variable }} syntax for dynamic content
    - {% if condition %} ... {% endif %} for conditional rendering
    - {% for item in list %} ... {% endfor %} for looping through lists
    - {% include "path/to/file %} for including other files
    """

    def __init__(self, template_str: str):
        self.template_str = template_str

    def render(self, context: dict) -> str:
        """
        Renders the template with the given context.
        :param context: A dictionary containing the context variables.
        :return: The rendered HTML string.
        """
        rendered_str = self.template_str
        # Include other files
        rendered_str = self._include_file(rendered_str)
        # Replace variables
        rendered_str = self._replace_variables(rendered_str, context)
        # Handle conditional rendering
        rendered_str = self._handle_conditionals(rendered_str, context)
        # Handle loops
        rendered_str = self._handle_loops(rendered_str, context)
        # Minify HTML
        rendered_str = self._minify_html(rendered_str)

        return rendered_str

    def _include_file(self, template: str) -> str:
        """
        Helper function to include other files in the template.
        :param template: The template string.
        :param context: The context dictionary.
        :return: The template string with included files.
        """
        include_placeholder = ure.compile(r"{%\s+include\s+\"(.+?)\"\s+%}")

        while include_placeholder.search(template):
            file_name = include_placeholder.search(template).group(1)
            try:
                with open(file_name, "r") as file:
                    included_content = file.read()
            except Exception as e:
                print(f"Error including file {file_name}: {e}")
                included_content = "Error including file"
            template = template.replace(
                include_placeholder.search(template).group(0), included_content
            )

        return template

    def _minify_html(self, html: str) -> str:
        """
        Minifies the HTML string by removing unnecessary whitespace and newlines.
        :param html: The HTML string to minify.
        :return: The minified HTML string.
        """
        # Remove comments
        html = ure.sub(r"<!--.*?-->", "", html)
        # Remove extra whitespace
        html = ure.sub(r"\s+", " ", html)
        # Remove leading and trailing whitespace
        html = html.strip()
        return html

    def _handle_loops(self, template: str, context) -> str:
        """
        Helper function to handle loops in the template.
        :param template: The template string.
        :param context: The context dictionary.
        :return: The template string with loops handled.
        """
        for for_obj in context.keys():
            start_placeholder = ure.compile(
                r"{%\s+for\s+(.+?)\s+in\s+" + for_obj + r"\s+%}"
            )
            end_placeholder = ure.compile(r"{%\s+endfor\s+%}")

            if start_placeholder.search(template):
                loop_body = template[
                    start_placeholder.search(template)
                    .end() : end_placeholder.search(template)
                    .start()
                ]
                for item in context[for_obj]:
                    proceed_loop_body = loop_body.replace("{% item %}", str(item))
                    template = template.replace(loop_body, proceed_loop_body)

                template = template.replace(
                    start_placeholder.search(template).group(0), ""
                )
                template = template.replace(
                    end_placeholder.search(template).group(0), ""
                )

        return template

    def _handle_conditionals(self, template: str, context) -> str:
        """
        Helper function to handle conditional rendering.
        :param template: The template string.
        :param context: The context dictionary.
        :return: The template string with conditionals handled.
        """
        for condition in context.keys():
            placeholder = "{% if " + condition + " %}"
            if placeholder in template:
                # Check if the condition is True
                if context[condition]:
                    # Remove the conditional tags
                    template = template.replace(placeholder, "")
                    template = template.replace("{% endif %}", "")
                else:
                    # Remove the content inside the conditional tags
                    start_index = template.index(placeholder)
                    end_index = template.index("{% endif %}") + len("{% endif %}")
                    template = template[:start_index] + template[end_index:]

        return template

    def _replace_variables(self, template: str, context) -> str:
        """
        Helper function to replace variables in the template.
        :param template: The template string.
        :param context: The context dictionary.
        :return: The template string with variables replaced.
        """
        for key, value in context.items():
            placeholder = "{{ " + key + " }}"

            if placeholder in template:
                template = template.replace(placeholder, str(value))

        return template

    @staticmethod
    def from_file(file_path: str) -> "HTMLPreprocessor":
        """
        Static method to create an instance of HTMLPreprocessor from a file.
        :param file_path: The path to the HTML file.
        :return: An instance of HTMLPreprocessor.
        """
        with open(file_path, "r") as file:
            template_str = file.read()
        return HTMLPreprocessor(template_str)
