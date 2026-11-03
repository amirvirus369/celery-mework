from django import forms
from main import models
from parler.forms import TranslatableModelForm
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

class Create_Job(TranslatableModelForm):
    class Meta:
        model = models.Job
        fields = '__all__'
        exclude = ('user','slug')
        widgets = {
            'career': forms.Select(),
            'level1': forms.Select(),
            'level2': forms.Select(),
            'level3': forms.Select(),
            'status_work':forms.Select(),
            'cooperate_work':forms.Select(),

            'discription': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _('شرح وظایف، شرح محیط کاری و انتظاراتی که از کارجو دارید را به طور کامل بنویسید...')
            }),

            'title': forms.TextInput(attrs={'placeholder': _('مثلاً: توسعه‌دهنده')}),
            'name_company': forms.TextInput(attrs={'placeholder': _('مثلاً: شرکت فناوری اطلاعات کاریار')}),
            'location': forms.TextInput(attrs={'placeholder': _('مثلاً: تهران، جردن (یا ریموت)')}),
            'price_min': forms.NumberInput(attrs={'placeholder': _('از (مثلاً ۲۰)')}),
            'price_max': forms.NumberInput(attrs={'placeholder': _('تا (مثلاً ۳۵)')}),
            'specialized_Skill1': forms.TextInput(attrs={'placeholder': _('مثلاً: Tailwind CSS, React.js...')}),
            'specialized_Skill2': forms.TextInput(attrs={'placeholder': _('مثلاً: Tailwind CSS, React.js...')}),
            'specialized_Skill3': forms.TextInput(attrs={'placeholder': _('مثلاً: Tailwind CSS, React.js...')}),
            'skill_score1': forms.TextInput(attrs={'placeholder': _('مهارت امتیازی ۱ (مثلاً Three.js)')}),
            'skill_score2': forms.TextInput(attrs={'placeholder': _('مهارت امتیازی ۲')}),
            'skill_score3': forms.TextInput(attrs={'placeholder': _('مهارت امتیازی ۳')}),
            'skill_score4': forms.TextInput(attrs={'placeholder': _('مهارت امتیازی ۴')}),
            'skill_score5': forms.TextInput(attrs={'placeholder': _('مهارت امتیازی ۵')}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style_standard = 'w-full bg-slate-50 border border-slate-200 text-slate-800 text-sm rounded-xl px-4 py-3.5 focus:outline-none focus:border-karyar-500 focus:bg-white transition-all'
        style_select = 'w-full bg-slate-50 border border-slate-200 text-slate-800 text-sm rounded-xl px-4 py-3.5 focus:outline-none focus:border-karyar-500 focus:bg-white transition-all appearance-none cursor-pointer'
        style_small = 'w-full bg-white border border-slate-200 text-slate-800 text-xs rounded-xl p-3 focus:outline-none focus:border-karyar-500 transition-all'
        style_level = 'w-full bg-white border border-slate-200 text-xs rounded-lg px-2.5 py-2 text-slate-700 focus:outline-none focus:border-karyar-500'
        style_textarea = 'w-full bg-slate-50 border border-slate-200 text-slate-800 text-sm rounded-xl p-4 focus:outline-none focus:border-karyar-500 focus:bg-white transition-all leading-relaxed'

        field_styles = {
            'career': style_select,
            'title': style_standard,
            'name_company': style_standard,
            'location': style_standard,
            'price_min': style_standard,
            'price_max': style_standard,
            'discription': style_textarea,
            'specialized_Skill1': style_small,
            'specialized_Skill2': style_small,
            'specialized_Skill3': style_small,
            'level1': style_level,
            'level2': style_level,
            'level3': style_level,
            'skill_score1': style_small,
            'skill_score2': style_small,
            'skill_score3': style_small,
            'skill_score4': style_small,
            'skill_score5': style_small,
            'status_work':style_level,
            'cooperate_work':style_level
        }

        for field_name, css_class in field_styles.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['class'] = css_class




class Experience_form(TranslatableModelForm):
    class Meta:
        model = models.Experience
        fields = '__all__'
        exclude = ('experience',)
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-brand-500',
                'placeholder':_(' عنوان شغلی (مثال: توسعه‌دهنده فرانت‌اند)')
            }),
            'company':forms.TextInput(attrs={
                 'class':'w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-brand-500',
                'placeholder':_('نام شرکت')
            }),
             'discription':forms.Textarea(attrs={
                 'class':'w-full px-3 py-2 rounded-lg border border-slate-200 text-sm focus:outline-none focus:border-brand-500',
                'placeholder':_('توضیحات مختصر مسئولیت‌ها و دستاوردها...')
            })
        }

        
class resumeh_form(TranslatableModelForm):
    class Meta:
        model = models.Resumeh_me
        fields = ['img', 'link_git', 'link_din', 'skill1', 'skill2', 'skill3', 'history']
        exclude = ('user',)
        widgets = {
             'img':forms.ClearableFileInput(attrs={
                'class':'w-full h-full object-cover rounded-full shadow-inner border-2 border-white',
            }),
            'link_git':forms.TextInput(attrs={
                 'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm',
                'placeholder':'https://github.com/username'
            }),
             'link_din':forms.TextInput(attrs={
                 'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm',
                'placeholder':'https://linkedin.com/in/username'
            }),
             'skill1':forms.TextInput(attrs={
                'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm',
                'placeholder':_('مثال: React.js, Tailwind CSS, Django, Vue.js (با کاما جدا کنید)')
            }),
            'skill2':forms.TextInput(attrs={
                 'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm',
                'placeholder':_('مثال: React.js, Tailwind CSS, Django, Vue.js (با کاما جدا کنید)')
            }),
             'skill3':forms.Textarea(attrs={
                 'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm',
                'placeholder':_('مثال: React.js, Tailwind CSS, Django, Vue.js (با کاما جدا کنید)')
            }),
             'history':forms.Textarea(attrs={
                 'class':'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-500 focus:ring-2 focus:ring-brand-200 outline-none transition-all text-sm resize-none',
                'placeholder':_('علاقه‌مندی‌ها، اهداف شغلی و دستاوردهای اصلی خود را در چند جمله بیان کنید...'),
                'rows':'3'
            })
        }


ExperienceFormSet = inlineformset_factory(
    parent_model=models.Resumeh_me,
    model=models.Experience,
    form=Experience_form,
    extra=3,           
    can_delete=True,   
)


