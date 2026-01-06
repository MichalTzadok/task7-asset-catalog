from client.watcher import Watcher

def test_callback_called():
    called = []

    def callback(path):
        called.append(path)

    handler = Watcher.Handler(callback)

    class FakeEvent:
        is_directory = False
        src_path = "file.txt"

    handler.on_created(FakeEvent())
    assert called == ["file.txt"]
