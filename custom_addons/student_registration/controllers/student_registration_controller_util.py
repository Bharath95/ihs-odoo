
import base64
import logging

from odoo import exceptions
from odoo.http import request

_logger = logging.getLogger(__name__)

def get_latest_student_record_for_logged_in_user():
    """Get the latest student registration record for the logged-in user."""
    user = request.env.user
    student_reg = request.env["student.registration"].sudo().search([
        ("user_id", "=", user.id),
        ("active", "=", True),
    ], order="create_date desc", limit=1)

    if not student_reg:
        raise exceptions.AccessError("No student record found for the logged-in user.")

    return student_reg

def render_error_template(error_message):
    """Render an error template with the given message."""
    return request.render("student_registration.registration_error_template", {
        "error_message": error_message,
    })

def get_string_value(field_name, post):
    """Get a string value from the post data."""
    value = post.get(field_name)
    return value if value else ""

def get_numeric_value(field_name, post):
    """Get a numeric value from the post data."""
    value = post.get(field_name, "")
    if value:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    return None

def get_boolean_value(field_name, post):
    """Get a boolean value from the post data."""
    value = post.get(field_name)
    if isinstance(value, bool):
        return value
    return value == "yes" if value in ("yes", "no") else False

def upload_file(ir_attachment, file_data, model_name, field_name, res_id, is_required=False):
    """Upload a file attachment."""
    if not file_data:
        if is_required:
            raise exceptions.ValidationError(f"Missing {field_name} file")
        return

    try:
        file_content = file_data.read()

        if not file_content:
            if is_required:
                raise exceptions.ValidationError(f"Empty {field_name} file")
            return

        # Create attachment
        attachment_vals = {
            "name": file_data.filename,
            "datas": base64.b64encode(file_content),
            "res_model": model_name,
            "res_field": field_name,
            "res_id": res_id,
            "type": "binary",
        }

        # Check if attachment already exists and update or create
        existing_attachment = ir_attachment.search([
            ("res_model", "=", model_name),
            ("res_field", "=", field_name),
            ("res_id", "=", res_id),
        ], limit=1)

        if existing_attachment:
            existing_attachment.write(attachment_vals)
        else:
            ir_attachment.create(attachment_vals)

    except Exception as e:
        _logger.error(f"Error uploading {field_name} file", exc_info=True)
        raise exceptions.UserError(f"Failed to upload {field_name} file: {e!s}")
