from django.db import models

# Create your models here.
class tenure_raw(models.Model):
    tenure       = models.CharField(max_length=128)
    # project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group        = models.CharField(max_length=128,default='')
    created_date = models.DateField()
    rate         = models.FloatField()


    ####ZF trying form
    ### This function is to validate phone number is 10 digits
    # def validate_digit_length(phone):
    #     if not (phone.isdigit() and len(phone) == 10):
    #         raise ValidationError('%(phone)s must be 10 digits',params={'phone':phone})

    # user_age               = models.IntegerField(null=True)
    # # user_emergency_contact = models.IntegerField()
    # user_emergency_contact = models.CharField(
    #     verbose_name="Phone number", 
    #     max_length=10,
    #     validators=[RegexValidator(regex='^(\d{10})$',message='Must be 10 digit number!',code="nomatch")],
    #     default=''
    #     )
    # #### End


    def __str__(self):
        return self.tenure

    # # helper function to get all the SearchKey by this project
    # def getSearchKey(self):
    #     searchKeys = SearchKey.objects.filter(project_id=self.project_id)
    #     return searchKeys