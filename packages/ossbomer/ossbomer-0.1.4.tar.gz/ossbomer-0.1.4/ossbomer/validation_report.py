import json
import xml.etree.ElementTree as ET
import yaml
import re
from jsonschema import validate, ValidationError
from pathlib import Path


class ValidationReport:
    """
    A class to generate and print the final validation report.
    """
    def __init__(self, metadata_validator, license_checker, purl_validator):
        self.metadata_validator = metadata_validator
        self.license_checker = license_checker
        self.purl_validator = purl_validator

    def generate_report(self):
        """Generate a validation report with all errors and warnings."""
        print("\nValidation Report:")
        print("------------------")

        # Metadata Validation
        if self.metadata_validator.errors:
            print("Metadata Errors:")
            for error in self.metadata_validator.errors:
                print(f"  - {error}")
        else:
            print("Metadata validation passed.")

        # License Validation
        if self.license_checker.blocked_licenses:
            print("Blocked Licenses:")
            for entry in self.license_checker.blocked_licenses:
                component = entry["component"]
                matched_spdx_id = entry["matched_spdx_id"]
                print(
                    f"  - Component '{component.get('name')}' "
                    f"uses blocked license {matched_spdx_id}"
                )
        else:
            print("No blocked licenses detected.")

        # PURL Validation
        if self.purl_validator.problematic_packages:
            print("Problematic Packages:")
            for component, signature in (
                self.purl_validator.problematic_packages
            ):
                print(
                    f"  - Component '{component.get('name')}' "
                    f"with PURL '{component.get('purl')}'"
                )
                print(
                    f"    Matched Signature: "
                    f"{signature.get('package_name')} "
                    f"[{signature.get('problem_type')}]"
                )
        else:
            print("No problematic packages detected.")
