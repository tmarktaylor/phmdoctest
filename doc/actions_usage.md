# Snippet of use in GitHub Actions
```yaml
jobs:
  venv_tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.x
      uses: actions/setup-python@v2
      with:
        python-version: 3.x
    - name: Windows Venv
      run: |
        python -m venv ${{ github.workspace }}\env
        ${{ github.workspace }}\env\Scripts\Activate.ps1
        python -m pip --version
      if: startswith(runner.os, 'Windows')
    - name: Linux/macOS Venv
      run: |
        python -m venv ${{ github.workspace }}/env
        source ${{ github.workspace }}/env/bin/activate
        python -m pip --version
      if: startswith(runner.os, 'Linux') || startswith(runner.os, 'macOS')
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install --no-deps "."
        python -m pip install -r requirements.txt
        python -m pip install "pytest>=6"
    - name: Tests
      run: |
        # The next line creates the tmp subdirectory in tests.
        python -c "from pathlib import Path; d = Path('tests') / 'tmp'; d.mkdir()"
        phmdoctest project.md --report --outfile tests/tmp/test_project.py
        pytest --doctest-modules -vv tests
```