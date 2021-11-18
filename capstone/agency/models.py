from django.db import models
from accounts.models import User
import datetime
from django.urls import reverse
from capstone.helper import docs_upload_directory, images_upload_directory
# Create your models here.

class JobCategory(models.Model):
    name = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
      return f"Name : {self.name}; # discription :  {self.discription}"


class Address(models.Model):
    first_line = models.CharField(max_length=100)
    street_name = models.CharField(max_length=64)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=64)
    address_type = models.IntegerField(  
        choices=[(1, 'Home'),(2, 'Business'),(3, 'Postal')],
        default=1,
    ) 
    created = models.DateTimeField(auto_now=True, blank=True)

    def get_absolute_url(self):
        return reverse('address-detail', kwargs={'pk': self.pk})
        
    class Meta:
        ordering = ['created']

    def __str__(self):
      return f"first line : {self.first_line}; ### city :  {self.city}"

class Office(models.Model):
    manager = models.ForeignKey(User, on_delete=models.PROTECT,blank=True, null=True )
    name = models.CharField(max_length=100)
    discription = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    location = models.ForeignKey(Address, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, blank=True)
    image = models.FileField(blank=True, null=True,verbose_name="Logo optional", upload_to=images_upload_directory)
    imgUrl = models.CharField(max_length=100, blank=True, null=True, default="agency/images/avatar.png")

    def get_absolute_url(self):
        return reverse('office-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['created']

    def __str__(self):
      return  self.name

class Job(models.Model):
    title = models.CharField(max_length=100)    
    contract_type = models.IntegerField(  
        choices=[(1, 'Permanent'),(2, 'Temporary'),(3, 'Pay as you go')],
        default=1,
    )  
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    isSecured = models.BooleanField(default=False)
    inAddvert = models.BooleanField(default=True)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    hire_date = models.DateTimeField(null= True, blank=True)
    termination_date = models.DateTimeField(null= True, blank=True)   
    created = models.DateTimeField(auto_now=True, blank=True)   
    employee = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='employee')
    job_discription_url = models.URLField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Job Title : {self.title}"

class Advert(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    Core_requirements = models.TextField(max_length=300,null= True, blank=True)  
    open_date = models.DateTimeField()
    close_date = models.DateTimeField(null= True, blank=True)
    created = models.DateTimeField(auto_now=True, blank=True) 
    positions = models.IntegerField(default=0)  
    closed = models.BooleanField(default=False)
    image = models.FileField(blank=True,verbose_name="Logo optional", null=True,upload_to=images_upload_directory)
    imgUrl = models.CharField(max_length=100, blank=True, null=True, default="agency/images/avatar.png")
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT,blank=True, null=True )
    #applications = models.ManyToManyField(Application,blank=True, related_name="job_applications")


    def isClosed(self):
        if self.close_date <= datetime.datetime.now():
            self.Closed = True
            self.save()
            return True;
        return False

    def get_absolute_url(self):
        return reverse('advert-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Job Title : {self.job}; open date: {self.open_date}; close date: {self.close_date};"

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applicant")    
    #address = models.ForeignKey(Address, on_delete=models.PROTECT)   
    cover_letter = models.TextField(blank=True, null=True)
    cv = models.FileField(verbose_name="Upload CV",upload_to=docs_upload_directory)
    fileUrl = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=True, blank=True)
    isSelected = models.BooleanField(default=False)
    advert = models.ForeignKey(Advert, on_delete=models.PROTECT,blank=True, null=True )
    
    def get_absolute_url(self):
        return reverse('application-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']

    def __str__(self):
      return f"First Name : {self.applicant.first_name}; # Last Name : {self.applicant.last_name}"

