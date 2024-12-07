import json
import xml.etree.ElementTree as ET
import yaml
import re
from jsonschema import validate, ValidationError
from pathlib import Path


class SBOMParser:
    """
    A class to parse SBOM files in SPDX or CycloneDX formats.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.format = None
        self.load_sbom()

    def load_sbom(self):
        if self.file_path.endswith(('.json', '.yaml', '.yml')):
            self.data = self._load_json_or_yaml()
        elif self.file_path.endswith('.xml'):
            self.data = self._load_xml()
        else:
            raise ValueError(
                f"Unsupported file format. "
                f"Only JSON, YAML, and XML are supported."
            )
        self.format = self.detect_format()

    def _load_json_or_yaml(self):
        """Load a JSON or YAML SBOM file."""
        with open(self.file_path, 'r') as file:
            if self.file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(file)
            return json.load(file)

    def _load_xml(self):
        """Load and parse an XML SBOM file."""
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return self._element_to_dict(root)

    def _element_to_dict(self, element):
        parsed_data = {element.tag: {}}
        for child in element:
            parsed_data[element.tag][child.tag] = self._element_to_dict(child)
        if element.attrib:
            parsed_data[element.tag]['@attributes'] = element.attrib
        if element.text and element.text.strip():
            parsed_data[element.tag]['#text'] = element.text.strip()
        return parsed_data

    def detect_format(self):
        if 'spdxVersion' in self.data:
            return 'spdx'
        elif (
            'bomFormat' in self.data and
            self.data['bomFormat'] == 'CycloneDX'
        ):
            return 'cyclonedx'
        else:
            raise ValueError(
                f"Unknown SBOM format. "
                f"Supported formats are SPDX and CycloneDX."
            )
