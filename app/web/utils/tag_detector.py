""" Se trata de una clase que hereda de HTMLParser y cuyo cometido es detectar la presencia de html tags.
IMPORTANTE: No es thread-safe, no usar en concurrencia sin protección"""

from html.parser import HTMLParser
from html import unescape

class TagDetector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_tag = False

    # Sobreescribir los eventos de HTMLPaser que se lanzan cuando detecta tags
    def handle_starttag(self, tag, attrs):
        self.found_tag = True

    def handle_endtag(self, tag):
        self.found_tag = True

    def reset_state(self):
        self.found_tag = False
        self.reset()

    # Metodo própio para realizar el análisis de un text
    def detect_html(self, text: str) -> bool:
        text = unescape(text)
        self.reset_state()
        self.feed(text)
        return self.found_tag

# Instancia global de la clase (emula un Singleton más simple) 
tag_detector = TagDetector()
