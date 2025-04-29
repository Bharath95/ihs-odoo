# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, Response
import logging
import json

_logger = logging.getLogger(__name__)

ALLOWED_ORIGIN = 'http://localhost:5173'

class StudentAdmissionController(http.Controller):

    def _prepare_cors_headers(self):
        """Helper method to generate standard CORS headers."""
        return {
            'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }

    @http.route('/student-admission/create', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def create_student_admission_http(self, **kw):
        cors_headers = self._prepare_cors_headers()

        if request.httprequest.method == 'OPTIONS':
            return Response(status=204, headers=cors_headers)

        if request.httprequest.method == 'POST':
            vals = {}
            try:
                # --- JSON Parsing ---
                body = request.httprequest.data
                body_str = body.decode('utf-8')
                vals = json.loads(body_str)
                _logger.info("Received student admission data via HTTP API (first 500 chars): %s", str(vals)[:500]) # Log truncated data

                # --- If JSON parsing succeeds, continue inside the try block ---

                # --- Server-Side Data Validation ---
                required_fields = ['full_name', 'application_year', 'applied_for', 'date_of_birth']
                missing_fields = [field for field in required_fields if not vals.get(field)]
                if missing_fields:
                    error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                    _logger.error(error_msg)
                    request.env.cr.rollback()
                    error_body = json.dumps({'success': False, 'error': error_msg})
                    return Response(error_body, status=400, headers=cors_headers, content_type='application/json')

                # --- Data Preparation for Odoo Create ---
                vals_copy = vals.copy()

                # Process binary fields
                binary_fields = [
                    'recent_photograph', 'birth_certificate', 'id_proof_document',
                    'vaccine_certificates', 'medical_prescription', 'court_order_document',
                    'legal_rights_document'
                ]
                for field_name in binary_fields:
                    if field_name in vals_copy and isinstance(vals_copy[field_name], str) and not vals_copy[field_name]:
                        vals_copy[field_name] = False
                    filename_field = f"{field_name}_filename"
                    if field_name in vals_copy and vals_copy[field_name] and filename_field not in vals_copy:
                        vals_copy[filename_field] = f"uploaded_{field_name}.bin"
                        _logger.warning(f"Filename field '{filename_field}' missing for binary field '{field_name}'. Using default.")

                # Remove fields not in the Odoo model
                fields_to_remove = [
                    'optional_language_table', 'previous_schools',
                    'guardian_information', 'payment_program_links',
                    'board_affiliation'
                ]
                for f in fields_to_remove:
                    vals_copy.pop(f, None)

                # Convert empty strings for Date fields to False (NULL)
                date_fields = [
                    'date_of_birth', 'date_of_issue', 'date_of_expiry', 'date'
                ]
                for date_field in date_fields:
                    if date_field in vals_copy and vals_copy[date_field] == '':
                        _logger.info(f"Converting empty string for date field '{date_field}' to False.")
                        vals_copy[date_field] = False

                # --- Create the Odoo Record ---
                # This is now also inside the main try block
                new_admission = request.env['student.admission'].sudo().create(vals_copy)
                _logger.info(f"Successfully created student admission record with ID: {new_admission.id}")

                # Prepare and return success response
                success_body = json.dumps({
                    'success': True,
                    'message': 'Registration submitted successfully!',
                    'registration_id': new_admission.id
                })
                return Response(success_body, status=200, headers=cors_headers, content_type='application/json')

            # Exception handling block starts here
            except json.JSONDecodeError as e:
                _logger.error("Error parsing JSON request body (JSONDecodeError): %s", e)
                error_body = json.dumps({'success': False, 'error': 'Invalid JSON data format'})
                return Response(error_body, status=400, headers=cors_headers, content_type='application/json')
            except Exception as e:
                # Catch other errors during parsing OR during validation/prep/create
                _logger.exception("Error processing student admission request:") # Use .exception to log traceback
                request.env.cr.rollback() # Rollback on any error after parsing
                error_body = json.dumps({'success': False, 'error': 'Internal Server Error'})
                return Response(error_body, status=500, headers=cors_headers, content_type='application/json')

        # Fallback for other methods
        return Response('Method Not Allowed', status=405, headers=cors_headers)