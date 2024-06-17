from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Sticky_Notes
from .forms import StickyForm

# logic to handle show all, creating notes, deleting and updating

# pass in request to function 
def notes_all(request):

    # store all notes created so far in notes variable
    notes = Sticky_Notes.objects.all()

    # create dicationary to pass into sticky_list template to be used a dynamic values 
    context = {
        'notes': notes,
        'sticky_note_title': 'Things to do',
    }

    # render correct page and pass in context object
    return render(request, 'sticky_notes/sticky_list.html', context)


# function for adding notes
def manage_notes(request):
    if request.method == 'POST':

# grab the parameters from the post request and store them to variable form
        form = StickyForm(request.POST)

# if truthy then save the values to the db / form
        if form.is_valid():
            notes = form.save(commit=False)
            notes.save()
            return redirect('notes_all')
#else create a new instance of 
# stickyForm and redirect to same page to populate
    else:
        form = StickyForm()
    return render(request, 'sticky_notes/sticky_form.html', {'form': form})


"""if the method is POST, grab the note-id 
and pass as parameter for id to get_object, if it exists, 
delete and return success messages"""

def delete_note(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        note = get_object_or_404(Sticky_Notes, id=note_id)
        note.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    

"""update function using primary key
 to select and update the correct sticky note"""
def update_note(request, pk):

    # pass in instance along with primary key to select correct sticky note to be updated
    note = get_object_or_404(Sticky_Notes, pk=pk)

    # if post, then pass in post parameters along with instance object of class as value for instance argument
    if request.method == 'POST':
        form = StickyForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_all')
    else:

        # redirect if back to same page if error
        form = StickyForm(instance=note)
    return render(request, 'sticky_notes/update_form.html', {'form': form, 'note': note})

