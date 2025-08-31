# app/tests/test_graph_controller.py
import importlib
from types import SimpleNamespace
from datetime import datetime
import pytest

MODULE_PATH = "api.controllers.graph_controller"

@pytest.fixture(scope="module")
def mod():
    return importlib.import_module(MODULE_PATH)

# ----------------- Dummy Beanie layer -----------------
class _DummyBeanieObj:
    def __init__(self, d: dict):
        self._d = d
    def model_dump(self):
        return self._d
    # Permite acceder como atributo a las claves del dict (p.ej. obj.entity)
    def __getattr__(self, name):
        try:
            return self._d[name]
        except KeyError:
            raise AttributeError(name)
class _DummyQuery:
    def __init__(self, data):
        self._data = [_DummyBeanieObj(d) for d in data]
    def project(self, *_args, **_kwargs):
        return self
    async def to_list(self):
        return self._data

class _DummySmishing:
    _data = []
    @classmethod
    def set_data(cls, data):
        cls._data = data
    @classmethod
    def find(cls, _query):
        # Ignoramos filtros start/end para simplificar unit tests
        return _DummyQuery(cls._data)

@pytest.fixture
def patch_smishing(mod, monkeypatch):
    monkeypatch.setattr(mod, "Smishing", _DummySmishing)
    return _DummySmishing

# =====================================================
#                _group_data_by_time_interval
# =====================================================
def test_group_data_by_time_interval_ok(mod):
    import pandas as pd
    base = pd.DataFrame({"created_at": pd.to_datetime([
        "2025-08-30T10:15:00Z", "2025-08-30T11:00:00Z"
    ])})

    for interval in ["D", "H", "W", "M"]:
        df = base.copy()
        out = mod._group_data_by_time_interval(df, interval)
        assert "time_group" in out.columns
        assert len(out["time_group"]) == 2

def test_group_data_by_time_interval_invalid(mod):
    import pandas as pd
    df = pd.DataFrame({"created_at": pd.to_datetime(["2025-08-30T10:00:00Z"])})
    with pytest.raises(ValueError):
        mod._group_data_by_time_interval(df, "X")

# =====================================================
#         get_graph_message_category_data
# =====================================================
@pytest.mark.asyncio
async def test_get_graph_message_category_data_ok(mod, patch_smishing):
    patch_smishing.set_data([
        {"flavour": "bank", "created_at": "2025-08-30T10:00:00Z"},
        {"flavour": "bank", "created_at": "2025-08-30T11:00:00Z"},
        {"flavour": "delivery", "created_at": "2025-08-31T10:00:00Z"},
    ])
    resp = await mod.get_graph_message_category_data(None, None)
    # value_counts ordena por frecuencia desc → bank primero
    assert resp["labels"] == ["bank", "delivery"]
    assert resp["counts"] == [2, 1]

@pytest.mark.asyncio
async def test_get_graph_message_category_data_empty(mod, patch_smishing):
    patch_smishing.set_data([])
    resp = await mod.get_graph_message_category_data(None, None)
    assert resp is None

# =====================================================
#      get_stacked_bar_time_categories_data
# =====================================================
@pytest.mark.asyncio
async def test_get_stacked_bar_time_categories_data_day(mod, patch_smishing):
    patch_smishing.set_data([
        {"flavour": "bank", "created_at": "2025-08-30T10:15:00Z"},
        {"flavour": "bank", "created_at": "2025-08-30T10:45:00Z"},
        {"flavour": "delivery", "created_at": "2025-08-30T11:00:00Z"},
        {"flavour": "bank", "created_at": "2025-08-31T10:00:00Z"},
    ])
    resp = await mod.get_stacked_bar_time_categories_data(None, None, "D")
    # categorías (filas) ordenadas alfabéticamente por groupby: bank, delivery
    assert resp["categories"] == ["bank", "delivery"]
    # timestamps con formato "%d-%m-%Y %H:%M:%S" (dos días)
    assert len(resp["timestamps"]) == 2
    # valores por categoría
    vals = resp["values"]
    assert set(vals.keys()) == {"bank", "delivery"}
    # bank tiene 3 mensajes repartidos en dos días (2 en el primero, 1 en el segundo)
    assert sum(vals["bank"]) == 3
    # delivery solo en el primer día
    assert sum(vals["delivery"]) == 1

@pytest.mark.asyncio
async def test_get_stacked_bar_time_categories_data_empty(mod, patch_smishing):
    patch_smishing.set_data([])
    resp = await mod.get_stacked_bar_time_categories_data(None, None, "H")
    assert resp is None

# =====================================================
#  get_stacked_barh_categories_organizarions_data
# =====================================================
@pytest.mark.asyncio
async def test_get_stacked_barh_categories_organizarions_data_ok(mod, patch_smishing):
    # Incluye una entidad vacía para comprobar el filtro
    patch_smishing.set_data([
        {"entity": "OrgA", "flavour": "bank", "created_at": "2025-08-30T10:00:00Z"},
        {"entity": "OrgA", "flavour": "delivery", "created_at": "2025-08-30T11:00:00Z"},
        {"entity": "OrgB", "flavour": "bank", "created_at": "2025-08-31T10:00:00Z"},
        {"entity": "",     "flavour": "bank", "created_at": "2025-08-31T11:00:00Z"},  # se debe excluir
    ])
    resp = await mod.get_stacked_barh_categories_organizarions_data(None, None)
    # Conjunto de organizaciones y categorías
    assert set(resp["organizations"]) == {"OrgA", "OrgB"}
    assert set(resp["categories"]) == {"bank", "delivery"}
    # Estructura values: dict[categoria] -> lista de recuentos por organización (mismo orden que columns)
    assert set(resp["values"].keys()) == {"bank", "delivery"}
    # bank aparece en OrgA y OrgB; delivery solo en OrgA
    # (No verificamos orden exacto de columnas; comprobamos suma total por categoría)
    assert sum(resp["values"]["bank"]) == 3 - 1  # total sin el registro de entity=="" => 2
    assert sum(resp["values"]["delivery"]) == 1

@pytest.mark.asyncio
async def test_get_stacked_barh_categories_organizarions_data_empty(mod, patch_smishing):
    patch_smishing.set_data([])
    resp = await mod.get_stacked_barh_categories_organizarions_data(None, None)
    assert resp is None

# =====================================================
#            get_graph_messages_data
# =====================================================
@pytest.mark.asyncio
async def test_get_graph_messages_data_ok(mod, patch_smishing):
    patch_smishing.set_data([
        {"msg": "hola banco", "created_at": "2025-08-30T10:00:00Z"},
        {"msg": "verifica tu cuenta", "created_at": "2025-08-30T11:00:00Z"},
        {"flavour": "bank", "created_at": "2025-08-31T10:00:00Z"},  # sin 'msg' → se ignora
    ])
    resp = await mod.get_graph_messages_data(None, None)
    assert resp["msg_list"] == ["hola banco", "verifica tu cuenta"]
    assert resp["joined"] == "hola banco verifica tu cuenta"

@pytest.mark.asyncio
async def test_get_graph_messages_data_empty(mod, patch_smishing):
    patch_smishing.set_data([])
    resp = await mod.get_graph_messages_data(None, None)
    assert resp is None

