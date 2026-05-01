from .models import Department, Location


def global_context(request):
    return {
        'departments': Department.objects.all(),
        'locations': Location.objects.all(),
    }
