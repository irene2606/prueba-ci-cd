from app import evaluar_motor

def test_motor_seguro():
    assert evaluar_motor(80) == "OK"

def test_motor_peligro():
    assert evaluar_motor(95) == "ALERTA"
    