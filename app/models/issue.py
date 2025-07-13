# Clase para cada mensaje
class Issue:
    # Constructor de la clase
    def __init__(self, msg = "", flavour = "", entity = "", url = "", mail = "", phone = "", html = "", embeddings = [], norm_embeddings = [], campaign = ""):
        self.msg = msg 
        self.flavour = flavour 
        self.entity = entity 
        self.url = url 
        self.mail = mail 
        self.phone = phone 
        self.html = html 
        self.norm_embeddings = norm_embeddings
        self.embeddings = embeddings
        self.campaign = campaign

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    def msg(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("msg debe ser una cadena.")
        self._msg = valor

    @property
    def flavour(self) -> str:
        return self._flavour

    @flavour.setter
    def flavour(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("flavour debe ser una cadena.")
        self._flavour = valor

    @property
    def entity(self) -> str:
        return self._entity

    @entity.setter
    def entity(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("entity debe ser una cadena.")
        self._entity = valor

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("url debe ser una cadena.")
        self._url = valor

    @property
    def mail(self) -> str:
        return self._mail

    @mail.setter
    def mail(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("mail debe ser una cadena.")
        self._mail = valor

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("phone debe ser una cadena.")
        self._phone = valor

    @property
    def html(self) -> str:
        return self._html

    @html.setter
    def html(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("html debe ser una cadena.")
        self._html = valor

    @property
    def embeddings(self) -> list[float]:
        return self._embeddings

    @embeddings.setter
    def embeddings(self, valor: list[float]):
        if not isinstance(valor, list) or not all(isinstance(x, float) for x in valor):
            raise TypeError("embeddings debe ser una lista de floats.")
        self._embeddings = valor

    @property
    def norm_embeddings(self) -> list[float]:
        return self._norm_embeddings

    @norm_embeddings.setter
    def norm_embeddings(self, valor: list[float]):
        if not isinstance(valor, list) or not all(isinstance(x, float) for x in valor):
            raise TypeError("Normalized embeddings debe ser una lista de floats.")
        self._norm_embeddings = valor

    @property
    def campaign(self) -> str:
        return self._campaign

    @campaign.setter
    def campaign(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("campaign debe ser una cadena.")
        self._campaign = valor

    # Devuelve un reporte BÁSICO a partir de los datos del ejemplo
    def report_basic():
        return {
                "type": "Basic",
                "result": "Smishing"
                }

    # Devuelve un reporte ELABORADO a partir de los datos del ejemplo
    def report_advanced():
        return {
                "type": "advanced",
                "result": "Ham"
                }

    # Devuelte el contenido de la ISSUE en formato JSON (dict)
    def to_dict(self):
        return {
                "msg": self._msg ,
                "flavour": self._flavour ,
                "entity": self._entity ,
                "url": self._url ,
                "mail": self._mail ,
                "phone": self._phone ,
                "html": self._html ,
                "embeddings": self._embeddings ,
                "norm_embeddings": self._norm_embeddings,
                "campaign": self._campaign ,
                }
