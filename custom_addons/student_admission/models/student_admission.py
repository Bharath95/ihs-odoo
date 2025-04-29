# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64 # Needed for handling binary data if needed later

class StudentAdmission(models.Model):
    _name = 'student.admission'
    _description = 'Student Admission Registration'
    _order = 'create_date desc' # Optional: Default sorting

    # --- Application & Personal Information ---
    application_year = fields.Char(string="Application Academic Year", required=True) # Treat Link as Char for now
    applied_for = fields.Char(string="Applied For Grade", required=True) # Treat Link as Char for now
    applicant_user = fields.Char(string="Applicant User") # Treat Link as Char for now

    applied_to_ihs_before = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
    ], string="Applied to IHS Before?", required=True)
    previous_application_application_year = fields.Char(string="Previous Application Year") # Treat Link as Char
    previous_application_applied_for = fields.Char(string="Previously Applied For Grade") # Treat Link as Char
    previous_application_remarks = fields.Char(string="Previous Application Remarks")

    full_name = fields.Char(string="Full Name", required=True)
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ], string="Gender", required=True)
    other_gender = fields.Char(string="Other Gender Detail")
    nationality = fields.Char(string="Nationality", required=True) # Treat Link as Char
    country_of_residence = fields.Char(string="Country of Residence", required=True) # Treat Link as Char
    country = fields.Char(string="Country of Birth", required=True) # Treat Link as Char
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age") # Keep as Char for simplicity, could be computed later

    # Communication Address
    comm_address_line_1 = fields.Char(string="Address Line 1", required=True)
    comm_address_line_2 = fields.Char(string="Address Line 2")
    comm_address_city = fields.Char(string="City/ Town", required=True)
    comm_address_state = fields.Char(string="State", required=True)
    comm_address_area_code = fields.Char(string="Area Code/ Pincode", required=True)
    comm_address_country = fields.Char(string="Country", required=True) # Redundant? Present above. Keeping based on form.

    # Other Personal Info
    identification_mark_1 = fields.Char(string="Identification Mark 1", required=True)
    identification_mark_2 = fields.Char(string="Identification Mark 2", required=True)
    religion = fields.Selection([
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Sikh', 'Sikh'),
        ('Jew', 'Jew'),
        ('Other', 'Other'),
    ], string="Religion", required=True)
    other_religion = fields.Char(string="Other Religion Detail")
    community = fields.Selection([
        ('OC', 'OC'),
        ('BC', 'BC'),
        ('BC-Others', 'BC-Others'),
        ('MBC', 'MBC'),
        ('SC-Arunthathiyar', 'SC-Arunthathiyar'),
        ('SC-Others', 'SC-Others'),
        ('DNC (Denotified Communities)', 'DNC (Denotified Communities)'),
        ('ST', 'ST'),
        ('Other', 'Other'),
    ], string="Community", required=True)
    other_community = fields.Char(string="Other Community Detail")

    # Languages
    mother_tongue = fields.Char(string="Mother Tongue", required=True)
    second_language = fields.Char(string="Second Language") # Treat Link as Char
    third_language = fields.Char(string="Third Language") # Treat Link as Char
    # optional_language_table -> Skipped (Table field)

    # Sibling Info
    has_sibling_in_ihs = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),
    ], string="Sibling Studying/ Studied in IHS?", required=True)
    sibling_1_full_name = fields.Char(string="Sibling 1 Full Name")
    sibling_1_grade_status = fields.Char(string="Sibling 1 Grade/Status")
    sibling_1_school_name = fields.Char(string="Sibling 1 School Name (if IHS)")

    # Supporting Documents (Binary fields need matching _filename fields)
    recent_photograph = fields.Binary(string="Recent Photograph", attachment=True)
    recent_photograph_filename = fields.Char("Recent Photograph Filename")
    birth_certificate = fields.Binary(string="Birth Certificate", attachment=True)
    birth_certificate_filename = fields.Char("Birth Certificate Filename")
    id_proof = fields.Selection([
        ('Aadhaar Card', 'Aadhaar Card'),
        ('Passport', 'Passport'),
    ], string="ID Proof Type", required=True)
    id_proof_document = fields.Binary(string="ID Proof Document", attachment=True)
    id_proof_document_filename = fields.Char("ID Proof Document Filename")
    aadhaar_number = fields.Char(string="Aadhaar Number")
    passport_number = fields.Char(string="Passport Number")
    place_of_issue = fields.Char(string="Passport Place of Issue")
    date_of_issue = fields.Date(string="Passport Date of Issue")
    date_of_expiry = fields.Date(string="Passport Date of Expiry")

    # --- Academic Information ---
    is_home_schooled = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Currently Home Schooled?", required=True)
    current_school_name = fields.Char(string="Current School Name")
    # board_affiliation = fields.Char(string="Board Affiliation") # This seems unused in form logic?
    board_affiliation_data2 = fields.Char(string="Board Affiliation") # Used in form
    phone_number = fields.Char(string="School Phone Number")
    current_school_country = fields.Char(string="School Country") # Treat Link as Char
    current_school_area_code = fields.Char(string="School Area Code/ Pincode")
    current_school_city = fields.Char(string="School City/ Town")
    current_school_state = fields.Char(string="School State")
    email_address = fields.Char(string="School Email Address")
    current_school_a_line1 = fields.Char(string="School Address Line 1")
    current_school_a_line2 = fields.Char(string="School Address Line 2")

    was_the_applicant_ever_home_schooled = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Was Applicant Ever Home Schooled?")
    been_to_school_previously = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Studied Previously in Any School?", required=True)
    # previous_schools -> Skipped (Table field)
    emis_id = fields.Char(string="EMIS ID")

    academic_strengths_and_weaknesses = fields.Text(string="Academic Strengths and Weaknesses", required=True)
    hobbies_interests_and_extra_curricular_activities = fields.Text(string="Hobbies, Interests & Extra-Curricular", required=True)
    other_details_of_importance = fields.Text(string="Other Details of Importance")
    temperament_and_personality = fields.Text(string="Temperament and Personality", required=True)
    special_learning_needs_or_learning_disability = fields.Text(string="Special Learning Needs or Disability", required=True)

    # --- Health Information ---
    # Vaccines
    done_smallpox_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Smallpox?", required=True)
    done_hepatitis_a_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Hepatitis A?", required=True)
    done_hepatitis_b_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Hepatitis B?", required=True)
    done_tdap_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Tdap?", required=True)
    done_typhoid_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Typhoid?", required=True)
    done_measles_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Measles?", required=True)
    done_polio_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Polio?", required=True)
    done_mumps_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Mumps?", required=True)
    done_rubella_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Rubella?", required=True)
    done_varicella_vaccine = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Protected from Varicella?", required=True)
    other_vaccines = fields.Char(string="Other Vaccinations")
    vaccine_certificates = fields.Binary(string="Vaccine Certificate(s)", attachment=True)
    vaccine_certificates_filename = fields.Char("Vaccine Certificate(s) Filename")

    # Additional Health
    blood_group = fields.Selection([
        ('Blood Group A+', 'A+'), ('Blood Group A-', 'A-'),
        ('Blood Group B+', 'B+'), ('Blood Group B-', 'B-'),
        ('Blood Group O+', 'O+'), ('Blood Group O-', 'O-'),
        ('Blood Group AB+', 'AB+'), ('Blood Group AB-', 'AB-'),
    ], string="Blood Group", required=True)
    wears_glasses_or_lens = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Wears glasses or lenses?", required=True)
    right_eye_power = fields.Char(string="Right Eye Power")
    left_eye_power = fields.Char(string="Left Eye Power")
    is_toilet_trained = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Is Applicant toilet-trained?")
    wets_bed = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Does Applicant bed-wet?")

    # Challenges
    has_hearing_challenges = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Any hearing challenges?", required=True)
    hearing_challenges = fields.Text(string="Hearing Challenges Details")
    has_behavioural_challenges = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Any psych./behavioural challenges?", required=True)
    behavioural_challenges = fields.Text(string="Psych./Behavioural Challenges Details") # Fixed typo
    has_physical_challenges = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Any physical challenges?", required=True)
    physical_challenges = fields.Text(string="Physical Challenges Details")
    has_speech_challenges = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Any speech challenges?", required=True)
    speech_challenges = fields.Text(string="Speech Challenges Details")

    # Medical History
    has_injury = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="History of accident/ injury?", required=True)
    injury_details = fields.Text(string="Accident/ Injury Details")
    on_medication = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="On regular medication?", required=True)
    medication_details = fields.Text(string="Medication Details") # Fixed typo
    medical_prescription = fields.Binary(string="Medical Prescription", attachment=True)
    medical_prescription_filename = fields.Char("Medical Prescription Filename")
    has_health_issue = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="History of any health Issue?", required=True)
    health_issue_details = fields.Text(string="Health Issue Details")
    was_hospitalized = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="History of hospitalization/ surgery?", required=True)
    hospitalization_details = fields.Text(string="Hospitalization/ Surgery Details")
    needs_special_attention = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Other health issue needing special attention?")
    attention_details = fields.Text(string="Special Attention Details")
    has_allergies = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Any food/ drug allergies?", required=True) # Fixed typo
    allergy_details = fields.Text(string="Allergy Details")

    # --- Parent & Guardian Information ---
    # Mother
    mother_full_name = fields.Char(string="Mother's Full Name", required=True)
    mother_email = fields.Char(string="Mother's Email")
    mother_phone = fields.Char(string="Mother's Phone", required=True)
    mother_occupation = fields.Char(string="Mother's Occupation")
    mother_education = fields.Char(string="Mother's Education")

    # Father
    father_full_name = fields.Char(string="Father's Full Name", required=True)
    father_email = fields.Char(string="Father's Email")
    father_phone = fields.Char(string="Father's Phone", required=True)
    father_occupation = fields.Char(string="Father's Occupation")
    father_education = fields.Char(string="Father's Education")

    # Marital Status
    parent_marital_status = fields.Selection([
        ('Married', 'Married'),
        ('Separated', 'Separated'),
        ('Divorced', 'Divorced'),
        ('Single Parent', 'Single Parent'),
    ], string="Parent Marital Status", required=True)
    # Note: Corrected typo in React field name for responsibility
    who_is_responsible_for_paying_applicants_tuition_fee = fields.Selection([
        ('Father', 'Father'), ('Mother', 'Mother'), ('Both', 'Both')
        ], string="Who pays tuition fee?")
    court_order_document = fields.Binary(string="Court Order Document", attachment=True)
    court_order_document_filename = fields.Char("Court Order Document Filename")
    who_is_allowed_to_receive_school_communication = fields.Selection([
        ('Father', 'Father'), ('Mother', 'Mother'), ('Both', 'Both')
        ], string="Who receives communication?")
    legal_rights_document = fields.Binary(string="Legal Rights Document", attachment=True)
    legal_rights_document_filename = fields.Char("Legal Rights Document Filename")
    who_is_allowed_to_receive_report_cards = fields.Selection([
        ('Father', 'Father'), ('Mother', 'Mother'), ('Both', 'Both')
        ], string="Who receives report cards?")
    visit_rights = fields.Selection([
        ('Father', 'Father'), ('Mother', 'Mother'), ('Both', 'Both')
        ], string="Who can visit child?")

    # Guardian
    parents_are_guardians = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Are Parents the Local Guardians?")
    # guardian_information -> Skipped (Table field)

    # --- Class XI Specific (Conditional in Form) ---
    group_a = fields.Selection([('Physics', 'Physics'), ('Accounts', 'Accounts'), ('History', 'History')], string="Group A Preference")
    group_b = fields.Selection([('Chemistry', 'Chemistry'), ('Economics', 'Economics')], string="Group B Preference")
    group_c = fields.Selection([('Biology', 'Biology'), ('Computer Science', 'Computer Science'), ('Commerce', 'Commerce'), ('Political Science', 'Political Science')], string="Group C Preference")
    group_d = fields.Selection([('Mathematics', 'Mathematics'), ('Environmental Studies', 'Environmental Studies'), ('Fine Arts', 'Fine Arts')], string="Group D Preference")
    q1_applicant_response = fields.Text("Q1 Response (Applicant)")
    q2_applicant_response = fields.Text("Q2 Response (Applicant)")
    q3_applicant_response = fields.Text("Q3 Response (Applicant)")
    q4_applicant_response = fields.Text("Q4 Response (Applicant)")
    q5_applicant_response = fields.Text("Q5 Response (Applicant)")
    q6_applicant_response = fields.Text("Q6 Response (Applicant)")
    q7_applicant_response = fields.Text("Q7 Response (Applicant)")
    q1_parent_response = fields.Text("Q1 Response (Parent)")
    q2_parent_response = fields.Text("Q2 Response (Parent)")
    q3_parent_response = fields.Text("Q3 Response (Parent)")
    q4_parent_response = fields.Text("Q4 Response (Parent)")
    q5_parent_response = fields.Text("Q5 Response (Parent)")
    q6_parent_response = fields.Text("Q6 Response (Parent)")

    # --- Declaration ---
    tnc_check = fields.Boolean(string="Agreed to T&C")
    date = fields.Date(string="Declaration Date", required=True)
    place = fields.Char(string="Declaration Place", required=True)

    # --- Billing Information ---
    billing_name = fields.Char(string="Billing Full Name", required=True)
    billing_phone = fields.Char(string="Billing Phone", required=True)
    billing_email = fields.Char(string="Billing Email", required=True)
    billing_country = fields.Char(string="Billing Country", required=True) # Treat Link as Char
    billing_area_code = fields.Char(string="Billing Area Code/ Pincode", required=True)
    billing_city = fields.Char(string="Billing City/ Town", required=True)
    billing_state = fields.Char(string="Billing State")
    billing_address_l1 = fields.Char(string="Billing Address Line 1", required=True)
    billing_address_l2 = fields.Char(string="Billing Address Line 2")

    # --- Status/Feedback Fields (Likely set internally in Odoo, not directly from this form) ---
    # Included here to match React, but maybe read-only/computed in Odoo Views later
    application_fee_status = fields.Selection([
        ('Pending', 'Pending'), ('In Progress', 'In Progress'),
        ('Completed', 'Completed'), ('Expired', 'Expired')
        ], string="Application Fee Status", default='Pending', readonly=True)
    program = fields.Char(string="Program", readonly=True) # Treat Link as Char
    # payment_program_links -> Skipped (Table field)
    amended_from = fields.Char(string="Amended From", readonly=True)
    # Feedback fields - Keep as text for now
    application_feedback_status = fields.Selection([('Yes', 'Yes'), ('No', 'No'), ('Maybe', 'Maybe')], string="Application Feedback Status")
    application_feedback = fields.Text(string="Application Feedback")
    orientation_feedback_status = fields.Selection([('Yes', 'Yes'), ('No', 'No'), ('Maybe', 'Maybe')], string="Orientation Feedback Status")
    academics_feedback = fields.Text(string="Academics Feedback")
    group_activities_feedback = fields.Text(string="Group Activities Feedback")
    sports_feedback = fields.Text(string="Sports Feedback")
    dining = fields.Text(string="Dining Feedback")
    other_feedback = fields.Text(string="Other Feedback")
    interview_feedback_status = fields.Selection([
        ('Probable Yes', 'Probable Yes'), ('Probable No', 'Probable No'), ('Maybe', 'Maybe')
        ], string="Interview Feedback Status")
    interview_feedback = fields.Text(string="Interview Feedback")

    # Ensure _rec_name is set if 'name' field doesn't exist
    _rec_name = 'full_name'