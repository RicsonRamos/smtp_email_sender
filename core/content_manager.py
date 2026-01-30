class EmailContent:
    """Stores email subjects and handles core content strings."""
    
    SUBJECT = "Internship Application – Criminal Law Area"
    
    @staticmethod
    def get_plain_text_template(content: str, empresa: str, nome: str) -> str:
        return content.format(empresa=empresa, nome=nome)

    @staticmethod
    def get_html_template(content: str, empresa: str, nome: str) -> str:
        return content.format(empresa=empresa, nome=nome)