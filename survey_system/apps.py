from django.apps import AppConfig


class SurveySystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'survey_system'
    def ready(self) -> None:
        import survey_system.signals