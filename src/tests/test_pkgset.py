import json
import unittest
from pathlib import Path
from pkgset import Package, PackageSet, create_pkgsets


data_path = Path(__file__).parent / "data"


def read_json_file(file_path):
    return json.loads(file_path.read_text())


class TestPackageSet(unittest.TestCase):
    def setUp(self):
        pkgs1 = read_json_file(data_path / "dataset1.json").get("packages")
        pkgs2 = read_json_file(data_path / "dataset2.json").get("packages")
        self.pkgset1 = create_pkgsets(pkgs1, "sisyphus")
        self.pkgset2 = create_pkgsets(pkgs2, "p10")

    def test_adding_invalid_packages(self):
        with self.assertRaises(TypeError):
            self.pkgset1.add(None)
        with self.assertRaises(TypeError):
            self.pkgset2.add([1, 2, 3, 4])

    def test_adding_packages(self):
        package = Package(
                name="gpg",
                epoch="0",
                version="2.1.7",
                release="atl1",
                arch="x86_64",
                disttag="sisyphus",
                buildtime="123432324",
                source="Cardinal"                
                )
        self.pkgset1.add(package)
        self.pkgset2.add(package)
        self.assertEqual(package, self.pkgset1.packages["x86_64"]["gpg"])
        self.assertEqual(package, self.pkgset2.packages["x86_64"]["gpg"])

    def test_pkgsets_diff(self):
        diff1 = read_json_file(data_path / "diff1.json")
        diff2 = read_json_file(data_path / "diff2.json")
        self.assertEqual(self.pkgset1.diff(self.pkgset2), diff1)
        self.assertEqual(self.pkgset2.diff(self.pkgset1), diff2)

    def test_pksets_newer_pkgs(self):
        newer1 = read_json_file(data_path / "newer1.json")
        newer2 = read_json_file(data_path / "newer2.json")
        self.assertEqual(self.pkgset1.newer_than(self.pkgset2), newer1)
        self.assertEqual(self.pkgset2.newer_than(self.pkgset1), newer2)


if __name__ == "__main__":
    unittest.main()
