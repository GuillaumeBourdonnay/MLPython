from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.renderers import JSONRenderer 
from rest_framework.parsers import JSONParser
from prediction.models import Incident 
from prediction.serializers import IncidentSerializer


def predict_incident(unscaled_data):
    from sklearn.externals import joblib
    colonnes = ['number', 'active', 'reassignment_count', 'reopen_count',
       'sys_mod_count', 'made_sla', 'caller_id', 'opened_by', 'sys_created_by',
       'sys_updated_by', 'location', 'category', 'subcategory', 'u_symptom',
       'impact', 'urgency', 'priority', 'assignment_group', 'assigned_to',
       'knowledge', 'u_priority_confirmation', 'closed_code', 'resolved_by',
       'opened_at_TS', 'sys_updated_at_TS', 'resolved_at_TS',
       'sys_created_at_TS', 'sys_updated_at_weekend', 'incident_state_Active',
       'incident_state_Awaiting_Evidence', 'incident_state_Awaiting_Problem',
       'incident_state_Awaiting_User_Info', 'incident_state_Awaiting_Vendor',
       'incident_state_Closed', 'incident_state_New',
       'incident_state_Resolved']
    path_to_model   = "../../model_randomForest.pkl"
    #path_for_scaler = "./ipynb/scaler.pkl"
    unscaled_data   = [unscaled_data[colonne] for colonne in colonnes]
    model           = joblib.load(path_to_model)
    #scaler          = joblib.load(path_for_scaler)
    #donnees_scalees = scaler.transform(unscaled_data)
    #medv            = model.predict(donnees_scalees)
    pred = model.predict(unscaled_data)
    return pred

@csrf_exempt
def predict(request):
    """
    Renvoie une Incident avec la MEDV completee
    (Attend une MEDV innexistante)
    """
    if request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'POST':
        print(request)
        data        = JSONParser().parse(request)
        serializer  = IncidentSerializer(data=data)
        if serializer.is_valid():
            data["MEDV"]        = predict_medv(data)
            serializer          = IncidentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data  , status=201)
        return     JsonResponse(serializer.errors, status=400)

@csrf_exempt
def incident_list(request):
	if request.method== 'GET':
		Incidents= Incident.objects.all()
		serializer= IncidentSerializer(Incidents, many=True)
		return JsonResponse(serializer.data, safe=False)
	elif request.method== 'POST':
		data        = JSONParser().parse(request)
		serializer= IncidentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return     JsonResponse(serializer.errors, status=400)

@csrf_exempt
def incident_detail(request, pk):
    """
    Retrieve, update or delete a Incident.
    """
    try:
        Incident = Incident.objects.get(pk=pk)
    except Incident.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IncidentSerializer(Incident)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IncidentSerializer(Incident, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Incident.delete()
        return HttpResponse(status=204)