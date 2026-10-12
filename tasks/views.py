from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        user=request.user
    ).order_by('due_date')

    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    context = {
        'tasks': tasks,
        'selected_status': status,
        'selected_priority': priority,
    }

    return render(
        request,
        'tasks/task_list.html',
        context
    )


@login_required
def create_task(request):

    if request.method == 'POST':

        Task.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            status=request.POST.get('status'),
            priority=request.POST.get('priority'),
            due_date=request.POST.get('due_date')
        )

        return redirect('task_list')

    return render(
        request,
        'tasks/create_task.html'
    )