from celery import shared_task

from celery import shared_task
from deep_translator import MyMemoryTranslator
from django.utils.text import slugify
from django.apps import apps
from main.models import Job  


# TASK 1 for create job

TEXT_FIELDS = [
    'title', 'discription', 'name_company', 'location',
    'specialized_Skill1', 'specialized_Skill2', 'specialized_Skill3',
    'skill_score1', 'skill_score2', 'skill_score3', 'skill_score4', 'skill_score5',
]
LANG_MAP = {'fa': 'fa-IR', 'en': 'en-GB', 'ar': 'ar-SA'}
LANGUAGES = ['fa', 'en', 'ar']


_TRANSLATION_MODEL = Job._parler_meta.root_model


def _fit(field, value):
    """Cut the text to the DB column's max_length (avoids DataError)."""
    max_length = _TRANSLATION_MODEL._meta.get_field(field).max_length
    if max_length and isinstance(value, str) and len(value) > max_length:
        return value[:max_length]
    return value


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def translate_job(self, job_id, source_lang, suffix):
    job = Job.objects.get(pk=job_id)

    job.set_current_language(source_lang)
    source_values = {f: getattr(job, f, None) for f in TEXT_FIELDS}

    for lang in LANGUAGES:
        if lang == source_lang:
            continue

        translator = MyMemoryTranslator(
            source=LANG_MAP[source_lang],
            target=LANG_MAP[lang],
        )
        job.set_current_language(lang)

        for field, val in source_values.items():
            if val and isinstance(val, str) and val.strip():
                try:
                    translated = translator.translate(val)
                    if not translated or 'MYMEMORY WARNING' in translated.upper():
                        translated = val
                    setattr(job, field, _fit(field, translated))
                except Exception as e:
                    print(f"Translation error {field} -> {lang}: {e}")
                    setattr(job, field, _fit(field, val))
            else:
                setattr(job, field, val)

        title = getattr(job, 'title', '')
        base = slugify(title, allow_unicode=True) if title else 'job'
        job.slug = f"{base}-{suffix}-{lang}"

    job.save()



# TASK 2 for resumeh 

RESUME_MODEL = ('main', 'Resumeh_me')      
EXPERIENCE_RELATED_NAME = 'experience_me'   
RESUME_FIELDS = ['skill1', 'skill2', 'skill3', 'history']
EXPERIENCE_FIELDS = ['title', 'company', 'discription']

LANG_MAP = {'fa': 'fa-IR', 'en': 'en-GB', 'ar': 'ar-SA'}
LANGUAGES = ['fa', 'en', 'ar']


def _translate_object(obj, fields, source_lang):
    """Translate `fields` of one parler object into the other languages and save it."""
    translation_model = obj._parler_meta.root_model

    obj.set_current_language(source_lang)
    source_values = {f: getattr(obj, f, None) for f in fields}

    for lang in LANGUAGES:
        if lang == source_lang:
            continue

        translator = MyMemoryTranslator(source=LANG_MAP[source_lang], target=LANG_MAP[lang])
        obj.set_current_language(lang)

        for field, val in source_values.items():
            if val and isinstance(val, str) and val.strip():
                try:
                    translated = translator.translate(val)
                    if not translated or 'MYMEMORY WARNING' in translated.upper():
                        translated = val
                except Exception as e:
                    print(f"Translation error {field} -> {lang}: {e}")
                    translated = val

                max_length = translation_model._meta.get_field(field).max_length
                if max_length and len(translated) > max_length:
                    translated = translated[:max_length]
                setattr(obj, field, translated)
            else:
                setattr(obj, field, val if val is not None else '')

    obj.save()


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def translate_resume(self, resume_id, source_lang):
    Resume = apps.get_model(*RESUME_MODEL)
    resume = Resume.objects.get(pk=resume_id)

    _translate_object(resume, RESUME_FIELDS, source_lang)

    for exp in getattr(resume, EXPERIENCE_RELATED_NAME).all():
        _translate_object(exp, EXPERIENCE_FIELDS, source_lang)