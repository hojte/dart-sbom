import json
import yaml
import requests
import argparse

def parse_pubspec_lock(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def fetch_component_info(package_name, package_version):
    # Fetch package info from pub.dev API
    url = f"https://pub.dev/api/packages/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            version_info = next((v for v in data['versions'] if v['version'] == package_version), None)
            if version_info:
                pubspec = version_info.get('pubspec', {})
                supplier = pubspec.get('author', None)
                hash_info = version_info.get('archive_sha256', None)
                repository = pubspec.get('repository', pubspec.get('homepage', None))
                description = pubspec.get('description', None)
                return supplier, hash_info, repository, description
        except (yaml.YAMLError, ValueError, KeyError):
            pass
    return None, None, None, None

def generate_sbom(dependencies):
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "components": []
    }
    for name, details in dependencies.items():
        supplier, hash_info, repository, description = fetch_component_info(name, details["version"])
        component = {
            "type": "library",
            "name": name,
            "version": details["version"],
            "purl": f"pkg:dart/{name}@{details['version']}",
        }
        if supplier:
            component["supplier"] = {"name": supplier}
        if hash_info:
            component["hashes"] = [{"alg": "SHA-256", "content": hash_info}]
        if repository:
            component["externalReferences"] = [{"type": "vcs", "url": repository}]
        if description:
            component["description"] = description

        sbom["components"].append(component)
    return sbom

def main():
    parser = argparse.ArgumentParser(description="Generate SBOM for Dart dependencies in a Flutter project.")
    parser.add_argument("pubspec_lock_path", help="Path to the pubspec.lock file")
    args = parser.parse_args()

    dependencies = parse_pubspec_lock(args.pubspec_lock_path)['packages']
    sbom = generate_sbom(dependencies)

    with open('bom.json', 'w') as file:
        json.dump(sbom, file, indent=2)

    print("SBOM generation completed. Output written to bom.json")

if __name__ == "__main__":
    main()
    
