from django.http import JsonResponse

from .models import Conference, Location, State

from django.views.decorators.http import require_http_methods
import json
from common.json import ModelEncoder


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
        "state",  # This is a reference to a State object
    ]

    def default(self, o):
        # Override the default method to handle State objects specifically
        if isinstance(o, State):
            return {
                "name": o.name, 
                "abbreviation": o.abbreviation
            }
        return super(LocationDetailEncoder, self).default(o)
    

class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = ["name"]


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder,  # Refer to the class, not an instance
    }

# def api_list_locations(request):
#     """
#     Lists the location names and the link to the location.

#     Returns a dictionary with a single key "locations" which
#     is a list of location names and URLS. Each entry in the list
#     is a dictionary that contains the name of the location and
#     the link to the location's information.

#     {
#         "locations": [
#             {
#                 "name": location's name,
#                 "href": URL to the location,
#             },
#             ...
#         ]
#     }
#     """
#     return JsonResponse({})

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def api_list_locations(request, id=None):
    if request.method == "GET":
        # List all locations
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations},
            encoder=LocationListEncoder,
            safe=False,
        )

    elif request.method == "POST":
        # Create a new location
        content = json.loads(request.body)
        try:
            # Convert state abbreviation to State object
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        location = Location.objects.create(**content)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )

    elif request.method == "PUT":
        # Update an existing location
        if id is None:
            return JsonResponse({"message": "Missing location ID"}, status=400)
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )

    elif request.method == "DELETE":
        # Delete a location
        if id is None:
            return JsonResponse({"message": "Missing location ID"}, status=400)
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})

    else:
        # HTTP method not allowed
        return JsonResponse(
            {"message": "Method not allowed"},
            status=405,
        )



# def api_show_location(request, id):
#     """
#     Returns the details for the Location model specified
#     by the id parameter.

#     This should return a dictionary with the name, city,
#     room count, created, updated, and state abbreviation.

#     {
#         "name": location's name,
#         "city": location's city,
#         "room_count": the number of rooms available,
#         "created": the date/time when the record was created,
#         "updated": the date/time when the record was updated,
#         "state": the two-letter abbreviation for the state,
#     }
#     """
#     return JsonResponse({})


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_location(request, id):
    # Try to get the location, or return a 404 if not found
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return JsonResponse({"message": "Location not found"}, status=404)

    if request.method == "GET":
        # Return the location details
        return JsonResponse(location, encoder=LocationDetailEncoder, safe=False)

    elif request.method == "PUT":
        # Update the location
        content = json.loads(request.body)
        try:
            # Handle state conversion if included
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse({"message": "Invalid state abbreviation"}, status=400)

        for key, value in content.items():
            setattr(location, key, value)
        location.save()
        return JsonResponse(location, encoder=LocationDetailEncoder, safe=False)

    elif request.method == "DELETE":
        # Delete the location
        location.delete()
        return JsonResponse({"deleted": True})

    else:
        # HTTP method not allowed
        return JsonResponse({"message": "Method not allowed"}, status=405)
    

# def api_list_conferences(request):
#     """
#     Lists the conference names and the link to the conference.

#     Returns a dictionary with a single key "conferences" which
#     is a list of conference names and URLS. Each entry in the list
#     is a dictionary that contains the name of the conference and
#     the link to the conference's information.

#     {
#         "conferences": [
#             {
#                 "name": conference's name,
#                 "href": URL to the conference,
#             },
#             ...
#         ]
#     }
#     """
    
@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
            safe=False,
        )
    else:  # POST
        content = json.loads(request.body)
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )

        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )
    



# def api_show_conference(request, id):
#     """
#     Returns the details for the Conference model specified
#     by the id parameter.

#     This should return a dictionary with the name, starts,
#     ends, description, created, updated, max_presentations,
#     max_attendees, and a dictionary for the location containing
#     its name and href.

#     {
#         "name": the conference's name,
#         "starts": the date/time when the conference starts,
#         "ends": the date/time when the conference ends,
#         "description": the description of the conference,
#         "created": the date/time when the record was created,
#         "updated": the date/time when the record was updated,
#         "max_presentations": the maximum number of presentations,
#         "max_attendees": the maximum number of attendees,
#         "location": {
#             "name": the name of the location,
#             "href": the URL for the location,
#         }
#     }
#     """


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_conference(request, id):
    try:
        conference = Conference.objects.get(id=id)
    except Conference.DoesNotExist:
        return JsonResponse({"message": "Conference not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(conference, encoder=ConferenceDetailEncoder, safe=False)

    elif request.method == "PUT":
        content = json.loads(request.body)
        if "location" in content:
            try:
                location = Location.objects.get(id=content["location"])
                content["location"] = location
            except Location.DoesNotExist:
                return JsonResponse({"message": "Invalid location id"}, status=400)
        
        for key, value in content.items():
            setattr(conference, key, value)
        conference.save()
        return JsonResponse(conference, encoder=ConferenceDetailEncoder, safe=False)

    elif request.method == "DELETE":
        conference.delete()
        return JsonResponse({"deleted": True})

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)



