from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ClientViewSet, QuestionnaireViewSet, ClientResponseViewSet

# Create a router and register the viewsets with it
router = DefaultRouter()
router.register(r"clients", ClientViewSet)  # Register the ClientViewSet
router.register(r"questionnaires", QuestionnaireViewSet)  # Register the QuestionnaireViewSet
router.register(r"questions", QuestionViewSet)  # Register the QuestionViewSet
router.register(r'clientresponse', ClientResponseViewSet)  # Register the ClientResponseViewSet

# Define the URL patterns for the application
urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("register/", views.register, name="register"),  # Registration page
    path("login/", views.login_view, name="login"),  # Login page
    path("logout/", views.logout_view, name="logout"),  # Logout functionality
    path("client_dashboard/", views.client_dashboard, name="client_dashboard"),  # Client dashboard
    path("questionnaire/<int:pk>/", views.questionnaire_detail, name="questionnaire_detail"),  # Questionnaire detail page
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),  # Admin dashboard
    path("client/<int:client_id>/", views.client_detail, name="client_detail"),  # Client detail page
    path("create_questionnaire/", views.create_questionnaire, name="create_questionnaire"),  # Create a new questionnaire
    path("client_list/", views.client_list, name="client_list"),  # List of clients
]

# Add the router's URLs to the urlpatterns
urlpatterns += router.urls
