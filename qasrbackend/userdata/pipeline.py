def save_phone_number(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        phone_number = response.get('phone_number')
        if phone_number:
            user.profile.phone_number = phone_number
            user.save()

    elif backend.name == 'facebook':
        phone_number = response.get('mobile_phone')
        if phone_number:
            user.profile.phone_number = phone_number
            user.save()
