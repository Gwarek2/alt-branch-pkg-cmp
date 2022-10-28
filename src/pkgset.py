import requests
from collections import defaultdict
from dataclasses import dataclass, asdict
from packaging import version
from typing import Optional
from urllib.parse import urljoin


@dataclass
class Package:
    name: str
    epoch: str
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: str
    source: str


class PackageSet:
    def __init__(self, branch: str, packages: Optional[dict] = None) -> None:
        self.branch = branch
        self.packages = packages if packages else defaultdict(dict)

    def add(self, pkg: Package) -> None:
        if not isinstance(pkg, Package):
            raise TypeError(f"{pkg} is not instance of {Package}")
        self.packages[pkg.arch][pkg.name] = pkg

    def diff(self, pkgset: "PackageSet") -> dict:
        self._validate_pkgset(pkgset)
        result = defaultdict(list)
        for arch, pkgs1 in self.packages.items():
            for name, pkg in pkgs1.items():
                if not pkgset.packages.get(arch, {}).get(name):
                    result[arch].append(asdict(pkg))
        return dict(result)

    def newer_than(self, pkgset: "PackageSet") -> dict:
        self._validate_pkgset(pkgset)
        result = defaultdict(list)
        for arch, pkgs1 in self.packages.items():
            for name, pkg1 in pkgs1.items():
                pkg2 = pkgset.packages.get(arch, {}).get(name)
                if pkg2 and version.parse(pkg1.version) > version.parse(pkg2.version):
                    result[arch].append(asdict(pkg1))
        return dict(result)

    def _validate_pkgset(self, pkgset) -> None:
        if not isinstance(pkgset, PackageSet):
            raise TypeError(f"{pkgset} is not an instance of {PackageSet}")

    def __repr__(self):
        output = {} 
        for arch, pkgs in self.packages.items():
            output[arch] = [pkg for pkg in pkgs.values()]
        return str(output)


api_url = "https://rdb.altlinux.org"


def get_branch_bin_pkgs(branch: str) -> dict:
    url_path = urljoin(api_url, f"api/export/branch_binary_packages/{branch}")
    response = requests.get(url_path)
    if response.status_code // 100 == 2:
        return response.json()
    print(f"Failed to retrive branch '{branch}' package lists. "
          f"Http error: {response.status_code}")
    return {}


def create_pkgsets(pkgs: list[dict], branch: str) -> PackageSet:
    result = PackageSet(branch)
    for pkg_data in pkgs:
        pkg = Package(**pkg_data) 
        result.add(pkg)
    return result

