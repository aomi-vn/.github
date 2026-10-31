import unittest

from baseline import install_uv


class InstallUvTest(unittest.TestCase):
    def test_download_url(self) -> None:
        url = install_uv._download_url("0.13.6", "x86_64-unknown-linux-gnu")
        self.assertIn("0.13.6", url)
        self.assertTrue(url.endswith("uv-x86_64-unknown-linux-gnu.tar.gz"))

    def test_arch_on_linux_ci(self) -> None:
        arch = install_uv._arch()
        self.assertIn(arch, {"x86_64-unknown-linux-gnu", "aarch64-unknown-linux-gnu"})


if __name__ == "__main__":
    unittest.main()
