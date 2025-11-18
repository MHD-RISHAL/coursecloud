from django.shortcuts import render,redirect
from django.views import View
from .forms import InstructorCreationForm



 
class InstructorRegview(View):
    def get(self, request):
        form = InstructorCreationForm()  
        return render(request, "insreg.html", {"form": form})

    def post(self, request):
        form_data = InstructorCreationForm(data=request.POST)
        if form_data.is_valid():
            form_data.instance.role = "instructor"
            form_data.instance.is_superuser = True
            form_data.instance.is_staff = True
            form_data.save()
            return redirect('instructor')
        return render(request, "insreg.html", {"form": form_data})


