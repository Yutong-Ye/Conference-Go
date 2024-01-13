from django.http import JsonResponse

from .models import Presentation
from events.models import Conference

from django.views.decorators.http import require_http_methods
import json
from common.json import ModelEncoder
from django.urls import reverse
from django.core import serializers


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title", "status"]

    def default(self, o):
        # First, use the parent class's default method to get the basic data
        data = super().default(o)

        # Then, add any custom data specific to Presentation
        if isinstance(o, Presentation):
            data["href"] = reverse('api_list_presentations', kwargs={'conference_id': o.conference_id})

        return data
    
    
class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]

    def default(self, o):
        if isinstance(o, self.model):
            serialized_data = super().default(o)
            
            # Add the 'href' property to the serialized data
            serialized_data["href"] = reverse('api_list_presentations', kwargs={'conference_id': o.conference_id})
            
            # You can also include more properties here as needed
            return serialized_data
        return super().default(o)
    

# def api_list_presentations(request, conference_id):
#     """
#     Lists the presentation titles and the link to the
#     presentation for the specified conference id.

#     Returns a dictionary with a single key "presentations"
#     which is a list of presentation titles and URLS. Each
#     entry in the list is a dictionary that contains the
#     title of the presentation, the name of its status, and
#     the link to the presentation's information.

#     {
#         "presentations": [
#             {
#                 "title": presentation's title,
#                 "status": presentation's status name
#                 "href": URL to the presentation,
#             },
#             ...
#         ]
#     }
#     """
    
@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)

        # Serialize the queryset of presentations using Django serializers
        serialized_presentations = serializers.serialize("json", presentations)
        
        # Wrap the serialized presentations inside a dictionary
        response_data = {"presentations": serialized_presentations}
        
        return JsonResponse(
            response_data,
            safe=False,
        )

    else:  # POST
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        # Add the conference instance to the content dictionary
        content["conference"] = conference
        # Create a new presentation
        presentation = Presentation.create(**content)
        
        # Serialize the newly created presentation using PresentationDetailEncoder
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    
# def api_show_presentation(request, id):
#     """
#     Returns the details for the Presentation model specified
#     by the id parameter.

#     This should return a dictionary with the presenter's name,
#     their company name, the presenter's email, the title of
#     the presentation, the synopsis of the presentation, when
#     the presentation record was created, its status name, and
#     a dictionary that has the conference name and its URL

#     {
#         "presenter_name": the name of the presenter,
#         "company_name": the name of the presenter's company,
#         "presenter_email": the email address of the presenter,
#         "title": the title of the presentation,
#         "synopsis": the synopsis for the presentation,
#         "created": the date/time when the record was created,
#         "status": the name of the status for the presentation,
#         "conference": {
#             "name": the name of the conference,
#             "href": the URL to the conference,
#         }
#     }
#     """



@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_presentation(request, id):   
    try:
        presentation = Presentation.objects.get(id=id)   
    except Presentation.DoesNotExist:
        return JsonResponse({"message": "Presentation not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(presentation, encoder=PresentationDetailEncoder, safe=False)

    elif request.method == "PUT":
        content = json.loads(request.body)
        for key, value in content.items():
            setattr(presentation, key, value)
        presentation.save()
        return JsonResponse(presentation, encoder=PresentationDetailEncoder, safe=False)

    elif request.method == "DELETE":
        presentation.delete()
        return JsonResponse({"deleted": True})