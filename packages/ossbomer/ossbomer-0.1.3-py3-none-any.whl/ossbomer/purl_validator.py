import json
import xml.etree.ElementTree as ET
import yaml
import re
from jsonschema import validate, ValidationError
from pathlib import Path


class PurlValidator:
    def __init__(self, sbom_parser, dataset_dir, license_validator):
        self.sbom_parser = sbom_parser
        self.schema_directory = Path(dataset_dir / "package_signatures")
        self.package_signatures_directory = self.schema_directory
        self.signatures = self._load_signatures()
        self._pkg_guidance = self.signatures
        self.problematic_packages = []
        self.license_validator = license_validator
        self.updated_blocked_licenses = []

    def _load_signatures(self):
        signatures = []
        for signature_file in self.package_signatures_directory.glob("*.json"):
            with open(signature_file, 'r') as file:
                signatures.append(json.load(file))
        return signatures

    def _license_validator(self):
        if self.license_validator.blocked_licenses:
            for entry in self.license_validator.blocked_licenses:
                component = entry["component"]
                pkg_purl = component.get('purl')
                if not self.check_purl(component, pkg_purl, False):
                    self.updated_blocked_licenses.append(entry)
        self.license_validator.blocked_licenses = self.updated_blocked_licenses
        return self.license_validator

    def check_purl(self, component, purl, blk):
        for signature in self.signatures:
            matched = False
            if "purls" in signature and purl in signature["purls"]:
                if signature["blocked"] and blk:
                    self.problematic_packages.append(
                        (component, signature)
                    )
                    matched = True
                if signature["approved"] and not blk:
                    return True

            if not matched and "regex" in signature:
                regex_list = signature["regex"]
                if isinstance(regex_list, str):
                    regex_list = [regex_list]
                for regex in regex_list:
                    if re.search(regex, purl):
                        if signature["blocked"] and blk:
                            self.problematic_packages.append(
                                (component, signature)
                            )
                        if signature["approved"] and not blk:
                            return True
                        break
        return False

    def check_purls(self):
        components = self.sbom_parser.data.get('components', [])
        for component in components:
            purl = component.get('purl')
            if not purl:
                print(
                    f"Warning: Missing PURL for component"
                    f" {component.get('name', 'unknown')}"
                )
                continue
            self.check_purl(component, purl, True)
