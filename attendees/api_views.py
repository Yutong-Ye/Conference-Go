from django.http import JsonResponse

from .models import Attendee
from events.models import Conference

from django.views.decorators.http import require_http_methods
import json
from django.urls import reverse
from common.json import ModelEncoder


class AttendeeListEncoder(ModelEncoder):
    model = Attendee  # Model that this encoder handles
    properties = ["name", "email"]  # List of properties to include in JSON

    def encode(self, obj):
        # Check if obj is a dictionary, if so, directly return the serialized dict
        if isinstance(obj, dict):
            return super(AttendeeListEncoder, self).encode(obj)

        # If it's an Attendee instance, process and add extra fields
        data = {
            "name": obj.name,
            "email": obj.email,
            "href": reverse('attendee_detail', kwargs={'attendee_id': obj.id})
        }
        return super(AttendeeListEncoder, self).encode(data)
    

class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = ["email", "name", "company_name", "created", "conference"]

    # If you need to add extra data specific to Attendee
    def get_extra_data(self, obj):
        extra_data = {}
        if obj.conference:
            extra_data["conference"] = {
                "name": obj.conference.name
                # Removed the 'href' key since we don't have a suitable URL
            }
        return extra_data

# def api_list_attendees(request, conference_id):
#     """
#     Lists the attendees names and the link to the attendee
#     for the specified conference id.

#     Returns a dictionary with a single key "attendees" which
#     is a list of attendee names and URLS. Each entry in the list
#     is a dictionary that contains the name of the attendee and
#     the link to the attendee's information.

#     {
#         "attendees": [
#             {
#                 "name": attendee's name,
#                 "href": URL to the attendee,
#             },
#             ...
#         ]
#     }
#     """
#     return JsonResponse({})

@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        # Retrieve attendees as model instances
        attendees = Attendee.objects.filter(conference=conference_id)
        # Serialize using the encoder, which expects model instances
        return JsonResponse(
            {"attendees": list(attendees)},  # Convert queryset to list
            encoder=AttendeeListEncoder,
            safe=False,
        )
    else:  # POST
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )



# def api_show_attendee(request, id):
#     """
#     Returns the details for the Attendee model specified
#     by the id parameter.

#     This should return a dictionary with email, name,
#     company name, created, and conference properties for
#     the specified Attendee instance.

#     {
#         "email": the attendee's email,
#         "name": the attendee's name,
#         "company_name": the attendee's company's name,
#         "created": the date/time when the record was created,
#         "conference": {
#             "name": the name of the conference,
#             "href": the URL to the conference,
#         }
#     }
#     """
#     return JsonResponse({})

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_attendee(request, id):  # Changed attendee_id to id
    try:
        attendee = Attendee.objects.get(id=id)
    except Attendee.DoesNotExist:
        return JsonResponse({"message": "Attendee not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(attendee, encoder=AttendeeDetailEncoder, safe=False)

    elif request.method == "PUT":
        content = json.loads(request.body)
        for key, value in content.items():
            setattr(attendee, key, value)
        attendee.save()
        return JsonResponse(attendee, encoder=AttendeeDetailEncoder, safe=False)

    elif request.method == "DELETE":
        attendee.delete()
        return JsonResponse({"deleted": True})

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
