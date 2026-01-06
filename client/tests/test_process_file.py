from client.cli import process_file

class FakeUploader:
    def __init__(self):
        self.called = False

    def upload(self, _):
        self.called = True
        return True


def test_skip_existing_file(tmp_path):
    from client.state_store import StateStore

    file = tmp_path / "a.txt"
    file.write_text("hello")

    state = StateStore(state_file=tmp_path / "state.json")
    uploader = FakeUploader()

    # first upload
    process_file(str(file), state, uploader)
    assert uploader.called

    # second upload
    uploader.called = False
    process_file(str(file), state, uploader)

    assert uploader.called is False
