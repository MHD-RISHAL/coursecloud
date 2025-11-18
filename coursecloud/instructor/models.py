from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from embed_video.fields import EmbedVideoField




# Create your models here.


class User(AbstractUser):
    role_options = [
        ("instructor", "instructor"),
        ("student", "student"),
    ]
    role = models.CharField(max_length=30, choices=role_options, default="student")

class InstructorProfile(models.Model):
    expertise=models.CharField(max_length=100,null=True)
    picture=models.ImageField(upload_to="profilepics",null=True,blank=True,default="profilepic/default.png")
    description=models.CharField(max_length=200,null=True)
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    def __str__(self):
        return self.owner.username


def create_instructor_profile(sender,instance,created,**kwargs):
    if created and instance.role== "instructor":
        InstructorProfile.objects.create(owner=instance)

post_save.connect(create_instructor_profile,User  )    

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=6)
    picture=models.ImageField(upload_to="course_pics",null=True,blank=True,default="course_pics/default.png")
    thumbnail=EmbedVideoField()
    is_free=models.BooleanField(default=False)
    instructor=models.ForeignKey(User,on_delete=models.SET_NULL,related_name="courses",null=True)
    Category_obj=models.ManyToManyField(Category)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title

from django.db.models import Max    
    
from django.db import models
from django.db.models import Max

from django.db import models
from django.db.models import Max

class Module(models.Model):
    title = models.CharField(max_length=100)
    course_object = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules"
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically set order only when creating a new module
        if self.pk is None:
            max_order = (
                Module.objects
                .filter(course_object=self.course_object)
                .aggregate(max_order=Max("order"))
                .get("max_order")
                or 0
            )
            self.order = max_order + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]



class Lesson(models.Model):
    title = models.CharField(max_length=200)
    module_object = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    video = EmbedVideoField(null=True, blank=True)
    order = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.pk is None:  # only auto-assign when creating
            max_order = Lesson.objects.filter(module_object=self.module_object).aggregate(max_order=Max("order")).get("max_order") or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}.{self.module_object.title} - {self.title}"

    class Meta:
        ordering = ["order"]


class Cart(models.Model):
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name='basket')
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    course_object=models.ManyToManyField(Course,related_name="enrollment")
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    is_paid = models.BooleanField(default=False)
    rzr_order_id=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)

