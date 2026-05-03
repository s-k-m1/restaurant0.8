from django.utils import timezone

def current_time_ho(request):
    current_time = timezone.now()
    return {"ct": current_time}