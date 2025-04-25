import logging

from odoo import exceptions, http
from odoo.http import Response, request

from ..models.constants import NUMBER_OF_PROFILE_FORM_SECTIONS
from .student_registration_controller_util import *

_logger = logging.getLogger(__name__)


# This is the main class that handles the student registration form
class StudentRegistrationFullForm(http.Controller):

    # This route handles displaying the form to the user
    @http.route("/student-profile/", auth="public", website=True)
    def get_full_form(self, **kw):
        try:
            # First, check if user is logged in. If not, redirect to login page
            user = request.env.user
            if user.has_group("base.group_public"):
                return request.render("student_registration.sso_auto_redirect", {})

            # Update user permissions if needed
            self._update_access_rights_for_user(user)

            # Get the user's latest registration record and profile
            latest_student_record = get_latest_student_record_for_logged_in_user()
            latest_full_form_record = latest_student_record.student_profile_id

            # Show error if no profile exists
            if not latest_full_form_record.id:
                if latest_student_record.application_stage == "draft":
                    error_message = "Application review pending. Please wait for confirmation link"
                else:
                    error_message = "Failed to get profile information. Please contact us over email/phone."
                return render_error_template(error_message)

            # Get all dropdown values and selections that will be shown in the form
            values = self._get_full_form_selection_values()

            # Add emergency contact information
            for record in latest_full_form_record.emergency_contact_ids:
                if record.emergency_type == "primary":
                    values.update({
                        "primary_emergency_contact": record,
                    })
                if record.emergency_type == "secondary":
                    values.update({
                        "secondary_emergency_contact": record,
                    })

            # Add the user's profile record to be displayed in the form
            values.update({
                "student_profile_record": latest_full_form_record,
            })

            # Render the form template with all the values
            return request.render("student_registration.student_registration_full_form", values)

        except exceptions.AccessError as ex:
            _logger.error("Student full-form record fetch exception", exc_info=True)
            return render_error_template(ex.name)
        except Exception:
            _logger.error("Student full-form record fetch exception", exc_info=True)
            return render_error_template("Sorry something went wrong. Please try again.")

    # This route handles saving the form data when user submits
    @http.route("/student-profile/save/", type="json", auth="user", website=True)
    def save_full_form(self, **post):
        try:
            # Get the user's latest registration record
            latest_student_record = get_latest_student_record_for_logged_in_user()
            latest_full_form_record = latest_student_record.student_profile_id

            # Get and process the form values based on which section was submitted
            form_values = self._get_and_update_full_form_values(post, latest_full_form_record)

            if form_values:
                # If this is a section save (not just auto-save), validate the values
                if self._is_section_save(post):
                    self._validate_profile_form_values(form_values)
                # For auto-save, don't store section number
                elif "section_submitted" in form_values:
                    del form_values["section_submitted"]

                # Save the form values to database
                latest_full_form_record.write(form_values)
                return Response(status=200)

        except (exceptions.AccessError, exceptions.UserError, exceptions.ValidationError) as ex:
            _logger.error("Student full-form save exception", exc_info=True)
            raise ex
        except Exception:
            _logger.error("Student full-form save exception", exc_info=True)
            raise exceptions.UserError("Failed to save the application. Please try again or contact us over email/phone.")

    def _get_full_form_selection_values(self):
        values = {
            "gender_options": request.env["student.profile"]._fields["gender"].selection,
            "blood_group_options": request.env["student.profile"]._fields["blood_group"].selection,
            "religion_options": request.env["student.profile"]._fields["religion"].selection,
            "community_options": request.env["student.profile"]._fields["community"].selection,
            "marital_status_options": request.env["student.profile"]._fields["parent_marital_status"].selection,
            "emergency_type_options": request.env["student.emergency.contact"]._fields["emergency_type"].selection,
            "country_options": request.env["res.country"].sudo().search([]),
            "state_options": request.env["res.country.state"].sudo().search([]),
            "proof_type_options": request.env["proof.type"].sudo().search([]),
            "family_relation_options": request.env["student.family.details"]._fields["relation"].selection,
            "parent_permission_options": request.env["student.profile"]._fields["who_is_resposible_for_paying_applicants_tuition_fee"].selection,
            "group_a_options": request.env["student.profile"]._fields["group_a"].selection,
            "group_b_options": request.env["student.profile"]._fields["group_b"].selection,
            "group_c_options": request.env["student.profile"]._fields["group_c"].selection,
            "group_d_options": request.env["student.profile"]._fields["group_d"].selection,
        }
        return values

    def _get_and_update_full_form_values(self, post, latest_full_form_record):
        section_submitted = get_numeric_value("section_number", post)
        self._ensure_valid_section(section_submitted)
        mapped_function = self._get_section_mapping(section_submitted).get("form_values")
        form_values = mapped_function(post, latest_full_form_record)
        formatted_values_list = self._format_values([form_values])
        return formatted_values_list.pop(0)

    def _get_values_for_section_one(self, post, latest_full_form_record):
        """Process personal information section."""
        values = {
            "section_submitted": get_numeric_value("section_number", post),
            "section_1_submitted": True,
            "full_name": get_string_value("fullName", post),
            "gender": get_string_value("gender", post),
            "date_of_birth": get_string_value("dateOfBirth", post),
            "nationality_id": get_numeric_value("nationalityId", post),
            "country_of_residence_id": get_numeric_value("countryOfResidenceId", post),
            "country_of_birth_id": get_numeric_value("countryOfBirthId", post),
            "address_line_1": get_string_value("addressLine1", post),
            "address_line_2": get_string_value("addressLine2", post),
            "city": get_string_value("city", post),
            "state_id": get_numeric_value("stateId", post),
            "area_code": get_string_value("areaCode", post),
            "country_id": get_numeric_value("countryId", post),
            "identification_mark_1": get_string_value("identificationMark1", post),
            "identification_mark_2": get_string_value("identificationMark2", post),
            "religion": get_string_value("religion", post),
            "community": get_string_value("community", post),
            "phone": get_string_value("phoneNumber", post),
            "phone_country_code": get_string_value("phoneCountryCode", post),
            "has_name_changed": get_string_value("nameChanged", post),
            "previous_name": get_string_value("previousName", post),
            "is_mobile_same_as_phone": get_string_value("sameWhatsappNumber", post),
            "has_sibling_in_ihs": get_string_value("hasSiblingInIhs", post),
            "mother_tongue": get_string_value("motherTongue", post),
            "second_language": get_string_value("secondLanguage", post),
            "third_language": get_string_value("thirdLanguage", post),
        }

        # Handle other gender
        if values.get("gender") == "other":
            values["other_gender"] = get_string_value("otherGender", post)

        # Handle other religion
        if values.get("religion") == "other":
            values["other_religion"] = get_string_value("otherReligion", post)

        # Handle other community
        if values.get("community") == "other":
            values["other_community"] = get_string_value("otherCommunity", post)

        # Is same as whatApp number
        if values.get("is_mobile_same_as_phone") == "yes":
            values.update({
                "mobile": values["phone"],
                "mobile_country_code": values["phone_country_code"],
            })
        elif values.get("is_mobile_same_as_phone") == "no":
            values.update({
                "mobile": get_string_value("mobileNumber", post),
                "mobile_country_code": get_string_value("mobileCountryCode", post),
            })

        # Handle sibling information
        if values.get("has_sibling_in_ihs") == "yes":
            values.update({
                "sibling_1_full_name": get_string_value("sibling1FullName", post),
                "sibling_1_grade_status": get_string_value("sibling1GradeStatus", post),
                "sibling_1_school_name": get_string_value("sibling1SchoolName", post),
            })

        # Process ID proof information
        values.update({
            "id_proof_type": get_string_value("idProofType", post),
        })

        if values.get("id_proof_type") == "aadhaar":
            values.update({
                "aadhaar_number": get_string_value("aadhaarNumber", post),
            })
        elif values.get("id_proof_type") == "passport":
            values.update({
                "passport_number": get_string_value("passportNumber", post),
                "place_of_issue": get_string_value("placeOfIssue", post),
                "date_of_issue": get_string_value("dateOfIssue", post),
                "date_of_expiry": get_string_value("dateOfExpiry", post),
            })

        # Upload documents
        self._upload_section_one_documents(post, latest_full_form_record)

        return values

    def _upload_section_one_documents(self, post, latest_full_form_record):
        ir_attachment = request.env["ir.attachment"].sudo()
        is_section_save = self._is_section_save(post)

        # Upload recent photograph
        upload_file(ir_attachment, post.get("recentPhotograph"), "student.profile", "recent_photograph",
                   latest_full_form_record.id, is_section_save)

        # Upload birth certificate
        upload_file(ir_attachment, post.get("birthCertificate"), "student.profile", "birth_certificate",
                   latest_full_form_record.id, is_section_save)

        # Upload ID proof document
        upload_file(ir_attachment, post.get("idProofDocument"), "student.profile", "id_proof_document",
                   latest_full_form_record.id, is_section_save)

    def _get_values_for_section_two(self, post, latest_full_form_record):
        """Process academic information section."""
        values = {
            "section_submitted": get_numeric_value("section_number", post),
            "section_2_submitted": True,
            "is_home_schooled": get_string_value("isHomeSchooled", post),
            "was_ever_home_schooled": get_string_value("wasEverHomeSchooled", post),
            "been_to_school_previously": get_string_value("beenToSchoolPreviously", post),
            "academic_strengths_and_weaknesses": get_string_value("academicStrengthsWeaknesses", post),
            "hobbies_interests_and_extra_curricular_activities": get_string_value("hobbiesInterests", post),
            "other_details_of_importance": get_string_value("otherDetailsImportance", post),
            "temperament_and_personality": get_string_value("temperamentPersonality", post),
            "special_learning_needs_or_learning_disability": get_string_value("specialLearningNeeds", post),
            "emis_id": get_string_value("emisId", post),
        }

        # Current school information if not home-schooled
        if values.get("is_home_schooled") == "no":
            values.update({
                "current_school_name": get_string_value("currentSchoolName", post),
                "board_affiliation": get_string_value("boardAffiliation", post),
                "school_phone": get_string_value("schoolPhone", post),
                "school_email": get_string_value("schoolEmail", post),
                "school_address_line_1": get_string_value("schoolAddressLine1", post),
                "school_address_line_2": get_string_value("schoolAddressLine2", post),
                "school_city": get_string_value("schoolCity", post),
                "school_state_id": get_numeric_value("schoolStateId", post),
                "school_area_code": get_string_value("schoolAreaCode", post),
                "school_country_id": get_numeric_value("schoolCountryId", post),
            })

        # Update previous school details
        self._update_previous_school_details(post, latest_full_form_record)

        return values

    def _update_previous_school_details(self, post, latest_full_form_record):
        """Process and update previous school details."""
        if get_string_value("beenToSchoolPreviously", post) != "yes":
            # If student has not been to school previously, remove any existing records
            request.env["student.previous.school"].sudo().search([
                ("student_profile_id", "=", latest_full_form_record.id),
            ]).unlink()
            return

        previous_schools_data = post.get("previousSchools", [])
        if not previous_schools_data:
            return

        # Format the data and create/update records
        formatted_schools = self._format_values(previous_schools_data)
        if formatted_schools:
            # Add student_profile_id to each record
            for school in formatted_schools:
                school["student_profile_id"] = latest_full_form_record.id

            # Delete existing records and create new ones
            previous_schools = request.env["student.previous.school"].sudo()
            previous_schools.search([("student_profile_id", "=", latest_full_form_record.id)]).unlink()
            previous_schools.create(formatted_schools)
        elif self._is_section_save(post) and get_string_value("beenToSchoolPreviously", post) == "yes":
            raise exceptions.ValidationError("Missing values for previous schools section")

    def _get_values_for_section_three(self, post, latest_full_form_record):
        """Process health information section."""
        values = {
            "section_submitted": get_numeric_value("section_number", post),
            "section_3_submitted": True,
            # Vaccine information
            "done_smallpox_vaccine": get_string_value("doneSmallpoxVaccine", post),
            "done_hepatitis_a_vaccine": get_string_value("doneHepatitisAVaccine", post),
            "done_hepatitis_b_vaccine": get_string_value("doneHepatitisBVaccine", post),
            "done_tdap_vaccine": get_string_value("doneTdapVaccine", post),
            "done_typhoid_vaccine": get_string_value("doneTyphoidVaccine", post),
            "done_measles_vaccine": get_string_value("doneMeaslesVaccine", post),
            "done_polio_vaccine": get_string_value("donePolioVaccine", post),
            "done_mumps_vaccine": get_string_value("doneMumpsVaccine", post),
            "done_rubella_vaccine": get_string_value("doneRubellaVaccine", post),
            "done_varicella_vaccine": get_string_value("doneVaricellaVaccine", post),
            "other_vaccines": get_string_value("otherVaccines", post),

            # Additional health information
            "blood_group": get_string_value("bloodGroup", post),
            "wears_glasses_or_lens": get_string_value("wearsGlassesOrLens", post),
            "is_toilet_trained": get_string_value("isToiletTrained", post),
            "wets_bed": get_string_value("wetsBed", post),

            # Challenges
            "has_hearing_challenges": get_string_value("hasHearingChallenges", post),
            "hearing_challenges": get_string_value("hearingChallenges", post),
            "has_behavioural_challenges": get_string_value("hasBehaviouralChallenges", post),
            "behavioural_callenges": get_string_value("behaviouralChallenges", post),
            "has_physical_challenges": get_string_value("hasPhysicalChallenges", post),
            "physical_challenges": get_string_value("physicalChallenges", post),
            "has_speech_challenges": get_string_value("hasSpeechChallenges", post),
            "speech_challenges": get_string_value("speechChallenges", post),

            # Other medical information
            "has_injury": get_string_value("hasInjury", post),
            "injury_details": get_string_value("injuryDetails", post),
            "on_medication": get_string_value("onMedication", post),
            "medicaton_details": get_string_value("medicationDetails", post),
            "has_health_issue": get_string_value("hasHealthIssue", post),
            "health_issue_details": get_string_value("healthIssueDetails", post),
            "was_hospitalized": get_string_value("wasHospitalized", post),
            "hospitalization_details": get_string_value("hospitalizationDetails", post),
            "needs_special_attention": get_string_value("needsSpecialAttention", post),
            "attention_details": get_string_value("attentionDetails", post),

            # Allergies
            "has_alergies": get_string_value("hasAllergies", post),
            "allergy_details": get_string_value("allergyDetails", post),
        }

        # Eye power if wears glasses
        if values.get("wears_glasses_or_lens") == "yes":
            values.update({
                "right_eye_power": get_string_value("rightEyePower", post),
                "left_eye_power": get_string_value("leftEyePower", post),
            })

        # Upload vaccine certificates and medical prescription
        self._upload_section_three_documents(post, latest_full_form_record)

        return values

    def _upload_section_three_documents(self, post, latest_full_form_record):
        """Upload health-related documents."""
        ir_attachment = request.env["ir.attachment"].sudo()
        is_section_save = self._is_section_save(post)

        # Upload vaccine certificates
        upload_file(ir_attachment, post.get("vaccineCertificates"), "student.profile", "vaccine_certificates",
                   latest_full_form_record.id, is_section_save and any([
                       get_string_value("doneSmallpoxVaccine", post) == "yes",
                       get_string_value("doneHepatitisAVaccine", post) == "yes",
                       get_string_value("doneHepatitisBVaccine", post) == "yes",
                       get_string_value("doneTdapVaccine", post) == "yes",
                       get_string_value("doneTyphoidVaccine", post) == "yes",
                       get_string_value("doneMeaslesVaccine", post) == "yes",
                       get_string_value("donePolioVaccine", post) == "yes",
                       get_string_value("doneMumpsVaccine", post) == "yes",
                       get_string_value("doneRubellaVaccine", post) == "yes",
                       get_string_value("doneVaricellaVaccine", post) == "yes",
                   ]))

        # Upload medical prescription if on medication
        if get_string_value("onMedication", post) == "yes":
            upload_file(ir_attachment, post.get("medicalPrescription"), "student.profile", "medical_prescription",
                       latest_full_form_record.id, is_section_save)

    def _get_values_for_section_four(self, post, latest_full_form_record):
        """Process parents & guardians section."""
        values = {
            "section_submitted": get_numeric_value("section_number", post),
            "section_4_submitted": True,

            # Parents information
            "mother_full_name": get_string_value("motherFullName", post),
            "mother_email": get_string_value("motherEmail", post),
            "mother_phone": get_string_value("motherPhone", post),
            "mother_occupation": get_string_value("motherOccupation", post),
            "mother_education": get_string_value("motherEducation", post),

            "father_full_name": get_string_value("fatherFullName", post),
            "father_email": get_string_value("fatherEmail", post),
            "father_phone": get_string_value("fatherPhone", post),
            "father_occupation": get_string_value("fatherOccupation", post),
            "father_education": get_string_value("fatherEducation", post),

            "parent_marital_status": get_string_value("parentMaritalStatus", post),
            "parents_are_guardians": get_string_value("parentsAreGuardians", post),

            # Billing information
            "billing_name": get_string_value("billingName", post),
            "billing_phone": get_string_value("billingPhone", post),
            "billing_email": get_string_value("billingEmail", post),
            "billing_country_id": get_numeric_value("billingCountryId", post),
            "billing_area_code": get_string_value("billingAreaCode", post),
            "billing_city": get_string_value("billingCity", post),
            "billing_state_id": get_numeric_value("billingStateId", post),
            "billing_address_l1": get_string_value("billingAddressL1", post),
            "billing_address_l2": get_string_value("billingAddressL2", post),

            # Application Fee Status
            "application_fee_status": "pending",

            # Higher class specific fields (Class XI)
            "group_a": get_string_value("groupA", post),
            "group_b": get_string_value("groupB", post),
            "group_c": get_string_value("groupC", post),
            "group_d": get_string_value("groupD", post),

            # Question responses
            "q1_applicant_response": get_string_value("q1ApplicantResponse", post),
            "q2_applicant_response": get_string_value("q2ApplicantResponse", post),
            "q3_applicant_response": get_string_value("q3ApplicantResponse", post),
            "q4_applicant_response": get_string_value("q4ApplicantResponse", post),
            "q5_applicant_response": get_string_value("q5ApplicantResponse", post),
            "q6_applicant_response": get_string_value("q6ApplicantResponse", post),
            "q7_applicant_response": get_string_value("q7ApplicantResponse", post),

            "q1_parent_response": get_string_value("q1ParentResponse", post),
            "q2_parent_response": get_string_value("q2ParentResponse", post),
            "q3_parent_response": get_string_value("q3ParentResponse", post),
            "q4_parent_response": get_string_value("q4ParentResponse", post),
            "q5_parent_response": get_string_value("q5ParentResponse", post),
            "q6_parent_response": get_string_value("q6ParentResponse", post),

            # Declaration
            "tnc_check": get_boolean_value("tncCheck", post),
            "declaration_date": get_string_value("declarationDate", post),
            "declaration_place": get_string_value("declarationPlace", post),
        }

        # Divorce related fields
        if values.get("parent_marital_status") in ["separated", "divorced"]:
            values.update({
                "who_is_resposible_for_paying_applicants_tuition_fee": get_string_value("whoPaysTuitionFee", post),
                "who_is_allowed_to_receive_school_communication": get_string_value("whoReceivesSchoolCommunication", post),
                "who_is_allowed_to_receive_report_cards": get_string_value("whoReceivesReportCards", post),
                "visit_rights": get_string_value("visitRights", post),
            })

            # Upload divorce-related documents
            self._upload_section_four_documents(post, latest_full_form_record)

        # Update emergency contacts & guardians
        self._update_emergency_contacts(post, latest_full_form_record)
        self._update_guardian_details(post, latest_full_form_record)

        return values

    def _upload_section_four_documents(self, post, latest_full_form_record):
        """Upload parent/guardian-related documents."""
        ir_attachment = request.env["ir.attachment"].sudo()
        is_section_save = self._is_section_save(post)
        parent_marital_status = get_string_value("parentMaritalStatus", post)

        if parent_marital_status in ["separated", "divorced"]:
            # Upload court order document
            upload_file(ir_attachment, post.get("courtOrderDocument"), "student.profile", "court_order_document",
                       latest_full_form_record.id, is_section_save)

            # Upload legal rights document
            upload_file(ir_attachment, post.get("legalRightsDocument"), "student.profile", "legal_rights_document",
                       latest_full_form_record.id, is_section_save)

    def _update_emergency_contacts(self, post, latest_full_form_record):
        """Process and update emergency contact details."""
        emergency_contacts_data = post.get("emergencyContacts", [])
        if not emergency_contacts_data:
            return

        formatted_contacts = self._format_values(emergency_contacts_data)
        if formatted_contacts:
            # Add student_profile_id to each record
            for contact in formatted_contacts:
                contact["student_profile_id"] = latest_full_form_record.id

            # Delete existing records and create new ones
            emergency_contacts = request.env["student.emergency.contact"].sudo()
            emergency_contacts.search([("student_profile_id", "=", latest_full_form_record.id)]).unlink()
            emergency_contacts.create(formatted_contacts)
        elif self._is_section_save(post):
            raise exceptions.ValidationError("Missing values for emergency contacts section")

    def _update_guardian_details(self, post, latest_full_form_record):
        """Process and update guardian details."""
        if get_string_value("parentsAreGuardians", post) == "yes":
            # If parents are guardians, remove any existing guardian records
            request.env["student.guardian"].sudo().search([
                ("student_profile_id", "=", latest_full_form_record.id),
            ]).unlink()
            return

        guardian_data = post.get("guardians", [])
        if not guardian_data:
            return

        formatted_guardians = self._format_values(guardian_data)
        if formatted_guardians:
            # Add student_profile_id to each record
            for guardian in formatted_guardians:
                guardian["student_profile_id"] = latest_full_form_record.id

            # Delete existing records and create new ones
            guardians = request.env["student.guardian"].sudo()
            guardians.search([("student_profile_id", "=", latest_full_form_record.id)]).unlink()
            guardians.create(formatted_guardians)
        elif self._is_section_save(post) and get_string_value("parentsAreGuardians", post) == "no":
            raise exceptions.ValidationError("Missing values for guardians section")

    def _get_section_mapping(self, section_submitted):
        section_values_mapping = {
            1: {
                "form_values": self._get_values_for_section_one,
                "validation": self._get_mandatory_fields_for_section_one,
            },
            2: {
                "form_values": self._get_values_for_section_two,
                "validation": self._get_mandatory_fields_for_section_two,
            },
            3: {
                "form_values": self._get_values_for_section_three,
                "validation": self._get_mandatory_fields_for_section_three,
            },
            4: {
                "form_values": self._get_values_for_section_four,
                "validation": self._get_mandatory_fields_for_section_four,
            },
        }
        return section_values_mapping.get(section_submitted)

    def _validate_profile_form_values(self, form_values):
        mapped_function = self._get_section_mapping(form_values["section_submitted"]).get("validation")
        mandatory_field_list = mapped_function(form_values)
        missing_field_list = []
        for mandatory_field in mandatory_field_list:
            field_value = form_values.get(mandatory_field)
            if field_value is None or field_value == "":
                missing_field_list.append(mandatory_field)
        if len(missing_field_list) > 0:
            missing_fields = ", ".join(missing_field_list)
            raise exceptions.ValidationError("Please enter values for following mandatory fields: "
                                             f"{missing_fields}")

    def _get_mandatory_fields_for_section_one(self, form_values):
        mandatory_field_list = [
            "full_name",
            "gender",
            "date_of_birth",
            "nationality_id",
            "country_of_residence_id",
            "country_of_birth_id",
            "address_line_1",
            "city",
            "area_code",
            "country_id",
            "identification_mark_1",
            "religion",
            "community",
            "phone",
            "phone_country_code",
            "mother_tongue",
        ]

        # Conditional mandatory fields
        if form_values.get("gender") == "other":
            mandatory_field_list.append("other_gender")

        if form_values.get("religion") == "other":
            mandatory_field_list.append("other_religion")

        if form_values.get("community") == "other":
            mandatory_field_list.append("other_community")

        if form_values.get("has_name_changed") == "yes":
            mandatory_field_list.append("previous_name")

        if form_values.get("is_mobile_same_as_phone") == "no":
            mandatory_field_list.extend(["mobile", "mobile_country_code"])

        if form_values.get("has_sibling_in_ihs") == "yes":
            mandatory_field_list.extend(["sibling_1_full_name", "sibling_1_grade_status"])

        return mandatory_field_list

    def _get_mandatory_fields_for_section_two(self, form_values):
        mandatory_field_list = [
            "is_home_schooled",
            "was_ever_home_schooled",
            "been_to_school_previously",
            "academic_strengths_and_weaknesses",
            "hobbies_interests_and_extra_curricular_activities",
            "temperament_and_personality",
            "special_learning_needs_or_learning_disability",
        ]

        # Conditional mandatory fields
        if form_values.get("is_home_schooled") == "no":
            mandatory_field_list.extend([
                "current_school_name",
                "board_affiliation",
                "school_address_line_1",
                "school_city",
                "school_area_code",
                "school_country_id",
            ])

        return mandatory_field_list

    def _get_mandatory_fields_for_section_three(self, form_values):
        mandatory_field_list = [
            "done_smallpox_vaccine",
            "done_hepatitis_a_vaccine",
            "done_hepatitis_b_vaccine",
            "done_tdap_vaccine",
            "done_typhoid_vaccine",
            "done_measles_vaccine",
            "done_polio_vaccine",
            "done_mumps_vaccine",
            "done_rubella_vaccine",
            "done_varicella_vaccine",
            "blood_group",
            "wears_glasses_or_lens",
            "has_hearing_challenges",
            "has_behavioural_challenges",
            "has_physical_challenges",
            "has_speech_challenges",
            "has_injury",
            "on_medication",
            "has_health_issue",
            "was_hospitalized",
            "has_alergies",
        ]

        # Conditional mandatory fields
        if form_values.get("wears_glasses_or_lens") == "yes":
            mandatory_field_list.extend(["right_eye_power", "left_eye_power"])

        if form_values.get("has_hearing_challenges") == "yes":
            mandatory_field_list.append("hearing_challenges")

        if form_values.get("has_behavioural_challenges") == "yes":
            mandatory_field_list.append("behavioural_callenges")

        if form_values.get("has_physical_challenges") == "yes":
            mandatory_field_list.append("physical_challenges")

        if form_values.get("has_speech_challenges") == "yes":
            mandatory_field_list.append("speech_challenges")

        if form_values.get("has_injury") == "yes":
            mandatory_field_list.append("injury_details")

        if form_values.get("on_medication") == "yes":
            mandatory_field_list.append("medicaton_details")

        if form_values.get("has_health_issue") == "yes":
            mandatory_field_list.append("health_issue_details")

        if form_values.get("was_hospitalized") == "yes":
            mandatory_field_list.append("hospitalization_details")

        if form_values.get("has_alergies") == "yes":
            mandatory_field_list.append("allergy_details")

        return mandatory_field_list

    def _get_mandatory_fields_for_section_four(self, form_values):
        mandatory_field_list = [
            "mother_full_name",
            "mother_phone",
            "father_full_name",
            "father_phone",
            "parent_marital_status",
            "parents_are_guardians",
            "billing_name",
            "billing_phone",
            "billing_email",
            "billing_country_id",
            "billing_area_code",
            "billing_city",
            "billing_address_l1",
            "tnc_check",
            "declaration_date",
            "declaration_place",
        ]

        # Conditional mandatory fields
        if form_values.get("parent_marital_status") in ["separated", "divorced"]:
            mandatory_field_list.extend([
                "who_is_resposible_for_paying_applicants_tuition_fee",
                "who_is_allowed_to_receive_school_communication",
                "who_is_allowed_to_receive_report_cards",
                "visit_rights",
            ])

        return mandatory_field_list

    def _update_access_rights_for_user(self, user):
        if not user.has_group("student_registration.group_student_portal_profile"):
            user.sudo().write({
                "groups_id": [(4, request.env.ref("student_registration.group_student_portal_profile").id)],
            })

    def _ensure_valid_section(self, section_number):
        is_valid = 0 < section_number <= NUMBER_OF_PROFILE_FORM_SECTIONS
        if not is_valid:
            _logger.error("Student full-form: Invalid section submitted", exc_info=True)
            raise exceptions.UserError("Invalid section number")

    def _format_values(self, details_list):
        # Replace empty string with None: In case of partial save, empty string for date fields will throw exception
        filtered_list = []
        if details_list:
            for details in details_list:
                filtered_details = {k: v if v else None for k, v in list(details.items())}
                if self._is_valid_dict(filtered_details):
                    filtered_list.append(filtered_details)
        return filtered_list

    def _is_valid_dict(self, details_dict):
        return details_dict and isinstance(details_dict, dict) and any(val for val in details_dict.values())

    def _is_section_save(self, post):
        return post.get("is_section_save", False)
