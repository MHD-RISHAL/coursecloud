from django.shortcuts import render, redirect
from .forms import StudentReg,LoginForm
from django.views import View
from django.contrib.auth import authenticate,login
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView
from django.urls import reverse,reverse_lazy
from instructor.models import Course,Cart
from django.db.models import aggregates,Sum
from instructor.models import Order,Lesson,Module






class StudentRegistration(CreateView):
    template_name="student_reg.html"
    form_class=StudentReg
    success_url=reverse_lazy('student_login')
   
    
class LoginView(FormView):
    template_name="sign_in.html"
    form_class=LoginForm


    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pswd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pswd)

            if user:
                login(request, user)

                if getattr(user, "role", "").strip().lower() == "student":
                    return redirect("home")
                else:
                    return redirect(reverse("admin:login"))
            else:
                return redirect("student_login")
        else:
            return render(request, "sign_in.html", {"form": form})
  
class IndexView(ListView):
    template_name = "home.html"
    queryset = Course.objects.all()
    context_object_name = "courses"
  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        purchased_course = Order.objects.filter(student=self.request.user).values_list("course_object", flat=True)
        data["purchased_course"] = purchased_course  
        return data

class CourseDetails(DetailView):
    template_name="course_details.html"
    queryset=Course.objects.all()


class Addtocart(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        c_obj = Course.objects.get(id=id)
        user_object = request.user

        Cart.objects.get_or_create(
            course_object=c_obj,
            user_object=user_object
        )

        return redirect('home')

    


class CartSummery(View):
    def get(self, request):
        qs = request.user.basket.all()
        cart_total = qs.aggregate(total=Sum('course_object__price')).get('total')
        return render(request, "cartsummery.html", {"carts": qs, "basket_total": cart_total})

class Removefromcart(View):
    def get(self, request, **kwargs):
        id = kwargs.get('pk')
        Cart.objects.get(id=id).delete()
        return redirect('cartsummery')
    
class CheckOutView(View):
    def get(self,request,*args,**kwargs):
        basket_items=request.user.basket.all()
        order_total=sum([ci.course_object.price for ci in basket_items])
        order_instance=Order.objects.create(student=request.user,total=order_total)
        for ci in basket_items:
            order_instance.course_object.add(ci.course_object)
            ci.delete()
        order_instance.save()
        return redirect('home')

class Mycourse(View):
    def get(self, request, *args, **kwargs):
        orders= Order.objects.filter(student=request.user)
        return render(request, "mycourse.html", {"orders": orders}) 
        



