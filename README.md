<p align="center">
    <em>Simple CRUD - Created by and for FastAPI users</em>
</p>
<p align="center">
<img src="https://img.shields.io/github/last-commit/Kludex/simplecrud.svg">
<a href="https://codecov.io/gh/Kludex/simplecrud" target="_blank">
    <img src="https://codecov.io/gh/Kludex/simplecrud/branch/main/graph/badge.svg?token=J6D4HJ4G9X" alt="Coverage">
</a>
<a href="https://pypi.org/project/simplecrud" target="_blank">
    <img src="https://badge.fury.io/py/simplecrud.svg" alt="Package version">
</a>
    <img src="https://img.shields.io/pypi/pyversions/simplecrud.svg">
    <img src="https://img.shields.io/github/license/Kludex/simplecrud.svg">
</p>

---

Package based on the FastAPI [cookiecutter](https://github.com/cookiecutter/cookiecutter) [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py)

---

## Installation

```bash
pip install simplecrud
```

## Usage

The simplest example is as follow:

```python
from simplecrud.sync_sqlalchemy import CRUDBase

from app.models import User
from app.schemas import UserInDB, UserUpdate

crud_user = CRUDBase[User, UserInDB, UserUpdate](User)
```

If you want to see a full example, you can check the `examples/simple_api`.

Alternately, you can run the app on a `uvicorn` server:

```bash
uvicorn examples.simple_api.main:app --reload
```

## License

This project is licensed under the terms of the MIT license.
