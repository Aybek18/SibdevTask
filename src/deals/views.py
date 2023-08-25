from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from deals.serializers import DealCreateSerializer
from deals.services import DealService


class DealCreateAPIView(CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = DealCreateSerializer

    @extend_schema(
        responses={201: OpenApiResponse(description='{"message": "success"}')}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data["deals"]
        csv_data = csv_file.read().decode("utf-8")
        DealService.save_data(csv_data=csv_data)

        return Response({"message": "success"}, status=status.HTTP_201_CREATED)
