# ihs-odoo Project

This is your custom Odoo project. All custom modules go into `custom_addons/`.

- Odoo source code should be placed in the `odoo/` directory (ignored by git).
- Project-level configs and scripts are tracked in this repo.
- Use `.gitignore` to keep Odoo and other unnecessary files out of version control.

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install all dependencies:**
   ```sh
   pip3 install -r requirements.txt
   ```

3. **(First time only) Install pre-commit hooks:**
   ```sh
   pre-commit install
   ```

Now, every time you commit, Ruff will automatically lint your code and block commits if there are any errors.

---
