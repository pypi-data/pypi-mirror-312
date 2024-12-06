# Promuet

[![PyPI - Version](https://img.shields.io/pypi/v/promuet.svg)](https://pypi.org/project/promuet)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/promuet)](https://pypi.org/project/promuet)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/promuet.svg)](https://pypi.org/project/promuet)

*A simple yet powerful prompt templating engine*

Promuet is a simple Python library for designing complex chains of prompts using basic prompt templates. See below for an example.

## Example Usage

At the core, Promuet is just 

```python
template = TemplateMatchItem(
    """
        Task {{task_number:int}}: {{task_title}}
        Description: {{task_description}}

        Verification: {{task_verification_items:list}}
    """
)
input_string = """
    Task 12: Clean the house
    Description:
    I need to clean the house to make it nice.

    The floors need to be cleaned, the rugs vacuumed, and the laundry folded.

    Verification:
    - Floors should have no dust
    - Rugs should be free of dirt
    - Laundry should be folded
"""
data = template.parse(input_string)
assert data['.str'].strip() == textwrap.dedent(input_string).strip()
data = extract_data_vars(data)
assert data == dict(
    task_number=12,
    task_title='Clean the house',
    task_description='I need to clean the house to make it nice.\n\nThe floors need to be cleaned, the rugs vacuumed, and the laundry folded.',
    task_verification_items=[
        'Floors should have no dust',
        'Rugs should be free of dirt',
        'Laundry should be folded',
    ],
)
```


## Installation

```console
pip install promuet
```

## License

`promuet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
