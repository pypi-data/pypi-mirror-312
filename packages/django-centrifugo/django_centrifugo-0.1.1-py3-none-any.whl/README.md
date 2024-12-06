# django-centrifugo

[![GitHub Actions](https://github.com/pikhovkin/django-centrifugo/actions/workflows/tests.yaml/badge.svg)](https://github.com/pikhovkin/django-centrifugo/actions)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/pikhovkin/dc6f561d32b4e4e6d6f05bfd59c4ffaf/raw/covbadge.json)
[![PyPI - Version](https://img.shields.io/pypi/v/django-centrifugo.svg)](https://pypi.org/project/django-centrifugo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-centrifugo.svg)](https://pypi.org/project/django-centrifugo)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-centrifugo.svg)](https://pypi.org/project/django-centrifugo)
[![PyPI - License](https://img.shields.io/pypi/l/django-centrifugo.svg)](./LICENSE)

[![framework - Django](https://img.shields.io/badge/framework-Django-0C3C26.svg)](https://www.djangoproject.com/)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-FFDD00?logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/pikhovkin)
[![Support me](https://img.shields.io/badge/Support%20me-F16061?logo=ko-fi&logoColor=white&labelColor=F16061)](https://ko-fi.com/pikhovkin)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?logo=patreon)](https://patreon.com/pikhovkin)
[![Liberapay](https://img.shields.io/badge/Liberapay-F6C915?logo=liberapay&logoColor=black)](https://liberapay.com/pikhovkin)

Implementation of an outbox model for [Centrifugo](https://centrifugal.dev/docs/tutorial/outbox_cdc).

### Installation

```console
pip install django-centrifugo
```

### Usage

1. Install the package

2. Add `django_centrifugo` to your `INSTALLED_APPS` settings like this:

```python
INSTALLED_APPS = [
    ...,
    'django_centrifugo',
    ...,
]
```

## License

MIT
