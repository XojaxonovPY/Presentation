from django.utils import translation


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL-dan ?lang=uz qismini qidiradi
        language = request.GET.get('lang')
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)
        return response
