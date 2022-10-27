import argparse
import json
from pkgset import get_branch_bin_pkgs, create_pkgsets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="alt-pkgset-cmp",
            description="Compares packages from two given alt-linux branches "
                        "and outputs result in json format."
            )
    parser.add_argument("branch1", metavar="b1", help="First branch")
    parser.add_argument("branch2", metavar="b2", help="Second branch")
    args = parser.parse_args()

    branch1 = args.branch1
    branch2 = args.branch2 

    pkgs1_data = get_branch_bin_pkgs(branch1).get("packages")
    pkgs2_data = get_branch_bin_pkgs(branch2).get("packages")
    if not pkgs1_data or not pkgs2_data:
        exit(1)

    branch1_pkgset = create_pkgsets(pkgs1_data, branch1)
    branch2_pkgset = create_pkgsets(pkgs2_data, branch2)

    branch1_uniq_pkgs = branch1_pkgset.diff(branch2_pkgset)
    branch2_uniq_pkgs = branch2_pkgset.diff(branch1_pkgset)
    branch1_newer_pkgs = branch1_pkgset.newer_than(branch2_pkgset)
    output = {
            "branch1": branch1,
            "branch2": branch2,
            "diff": branch1_uniq_pkgs,
            "reverted_diff": branch2_uniq_pkgs,
            "newer_packages": branch1_newer_pkgs,
            }
            
    print(json.dumps(output))
