# install

```bash
pip install -r requirements.txt
```

# run

```bash
source. venv/bin/activate
uvicorn src.api.main:app --reload
```

# run tests
```
pytest
```
#watch tests
```
ptw
```

# linting
```bash
# Check your code
ruff check .

# Auto-fix issues when possible
ruff check --fix .
```