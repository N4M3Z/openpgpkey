"""The served tree equals what keys.yaml renders, and the WKD hash is right."""

import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
build_wkd = __import__("build-wkd")


class Wkd(unittest.TestCase):
    def test_domain_accepts_ascii_dns_names(self):
        for domain in (
            "martinzeman.net",
            "sub-domain.example",
            "xn--bcher-kva.example",
            ".".join(["a" * 63] * 3 + ["a" * 61]),
        ):
            with self.subTest(domain=domain):
                self.assertEqual(build_wkd.validate_domain(domain), domain)

    def test_invalid_domains_cannot_create_output_or_overwrite_outside_policy(self):
        with tempfile.TemporaryDirectory() as scratch:
            base = pathlib.Path(scratch)
            root = base / "repo"
            root.mkdir()
            outside = base / "outside"
            outside.mkdir()
            policy = outside / "policy"
            policy.write_bytes(b"preserve this policy")
            out = root / "rendered"
            domains = (
                str(outside),
                "../../outside",
                "../outside",
                ".",
                "..",
                "example/../../outside",
                "example\\outside",
                "",
                None,
                True,
                123,
                [],
                {},
                "example..net",
                ".example.net",
                "example.net.",
                "-example.net",
                "example-.net",
                "exa_mple.net",
                "example net",
                "example.net\n",
                "b\u00fccher.example",
                "a" * 64 + ".example",
                ".".join(["a" * 63] * 4),
            )
            for domain in domains:
                with self.subTest(domain=domain):
                    (root / "keys.yaml").write_text(
                        build_wkd.yaml.safe_dump({"domain": domain, "keys": []})
                    )
                    with mock.patch.object(build_wkd, "ROOT", root):
                        with self.assertRaisesRegex(SystemExit, "ASCII DNS name"):
                            build_wkd.render(out)
                    self.assertFalse(out.exists())
                    self.assertFalse((root / "outside").exists())
                    self.assertFalse((outside / "hu").exists())
                    self.assertEqual(policy.read_bytes(), b"preserve this policy")

    def test_zbase32_sha1_matches_the_gnupg_reference_vector(self):
        # gpg-wks-client --print-wkd-hash on "Joe.Doe@Example.ORG" yields this
        # (the local part is lowercased first), the vector the WKD draft uses.
        self.assertEqual(build_wkd.zbase32_sha1("Joe.Doe"), "iy9q119eutrkn8s1mk4r39qejnbu3n5q")

    def test_site_matches_keys_yaml(self):
        result = subprocess.run(  # noqa: S603
            [sys.executable, str(ROOT / "scripts" / "build-wkd.py"), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_every_served_key_is_binary_and_names_its_address(self):
        domain_dir = ROOT / "site" / ".well-known" / "openpgpkey" / "martinzeman.net"
        self.assertTrue((domain_dir / "policy").is_file())
        served = sorted((domain_dir / "hu").iterdir())
        self.assertTrue(served)
        for path in served:
            data = path.read_bytes()
            self.assertNotIn(b"BEGIN PGP", data, f"{path.name} is armored; WKD serves binary")
            self.assertEqual(
                data[0] & 0x80, 0x80, f"{path.name} does not start with an OpenPGP packet"
            )


if __name__ == "__main__":
    unittest.main()
