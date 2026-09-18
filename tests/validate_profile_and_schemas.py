# This script validates the GeoLocator-DP standard itself is valid (regarding JSON and Frictionless definitions)

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from frictionless import Schema
from jsonschema import Draft202012Validator

THIS_SCRIPT_PATH = Path(__file__).parent
REPOSITORY_ROOT_PATH = THIS_SCRIPT_PATH / ".."
PROFILE_PATH = REPOSITORY_ROOT_PATH / "geolocator-dp-profile.json"
EXAMPLE_PACKAGE_PATH = REPOSITORY_ROOT_PATH / "example" / "datapackage.json"
TABLE_SCHEMA_PATHS = [
    REPOSITORY_ROOT_PATH / "observations-table-schema.json",
    REPOSITORY_ROOT_PATH / "tags-table-schema.json",
    REPOSITORY_ROOT_PATH / "measurements-table-schema.json",
    REPOSITORY_ROOT_PATH / "staps-table-schema.json",
    REPOSITORY_ROOT_PATH / "twilights-table-schema.json",
    REPOSITORY_ROOT_PATH / "paths-table-schema.json",
    REPOSITORY_ROOT_PATH / "edges-table-schema.json",
    REPOSITORY_ROOT_PATH / "pressurepaths-table-schema.json",
]

EXPECTED_SCHEMA_RESOURCES = {
    "tags",
    "observations",
    "measurements",
    "staps",
    "twilights",
    "paths",
    "edges",
    "pressurepaths",
}

def load_json(filepath: Path) -> Optional[dict]:
    with open(filepath) as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError:
            return None


def validate_schema(file_path: Path) -> bool:
    report = Schema.validate_descriptor(descriptor=file_path)
    return report.valid


def get_schema_metadata_error_messages(file_path: Path) -> List[str]:
    """Return a list of error messages for the table schema at file_path

    Undefined behavior if the table schema is valid
    """
    report = Schema.validate_descriptor(descriptor=file_path)
    return [err.message for err in report.errors]


def _listify_fields(fields) -> List[str]:
    if isinstance(fields, str):
        return [fields]
    if isinstance(fields, list):
        return [field for field in fields if isinstance(field, str)]
    return []


def _get_schema_fields(descriptor: dict) -> set:
    fields = descriptor.get("fields", [])
    return {
        field.get("name")
        for field in fields
        if isinstance(field, dict) and isinstance(field.get("name"), str)
    }


def check_schema_coherence(schema_descriptors: Dict[Path, dict]) -> bool:
    encountered_errors = False
    resource_to_paths: Dict[str, List[Path]] = {}

    # 1) filename <-> schema name consistency
    for schema_path, descriptor in schema_descriptors.items():
        schema_name = descriptor.get("name")
        expected_name = schema_path.name.replace("-table-schema.json", "")

        if not isinstance(schema_name, str):
            print(f"✕ {schema_path.name}: missing or non-string `name`")
            encountered_errors = True
            continue

        resource_to_paths.setdefault(schema_name, []).append(schema_path)

        if schema_name != expected_name:
            print(
                f"✕ {schema_path.name}: schema `name` is `{schema_name}` but expected `{expected_name}`"
            )
            encountered_errors = True

    # 2) expected resources exist exactly once
    observed_resources = set(resource_to_paths.keys())
    missing_resources = sorted(EXPECTED_SCHEMA_RESOURCES - observed_resources)
    unexpected_resources = sorted(observed_resources - EXPECTED_SCHEMA_RESOURCES)

    for resource in missing_resources:
        print(f"✕ schema resources: missing expected resource `{resource}`")
        encountered_errors = True

    for resource in unexpected_resources:
        print(f"✕ schema resources: unexpected resource `{resource}`")
        encountered_errors = True

    for resource, paths in sorted(resource_to_paths.items()):
        if len(paths) > 1:
            path_list = ", ".join(path.name for path in paths)
            print(
                f"✕ schema resources: resource `{resource}` is defined more than once ({path_list})"
            )
            encountered_errors = True

    # 3) foreign keys reference existing resources and target fields
    fields_by_resource: Dict[str, set] = {}
    for resource, paths in resource_to_paths.items():
        if len(paths) == 1:
            fields_by_resource[resource] = _get_schema_fields(schema_descriptors[paths[0]])

    for schema_path, descriptor in schema_descriptors.items():
        foreign_keys = descriptor.get("foreignKeys", [])
        if not isinstance(foreign_keys, list):
            continue

        for foreign_key in foreign_keys:
            if not isinstance(foreign_key, dict):
                continue

            reference = foreign_key.get("reference", {})
            if not isinstance(reference, dict):
                print(f"✕ {schema_path.name}: malformed foreign key reference")
                encountered_errors = True
                continue

            target_resource = reference.get("resource")
            target_fields = _listify_fields(reference.get("fields"))

            if not isinstance(target_resource, str):
                print(f"✕ {schema_path.name}: foreign key reference missing `resource`")
                encountered_errors = True
                continue

            if target_resource not in resource_to_paths:
                print(
                    f"✕ {schema_path.name}: foreign key references unknown resource `{target_resource}`"
                )
                encountered_errors = True
                continue

            target_resource_fields = fields_by_resource.get(target_resource, set())
            missing_target_fields = [
                field for field in target_fields if field not in target_resource_fields
            ]

            if missing_target_fields:
                fields_str = ", ".join(missing_target_fields)
                print(
                    f"✕ {schema_path.name}: foreign key references missing field(s) in `{target_resource}`: {fields_str}"
                )
                encountered_errors = True

    return not encountered_errors


FIELDS_MATCH_VALUES = {"exact", "equal", "subset", "superset", "partial"}


def _is_array_of_strings(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def check_v2_spellings(schema_descriptors: Dict[Path, dict]) -> bool:
    """Check the table schemas use the Data Package v2 spelling of their keys.

    The published `tableschema.json` profile is more permissive than the
    standard on both counts, so these are checked here rather than left to
    `Schema.validate_descriptor()`:

    - `fieldsMatch` `MUST` be a string. The profile types it as an array, which
      is an error being fixed in v2.1
      (frictionlessdata/datapackage#965).
    - `primaryKey` and foreign key fields "should now always be an array of
      strings, not a string". The profile still allows the v1 string form.
    """
    encountered_errors = False

    for schema_path, descriptor in schema_descriptors.items():
        name = schema_path.name

        fields_match = descriptor.get("fieldsMatch")
        if fields_match is not None:
            if not isinstance(fields_match, str):
                print(
                    f"✕ {name}: `fieldsMatch` must be a string, got "
                    f"{type(fields_match).__name__} `{fields_match}`"
                )
                encountered_errors = True
            elif fields_match not in FIELDS_MATCH_VALUES:
                print(f"✕ {name}: unknown `fieldsMatch` value `{fields_match}`")
                encountered_errors = True

        primary_key = descriptor.get("primaryKey")
        if primary_key is not None and not _is_array_of_strings(primary_key):
            print(
                f"✕ {name}: `primaryKey` must be an array of strings, got `{primary_key}`"
            )
            encountered_errors = True

        for index, foreign_key in enumerate(descriptor.get("foreignKeys", [])):
            if not isinstance(foreign_key, dict):
                continue

            reference = foreign_key.get("reference")
            candidates = [("fields", foreign_key.get("fields"))]
            if isinstance(reference, dict):
                candidates.append(("reference.fields", reference.get("fields")))

            for label, fields in candidates:
                if not _is_array_of_strings(fields):
                    print(
                        f"✕ {name}: `foreignKeys[{index}].{label}` must be an array "
                        f"of strings, got `{fields}`"
                    )
                    encountered_errors = True

    return not encountered_errors


def check_categories(schema_descriptors: Dict[Path, dict]) -> bool:
    """Check `categories` and the `enum` constraint stay in step.

    The standard says the values of a field "`MUST` exactly match one of the
    values in `categories`" and that an `enum` alongside it `MUST` be a subset.
    Both are declared here because no implementation enforces `categories` yet:
    frictionless-py 5.19 accepts a value outside `categories` without an error,
    so dropping `enum` would silently drop the validation.

    Keeping both means they can drift, which is what this checks.
    """
    encountered_errors = False

    for schema_path, descriptor in schema_descriptors.items():
        for field in descriptor.get("fields", []):
            if not isinstance(field, dict):
                continue

            categories = field.get("categories")
            enum = field.get("constraints", {}).get("enum")
            location = f"{schema_path.name}: `{field.get('name')}`"

            if categories is None:
                if enum is not None:
                    print(f"✕ {location}: has an `enum` constraint but no `categories`")
                    encountered_errors = True
                continue

            values = [
                category.get("value") if isinstance(category, dict) else category
                for category in categories
            ]

            if len(values) != len(set(map(str, values))):
                print(f"✕ {location}: `categories` values are not unique")
                encountered_errors = True

            example = field.get("example")
            if example is not None and example not in values:
                print(
                    f"✕ {location}: `example` {example!r} is not one of its `categories`"
                )
                encountered_errors = True

            if enum is None:
                print(f"✕ {location}: has `categories` but no `enum` constraint")
                encountered_errors = True
            elif list(enum) != values:
                print(
                    f"✕ {location}: `enum` and `categories` differ\n"
                    f"\t   enum: {list(enum)}\n"
                    f"\t   categories: {values}"
                )
                encountered_errors = True

    return not encountered_errors


def check_example_package(profile: dict) -> bool:
    """Validate example/datapackage.json against the GeoLocator DP profile.

    Only the GeoLocator DP specific half of the profile (`allOf[1]`) is applied,
    so the check stays offline and deterministic; the other half is a `$ref` to
    the Data Package profile on datapackage.org.
    """
    encountered_errors = False

    descriptor = load_json(EXAMPLE_PACKAGE_PATH)
    if descriptor is None:
        print("✕ valid JSON")
        return False
    print("✔︎ valid JSON")

    validator = Draft202012Validator(profile["allOf"][1])
    errors = sorted(validator.iter_errors(descriptor), key=lambda err: list(err.path))
    if errors:
        print("✕ conforms to the GeoLocator DP profile, errors:")
        for err in errors:
            location = "/".join(str(part) for part in err.path) or "<root>"
            print(f"\t - {location}: {err.message}")
        encountered_errors = True
    else:
        print("✔︎ conforms to the GeoLocator DP profile")

    # Every referenced file and table schema must exist in this repository, which
    # catches typos while the version in the URL is not tagged yet.
    for resource in descriptor.get("resources", []):
        path = resource.get("path")
        if isinstance(path, str) and not (EXAMPLE_PACKAGE_PATH.parent / path).exists():
            print(f"✕ resource `{resource.get('name')}`: missing file `{path}`")
            encountered_errors = True

        schema = resource.get("schema")
        if isinstance(schema, str):
            schema_file = REPOSITORY_ROOT_PATH / re.sub(r"^.*/", "", schema)
            if not schema_file.exists():
                print(
                    f"✕ resource `{resource.get('name')}`: `schema` points at "
                    f"`{schema_file.name}`, which does not exist in this repository"
                )
                encountered_errors = True

    if not encountered_errors:
        print("✔︎ resource files and table schemas exist")

    return not encountered_errors


if __name__ == "__main__":
    encountered_errors = False
    schema_descriptors: Dict[Path, dict] = {}

    print(PROFILE_PATH.name)
    profile_json = load_json(PROFILE_PATH)
    if profile_json is not None:
        print("✔︎ valid JSON")
    else:
        print("✕ valid JSON")
        encountered_errors = True

    for table_schema in TABLE_SCHEMA_PATHS:
        print(f"\n{table_schema.name}")

        schema_json = load_json(table_schema)
        if schema_json is not None:
            schema_descriptors[table_schema] = schema_json
            print("✔︎ valid JSON")
            if validate_schema(table_schema):
                print("✔︎ valid Table Schema")
            else:
                print("✕ valid Table Schema, errors:")
                for err in get_schema_metadata_error_messages(table_schema):
                    print(f"\t - {err}")
                encountered_errors = True
        else:
            print("✕ valid JSON")
            encountered_errors = True

    print("\nSchema coherence")
    if check_schema_coherence(schema_descriptors):
        print("✔︎ schema coherence checks passed")
    else:
        encountered_errors = True

    print("\nData Package v2 spellings")
    if check_v2_spellings(schema_descriptors):
        print("✔︎ table schemas use the v2 spelling of `fieldsMatch` and keys")
    else:
        encountered_errors = True

    print("\nCategories")
    if check_categories(schema_descriptors):
        print("✔︎ `categories` and `enum` agree")
    else:
        encountered_errors = True

    print(f"\n{EXAMPLE_PACKAGE_PATH.parent.name}/{EXAMPLE_PACKAGE_PATH.name}")
    if profile_json is None or not check_example_package(profile_json):
        encountered_errors = True

    if encountered_errors:
        print("Errors were encountered")
        sys.exit(1)
    else:
        print("\nAll good!")
        sys.exit(0)
