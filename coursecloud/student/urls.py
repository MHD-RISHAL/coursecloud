from django.urls import path
from .views import *

urlpatterns = [
    path('studentreg', StudentRegistration.as_view(), name="studentreg"),
    path('student_login/', LoginView.as_view(), name='student_login'),
    path('home', IndexView.as_view(), name="home"),
    path('coursedet/<int:pk>/', CourseDetails.as_view(), name='course-details'),
    path('coursedet/<int:pk>/addtocart', Addtocart.as_view(), name='add_to_cart'),
    path('cartsummery', CartSummery.as_view(), name="cartsummery"),
    path('cartremove/<int:pk>/', Removefromcart.as_view(), name='cartremove'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('mycourse', Mycourse.as_view(), name='mycourse'),
]
