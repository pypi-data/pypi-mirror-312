import json
from jsonschema import validate, ValidationError
from pathlib import Path
import re


class MetadataValidator:
    """
    A class to validate metadata, schema, and consistency for SBOM files.
    """
    def __init__(self, sbom_parser, schema_directory):
        self.sbom_parser = sbom_parser
        self.schema_directory = Path(schema_directory)
        self.errors = []

    def validate_metadata(self):
        data = self.sbom_parser.data
        missing_fields = []

        if self.sbom_parser.format == 'spdx':
            required_fields = [
                'spdxVersion', 'name', 'documentNamespace', 'creationInfo'
            ]
        elif self.sbom_parser.format == 'cyclonedx':
            required_fields = ['bomFormat', 'specVersion']
        else:
            raise ValueError("Unsupported SBOM format.")

        for field in required_fields:
            if field not in data:
                missing_fields.append(field)

        if missing_fields:
            self.errors.append(
                f"Missing metadata fields: {', '.join(missing_fields)}"
            )

    def validate_schema(self):
        schema_file = self._get_schema_file()
        with open(schema_file, 'r') as schema:
            schema_data = json.load(schema)
        try:
            validate(instance=self.sbom_parser.data, schema=schema_data)
        except ValidationError as e:
            self.errors.append(f"Schema validation error: {e.message}")

    def validate_components(self):
        components = self.sbom_parser.data.get('components', [])
        seen_ids = set()
        id_type = None
        expected_hash_set = None
        expected_hash_lengths = {
            "MD5": 32,
            "SHA-1": 40,
            "SHA-256": 64,
            "SHA-384": 96,
            "SHA-512": 128,
            "SHA3-256": 64,
            "SHA3-384": 96,
            "SHA3-512": 128
        }

        for component in components:
            # Validate unique IDs, it would need improvements
            comp_id = component.get('purl')
            if not comp_id:
                self.errors.append(f"Component missing ID: {component}")
            elif comp_id in seen_ids:
                self.errors.append(f"Duplicate component ID found: {comp_id}")
            else:
                seen_ids.add(comp_id)

            current_id_type = (
                "purl" if comp_id and comp_id.startswith("pkg:")
                else "other"
            )
            if id_type is None:
                id_type = current_id_type
            elif id_type != current_id_type:
                self.errors.append(f"Inconsistent ID type: {comp_id}")

            # Validate hash types and lengths
            hashes = component.get('hashes', [])
            hash_set = set()

            for hash_obj in hashes:
                hash_algo = hash_obj.get("alg")
                hash_value = hash_obj.get("content")
                if not hash_algo or not hash_value:
                    self.errors.append(
                        f"Invalid hash: Missing 'alg' "
                        f"or 'content' for {comp_id}"
                    )
                    continue
                hash_set.add(hash_algo)
                expected_length = expected_hash_lengths.get(hash_algo)
                if expected_length is None:
                    self.errors.append(
                        f"Unknown hash algorithm: {hash_algo} for {comp_id}"
                    )
                elif len(hash_value) != expected_length:
                    self.errors.append(
                        f"Invalid hash length for alg: {hash_algo}. "
                        f"Expected {expected_length}, "
                        f"got {len(hash_value)} for {comp_id}"
                    )
            if expected_hash_set is None:
                expected_hash_set = hash_set
            elif hash_set != expected_hash_set:
                self.errors.append(
                    f"Inconsistent hash algorithms in component {comp_id}. "
                    f"Expected: {expected_hash_set}, Found: {hash_set}"
                )

    def _get_schema_file(self):
        if self.sbom_parser.format == 'spdx':
            return self.schema_directory / "spdx_schema.json"
        elif self.sbom_parser.format == 'cyclonedx':
            return self.schema_directory / "cyclonedx_schema.json"
        else:
            raise ValueError("Unsupported SBOM format.")
