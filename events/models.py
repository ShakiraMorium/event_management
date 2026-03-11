from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.conf import settings


class RSVP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)  
    status = models.CharField(max_length=10, choices=(('yes', 'Yes'), ('no', 'No')), default='yes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} RSVP'd {self.status} for {self.event.title}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Participant(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.name} - {self.event.name}"
  
    def participants_count(self):
        """Quick helper for templates/admin."""
        return self.participants.count()