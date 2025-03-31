from core.ctfs import load_ctfs, save_ctfs

def test_ctf_load_and_save():
    ctfs = load_ctfs()
    assert isinstance(ctfs, list)
    assert ctfs[0]["title"] == "CTF1"
    ctfs.append({"title": "CTF2", "completed": 0})
    save_ctfs(ctfs)
    new_ctfs = load_ctfs()
    assert any(c["title"] == "CTF2" for c in new_ctfs)
