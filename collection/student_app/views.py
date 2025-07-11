from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .db import get_db
import json
import requests
# Home page
def home(request):
    return render(request, 'home.html')

# Show a simple HTML page
def index(request):
    return render(request, 'index.html', {'error': None, 'success': None})

# Combined GET and POST for adding student

@csrf_exempt
def add_student(request):
    db = get_db()

    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                name = data.get("name")
                age = data.get("age")
                Id = data.get("id")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            name = request.POST.get("name")
            age = request.POST.get("age")
            Id = request.POST.get("id")
    elif request.method == "GET":
        name = request.GET.get("name")
        age = request.GET.get("age")
        Id = request.GET.get("id")
    else:
        return HttpResponseBadRequest("Unsupported method")

    if not name or not age:
        return JsonResponse({"error": "Missing data"}, status=400)

    try:
        db.insert_one({"name": name, "age": int(age), "id": int(Id)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Student added successfully"})

def list_students(request):
    db = get_db()
    students = list(db.find({}, {"_id": 0}))
    return render(request, 'students.html', {'students': students})

@csrf_exempt
def update_student(request, student_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Only PUT allowed")
    db = get_db()
    try:
        data = json.loads(request.body)
        update_fields = {}
        if "name" in data:
            update_fields["name"] = data["name"]
        if "age" in data:
            update_fields["age"] = int(data["age"])
        result = db.update_one({"id": int(student_id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return JsonResponse({"error": "Student not found"}, status=404)
        return JsonResponse({"message": "Student updated successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_student(request, student_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Only DELETE allowed")
    db = get_db()
    try:
        result = db.delete_one({"id": int(student_id)})
        if result.deleted_count == 0:
            return JsonResponse({"error": "Student not found"}, status=404)
        return JsonResponse({"message": "Student deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)