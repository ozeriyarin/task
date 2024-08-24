from django.apps import AppConfig

# Define a configuration class for the 'task' app
class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Specify the name of the app
    name = 'task'
    
    # This method is called when the application is ready
    def ready(self):
        # Import the signals module from the 'task' app
        import task.signals
