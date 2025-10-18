import logging
from datetime import datetime, timezone

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserProfileSerializer

logger = logging.getLogger(__name__)

class MeView(APIView):
    """
    GET /me
    Returns:
    {
      "status": "success",
      "user": { "email": "...", "name": "...", "stack": "..." },
      "timestamp": "<ISO8601 UTC with Z>",
      "fact": "<cat fact>"
    }
    """

    def get(self, request):
        # 1) load user from DB (first user) or fallback static info
        user = UserProfile.objects.first()
        if user:
            user_data = UserProfileSerializer(user).data
        else:
            user_data = {
                "email": "chmasamuel6@gmail.com",
                "name": "Chima Samuel",
                "stack": "Python/Django"
            }

        # 2) fetch cat fact from external API with timeout
        cat_fact = "No cat fact available right now."
        try:
            resp = requests.get(
                settings.CATFACT_API_URL,
                timeout=getattr(settings, "CATFACT_REQUEST_TIMEOUT", 5)
            )
            if resp.status_code == 200:
                json_data = resp.json()
                cat_fact = json_data.get("fact") or cat_fact
            else:
                logger.warning("Cat facts API returned non-200: %s", resp.status_code)
        except requests.exceptions.RequestException as exc:
            logger.exception("Failed to fetch cat fact: %s", exc)

        # 3) generate ISO 8601 UTC timestamp with Z and no microsecond precision
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

        # 4) compose response exactly as required
        payload = {
            "status": "success",
            "user": user_data,
            "timestamp": timestamp,
            "fact": cat_fact,
        }

        return Response(payload, status=status.HTTP_200_OK)
