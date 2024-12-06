import json
import xml.etree.ElementTree as ET
import yaml
import re
from jsonschema import validate, ValidationError
from pathlib import Path


class LicenseValidator:
    """
    A class to check licenses in the SBOM.
    """
    def __init__(self, sbom_parser, dataset_dir):
        self.sbom_parser = sbom_parser
        license_rules_file = Path(dataset_dir) / "license_rules.json"
        with open(license_rules_file, 'r') as file:
            self.license_rules = json.load(file)["licenses"]
        self.blocked_licenses = []

    def check_licenses(self):
        """Check for blocked licenses in the SBOM components."""
        components = self.sbom_parser.data.get('components', [])
        for component in components:
            license_declared = component.get('licenseDeclared', 'NOASSERTION')
            if license_declared in [
                rule["spdx_id"] for rule in self.license_rules
                if not rule["distribution"]
            ]:
                self.blocked_licenses.append(component)

            licenses = component.get("licenses", [])
            if not licenses:
                component_name = component.get('name', 'unknown')
                print(f"Warning: Missing license for '{component_name}'")
                continue

            for license_entry in licenses:
                license_id = license_entry.get("license", {}).get(
                    "id", "NOASSERTION"
                )
                if license_id.lower() == "noassertion":
                    component_name = component.get('name', 'unknown')
                    print(
                        f"Warning: 'noassertion' for '{component_name}'"
                    )
                    continue

                matching_rule = next(
                    (
                        rule for rule in self.license_rules
                        if rule["spdx_id"] == license_id
                    ),
                    None
                )
                if matching_rule:
                    if not matching_rule["distribution"]:
                        self.blocked_licenses.append({
                            "component": component,
                            "matched_spdx_id": license_id
                        })
                else:
                    print(
                        f"Warning: Unknown license '{license_id}' "
                        f"for '{component['name']}'"
                    )
