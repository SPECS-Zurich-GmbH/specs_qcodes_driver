import pytest
from qcodes_contrib_drivers.drivers.SPECS.Specs_Tramea import NanonisTramea


def test_driver_instantiates(monkeypatch):
    class DummySocket:
        def __init__(self):
            pass

        def connect(self, *args, **kwargs):
            pass

    class DummyNanonis:
        def __init__(self, socket):
            pass

        def Signals_ValGet(self, index, dummy):
            return [None, None, [0.0]]

        def UserOut_ValSet(self, out, val):
            return None

    # Patch socket and nanonis_tramea
    monkeypatch.setattr("socket.socket", lambda *a, **kw: DummySocket())
    monkeypatch.setattr("nanonis_tramea.Nanonis", DummyNanonis)

    # Try to instantiate
    driver = NanonisTramea(name="Test", address="127.0.0.1", port=6502)

    assert driver.name == "Test"
    assert hasattr(driver, "Output1")
    assert callable(driver.Output1.set)
    assert callable(driver.Output1.get)
    assert hasattr(driver, "Input1")
    assert callable(driver.Input1.get)
    assert driver.Input1.get() == 0.0
