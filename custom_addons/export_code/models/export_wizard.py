from __future__ import annotations

from pathlib import Path

from odoo import models


class ExportCodeWizard(models.TransientModel):
    _name = "export.code.wizard"
    _description = "Export UI changes to files"

    def action_export(self) -> None:
        """Sync UI edits: export views, export fields, then prune stale files."""
        expected_views = self._export_views()
        expected_fields = self._export_fields()
        self._prune_stale_files(expected_views, expected_fields)

    def _export_views(self) -> dict[str, set[str]]:
        """Export modified UI views to XML files per module."""
        expected: dict[str, set[str]] = {}
        views = self.env["ir.ui.view"].search([("arch_db", "!=", False)])
        for view in views:
            md = (
                self.env["ir.model.data"]
                .sudo()
                .search(
                    [("model", "=", "ir.ui.view"), ("res_id", "=", view.id)],
                    limit=1,
                )
            )
            if not md or not md.module:
                continue
            module_dir = self._find_module_path(md.module)
            if module_dir is None:
                continue
            views_dir = module_dir / "views"
            views_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{md.name}.xml"
            filepath = views_dir / filename
            filepath.write_text(
                '<?xml version="1.0"?>\n<odoo>\n  <data>\n'
                + view.arch_db
                + "\n  </data>\n</odoo>",
                encoding="utf-8",
            )
            expected.setdefault(md.module, set()).add(filename)
        return expected

    def _export_fields(self) -> dict[str, set[str]]:
        """Export manual fields to Python stub files per module."""
        expected: dict[str, set[str]] = {}
        fields = self.env["ir.model.fields"].search([("state", "=", "manual")])
        for fld in fields:
            md = (
                self.env["ir.model.data"]
                .sudo()
                .search(
                    [("model", "=", "ir.model.fields"), ("res_id", "=", fld.id)],
                    limit=1,
                )
            )
            if not md or not md.module:
                continue
            module_dir = self._find_module_path(md.module)
            if module_dir is None:
                continue
            models_dir = module_dir / "models"
            models_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{md.name}_fields.py"
            filepath = models_dir / filename
            cls_name = fld.model_id.model.replace(".", "_").title().replace("_", "")
            content = (
                "from odoo import fields, models\n\n"
                f"class {cls_name}(models.Model):\n"
                f'    _inherit = "{fld.model_id.model}"\n'
                f"    {fld.name} = fields.{fld.ttype.title()}()\n"
            )
            filepath.write_text(content, encoding="utf-8")
            expected.setdefault(md.module, set()).add(filename)
        return expected

    def _prune_stale_files(  # noqa: C901
        self,
        expected_views: dict[str, set[str]],
        expected_fields: dict[str, set[str]],
    ) -> None:
        """Remove files for views/fields that no longer exist in the database."""
        for module, files in expected_views.items():
            module_dir = self._find_module_path(module)
            if module_dir is None:
                continue
            views_dir = module_dir / "views"
            if views_dir.is_dir():
                for file in views_dir.iterdir():
                    if file.suffix == ".xml" and file.name not in files:
                        file.unlink()
        for module, files in expected_fields.items():
            module_dir = self._find_module_path(module)
            if module_dir is None:
                continue
            models_dir = module_dir / "models"
            if models_dir.is_dir():
                for file in models_dir.iterdir():
                    if file.name.endswith("_fields.py") and file.name not in files:
                        file.unlink()

    def _find_module_path(self, module_name: str) -> Path | None:
        """Return the filesystem Path of a module, or None if not found."""
        addons = self.env["ir.config_parameter"].sudo().get_param("addons_path", "")
        for path_str in addons.split(","):
            candidate = Path(path_str.strip()) / module_name
            if candidate.is_dir():
                return candidate
        return None
