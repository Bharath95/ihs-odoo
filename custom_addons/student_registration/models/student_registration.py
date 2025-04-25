from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .constants import (
    APPLICATION_STAGES,
    BLOOD_GROUP_SELECTION,
    COMMUNITY_SELECTION,
    GENDER_SELECTION,
    RELIGION_SELECTION,
    YES_NO_SELECTION,
)


class StudentRegistration(models.Model):
    _name = "student.registration"
    _description = "Student Registration"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "create_date desc"

    name = fields.Char("Registration Number", readonly=True, index=True, copy=False, default=lambda self: _("New"))
    active = fields.Boolean(default=True)
    student_profile_id = fields.Many2one("student.profile", string="Student Profile", ondelete="restrict")

    # Application Details
    application_year = fields.Char("Application Academic Year", required=True, tracking=True)
    applied_for = fields.Char("Applied For Grade", required=True, tracking=True)
    applicant_user = fields.Many2one("res.users", string="Applicant User")

    # Previous Application
    applied_to_ihs_before = fields.Selection(YES_NO_SELECTION, string="Applied to IHS Before", default="no", tracking=True)
    previous_application_application_year = fields.Char("Previous Application Year")
    previous_application_applied_for = fields.Char("Previous Application Grade")
    previous_application_remarks = fields.Text("Previous Application Remarks")

    # Personal Information
    full_name = fields.Char("Full Name", required=True, tracking=True)
    gender = fields.Selection(GENDER_SELECTION, string="Gender", tracking=True)
    other_gender = fields.Char("Other Gender")
    nationality = fields.Many2one("res.country", string="Nationality", tracking=True)
    country_of_residence = fields.Many2one("res.country", string="Country of Residence")
    country = fields.Many2one("res.country", string="Country of Birth")
    date_of_birth = fields.Date("Date of Birth", tracking=True)
    age = fields.Integer("Age", compute="_compute_age", store=True)

    # Communication Address
    comm_address_country = fields.Many2one("res.country", string="Address Country")
    comm_address_area_code = fields.Char("Area Code/Pincode")
    comm_address_line_1 = fields.Char("Address Line 1")
    comm_address_line_2 = fields.Char("Address Line 2")
    comm_address_city = fields.Char("City/Town")
    comm_address_state = fields.Many2one("res.country.state", string="State")

    # Other Personal Information
    identification_mark_1 = fields.Char("Identification Mark 1")
    identification_mark_2 = fields.Char("Identification Mark 2")
    religion = fields.Selection(RELIGION_SELECTION, string="Religion")
    other_religion = fields.Char("Other Religion")
    community = fields.Selection(COMMUNITY_SELECTION, string="Community")
    other_community = fields.Char("Other Community")

    # Languages
    mother_tongue = fields.Char("Mother Tongue")
    second_language = fields.Char("Second Language")
    third_language = fields.Char("Third Language")

    # Sibling Information
    has_sibling_in_ihs = fields.Selection(YES_NO_SELECTION, string="Has Sibling in IHS", default="no")
    sibling_1_full_name = fields.Char("Sibling 1 Name")
    sibling_1_grade_status = fields.Char("Sibling 1 Grade/Status")
    sibling_1_school_name = fields.Char("Sibling 1 School Name")

    # Supporting Documents
    recent_photograph = fields.Binary("Recent Photograph", attachment=True)
    birth_certificate = fields.Binary("Birth Certificate", attachment=True)
    id_proof = fields.Selection([
        ("aadhaar", "Aadhaar Card"),
        ("passport", "Passport"),
    ], string="ID Proof Type")
    id_proof_document = fields.Binary("ID Proof Document", attachment=True)

    # ID Proof Details
    aadhaar_number = fields.Char("Aadhaar Number")
    passport_number = fields.Char("Passport Number")
    place_of_issue = fields.Char("Place of Issue")
    date_of_issue = fields.Date("Date of Issue")
    date_of_expiry = fields.Date("Date of Expiry")

    # Current/Previous School Information
    is_home_schooled = fields.Selection(YES_NO_SELECTION, string="Is Home Schooled", default="no")
    current_school_name = fields.Char("Current School Name")
    board_affiliation = fields.Char("Board Affiliation")
    phone_number = fields.Char("School Phone Number")
    current_school_country = fields.Many2one("res.country", string="School Country")
    current_school_area_code = fields.Char("School Area Code")
    current_school_city = fields.Char("School City")
    current_school_state = fields.Many2one("res.country.state", string="School State")
    email_address = fields.Char("School Email Address")
    current_school_a_line1 = fields.Char("School Address Line 1")
    current_school_a_line2 = fields.Char("School Address Line 2")

    # Previous School Information
    was_the_applicant_ever_home_schooled = fields.Selection(YES_NO_SELECTION, string="Was Ever Home Schooled", default="no")
    been_to_school_previously = fields.Selection(YES_NO_SELECTION, string="Been to School Previously", default="no")
    emis_id = fields.Char("EMIS ID")

    # More Academic Information
    academic_strengths_and_weaknesses = fields.Text("Academic Strengths and Weaknesses")
    hobbies_interests_and_extra_curricular_activities = fields.Text("Hobbies, Interests and Extra-Curricular Activities")
    other_details_of_importance = fields.Text("Other Details of Importance")
    temperament_and_personality = fields.Text("Temperament and Personality")
    special_learning_needs_or_learning_disability = fields.Text("Special Learning Needs or Learning Disability")

    # Health Information - Vaccines
    done_smallpox_vaccine = fields.Selection(YES_NO_SELECTION, string="Smallpox Vaccine")
    done_hepatitis_a_vaccine = fields.Selection(YES_NO_SELECTION, string="Hepatitis A Vaccine")
    done_hepatitis_b_vaccine = fields.Selection(YES_NO_SELECTION, string="Hepatitis B Vaccine")
    done_tdap_vaccine = fields.Selection(YES_NO_SELECTION, string="Tdap Vaccine")
    done_typhoid_vaccine = fields.Selection(YES_NO_SELECTION, string="Typhoid Vaccine")
    done_measles_vaccine = fields.Selection(YES_NO_SELECTION, string="Measles Vaccine")
    done_polio_vaccine = fields.Selection(YES_NO_SELECTION, string="Polio Vaccine")
    done_mumps_vaccine = fields.Selection(YES_NO_SELECTION, string="Mumps Vaccine")
    done_rubella_vaccine = fields.Selection(YES_NO_SELECTION, string="Rubella Vaccine")
    done_varicella_vaccine = fields.Selection(YES_NO_SELECTION, string="Varicella Vaccine")
    other_vaccines = fields.Text("Other Vaccines")
    vaccine_certificates = fields.Binary("Vaccine Certificates", attachment=True)

    # Additional Health Information
    blood_group = fields.Selection(BLOOD_GROUP_SELECTION, string="Blood Group")
    wears_glasses_or_lens = fields.Selection(YES_NO_SELECTION, string="Wears Glasses or Lens", default="no")
    right_eye_power = fields.Char("Right Eye Power")
    left_eye_power = fields.Char("Left Eye Power")
    is_toilet_trained = fields.Selection(YES_NO_SELECTION, string="Is Toilet Trained")
    wets_bed = fields.Selection(YES_NO_SELECTION, string="Wets Bed")

    # Physical and Mental Health Information
    has_hearing_challenges = fields.Selection(YES_NO_SELECTION, string="Has Hearing Challenges", default="no")
    hearing_challenges = fields.Text("Hearing Challenges Details")
    has_behavioural_challenges = fields.Selection(YES_NO_SELECTION, string="Has Behavioural Challenges", default="no")
    behavioural_callenges = fields.Text("Behavioural Challenges Details")
    has_physical_challenges = fields.Selection(YES_NO_SELECTION, string="Has Physical Challenges", default="no")
    physical_challenges = fields.Text("Physical Challenges Details")
    has_speech_challenges = fields.Selection(YES_NO_SELECTION, string="Has Speech Challenges", default="no")
    speech_challenges = fields.Text("Speech Challenges Details")

    # Other Medical Information
    has_injury = fields.Selection(YES_NO_SELECTION, string="Has Injury History", default="no")
    injury_details = fields.Text("Injury Details")
    on_medication = fields.Selection(YES_NO_SELECTION, string="On Medication", default="no")
    medicaton_details = fields.Text("Medication Details")
    medical_prescription = fields.Binary("Medical Prescription", attachment=True)
    has_health_issue = fields.Selection(YES_NO_SELECTION, string="Has Health Issues", default="no")
    health_issue_details = fields.Text("Health Issue Details")
    was_hospitalized = fields.Selection(YES_NO_SELECTION, string="Was Hospitalized", default="no")
    hospitalization_details = fields.Text("Hospitalization Details")
    needs_special_attention = fields.Selection(YES_NO_SELECTION, string="Needs Special Attention", default="no")
    attention_details = fields.Text("Special Attention Details")

    # Allergies
    has_alergies = fields.Selection(YES_NO_SELECTION, string="Has Allergies", default="no")
    allergy_details = fields.Text("Allergy Details")

    # Application Status
    application_stage = fields.Selection(
        APPLICATION_STAGES,
        string="Application Stage",
        default="draft",
        tracking=True,
    )

    # Dates
    submission_date = fields.Datetime("Submission Date")
    review_date = fields.Datetime("Review Date")
    decision_date = fields.Datetime("Decision Date")

    # User reference
    user_id = fields.Many2one("res.users", string="Related User", index=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("student.registration") or _("New")
        return super(StudentRegistration, self).create(vals_list)

    def action_submit_application(self):
        self.ensure_one()
        if not self.student_profile_id:
            # Create student profile if it doesn't exist
            profile_vals = {
                "student_reg_id": self.id,
                "full_name": self.full_name,
                "gender": self.gender,
                "date_of_birth": self.date_of_birth,
                "nationality_id": self.nationality.id if self.nationality else False,
            }
            profile = self.env["student.profile"].create(profile_vals)
            self.student_profile_id = profile.id

        self.write({
            "application_stage": "submitted",
            "submission_date": fields.Datetime.now(),
            "registration_complete": True,
        })

        # Send notification email
        template = self.env.ref("student_registration.email_template_application_submitted", raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

        return True

    def action_review_application(self):
        self.ensure_one()
        self.write({
            "application_stage": "under_review",
            "review_date": fields.Datetime.now(),
        })
        return True

    def action_approve_application(self):
        self.ensure_one()
        self.write({
            "application_stage": "approved",
            "decision_date": fields.Datetime.now(),
        })

        # Send acceptance email
        template = self.env.ref("student_registration.email_template_application_approved", raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

        return True

    def action_reject_application(self):
        self.ensure_one()
        self.write({
            "application_stage": "rejected",
            "decision_date": fields.Datetime.now(),
        })

        # Send rejection email
        template = self.env.ref("student_registration.email_template_application_rejected", raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

        return True

    @api.constrains("date_of_birth")
    def _check_date_of_birth(self) -> None:
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError(_("Date of birth cannot be in the future."))
