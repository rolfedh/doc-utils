# Find Unused AsciiDoc Attributes

This tool scans a user-specified attributes file (typically named `attributes.adoc`) for attribute definitions (e.g., `:version: 1.1`). It then recursively scans all `.adoc` files in the current directory (ignoring symlinks) for usages of those attributes (e.g., `{version}`).

Any attribute defined in the attributes file but not used in any `.adoc` file is reported as **NOT USED** in both the command line output and a timestamped output file (if requested).

## Installation

After installing the package from PyPI:

```sh
pip install rolfedh-doc-utils
```

You can run the tool from anywhere using:

```sh
find-unused-attributes attributes.adoc [-o|--output]
```

Or, if running from source:

```sh
python3 find_unused_attributes.py attributes.adoc [-o|--output]
```

## Example

Suppose `attributes.adoc` contains:

```
:version: 1.1
:product: MyApp
:unused: something
```

And your `.adoc` files use `{version}` and `{product}` but not `{unused}`. The output will be:

```
Unused attributes:
:unused:  NOT USED
```

If you use `-o`, a file like `~/unused_attributes_20250611123456.txt` will be created with the same content.

## Notes

- Only `.adoc` files in the current directory and its subdirectories are scanned.
- Symlinks are ignored.
- Attribute names are matched as `{name}` in `.adoc` files.
- The script does not modify any files.

---

See the main [README.md](README.md) for more details on installation and usage as a package.
