from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify



class Career_field(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200,verbose_name='مربوط یو ار ال ',unique=True,null=True,blank=True)

    )
    icon = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'دسته بندی اگهی '
        verbose_name_plural = 'دسته بندی اگهی ها'
    def save(self, *args, **kwargs):
        if not self.safe_translation_getter('slug', any_language=True):
            name = self.safe_translation_getter('name', any_language=True)
            if name:
                self.slug = slugify(name, allow_unicode=True)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('work:category_job',kwargs={'slug':self.slug})

class Job(TranslatableModel):
    status_show = models.BooleanField(default=False,verbose_name='دیدن برای عموم')
    is_closed = models.BooleanField(default=False, verbose_name=_("پایان یافته/بسته شده"))
    career = models.ForeignKey(Career_field,on_delete=models.CASCADE,related_name='careerـfield_job')
    LEVEL_CHOICES = [
        ('JUNIOR', _("مبتدی (Junior)")),
        ('SENIOR', _("ارشد (Senior)")),
        ('EXPERT', _("تسلط کامل(expert)")),
    ]
    status_w = [
        ('remote',_('دورکاری')),
        ('Internship',_('کاراموزی')),
        ('In-person',_('حضوری'))
    ]
    cooperate = [
        ('full_time',_('تمام وقت')),
        ('Part-time',_('پاره وقت')),
        ('Project',_('پروژه ای'))
    ]
    price_min = models.IntegerField(default=0)
    price_max = models.IntegerField(default=0)
    cooperate_work = models.CharField(max_length=30,choices=cooperate)
    status_work = models.CharField(max_length=30,choices=status_w)
    level1 = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    level2 = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    level3 = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    translations = TranslatedFields(
    title = models.CharField(max_length=100),
    name_company = models.CharField(max_length=100),
    location = models.CharField(max_length=100),
    discription = models.TextField(),
    specialized_Skill1 = models.CharField(max_length=100),
    specialized_Skill2 = models.CharField(max_length=100),
    specialized_Skill3 = models.CharField(max_length=100),
    skill_score1 = models.CharField(max_length=100),
    skill_score2 = models.CharField(max_length=100),
    skill_score3 = models.CharField(max_length=100),
    skill_score4 = models.CharField(max_length=100),
    skill_score5 = models.CharField(max_length=100),
    slug = models.SlugField(max_length=200,verbose_name='مربوط یو ار ال ',unique=True,null=True,blank=True,allow_unicode=True)
    )
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'شغل'
        verbose_name_plural = 'شغل ها'
    def get_absolute_url(self):
        return reverse('work:detail_job',kwargs={'slug':self.slug})




class Resumeh_me(TranslatableModel):
    img = models.ImageField(upload_to='img')
    link_git = models.CharField(max_length=100)
    link_din = models.CharField(max_length=100)
    translations = TranslatedFields(
        skill1 = models.CharField(max_length=200),
        skill2 = models.CharField(max_length=200),
        skill3 = models.CharField(max_length=200),
        history = models.TextField()
    )
    class Meta:
        verbose_name = 'رزومه'
        verbose_name_plural = 'رزومه ها'


class Experience(TranslatableModel):
    experience = models.ForeignKey(Resumeh_me,on_delete=models.CASCADE,related_name='experience_me')
    translations = TranslatedFields(
        title = models.CharField(max_length=100),
        company = models.CharField(max_length=100),
        discription = models.TextField()
    )
    
