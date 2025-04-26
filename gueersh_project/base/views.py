from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.auth.decorators import login_required

logging.basicConfig(level=logging.INFO)

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def about(request):
    context = {}
    return render(request, 'base/about.html', context)

def music(request):
    context = {}
    return render(request, 'base/music.html', context)

"""
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

def submit_worker_node(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        files = request.FILES
        audience = settings.WORKER_NODE_HOST + settings.WORKER_NODE_PORT
        endpoint = audience + "/multi_process"
    
        logging.info(f"audience: {audience}\nendpoint: {endpoint}")

        try:
            lang = form_data['prog_lang']
            problem_id = int(form_data['problem_id'])
            
            found_solution = False
            for problem in settings.PROBLEMS:
                if problem['id'] == problem_id and problem['lang'] == lang:
                    form_data['professor_code'] = problem['prof_code']
                    form_data['func'] = problem['header']
                    form_data['return_type'] = problem['return_type']
                    form_data['test_cases'] = problem['test_cases']
                    found_solution = True
                    break
                       
            if not found_solution:
                return JsonResponse({"error": "Error on getting solution and test cases"}, status=400)

            #Enviando os dados para o worker-node
            logging.info(f"debug mode: {settings.DEBUG}")

            return JsonResponse(flask_response, safe=False)    #Preciso do safe=False já que o worker-node retorna uma lista de dicionários
        except requests.exceptions.RequestException as e:
            print("Request exception:", str(e))
            return JsonResponse({"error": "Failed to communicate with Worker-Node", "details": str(e)}, status=500)
        except Exception as e:
            print("Unexpected exception:", str(e))
            return JsonResponse({"error": "Unexpected error", "details": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
"""