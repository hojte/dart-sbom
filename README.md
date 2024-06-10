# dart-sbom
Generate minimilistic SBOMs for pubspec lock files

```
python3 sbom_gen.py ./path_to_pubspec.lock
```

## Example result
```
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "version": 1,
  "components": [
    {
          "type": "library",
          "name": "async",
          "version": "2.11.0",
          "purl": "pkg:dart/async@2.11.0",
          "hashes": [
            {
              "alg": "SHA-256",
              "content": "947bfcf187f74dbc5e146c9eb9c0f10c9f8b30743e341481c1e2ed3ecc18c20c"
            }
          ],
          "externalReferences": [
            {
              "type": "repository",
              "url": "https://github.com/dart-lang/async"
            }
          ],
          "description": "Utility functions and classes related to the 'dart:async' library."
    }
  ]
}
```
