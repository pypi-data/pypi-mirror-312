from rest_framework.decorators import action

from django_access_point.models.custom_field import CUSTOM_FIELD_STATUS
from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES
from django_access_point.views.custom_field import CustomFieldViewSet
from django_access_point.views.crud import CrudViewSet
from django_access_point.utils_response import success_response, error_response, validation_error_response
from django_access_point.views.helpers_crud import (custom_field_values_related_name, _get_custom_field_queryset,
                                            _prefetch_custom_field_values, _format_custom_field_submitted_values)
from django_access_point.excel_report import ExcelReportGenerator

from .models import User, UserCustomField, UserCustomFieldOptions, UserCustomFieldValue
from .serializers import UserSerializer, UserCustomFieldSerializer


class PlatformUser(CrudViewSet):
    queryset = User.objects.filter(user_type=USER_TYPE_CHOICES[0][0]).exclude(
        status=USER_STATUS_CHOICES[0][0])
    list_fields = {"id": "ID", "name": "Name", "email": "Email Address", "phone_no": "Phone No"}
    list_search_fields = ["name", "email", "phone_no"]
    serializer_class = UserSerializer
    custom_field_model = UserCustomField
    custom_field_value_model = UserCustomFieldValue
    custom_field_options_model = UserCustomFieldOptions

    @action(detail=False, methods=['post'], url_path='complete-profile-setup')
    def complete_profile_setup(self, request, *args, **kwargs):
        """
        Complete Profile Setup.
        """
        password = request.data.get('password')
        pass

    @action(detail=False, methods=['post'], url_path='generate-user-report')
    def generate_user_report(self, request, *args, **kwargs):
        """
        Generate User Report.
        """
        users_queryset = self.queryset

        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if start_date and end_date:
            users_queryset = users_queryset.filter(created_at__range=[start_date, end_date])

        users_queryset = users_queryset.order_by("created_at")

        # Get User Custom Fields
        active_custom_fields = _get_custom_field_queryset(self.custom_field_model)

        # Pre-fetch User Custom Field Values
        users_queryset = _prefetch_custom_field_values(
            users_queryset, active_custom_fields, self.custom_field_value_model
        )

        # Define headers for the report
        def get_headers():
            headers = ["Name", "Email Address", "Phone No"]

            # Add Custom Field Headers if any
            for field in active_custom_fields:
                headers.append(field.label)

            return headers

        # Prepare row data for each user, including custom fields
        def get_row_data(user):
            row = [user.name, user.email, user.phone_no]

            # Get custom field values, if any
            if active_custom_fields:
                if hasattr(user, custom_field_values_related_name):
                    custom_field_submitted_values = getattr(user, custom_field_values_related_name).all()
                    formatted_custom_field_submitted_values = _format_custom_field_submitted_values(
                        custom_field_submitted_values
                    )

                    # Append each custom field value to the row
                    for field in active_custom_fields:
                        row.append(formatted_custom_field_submitted_values.get(field.id, ""))

            return row

        # Ensure the queryset has results before proceeding
        if not users_queryset.exists():
            return error_response("No users found for the report.")

        # Generate the Excel report
        report_generator = ExcelReportGenerator(
            title="User Report",
            queryset=users_queryset,
            get_headers=get_headers,
            get_row_data=get_row_data
        )

        # Generate and return the report as an HTTP response
        return report_generator.generate_report()


    def after_save(self, request, instance):
        """
        Handle after save.
        """
        email = instance.email

        self.send_invite_user_email(email)

    def send_invite_user_email(self, email):
        """
        Send invitation email to the user.
        """
        pass


class PlatformUserCustomField(CustomFieldViewSet):
    queryset = UserCustomField.objects.filter(status=CUSTOM_FIELD_STATUS[1][0]).order_by("field_order")
    serializer_class = UserCustomFieldSerializer
    custom_field_options_model = UserCustomFieldOptions
