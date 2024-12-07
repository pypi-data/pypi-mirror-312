import click
import os
from pathlib import Path
from ossbomer.sbom_parser import SBOMParser
from ossbomer.metadata_validator import MetadataValidator
from ossbomer.license_validator import LicenseValidator
from ossbomer.purl_validator import PurlValidator
from ossbomer.validation_report import ValidationReport
from ossbomer.dataset_manager import update_datasets, get_inventory
from ossbomer.dataset_manager import update_package_signatures


@click.group()
def main():
    """OSSBOMER CLI for validating SBOMs."""
    pass


@main.command()
@click.argument("sbom_path")
def validate(sbom_path):
    try:
        parser = SBOMParser(sbom_path)
    except ValueError as e:
        click.echo(f"Error: {e}")
        return
    package_dir = Path(__file__).resolve().parent
    dataset_dir = package_dir / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # Metadata Validation
    metadata_validator = MetadataValidator(parser, dataset_dir)
    metadata_validator.validate_metadata()
    metadata_validator.validate_schema()
    metadata_validator.validate_components()

    # License Validation
    license_validator = LicenseValidator(parser, dataset_dir)
    license_validator.check_licenses()

    # PURL Validation
    purl_validator = PurlValidator(parser, dataset_dir, license_validator)
    purl_validator.check_purls()
    license_validator = purl_validator._license_validator()

    # Generate and Print Report
    report = ValidationReport(
        metadata_validator, license_validator, purl_validator
    )
    report.generate_report()


@main.command()
def update():
    update_datasets()
    update_package_signatures()
    click.echo("Datasets updated successfully!")


@main.command()
def version():
    from ossbomer import __version__
    click.echo(f"OSSBOMER version: {__version__}")


@main.command()
def inventory():
    get_inventory()
