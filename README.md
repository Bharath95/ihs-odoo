# ihs-odoo Project

This is our custom Odoo project. All custom modules go into `custom_addons/`.

- Odoo source code(18.0) should be cloned and placed in the `odoo/` directory (ignored by git).
- Project-level configs and scripts are tracked in this repo.
- Used `.gitignore` to keep Odoo and other unnecessary files out of version control.

## Project Features

- Debugger support is pre-configured for easier development.
- The `custom_addons` path is linked and ready for your custom modules.
- Ruff linter is enforced both locally (via pre-commit) and in CI (via GitHub Actions) to maintain code quality.
- GitHub Actions workflow is set up for automated linting on every push and pull request.

## Future Improvements

- GitHub Action workflow for automated testing (Actionflow) will be added soon.

## Cloning the Repository & Setting Up Odoo Source

1. **Clone this repository:**
   ```sh
   git clone git@github.com:Bharath95/ihs-odoo.git
   cd ihs-odoo
   ```

2. **Download the Odoo source code (for example, Odoo 18.0):**
   ```sh
   git clone --depth 1 --branch 18.0 https://github.com/odoo/odoo.git odoo
   ```
   - This will place the Odoo source in the `odoo/` directory, which is ignored by git.
   - You can change the version by modifying the `--branch` parameter (e.g., `16.0`, `17.0`, etc.).

## PostgreSQL Setup

Before running Odoo, make sure you have PostgreSQL running and a database/user created with the credentials specified in `odoo.conf`:

- **Database user:** odoo
- **Database password:** odoo
- **Database name:** ihs_root

You can create the user and database with the following commands (run as a user with permission to manage PostgreSQL, e.g., via `psql`):

```sh
# Start PostgreSQL service (if not already running)
# On macOS (Homebrew):
brew services start postgresql
# On Linux (systemd):
sudo service postgresql start

# Open the PostgreSQL shell (as the postgres user)
sudo -u postgres psql

# Inside the psql shell, run:
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE ihs_root OWNER odoo;
# Optionally, grant privileges:
ALTER ROLE odoo SUPERUSER;
\q
```

Make sure these values match your `odoo.conf` file. You can change the database name, user, or password as needed, but update both `odoo.conf` and your PostgreSQL setup to match.

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

## Checking and Formatting Code Locally

You can check your code for errors and style issues at any time using Ruff:

```sh
ruff check .
```

To automatically fix and format your code, run:

```sh
ruff check . --fix
```

If you want to apply even more aggressive ("unsafe") fixes, use:

```sh
ruff check . --fix --unsafe-fixes
```

It's a good habit to run these commands before committing your changes!

### Formatting Code with Ruff

You can also use Ruff's dedicated formatter to automatically format your code according to standard conventions:

```sh
ruff format .
```

This command will reformat all Python files in your project for consistent style (similar to tools like Black).

---
