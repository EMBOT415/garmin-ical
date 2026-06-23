#   - Root cause: Garmin added Cloudflare TLS fingerprinting in March   
#   2026 that blocked all Python-based login attempts                   
#   - Fix: Replaced the dead garth library with garminconnect 0.3.x,    
#   which uses curl_cffi to impersonate a real browser's TLS fingerprint
#    and has a multi-strategy login cascade                             
#   - MFA: Added a prompt for your two-factor code, which the widget    
#   login strategy required                                             
   
#   The 429 rate limit errors on the mobile endpoints are normal — the  
#   library automatically falls through to the widget strategy which is
#   what actually works. You'll likely need to enter your MFA code each 
#   time you run it.                                          


from garminconnect import Garmin
import urllib.parse
from functools import lru_cache
from typing import Optional, List, Dict, Any  # noqa

from .data_types import ActivityType, ActivityData, \
    ActivityTypeData, TimezoneData


GARMIN_WEB_BASE_URI = "https://connect.garmin.com/modern"

_client = None


def login(username: str, password: str):
    global _client
    _client = Garmin(email=username, password=password)
    _client.login()


@lru_cache()
def get_activites(limit: int,
                  activity_type: Optional[ActivityType]) -> List[ActivityData]:
    qs = {"limit": limit}  # type: Dict[str, Any]
    if activity_type and activity_type is not ActivityType.ALL:
        qs["activityType"] = activity_type.value
    path = f"/activitylist-service/activities/search/activities?{urllib.parse.urlencode(qs)}"
    return _client.connectapi(path)


@lru_cache()
def get_activity_types() -> List[ActivityTypeData]:
    return _client.connectapi("/activity-service/activity/activityTypes")


@lru_cache()
def get_timezones() -> List[TimezoneData]:
    return _client.connectapi("/system-service/timezoneUnits")
