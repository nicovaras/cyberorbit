from core.data import load_data, save_data

def test_load_and_save_data():
    data = load_data()
    assert isinstance(data, list)
    assert data[0]["id"] == "n1"
    data.append({"id": "n2", "title": "Another", "type": "main", "children": []})
    save_data(data)
    reloaded = load_data()
    assert any(n["id"] == "n2" for n in reloaded)
