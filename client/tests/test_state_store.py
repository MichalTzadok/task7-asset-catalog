from client.state_store import StateStore

def test_empty_state(tmp_path):
    state = StateStore(state_file=tmp_path / "state.json")
    assert state.data["files"] == {}
    assert state.data["hashes"] == {}


def test_add_and_exists(tmp_path):
    state = StateStore(state_file=tmp_path / "state.json")
    state.add_file("a.txt", "hash123")

    assert state.exists("hash123")


def test_state_recovery(tmp_path):
    state_file = tmp_path / "state.json"

    s1 = StateStore(state_file=state_file)
    s1.add_file("a.txt", "hash123")

    s2 = StateStore(state_file=state_file)
    assert s2.exists("hash123")
