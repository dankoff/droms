from app import make_app

def test_config():
    assert not make_app().testing
    assert make_app({'TESTING': True}).testing
