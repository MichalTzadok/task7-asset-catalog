from client.hasher import compute_hash

def test_same_content_same_hash(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hello")

    h1 = compute_hash(f)
    h2 = compute_hash(f)

    assert h1 == h2


def test_different_content_different_hash(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"

    f1.write_text("hello")
    f2.write_text("hello!")

    assert compute_hash(f1) != compute_hash(f2)
