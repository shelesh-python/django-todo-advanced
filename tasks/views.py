# =======================
# 1️⃣ IMPORTS
# =======================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .decorators import admin_required


# =======================
# 2️⃣ AUTHENTICATION VIEWS
# =======================

def register_view(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)

            # 🔐 Role-based redirect
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# =======================
# 3️⃣ DASHBOARD VIEWS
# =======================

@login_required
def user_dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    return render(request, 'user_dashboard.html', {
        'tasks': tasks,
        'completed': completed,
        'pending': pending
    })


# =======================
# ADMIN DASHBOARD
# =======================


@login_required
@admin_required
def admin_dashboard(request):
    tasks = Task.objects.all()
    users = User.objects.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    return render(request, 'admin_dashboard.html', {
        'tasks': tasks,
        'users': users,
        'completed': completed,
        'pending': pending
    })


# =======================
# 4️⃣ TASK CRUD VIEWS
# =======================

@login_required
def add_task(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title']
        )
    return redirect('user_dashboard')


@login_required
def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('user_dashboard')


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('user_dashboard')


# =======================
# 5️⃣ REST API VIEWS
# =======================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_api(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_task_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
