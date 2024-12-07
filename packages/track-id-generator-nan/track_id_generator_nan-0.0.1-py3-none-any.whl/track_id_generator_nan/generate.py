import random
import string

def generate_unique_track_id(model, field_name="track_id", length=12):
    if length <= 0:
        raise ValueError("The length of the tracking ID must be greater than 0.")

    while True:
        track_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        filter_kwargs = {field_name: track_id}
        if not model.objects.filter(**filter_kwargs).exists():
            return track_id