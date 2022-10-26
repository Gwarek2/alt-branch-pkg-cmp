import requests
from collections import namedtuple
from packaging import version
from typing import Optional
from urllib.parse import urljoin

api_url = "https://rdb.altlinux.org/api"


def get_branch_bin_pkgs(branch: str) -> tuple[int, list]:
    url_path = urljoin(api_url, f"export/branch_binary_packages/{branch}")
    response = requests.get(url_path)
    return response.status_code, response.json().get("packages")


def get_branch_archs(pkgset: set) -> set:
    return set(pkg.get("arch") for pkg in pkgset)

Package = namedtuple(
        "Package",
        ["name", "epoch", "version", "release", "arch", "disttag", "buildtime", "source"]
        )


class PackageSet:
    def __init__(self, packages: list[Package]) -> None:
        self.packages = packages
        self.archs = self._get_branch_archs(packages) 

    def __hash__(self, arch) -> list[Package]:
        return list(filter(lambda pkg: pkg.arch == arch, self.packages))

    def __sub__(self, pkgset: PackageSet) -> PackageSet:
        pkgset1, pkgset2  = set(self.packages), set(pkgset.packages)
        return PackageSet(list(pkgset1 - pkgset2))

    def packages_newer_than(self, pkgset: PackageSet) -> list[Package]:
        pkgs1 = self.packages
        pkgs2 = pkgset.packages
        result = []
        for pkg1 in pkgs1:
            pkg2 = self._find_pkg(pkg1.name, pkg1.arch, pkgs2)
            if pkg2 and version.parse(pkg1.version) > version.parse(pkg2.version):
                result.append(pkg1)
        return result
        
    def _get_branch_archs(self, pkgset: list[Package]) -> set:
        return set(pkg.arch for pkg in pkgset)

    def _find_pkg(self, pkg_name: str, arch: str, pkgset: set) -> Package | None:
        for pkg in pkgset:
            if pkg.name == pkg_name and pkg.arch == arch:
                return pkg
        return None

