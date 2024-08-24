from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Client, Questionnaire, Question, ClientResponse
from .serializers import ClientSerializer, QuestionnaireSerializer, QuestionSerializer
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm, QuestionnaireForm, QuestionFormSet

# ViewSet for Client model, allowing CRUD operations via the Django REST Framework
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  # Retrieves all Client objects
    serializer_class = ClientSerializer  # Specifies the serializer class for Client

# ViewSet for Questionnaire model, allowing CRUD operations via the Django REST Framework
class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()  # Retrieves all Questionnaire objects
    serializer_class = QuestionnaireSerializer  # Specifies the serializer class for Questionnaire

# ViewSet for Question model, allowing CRUD operations via the Django REST Framework
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()  # Retrieves all Question objects
    serializer_class = QuestionSerializer  # Specifies the serializer class for Question

# ViewSet for ClientResponse model, allowing CRUD operations via the Django REST Framework
class ClientResponseViewSet(viewsets.ModelViewSet):
    queryset = ClientResponse.objects.all()  # Retrieves all ClientResponse objects
    serializer_class = ClientResponse  # Specifies the serializer class for ClientResponse

# Home page view
def home(request):
    return render(request, "home.html")  # Renders the home.html template

# Registration view for new users
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            user = form.save()  # Save the user if the form is valid
            login(request, user)  # Log the user in
            if user.is_staff:
                return redirect("admin_dashboard")  # Redirect to admin dashboard if user is staff
            else:
                return redirect("client_dashboard")  # Redirect to client dashboard if user is a client
    else:
        form = RegisterForm()  # Create a blank form if the request method is GET
    return render(request, "register.html", {"form": form})  # Render the register.html template with the form

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Bind the form with POST data
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            login(request, user)  # Log the user in
            if user.is_staff:
                return redirect("admin_dashboard")  # Redirect to admin dashboard if user is staff
            else:
                return redirect("client_dashboard")  # Redirect to client dashboard if user is a client
    else:
        form = LoginForm()  # Create a blank form if the request method is GET
    return render(request, "login.html", {"form": form})  # Render the login.html template with the form

# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect("login")  # Redirect to the login page

# Admin dashboard view
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  # Renders the admin_dashboard.html template

# Client dashboard view
def client_dashboard(request):
    client = request.user.client  # Get the client associated with the current user
    questionnaires = Questionnaire.objects.all()  # Retrieve all questionnaires

    # Check which questionnaires have been answered by the client
    answered_questionnaires = {
        response.questionnaire_id: True
        for response in ClientResponse.objects.filter(client=client)
    }

    if request.method == "POST":
        questionnaire_id = request.POST.get('questionnaire_id')  # Get the questionnaire ID from POST data
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        for question in questionnaire.questions.all():
            answer = request.POST.get(f'question_{question.id}')  # Get the answer for each question
            if answer:
                ClientResponse.objects.update_or_create(
                    client=client,
                    questionnaire=questionnaire,
                    question=question,
                    answer=answer
                )
        return redirect('client_dashboard')  # Redirect to the client dashboard

    return render(request, "client_dashboard.html", {"questionnaires": questionnaires, "answered_questionnaires": answered_questionnaires})

# View to display a list of all clients (admin only)
def client_list(request):
    clients = Client.objects.all()  # Retrieve all clients
    return render(request, "client_list.html", {"clients": clients})  # Render the client_list.html template

# View to display details of a specific client (admin only)
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)  # Get the specific client or return a 404 error
    questionnaires = Questionnaire.objects.all()  # Retrieve all questionnaires

    # Check which questionnaires have been answered by the client
    answered_questionnaires = {
        response.questionnaire_id: True
        for response in ClientResponse.objects.filter(client=client)
    }
    
    return render(
        request,
        "client_detail.html",
        {
            "client": client,
            'questionnaires': questionnaires,
            "answered_questionnaires": answered_questionnaires,
        },
    )

# View to display and manage a specific questionnaire
def questionnaire_detail(request, pk):
    questionnaire = get_object_or_404(Questionnaire, pk=pk)  # Get the specific questionnaire or return a 404 error
    
    if request.user.is_staff:
        client_id = request.GET.get('client_id')  # Get client ID from GET parameters
        client = get_object_or_404(Client, id=client_id) if client_id else None
    else:
        client = request.user.client  # Get the client associated with the current user

    if request.method == "POST":
        # Handle clearing answers
        if 'clear_answers' in request.POST and client:
            ClientResponse.objects.filter(client=client, questionnaire=questionnaire).delete()  # Delete client responses
            return redirect("questionnaire_detail", pk=pk)

        # Handle submitting answers
        if client:
            # Save or update answers
            for question in questionnaire.questions.all():
                answer = request.POST.get(f"question_{question.id}")  # Get the answer for each question
                if answer:
                    ClientResponse.objects.update_or_create(
                        client=client,
                        questionnaire=questionnaire,
                        question=question,
                        defaults={'answer': answer}
                    )
            return redirect("questionnaire_detail", pk=pk)

    # Fetch existing responses for the client
    client_responses = {
        response.question_id: response.answer 
        for response in ClientResponse.objects.filter(client=client, questionnaire=questionnaire)
    } if client else {}
    
    # Prepare questions with options and correct answers
    questions_with_options = []
    for question in questionnaire.questions.all():
        options = []
        correct_answer_id = None
        client_answer_is_correct = False

        for i in range(1, 6):
            option = getattr(question, f'option_{i}', None)
            if option:
                selected = client_responses.get(question.id) == i
                is_correct = question.answer == i  

                if is_correct:
                    correct_answer_id = i

                if selected and is_correct:
                    client_answer_is_correct = True

                options.append((i, option, selected))

        questions_with_options.append({
            'question': question,
            'options': options,
            'correct_answer_id': correct_answer_id,
            'correct_answer_text': correct_answer_id and options[correct_answer_id-1][1],
            'client_answer_is_correct': client_answer_is_correct,
        })
        
    answered_all_questions = len(client_responses) == questionnaire.questions.count()

    return render(
        request, "questionnaire_detail.html", 
        {
        "questionnaire": questionnaire,
        'questions_with_options': questions_with_options,
        'client_responses': client_responses,
        'answered_all_questions': answered_all_questions,
        'is_staff': request.user.is_staff,
    })

# View to create a new questionnaire (admin only)
def create_questionnaire(request):
    if request.method == "POST":
        form = QuestionnaireForm(request.POST)  # Bind the form with POST data
        formset = QuestionFormSet(request.POST, queryset=Question.objects.none())  # Bind the formset with POST data
        
        if form.is_valid() and formset.is_valid():
            questionnaire = form.save(commit=False)  # Save the questionnaire but don't commit to DB yet
            questionnaire.client = request.user.client  # Assign the current client to the questionnaire
            questionnaire.save()  # Save the questionnaire to the database
            
            questions = formset.save(commit=False)  # Save the questions but don't commit to DB yet
            for question in questions:
                question.questionnaire = questionnaire  # Assign the questionnaire to each question
                question.save()  # Save the question to the database

            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        
    else:
        form = QuestionnaireForm()  # Create a blank form
        formset = QuestionFormSet(queryset=Question.objects.none())  # Create a blank formset

    return render(request, 'create_questionnaire.html', {
        'form': form,
        'formset': formset,
    })  # Render the create_questionnaire.html template with the form and formset
