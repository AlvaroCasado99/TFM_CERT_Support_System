import importlib
import asyncio
import pytest
from types import SimpleNamespace

MODULE_PATH = "api.controllers.message_analysis_controller"

@pytest.fixture(scope="module")
def mod():
    return importlib.import_module(MODULE_PATH)

# ----------------- Dummies Beanie/Model -----------------
class _DummyBeanieObj:
    def __init__(self, d: dict):
        self.__dict__.update(d)
    def model_dump(self):
        return dict(self.__dict__)

class _DummyQuery:
    def __init__(self, data):
        # Simula proyección de Beanie
        self._data = [_DummyBeanieObj(d) for d in data]
    def project(self, *_args, **_kwargs):
        return self
    async def to_list(self):
        return self._data

class _DummySmishing:
    _data = []
    _inserted = []

    def __init__(self, **kwargs):
        # Permite construir como el modelo real: Smishing(msg=..., flavour=..., ...)
        self.__dict__.update(kwargs)

    @classmethod
    def set_find_data(cls, data):
        cls._data = data
    @classmethod
    def clear_inserted(cls):
        cls._inserted.clear()
    @classmethod
    def find(cls, _query):
        return _DummyQuery(cls._data)
    @classmethod
    async def insert_one(cls, doc):
        cls._inserted.append(doc)

# Dummy Issue con campos por defecto y to_dict()
class _DummyIssue:
    def __init__(self):
        self.msg = ""
        self.flavour = ""
        self.flavour_13c = ""
        self.entity = ""
        self.embeddings = []
        self.norm_embeddings = []
        self.url = ""
        self.mail = []
        self.phone = ""
        self.html = ""       # importante: default para rama sin URL
        self.campaign = ""
    def to_dict(self):
        return {
            "msg": self.msg,
            "flavour": self.flavour,
            "flavour_13c": self.flavour_13c,
            "entity": self.entity,
            "embeddings": self.embeddings,
            "norm_embeddings": self.norm_embeddings,
            "url": self.url,
            "mail": self.mail,
            "phone": self.phone,
            "html": self.html,
            "campaign": self.campaign,
        }

@pytest.fixture
def patch_models(mod, monkeypatch):
    # Parchea Smishing e Issue
    monkeypatch.setattr(mod, "Smishing", _DummySmishing)
    monkeypatch.setattr(mod, "Issue", _DummyIssue)
    _DummySmishing.set_find_data([])
    _DummySmishing.clear_inserted()
    return _DummySmishing

# =====================================================
#                     db_test
# =====================================================
@pytest.mark.asyncio
async def test_db_test_returns_results_list(mod, patch_models):
    # Prepara datos con ids (como si fuera proyección FAISS)
    patch_models.set_find_data([{"id": "a1"}, {"id": "b2"}, {"id": "c3"}])
    out = await mod.db_test()
    assert "results" in out
    assert len(out["results"]) == 3
    # Cada elemento debe tener atributo id (simulado)
    ids = [r.id for r in out["results"]]
    assert ids == ["a1", "b2", "c3"]

# =====================================================
#             advanced_text_analysis
# =====================================================
@pytest.mark.asyncio
async def test_advanced_text_analysis_single(mod, patch_models, monkeypatch):
    async def fake_analyse_text(m):
        return {"msg": m, "ok": True}
    monkeypatch.setattr(mod, "_analyse_text", fake_analyse_text)
    out = await mod.advanced_text_analysis("hola")
    assert out == {"msg": "hola", "ok": True}

@pytest.mark.asyncio
async def test_advanced_text_analysis_list(mod, patch_models, monkeypatch):
    calls = []
    async def fake_analyse_text(m):
        calls.append(m)
        return {"msg": m}
    monkeypatch.setattr(mod, "_analyse_text", fake_analyse_text)
    out = await mod.advanced_text_analysis(["a", "b", "c"])
    assert [x["msg"] for x in out] == ["a", "b", "c"]
    assert calls == ["a", "b", "c"]

# =====================================================
#             _limited_post_request
# =====================================================
@pytest.mark.asyncio
async def test_limited_post_request_respects_semaphore(mod, monkeypatch):
    # Espía de concurrencia para _normal_post_request
    counters = {"cur": 0, "max": 0}
    async def spy_normal(url, data, timeout=10.0):
        counters["cur"] += 1
        counters["max"] = max(counters["max"], counters["cur"])
        await asyncio.sleep(0.01)
        counters["cur"] -= 1
        return {"url": url, "data": data, "t": timeout}
    monkeypatch.setattr(mod, "_normal_post_request", spy_normal)

    # Lanza más de 5 en paralelo: el semáforo es de 5
    tasks = [
        mod._limited_post_request("u", {"i": i}, timeout=1.0)
        for i in range(20)
    ]
    res = await asyncio.gather(*tasks)
    assert len(res) == 20
    assert counters["max"] <= 5  # ¡clave!

# =====================================================
#             _normal_post_request
# =====================================================
@pytest.mark.asyncio
async def test_normal_post_request_ok_json_result(mod, monkeypatch):
    # Mock de httpx.AsyncClient
    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"result": {"x": 1}}
    class _Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): return False
        async def post(self, url, json, timeout):
            return _Resp()
    monkeypatch.setattr(mod, "httpx", SimpleNamespace(AsyncClient=_Client, ConnectError=Exception,
                                                     ReadTimeout=Exception, HTTPStatusError=Exception, RequestError=Exception))
    out = await mod._normal_post_request("http://x", {"a": 1}, timeout=0.1)
    assert out == {"x": 1}

@pytest.mark.asyncio
async def test_normal_post_request_handles_exceptions(mod, monkeypatch):
    # Verifica que ante cualquier excepción devuelve None (por los prints)
    class _ClientErr:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): return False
        async def post(self, *a, **kw): raise ValueError("boom")
    monkeypatch.setattr(mod, "httpx", SimpleNamespace(AsyncClient=_ClientErr,
                                                     ConnectError=ValueError, ReadTimeout=ValueError,
                                                     HTTPStatusError=ValueError, RequestError=ValueError))
    out = await mod._normal_post_request("http://x", {"a": 1}, timeout=0.1)
    assert out is None

# =====================================================
#                 _analyse_text (URL presente)
# =====================================================
@pytest.mark.asyncio
async def test_analyse_text_with_url(mod, patch_models, monkeypatch):
    # Fakes para _limited_post_request (tres primeras llamadas ms1 / embedding y luego ms2+ms3)
    async def fake_limited(url, data, timeout=10.0):
        if url.endswith("/check"):
            return {"7c": "bank", "13c": "banking_fees"}
        if url.endswith("/entity"):
            return {"org": ["BancoX"], "url": "http://phish", "email": ["a@b.com"]}
        if url.endswith("/embedding"):
            return {"embeddings": [0.1, 0.2], "norm_embeddings": [0.01, 0.02]}
        if url.endswith("/url"):
            return "<html>ok</html>"
        if url.endswith("/campaign"):
            return "Camp-1"
        raise AssertionError(f"URL inesperada {url}")
    monkeypatch.setattr(mod, "_limited_post_request", fake_limited)

    # Fake para _normal_post_request: update y no usado para campaign en esta rama
    seen = {"updates": 0}
    async def fake_normal(url, data, timeout=10.0):
        if url.endswith("/update"):
            seen["updates"] += 1
            return {"ok": True}
        raise AssertionError("No debería llamarse a campaign normal cuando hay URL")
    monkeypatch.setattr(mod, "_normal_post_request", fake_normal)

    out = await mod._analyse_text("texto sospechoso")
    # Comprobaciones clave
    assert out["flavour"] == "bank"
    assert out["flavour_13c"] == "banking_fees"
    assert out["entity"] == "BancoX"
    assert out["url"] == "http://phish"
    assert out["html"] == "<html>ok</html>"
    assert out["campaign"] == "Camp-1"
    assert out["embeddings"] == [0.1, 0.2]
    assert out["norm_embeddings"] == [0.01, 0.02]
    # Se insertó en "BD"
    assert len(_DummySmishing._inserted) == 1
    assert seen["updates"] == 1

# =====================================================
#              _analyse_text (sin URL)
# =====================================================
@pytest.mark.asyncio
async def test_analyse_text_without_url(mod, patch_models, monkeypatch):
    async def fake_limited(url, data, timeout=10.0):
        if url.endswith("/check"):
            return {"7c": "delivery", "13c": "package_hold"}
        if url.endswith("/entity"):
            # Sin URL
            return {"org": [], "url": "", "email": []}
        if url.endswith("/embedding"):
            return {"embeddings": [1, 2, 3], "norm_embeddings": [0.1, 0.2, 0.3]}
        # En esta rama, también puede llamarse /campaign por limited? (no, va por normal)
        raise AssertionError(f"URL inesperada {url}")
    monkeypatch.setattr(mod, "_limited_post_request", fake_limited)

    seen = {"campaign": 0, "update": 0}
    async def fake_normal(url, data, timeout=10.0):
        if url.endswith("/campaign"):
            seen["campaign"] += 1
            return "Camp-2"
        if url.endswith("/update"):
            seen["update"] += 1
            return {"ok": True}
        raise AssertionError(f"URL inesperada {url}")
    monkeypatch.setattr(mod, "_normal_post_request", fake_normal)

    out = await mod._analyse_text("otro mensaje")
    assert out["url"] == ""
    assert out["campaign"] == "Camp-2"
    assert out["flavour"] == "delivery"
    assert out["flavour_13c"] == "package_hold"
    assert out["embeddings"] == [1, 2, 3]
    assert out["norm_embeddings"] == [0.1, 0.2, 0.3]
    assert seen["campaign"] == 1
    assert seen["update"] == 1
    assert len(_DummySmishing._inserted) == 1

