import json
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_access_point.models.custom_field import (CUSTOM_FIELD_TYPE, CUSTOM_FIELD_STATUS,
                                                     CUSTOM_FIELD_OPTIONS_STATUS)

custom_field_values_related_name = "custom_field_values"


def _validate_custom_fields_attributes(custom_field_model, custom_field_value_model, custom_field_options_model):
    """
    Validates that if `custom_field_model` is defined, `custom_field_value_model` must also be defined.

    :param custom_field_model - Custom Field model name
    :param custom_field_value_model - Custom Field Value model name
    :param custom_field_options_model - Custom Field Options model name
    """
    if custom_field_model:
        if not custom_field_value_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_value_model' is missing."
            )
        if not custom_field_options_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_options_model' is missing."
            )
    elif custom_field_value_model:
        if not custom_field_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_model' is missing."
            )
        if not custom_field_options_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_options_model' is missing."
            )
    elif custom_field_options_model:
        if not custom_field_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_model' is missing."
            )
        if not custom_field_value_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_value_model' is missing."
            )


def _get_custom_field_queryset(custom_field_model):
    """
    Get active custom fields queryset.

    :param custom_field_model - Custom Field model name
    """
    return custom_field_model.objects.filter(status=CUSTOM_FIELD_STATUS[1][0]).order_by("field_order")


def _prefetch_custom_field_values(
    queryset,
    custom_field_queryset,
    custom_field_value_model,
):
    """
    Prefetch related custom field values for the given queryset.

    :param queryset - CRUD queryset
    :param custom_field_queryset - Custom Field queryset
    :param custom_field_value_model - Custom Field Value model name
    """
    active_custom_fields = custom_field_queryset

    return queryset.prefetch_related(
        Prefetch(
            custom_field_values_related_name,
            queryset=custom_field_value_model.objects.filter(
                custom_field__in=active_custom_fields
            ).only("id", "custom_field", "text_field"),
        )
    )


def _get_ordering_params(request):
    """
    Get ordering parameters from request.

    :param request - The request object, typically containing data sent by the client, including query parameters, body content, and other metadata
    """
    order_by = request.query_params.get("order_by", "created_at")
    direction = request.query_params.get("direction", "desc")

    # Validate order_by field
    if order_by not in ["created_at", "updated_at"]:
        raise ValueError(
            "Invalid 'order_by' field. Only 'created_at' or 'updated_at' are allowed."
        )

    # Validate direction
    if direction not in ["asc", "desc"]:
        raise ValueError("Invalid 'direction'. Only 'asc' or 'desc' are allowed.")

    # Apply ordering direction
    return f"-{order_by}" if direction == "desc" else order_by


def _get_search_filter(request, list_search_fields, custom_field_model = None, custom_field_value_model = None, is_custom_field_enabled = False):
    """
    Generate search filter based on query parameters.

    :param request - The request object, typically containing data sent by the client, including query parameters, body content, and other metadata
    :param list_search_fields - A list of CRUD model field names that should be used for search filtering
    :param custom_field_model - Custom Field model name
    :param custom_field_value_model - Custom Field Value model name
    :param is_custom_field_enabled
    """
    search_term = request.query_params.get("search", "")
    filter_term = request.query_params.get("filter", "{}")

    if not search_term and not filter_term:
        return Q()  # Empty filter if no search & filter term is provided

    search_filter = Q()

    if search_term:
        # Search
        search_filter = apply_search(search_filter,
                                     search_term,
                                     list_search_fields,
                                     is_custom_field_enabled,
                                     custom_field_value_model)

    if filter_term:
        # Filter
        search_filter = apply_filter(search_filter,
                                     request,
                                     is_custom_field_enabled,
                                     custom_field_model,
                                     custom_field_value_model)

    return search_filter

def apply_search(search_filter_queryset, search_term, list_search_fields, is_custom_field_enabled, custom_field_value_model ):
    """
    Apply Search

    :param search_filter_queryset
    :param search_term
    :param list_search_fields
    :param is_custom_field_enabled
    :param custom_field_value_model
    """
    for field in list_search_fields:
        # Regular model field search
        search_filter_queryset |= Q(**{f"{field}__icontains": search_term})

    if is_custom_field_enabled:
        custom_field_value_subquery = (custom_field_value_model.objects.
                                       filter(text_field__icontains=search_term).values('submission'))

        search_filter_queryset |= Q(id__in=custom_field_value_subquery)

    return search_filter_queryset


def apply_filter(search_filter_queryset, request, is_custom_field_enabled, custom_field_model, custom_field_value_model):
    """
    Apply Filter using query parameters.

    :param search_filter_queryset: The initial queryset to be filtered
    :param request: The request object, containing the query parameters
    :param is_custom_field_enabled: Boolean indicating if custom fields should be considered
    :param custom_field_model: Custom Field model name
    :param custom_field_value_model: The model for custom field values to apply filters on
    """
    filters = {}

    # Retrieve filters from query parameters
    for key, value in request.GET.items():
        if key.startswith("filter_"):
            # Remove the "filter_" prefix to get the field name
            field = key.replace("filter_", "").lower()
            filters[field] = value
        elif key.startswith("combined_filter_"):
            # Handle combined filters (e.g., combined_filter_name: john)
            field_combination = key.replace("combined_filter_", "").lower()
            combined_filters = parse_combined_filter(field_combination, value)
            # Apply combined filters to the queryset
            search_filter_queryset &= combined_filters

    if filters:
        custom_field_id_details = {}
        # First, gather the custom field IDs that need filtering
        for field, value in filters.items():
            if is_custom_field_enabled and field.startswith("custom_field_"):
                custom_field_id = field.replace("custom_field_", "")  # Extract the custom field ID
                custom_field_id_details[custom_field_id] = value

        # Pre-fetch custom field types for all the custom fields to avoid multiple queries
        custom_fields = (custom_field_model.objects.filter(id__in=custom_field_id_details.keys())
                         .filter(status=CUSTOM_FIELD_STATUS[1][0]).values("id", "field_type"))

        # Create a dictionary for fast lookup of field types
        custom_field_types = {str(custom_field["id"]): custom_field["field_type"] for custom_field in custom_fields}

        # Now apply the filters
        for field, value in filters.items():
            if is_custom_field_enabled and field.startswith("custom_field_"):
                custom_field_id = field.replace("custom_field_", "")  # Extract the custom field ID

                # Look up the custom field type from the pre-fetched dictionary
                custom_field_type = custom_field_types.get(custom_field_id, None)

                if custom_field_type:
                    # Apply the filter based on the custom field type
                    if custom_field_type == CUSTOM_FIELD_TYPE[6][0]: #dropdown
                        search_filter_queryset &= Q(
                            id__in=custom_field_value_model.objects.filter(
                                custom_field_id=custom_field_id, dropdown_field__icontains=value
                            ).values("submission")
                        )
                    elif custom_field_type == CUSTOM_FIELD_TYPE[7][0]: #radio
                        search_filter_queryset &= Q(
                            id__in=custom_field_value_model.objects.filter(
                                custom_field_id=custom_field_id, radio_field=value
                            ).values("submission")
                        )
                    elif custom_field_type == CUSTOM_FIELD_TYPE[11][0]: #multiselect_checkbox
                        search_filter_queryset &= Q(
                            id__in=custom_field_value_model.objects.filter(
                                custom_field_id=custom_field_id, multiselect_checkbox_field__icontains=value
                            ).values("submission")
                        )
                    else:
                        # Handle other custom field types (text_field, website_url, text_area, number, email,
                        # phone_number, hidden)
                        search_filter_queryset &= Q(
                            id__in=custom_field_value_model.objects.filter(
                                custom_field_id=custom_field_id, text_field__icontains=value
                            ).values("submission")
                        )
                else:
                    # Skip this filter if the custom field type is not found
                    continue
            else:
                # Regular model field filtering (non-custom field)
                search_filter_queryset &= Q(**{f"{field}__icontains": value})

    return search_filter_queryset


def parse_combined_filter(field_combination, value):
    """
    Parse the combined filter and return the corresponding Q object for query filtering.

    :param field_combination: The field names involved in the combined filter.
    :param value: The filter value to compare with.
    :return: Q object representing the combined condition.
    """
    # Split the field_combination into segments, handling both `|` and `&`
    or_segments = field_combination.split('|')

    q_objects = []

    for segment in or_segments:
        # Split segment by `&` for AND logic
        and_conditions = segment.split('&')
        and_q_objects = []

        for field in and_conditions:
            # Create a Q object for each field with the given value
            and_q_objects.append(Q(**{f"{field}__icontains": value}))

        # Combine all fields in this AND segment
        combined_and_q = and_q_objects.pop(0)
        for q in and_q_objects:
            combined_and_q &= q

        q_objects.append(combined_and_q)

    # Combine all AND segments using OR logic
    final_q = q_objects.pop(0)
    for q in q_objects:
        final_q |= q

    return final_q

def _get_pagination(request, queryset):
    """
    Handle pagination logic and return paginated data.

    :param request - The request object
    :param queryset - The queryset to be paginated
    """
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 10)

    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        raise ValueError("Invalid 'page' or 'page_size'. They must be integers.")

    paginator = Paginator(queryset, page_size)
    try:
        return paginator.get_page(page)
    except (EmptyPage, PageNotAnInteger):
        raise ValueError("Invalid page number or page size. Ensure the page is valid.")


def _format_custom_fields(custom_field_queryset):
    """
    Format custom fields.

    :param custom_field_queryset - Custom Field queryset
    """
    formatted_custom_fields = {}

    if custom_field_queryset:
        for custom_field in custom_field_queryset:
            formatted_custom_fields[custom_field.id] = custom_field.label

    return formatted_custom_fields


def _prepare_data_rows(page_obj, list_fields_to_use, active_custom_fields, custom_field_options_model):
    """
    Prepare the data rows for the list view response.

    :param page_obj
    :param list_fields_to_use - A list of CRUD model field names that should be used on list response.
    :param active_custom_fields - Active Custom Fields
    :param custom_field_options_model - Custom Field Options Model
    """
    data = []
    for obj in page_obj.object_list:
        formatted_custom_field_submitted_values = {}
        if active_custom_fields:
            if hasattr(obj, custom_field_values_related_name):
                custom_field_submitted_values = getattr(obj, custom_field_values_related_name).all()
                formatted_custom_field_submitted_values \
                    = _format_custom_field_submitted_values(custom_field_submitted_values, custom_field_options_model)

        # CRUD submitted data
        row = [getattr(obj, field, "") for field in list_fields_to_use]

        # Custom Field submitted data
        if active_custom_fields:
            for custom_field in active_custom_fields:
                row.append(formatted_custom_field_submitted_values.get(custom_field, ""))

        data.append(row)

    return data


def _format_custom_field_submitted_values(custom_field_submitted_values, custom_field_options_model):
    """
    Format custom field values based on field type.

    :param custom_field_submitted_values
    :param custom_field_options_model - Custom Field Options Model
    """
    formatted_values = {}
    for submitted_value in custom_field_submitted_values:
        field_type = submitted_value.custom_field.field_type
        if field_type == CUSTOM_FIELD_TYPE[1][0]:  # Date field
            formatted_values[submitted_value.custom_field.id] = submitted_value.text_field.strftime("%Y-%m-%d")
        elif field_type == CUSTOM_FIELD_TYPE[6][0]:  # Dropdown field
            dropdown_values = _format_string_to_json_array(submitted_value.dropdown_field)
            formatted_dropdown_values = _get_field_option_values(dropdown_values, custom_field_options_model)
            formatted_values[submitted_value.custom_field.id] = " ,".join(formatted_dropdown_values)
        else:
            # Other field types
            formatted_values[submitted_value.custom_field.id] = submitted_value.text_field

    return formatted_values

def _format_string_to_json_array(json_string):
    """
    Format string to JSON array

    :param json_string
    """
    try:
        json_value = json.loads(json_string)
        if type(json_value) is str:
            json_value = json.loads(json_value)
        if type(json_value) is list:
            formatted_string = json_value
        else:
            formatted_string = None
    except:
        formatted_string = None

    return formatted_string

def _get_field_option_values(option_ids, custom_field_options_model):
    """
    Get Field Option Values - If option is non deleted

    :param option_ids
    :param custom_field_options_model
    """
    option_values = []

    if option_ids:
        field_options = custom_field_options_model.objects.filter(id__in=option_ids).filter(status=CUSTOM_FIELD_OPTIONS_STATUS[1][0])

        if field_options:
            for field_option in field_options:
                option_values.append(field_option.label)

    return option_values