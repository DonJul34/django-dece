from django.utils.translation import activate, get_language


class DebugLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        active_language = get_language()
        session_language = request.session.get('django_language', 'en')  # Default to English
        print(f"Active language: {active_language}, Session language: {session_language}")
        
        # Force the active language to match the session language
        if session_language and session_language != active_language:
            from django.utils.translation import activate
            activate(session_language)

        return self.get_response(request)


class ForceLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_language = request.session.get('django_language', 'en')  # Default to English
        activate(session_language)  # Activate session language
        request.LANGUAGE_CODE = session_language  # Explicitly set it in the request object
        print(f"Forced activation: {session_language}, Current active: {get_language()}")
        return self.get_response(request)
