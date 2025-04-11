from django.shortcuts import render, get_object_or_404
from .models import Scenario

def scenario_list(request):
    scenarios = Scenario.objects.all()
    return render(request, 'scenarios/scenario_list.html', {'scenarios': scenarios})

def scenario_detail(request, scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    dialogues = scenario.dialogues.order_by('order')  # Ensure messages are in order
    return render(request, 'scenarios/scenario_detail.html', {'scenario': scenario, 'dialogues': dialogues})
