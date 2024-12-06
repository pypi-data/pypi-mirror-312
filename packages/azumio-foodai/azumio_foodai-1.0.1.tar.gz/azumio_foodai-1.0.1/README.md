# Food AI 

Instant Food Recognition

## Installation

```
pip install azumio-foodai
```

## Usage

**Import lib**

```python
from azumio_foodai import FoodAI
```

1. **Load image**
Must be PIL image

```python
from PIL import Image
img = Image.open("path_to_image.jpg")
```

2. **Recognize image**

Create environment variable
`export FOODAI_API_KEY=abc`

Direct call: 
```
from azumio_foodai import FoodAI
foodai.analyze(img)
```

or intialize client with api key: 
```python
client = FoodAI(api_key="abc")
client.analyze(img)
```

or with optional parameters:
```python
client.analyze(img, top=5) # top 5 results
```

## Development

```
pip install -e .
```

Running tests:
```
python -m unittest test_foodai.py
```