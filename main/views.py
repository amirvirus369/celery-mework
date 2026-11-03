from django.shortcuts import render
import uuid
from django.db import transaction
from django.utils.text import slugify
from main.tasks.task1 import translate_job,translate_resume, RESUME_FIELDS, EXPERIENCE_FIELDS
from main import forms
from deep_translator import MyMemoryTranslator



# create job with celery 

def creat_job_celery(request):
    if request.method == 'POST':
        form = forms.Create_Job(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            
            common_fields = ['career', 'level1', 'level2', 'level3', 'status_work',
                             'cooperate_work', 'price_min', 'price_max']
            for field in common_fields:
                if field in form.cleaned_data:
                    setattr(ins, field, form.cleaned_data.get(field))

            current_lang = getattr(request, 'LANGUAGE_CODE', 'fa')
            if current_lang.startswith('fa'):
                current_lang = 'fa'

            text_fields = [
                'title', 'discription', 'name_company', 'location',
                'specialized_Skill1', 'specialized_Skill2', 'specialized_Skill3',
                'skill_score1', 'skill_score2', 'skill_score3', 'skill_score4', 'skill_score5',
            ]

            ins.set_current_language(current_lang)
            for field in text_fields:
                setattr(ins, field, form.cleaned_data.get(field))

            unique_suffix = str(uuid.uuid4())[:6]
            title = form.cleaned_data.get('title')
            base = slugify(title, allow_unicode=True) if title else 'job'
            ins.slug = f"{base}-{unique_suffix}"

            ins.save()

            transaction.on_commit(
                lambda: translate_job.delay(ins.pk, current_lang, unique_suffix)
            )

            return render(request, 'creat-job.html',
                          {'form': forms.Create_Job(), 'success_redirect': True})
    else:
        form = forms.Create_Job()

    return render(request, 'creat-job.html', {'form': form})





# create job without celery


def creat_job(request):
    if request.method == 'POST':
        form = forms.Create_Job(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            
            ins.user = request.user
            
            common_fields = ['career', 'level1', 'level2', 'level3', 'status_work', 'cooperate_work', 'price_min', 'price_max']
            for field in common_fields:
                if field in form.cleaned_data:
                    setattr(ins, field, form.cleaned_data.get(field))

            current_lang = getattr(request, 'LANGUAGE_CODE', 'fa')
            if current_lang.startswith('fa'):
                current_lang = 'fa'

            text_fields = [
                'title', 'discription', 'name_company', 'location',
                'specialized_Skill1', 'specialized_Skill2', 'specialized_Skill3',
                'skill_score1', 'skill_score2', 'skill_score3', 'skill_score4', 'skill_score5'
            ]
            
            lang_map = {
                'fa': 'fa-IR',
                'en': 'en-GB',
                'ar': 'ar-SA'
            }

            languages = ['fa', 'en', 'ar']
            unique_suffix = str(uuid.uuid4())[:6]
            for lang in languages:
                ins.set_current_language(lang)

                if lang == current_lang:
                    for field in text_fields:
                        setattr(ins, field, form.cleaned_data.get(field))
                else:
                    target_code = lang_map.get(lang, lang)
                    source_code = lang_map.get(current_lang, 'fa-IR')
                    
                    translator = MyMemoryTranslator(source=source_code, target=target_code)
                    
                    for field in text_fields:
                        val = form.cleaned_data.get(field)
                        if val and isinstance(val, str) and val.strip():
                            try:
                                translated_text = translator.translate(val)
                                setattr(ins, field, translated_text if translated_text else val)
                            except Exception as e:
                                print(f"Translation Error for {field} in {lang}: {e}")
                                setattr(ins, field, val)
                        else:
                            setattr(ins, field, val)

                
                translated_title = getattr(ins, 'title', '')
                if translated_title:
                    lang_slug = slugify(translated_title, allow_unicode=True)
                    ins.slug = f"{lang_slug}-{unique_suffix}"
                else:
                    ins.slug = f"job-{unique_suffix}"

            ins.save()
            return render(request, 'creat-job.html', {'form': forms.Create_Job(), 'success_redirect': True})
    else:
        form = forms.Create_Job()

    context = {'form': form}
    return render(request, 'creat-job.html', context)



# create resumeh with celery 


def resumeh_celery(request):
    if request.method == 'POST':
        form = forms.resumeh_form(request.POST, request.FILES)
        formset = forms.ExperienceFormSet(request.POST, prefix='experiences')
 
        if form.is_valid() and formset.is_valid():
            current_lang = getattr(request, 'LANGUAGE_CODE', 'fa')
            if current_lang.startswith('fa'):
                current_lang = 'fa'
 
            with transaction.atomic():
                ins = form.save(commit=False)
 
                ins.set_current_language(current_lang)
                for field in RESUME_FIELDS:
                    setattr(ins, field, form.cleaned_data.get(field))
                ins.save()
 
                formset.instance = ins
                experiences = formset.save(commit=False)
 
                for exp in experiences:
                    matching_form = next(
                        (f for f in formset.forms if f.cleaned_data and f.instance == exp),
                        None
                    )
                    if not matching_form:
                        continue
                    exp.set_current_language(current_lang)
                    for field in EXPERIENCE_FIELDS:
                        setattr(exp, field, matching_form.cleaned_data.get(field))
                    exp.save()
 
                for deleted_obj in formset.deleted_objects:
                    deleted_obj.delete()
 
                resume_pk = ins.pk
                transaction.on_commit(
                    lambda: translate_resume.delay(resume_pk, current_lang)
                )
 
            return render(
                request,
                'build-resume.html',
                {
                    'form': forms.resumeh_form(),
                    'formset': forms.ExperienceFormSet(prefix='experiences'),
                    'success_redirect': True,
                }
            )
    else:
        form = forms.resumeh_form()
        formset = forms.ExperienceFormSet(prefix='experiences')
 
    return render(request, 'build-resume.html', {'form': form, 'formset': formset})



# create resumeh without celery 


def resumeh(request):
    LANG_MAP = {
        'fa': 'fa-IR',
        'en': 'en-GB',
        'ar': 'ar-SA'
    }
    LANGUAGES = ['fa', 'en', 'ar']

    if request.method == 'POST':
        form = forms.resumeh_form(request.POST, request.FILES)
        formset = forms.ExperienceFormSet(request.POST, prefix='experiences')

        if form.is_valid() and formset.is_valid():
            current_lang = getattr(request, 'LANGUAGE_CODE', 'fa')
            if current_lang.startswith('fa'):
                current_lang = 'fa'

            ins = form.save(commit=False)
            resume_text_fields = ['skill1', 'skill2', 'skill3', 'history']

            for lang in LANGUAGES:
                ins.set_current_language(lang)
                if lang == current_lang:
                    for field in resume_text_fields:
                        setattr(ins, field, form.cleaned_data.get(field))
                else:
                    source_code = LANG_MAP.get(current_lang, 'fa-IR')
                    target_code = LANG_MAP.get(lang, lang)
                    translator = MyMemoryTranslator(source=source_code, target=target_code)

                    for field in resume_text_fields:
                        val = form.cleaned_data.get(field)
                        if val and isinstance(val, str) and val.strip():
                            try:
                                translated_text = translator.translate(val)
                                setattr(ins, field, translated_text if translated_text else val)
                            except Exception as e:
                                print(f"Translation Error for {field} in {lang}: {e}")
                                setattr(ins, field, val)
                        else:
                            setattr(ins, field, val)
            ins.save()

            formset.instance = ins
            experiences = formset.save(commit=False)
            exp_text_fields = ['title', 'company', 'discription']

            for exp in experiences:
                matching_form = next(
                    (f for f in formset.forms if f.cleaned_data and f.instance == exp), 
                    None
                )
                if not matching_form:
                    continue

                for lang in LANGUAGES:
                    exp.set_current_language(lang)
                    if lang == current_lang:
                        for field in exp_text_fields:
                            setattr(exp, field, matching_form.cleaned_data.get(field))
                    else:
                        source_code = LANG_MAP.get(current_lang, 'fa-IR')
                        target_code = LANG_MAP.get(lang, lang)
                        translator = MyMemoryTranslator(source=source_code, target=target_code)

                        for field in exp_text_fields:
                            val = matching_form.cleaned_data.get(field)
                            if val and isinstance(val, str) and val.strip():
                                try:
                                    translated_text = translator.translate(val)
                                    setattr(exp, field, translated_text if translated_text else val)
                                except Exception as e:
                                    print(f"Exp Translation Error for {field} in {lang}: {e}")
                                    setattr(exp, field, val)
                            else:
                                setattr(exp, field, val)
                exp.save()

            for deleted_obj in formset.deleted_objects:
                deleted_obj.delete()

            return render(
                request, 
                'build-resume.html', 
                {
                    'form': forms.resumeh_form(), 
                    'formset': forms.ExperienceFormSet(prefix='experiences'), 
                    'success_redirect': True
                }
            )

    else:
        form = forms.resumeh_form()
        
        formset = forms.ExperienceFormSet(prefix='experiences')
       
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'build-resume.html', context)




def main(request):
    text = 'یکی رو انتخاب کن'
    choise_1 = 'ساخت اگهی  '
    choise_2 =  'ساخت رزومه '
    page = 1
    context = {
        'choise1':choise_1,
        'choise2':choise_2,
        'page':page,
        'text':text
    }
    return render(request,'choise.html',context)


def job(request):
    text = 'قسمت اگهی '
    choise_1 = 'با سلری'
    choise_2 = 'بدون سلری'
    page = 2
    context = {
        'choise1':choise_1,
        'text':text,
        'choise2':choise_2,
        'page':page
    }
    return render(request,'choise.html',context)


def res(request):
    text = 'قسمت رزومه '
    choise_1 = 'با سلری'
    choise_2 = 'بدون سلری'
    page = 3
    context = {
        'text':text,
        'choise1':choise_1,
        'choise2':choise_2,
        'page':page
    }
    return render(request,'choise.html',context)