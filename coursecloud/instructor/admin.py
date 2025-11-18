from django.contrib import admin
from .models import User,Category,Course,Module,Lesson

# Register your models here.
admin.site.register(User)
admin.site.register(Category)

class LessonInline(admin.TabularInline):
    model=Lesson
    extra=1

class ModuleAdmin(admin.ModelAdmin):
    inlines=[LessonInline ]
    exclude=('order', )

class CourseAdmin(admin.ModelAdmin):
    exclude=('instructor',)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.instructor=request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Course,CourseAdmin)
admin.site.register(Module,ModuleAdmin)
# admin.site.register(Lesson)
