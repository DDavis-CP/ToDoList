from django.shortcuts import render, redirect
from django.views import View

from todo.models import Task, Note
from todo.forms import TaskForm, NoteForm


class TodoListView(View):
    def get(self, request):
        '''GET the todo list homepage, listing all tasks in reverse order that they were created'''
        incomplete_tasks = Task.objects.filter(completed =False)
        complete_tasks = Task.objects.filter(completed =True)
        form = TaskForm()

        return render(
            request=request, template_name = 'list.html', context = {'incomplete_tasks':incomplete_tasks,'complete_tasks':complete_tasks, 'form': form}
        )

    def post(self, request):
        '''POST the data in the from submitted by the user, creating a new task in the todo list'''
        form=TaskForm(request.POST)
        if form.is_valid():
            task_description = form.cleaned_data['description']
            Task.objects.create(description=task_description)

        # "redirect" to the todo homepage
        return redirect('todo_list')

class TodoNotesView(View):
    def get(self, request):
        '''GET the notes list homepage, listing all notes in reverse order that they were created'''
        notes = Note.objects.all()
        form = NoteForm()

        return render(
            request=request, template_name = 'notes.html', context = {'notes':notes, 'form': NoteForm}
        )

    def post(self, request):
        '''POST the data in the from submitted by the user, creating a new note in the note list'''
        form=NoteForm(request.POST)
        if form.is_valid():
            Note_text = form.cleaned_data['description']
            Note.objects.create(text=Note_text)

        # "redirect" to the notes page
        return redirect('notes')

class TodoDetailView(View):
    def get(self, request, task_id):
        '''GET the detail view of a single task on the todo list'''
        task = Task.objects.get(id=task_id)
        form = TaskForm(initial={'description': task.description})
        return render(
            request=request, template_name='detail.html', context={'form':form, 'id': task_id}
        )



    def post(self, request, task_id):
        '''Update or delete the specific task based on what the user submitted in the form'''
        task = Task.objects.filter(id=task_id)
        if 'save' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task_description = form.cleaned_data['description']
                task.update(description=task_description)
        elif 'delete' in request.POST:
            task.delete()
        elif 'complete' in request.POST:
            task.update(completed=True)

        # "redirect" to the todo homepage
        return redirect('todo_list')
