# How to deploy new package version

## 1. Tag new version
* Update [`pyproject.toml`](./pyproject.toml) with new version
* Merge work to main branch
* Create [new release on GitHub](https://github.com/Max-Derner/colour_fx/releases/new)

## 2. Create new distribution
* Run `python3 -m build`

## 3. Upload to [test PyPI](https://test.pypi.org/)
* `python3 -m twine upload --repository testpypi dist/*`

