import importlib.util
from pathlib import Path
import socket
import unittest

spec = importlib.util.spec_from_file_location("iqa_launcher", Path(__file__).resolve().parents[1] / "run_api.py")
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def test_existing_process_is_not_reused(self):
        with socket.create_server(("127.0.0.1", 0)) as occupied:
            port = occupied.getsockname()[1]
            with launcher.reserve_listener("127.0.0.1", port) as fresh:
                self.assertNotEqual(fresh.getsockname()[1], port)
                self.assertLess(fresh.getsockname()[1], port + 20)

    def test_ephemeral_port_is_reserved(self):
        with launcher.reserve_listener("127.0.0.1", 0) as listener:
            self.assertGreater(listener.getsockname()[1], 0)
