from django.db import models
from django.contrib.auth.models import User
from .blog_email import send_email


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image1 = models.ImageField(upload_to='images', max_length = 100, null=True, blank = True)
    image2 = models.ImageField(upload_to='images', max_length = 100, null=True, blank = True)
    image3 = models.ImageField(upload_to='images', max_length = 100, null=True, blank = True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')

    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        email_list = EmailSubscription.objects.all()
        send_email(email_list)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class EmailSubscription(models.Model):
    sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    email = models.EmailField(unique = True)
    status = models.CharField(max_length=64, null=False, blank=True)
    created_date = models.DateTimeField(auto_now = True, null=False, blank=True)
    updated_date = models.DateTimeField(auto_now = True, null=False, blank=True)

    def __str__(self):
        return self.email
    