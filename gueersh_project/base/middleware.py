from django.contrib import messages

class ClearMessagesInAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #Se estiver acessando o Django Admin, vou limpar as mensagens
        if request.path.startswith('/admin/'):
            list(messages.get_messages(request))

        response = self.get_response(request)
        return response