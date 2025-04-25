
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .constants import (
    BLOOD_GROUP_SELECTION,
    COMMUNITY_SELECTION,
    GENDER_SELECTION,
    GROUP_A_SELECTION,
    GROUP_B_SELECTION,
    GROUP_C_SELECTION,
    GROUP_D_SELECTION,
    MARITAL_STATUS_SELECTION,
    PARENT_PERMISSION_SELECTION,
    RELIGION_SELECTION,
    YES_NO_SELECTION,
)


class StudentProfile(models.Model):
    _name = "student.profile"
    _description = "Student Profile"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "full_name"

    student_reg_id = fields.Many2one("student.registration", string="Registration", ondelete="cascade")

    # Personal Information (mirrored from registration for easy access)
    full_name = fields.Char("Full Name", required=True, tracking=True)
    gender = fields.Selection(GENDER_SELECTION, string="Gender", tracking=True)
    date_of_birth = fields.Date("Date of Birth", tracking=True)
    age = fields.Integer("Age", compute="_compute_age", store=True)
    blood_group = fields.Selection(BLOOD_GROUP_SELECTION, string="Blood Group")
    religion = fields.Selection(RELIGION_SELECTION, string="Religion")
    other_religion = fields.Char("Other Religion")
    community = fields.Selection(COMMUNITY_SELECTION, string="Community")
    other_community = fields.Char("Other Community")
    nationality_id = fields.Many2one("res.country", string="Nationality")
    country_of_residence_id = fields.Many2one("res.country", string="Country of Residence")
    country_of_birth_id = fields.Many2one("res.country", string="Country of Birth")

    # Identification Marks
    identification_mark_1 = fields.Char("Identification Mark 1")
    identification_mark_2 = fields.Char("Identification Mark 2")

    # Has name changed
    has_name_changed = fields.Selection(YES_NO_SELECTION, string="Has Name Changed", default="no")
    previous_name = fields.Char("Previous Name")

    # Address & Contact
    address_line_1 = fields.Char("Address Line 1", tracking=True)
    address_line_2 = fields.Char("Address Line 2")
    city = fields.Char("City/Town")
    state_id = fields.Many2one("res.country.state", string="State")
    area_code = fields.Char("Area Code/Pincode")
    country_id = fields.Many2one("res.country", string="Country")
    phone = fields.Char("Phone")
    phone_country_code = fields.Char("Phone Country Code")
    mobile = fields.Char("Mobile")
    mobile_country_code = fields.Char("Mobile Country Code")
    is_mobile_same_as_phone = fields.Selection(YES_NO_SELECTION, string="Is Mobile Same as Phone", default="yes")

    # Language Information
    mother_tongue = fields.Char("Mother Tongue")
    second_language = fields.Char("Second Language")
    third_language = fields.Char("Third Language")

    # ID Information
    id_proof_type = fields.Selection([
        ("aadhaar", "Aadhaar Card"),
        ("passport", "Passport"),
    ], string="ID Proof Type")
    id_proof_document = fields.Binary("ID Proof Document", attachment=True)
    aadhaar_number = fields.Char("Aadhaar Number")
    passport_number = fields.Char("Passport Number")
    place_of_issue = fields.Char("Place of Issue")
    date_of_issue = fields.Date("Date of Issue")
    date_of_expiry = fields.Date("Date of Expiry")

    # Sibling Information
    has_sibling_in_ihs = fields.Selection(YES_NO_SELECTION, string="Has Sibling in IHS", default="no")
    sibling_1_full_name = fields.Char("Sibling 1 Name")
    sibling_1_grade_status = fields.Char("Sibling 1 Grade/Status")
    sibling_1_school_name = fields.Char("Sibling 1 School Name")

    # Supporting Documents
    recent_photograph = fields.Binary("Recent Photograph", attachment=True)
    birth_certificate = fields.Binary("Birth Certificate", attachment=True)

    # School Information
    is_home_schooled = fields.Selection(YES_NO_SELECTION, string="Is Home Schooled", default="no")
    current_school_name = fields.Char("Current School Name")
    board_affiliation = fields.Char("Board Affiliation")
    school_phone = fields.Char("School Phone Number")
    school_email = fields.Char("School Email")
    school_address_line_1 = fields.Char("School Address Line 1")
    school_address_line_2 = fields.Char("School Address Line 2")
    school_city = fields.Char("School City")
    school_state_id = fields.Many2one("res.country.state", string="School State")
    school_area_code = fields.Char("School Area Code")
    school_country_id = fields.Many2one("res.country", string="School Country")

    # Previous School Information
    was_ever_home_schooled = fields.Selection(YES_NO_SELECTION, string="Was Ever Home Schooled", default="no")
    been_to_school_previously = fields.Selection(YES_NO_SELECTION, string="Been to School Previously", default="no")
    emis_id = fields.Char("EMIS ID")

    # Academic Information
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

    # Parents & Guardians Information
    mother_full_name = fields.Char("Mother's Full Name")
    mother_email = fields.Char("Mother's Email")
    mother_phone = fields.Char("Mother's Phone")
    mother_occupation = fields.Char("Mother's Occupation")
    mother_education = fields.Char("Mother's Education")

    father_full_name = fields.Char("Father's Full Name")
    father_email = fields.Char("Father's Email")
    father_phone = fields.Char("Father's Phone")
    father_occupation = fields.Char("Father's Occupation")
    father_education = fields.Char("Father's Education")

    parent_marital_status = fields.Selection(MARITAL_STATUS_SELECTION, string="Parent Marital Status")

    # Divorce related fields
    who_is_resposible_for_paying_applicants_tuition_fee = fields.Selection(
        PARENT_PERMISSION_SELECTION,
        string="Who is Responsible for Tuition Fee",
    )
    court_order_document = fields.Binary("Court Order Document", attachment=True)
    who_is_allowed_to_receive_school_communication = fields.Selection(
        PARENT_PERMISSION_SELECTION,
        string="Who Receives School Communication",
    )
    legal_rights_document = fields.Binary("Legal Rights Document", attachment=True)
    who_is_allowed_to_receive_report_cards = fields.Selection(
        PARENT_PERMISSION_SELECTION,
        string="Who Receives Report Cards",
    )
    visit_rights = fields.Selection(
        PARENT_PERMISSION_SELECTION,
        string="Visit Rights",
    )

    # Guardian Information
    parents_are_guardians = fields.Selection(YES_NO_SELECTION, string="Parents are Guardians", default="yes")

    # Class XI Subject Preferences (for higher classes)
    group_a = fields.Selection(GROUP_A_SELECTION, string="Group A Subject")
    group_b = fields.Selection(GROUP_B_SELECTION, string="Group B Subject")
    group_c = fields.Selection(GROUP_C_SELECTION, string="Group C Subject")
    group_d = fields.Selection(GROUP_D_SELECTION, string="Group D Subject")

    # Question Responses
    q1_applicant_response = fields.Text("Applicant Question 1 Response")
    q2_applicant_response = fields.Text("Applicant Question 2 Response")
    q3_applicant_response = fields.Text("Applicant Question 3 Response")
    q4_applicant_response = fields.Text("Applicant Question 4 Response")
    q5_applicant_response = fields.Text("Applicant Question 5 Response")
    q6_applicant_response = fields.Text("Applicant Question 6 Response")
    q7_applicant_response = fields.Text("Applicant Question 7 Response")

    q1_parent_response = fields.Text("Parent Question 1 Response")
    q2_parent_response = fields.Text("Parent Question 2 Response")
    q3_parent_response = fields.Text("Parent Question 3 Response")
    q4_parent_response = fields.Text("Parent Question 4 Response")
    q5_parent_response = fields.Text("Parent Question 5 Response")
    q6_parent_response = fields.Text("Parent Question 6 Response")

    # Declaration and Date
    tnc_check = fields.Boolean("Terms & Conditions Accepted")
    declaration_date = fields.Date("Declaration Date")
    declaration_place = fields.Char("Declaration Place")

    # Billing Information
    billing_name = fields.Char("Billing Name")
    billing_phone = fields.Char("Billing Phone")
    billing_email = fields.Char("Billing Email")
    billing_country_id = fields.Many2one("res.country", string="Billing Country")
    billing_area_code = fields.Char("Billing Area Code")
    billing_city = fields.Char("Billing City")
    billing_state_id = fields.Many2one("res.country.state", string="Billing State")
    billing_address_l1 = fields.Char("Billing Address Line 1")
    billing_address_l2 = fields.Char("Billing Address Line 2")

    # Application Fee Status
    application_fee_status = fields.Selection([
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    ], string="Application Fee Status", default="pending")

    # Related fields
    emergency_contact_ids = fields.One2many("student.emergency.contact", "student_profile_id", string="Emergency Contacts")
    family_detail_ids = fields.One2many("student.family.details", "student_profile_id", string="Family Details")
    previous_school_ids = fields.One2many("student.previous.school", "student_profile_id", string="Previous Schools")
    guardian_ids = fields.One2many("student.guardian", "student_profile_id", string="Guardians")

    # Submission status for each section
    section_1_submitted = fields.Boolean("Personal Info Section Submitted", default=False)
    section_2_submitted = fields.Boolean("Academic Info Section Submitted", default=False)
    section_3_submitted = fields.Boolean("Health Info Section Submitted", default=False)
    section_4_submitted = fields.Boolean("Parent Info Section Submitted", default=False)

    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                delta = today - record.date_of_birth
                record.age = int(delta.days / 365.25)
            else:
                record.age = 0

    @api.constrains("religion", "other_religion")
    def _check_other_religion(self):
        for record in self:
            if record.religion == "other" and not record.other_religion:
                raise ValidationError(_("Please specify the other religion."))

    @api.constrains("community", "other_community")
    def _check_other_community(self):
        for record in self:
            if record.community == "other" and not record.other_community:
                raise ValidationError(_("Please specify the other community."))

class ProofType(models.Model):
    _name = "proof.type"
    _description = "Proof Type"

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")
    description = fields.Text("Description")

class StudentEmergencyContact(models.Model):
    _name = "student.emergency.contact"
    _description = "Student Emergency Contact"

    student_profile_id = fields.Many2one("student.profile", string="Student Profile", ondelete="cascade")
    emergency_type = fields.Selection([
        ("primary", "Primary"),
        ("secondary", "Secondary"),
    ], string="Contact Type", required=True)
    name = fields.Char("Name", required=True)
    relationship = fields.Char("Relationship", required=True)
    phone = fields.Char("Phone", required=True)
    phone_country_code = fields.Char("Phone Country Code")
    email = fields.Char("Email")
    address = fields.Char("Address")

class StudentFamilyDetails(models.Model):
    _name = "student.family.details"
    _description = "Student Family Details"

    student_profile_id = fields.Many2one("student.profile", string="Student Profile", ondelete="cascade")
    relation = fields.Selection([
        ("father", "Father"),
        ("mother", "Mother"),
        ("guardian", "Guardian"),
        ("sibling", "Sibling"),
        ("other", "Other"),
    ], string="Relation", required=True)
    name = fields.Char("Name", required=True)
    gender = fields.Selection(GENDER_SELECTION, string="Gender")
    occupation = fields.Char("Occupation")
    education = fields.Char("Education")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    is_guardian = fields.Boolean("Is Guardian")
    has_custody = fields.Boolean("Has Custody")

class StudentPreviousSchool(models.Model):
    _name = "student.previous.school"
    _description = "Student Previous School"

    student_profile_id = fields.Many2one("student.profile", string="Student Profile", ondelete="cascade")
    name = fields.Char("School Name", required=True)
    address = fields.Char("Address")
    city = fields.Char("City")
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one("res.country", string="Country")
    board_affiliation = fields.Char("Board Affiliation")
    grade = fields.Char("Grade/Class")
    year_from = fields.Char("Year From")
    year_to = fields.Char("Year To")
    reason_for_leaving = fields.Text("Reason for Leaving")

class StudentGuardian(models.Model):
    _name = "student.guardian"
    _description = "Student Guardian"

    student_profile_id = fields.Many2one("student.profile", string="Student Profile", ondelete="cascade")
    name = fields.Char("Name", required=True)
    relation = fields.Char("Relationship", required=True)
    gender = fields.Selection(GENDER_SELECTION, string="Gender")
    occupation = fields.Char("Occupation")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    address = fields.Char("Address")
    city = fields.Char("City")
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one("res.country", string="Country")
    has_custody = fields.Boolean("Has Custody")
