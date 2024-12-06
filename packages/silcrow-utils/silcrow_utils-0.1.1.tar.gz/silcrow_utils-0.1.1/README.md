# silcrow-utils
A package for housing all my personalized python functions and classes, made available via pip install.

# To User
```
# main.py
from silcrow_utils.module1 import hello_Bubu

if __name__ == '__main__':
    result = hello_Bubu()
    print(result)
```

# To Dev

## Each Release

Don't forget to increment the version number, then:
```zsh
pip install build twine
python -m build
twine upload dist/*
```

## Might do
- [ ] use poetry instead of requirements.txt, edit setup.py accordingly. 