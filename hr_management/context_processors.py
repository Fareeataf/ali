def user_profile(request):
    profile_url = None
    if request.user.is_authenticated:
        try:
            emp = request.user.employee
            if emp.profile:
                profile_url = emp.profile.url
        except Exception:
            profile_url = None
    return {'user_profile_url': profile_url}