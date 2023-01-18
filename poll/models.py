from django.db import models
from django.contrib.auth.models import User

class StudentRange(models.Model):
    student_range = models.CharField(max_length=50)
    def __str__(self):
        return self.student_range


class StudentCourse(models.Model):
    student_course = models.CharField(max_length=50)
    def __str__(self):
        return self.student_course

class Position(models.Model):
	person_position = models.CharField(max_length=200)
	def __str__(self):
		return self.person_position


class Poll(models.Model):
    person_name = models.CharField(max_length=200)
    person_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    person_position = models.ForeignKey(Position, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    person_photo = models.ImageField(blank=True, null=True)
    have_vote = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class CompleteRegistration(models.Model):
    student_range = models.ForeignKey(StudentRange, on_delete=models.CASCADE)
    your_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, default=0)
    profile_picture = models.ImageField()
    relation = models.OneToOneField(User, on_delete=models.CASCADE)
    can_vote = models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        self.profile_picture.delete()
        super(CompleteRegistration, self).delete(*args, **kwargs)

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message
    
class AdminSitting1(models.Model):
    start_vote = models.BooleanField(default=False)
    registration_complete = models.BooleanField(default=False)
    show_results = models.BooleanField(default=False)
    be_inform = models.CharField(max_length=200)
    