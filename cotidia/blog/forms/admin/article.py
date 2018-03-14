import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from betterforms.forms import BetterModelForm

from cotidia.blog.models import Article, ArticleTranslation, ArticleDataSet
from cotidia.blog.settings import BLOG_TEMPLATES
from cotidia.admin.widgets import DateInput, TimeInput
from cotidia.account.models import User


class ArticleAddForm(BetterModelForm):

    display_title = forms.CharField(
        help_text=_(
            "The display title is only used to represent the page "
            "within the CMS. This value should not be used for the title "
            "displayed on the web page."
        ),
        widget=forms.TextInput(attrs={'class': 'form__text'})
    )

    template = forms.ChoiceField(
        help_text=_(
            "The template defines the layout of page, as well as the "
            "editable areas."
        ),
        choices=BLOG_TEMPLATES,
        widget=forms.Select(attrs={'class': 'form__select'})
    )

    date = forms.DateField(
        label="Publish date",
        widget=DateInput,
        initial=timezone.now()
    )

    time = forms.TimeField(
        label="Publish time",
        widget=TimeInput,
        required=False,
        initial=timezone.now()
    )

    author = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.Select(attrs={'class': "form__select"}),
        empty_label=""
    )

    class Meta:
        model = Article
        fields = [
            'display_title',
            'template',
            'date',
            'time',
            'author',
        ]
        fieldsets = (
            ('info', {
                'fields': (
                    'display_title',
                    'template',
                ),
                'legend': 'Article information'
            }),
            ('options', {
                'fields': (
                    ('date', 'time'),
                    'author'
                ),
                'legend': 'Options'
            }),
        )

    def __init__(self, *args, **kwargs):
        super(ArticleAddForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.publish_date:
            self.fields['date'].initial = self.instance.publish_date
            self.fields['time'].initial = self.instance.publish_date

    def clean_home(self):
        home = self.cleaned_data['home']

        if home:
            err_message = _("There is already another page set as home.")

            # Check if other pages are already home excluded the current
            # edited page
            if self.instance:
                if self.Meta.model.objects.filter(published_from=None, home=True).exclude(id=self.instance.id):
                    raise forms.ValidationError(err_message)
            # Check if other pages are already home excluded
            else:
                if self.Meta.model.objects.filter(published_from=None, home=True):
                    raise forms.ValidationError(err_message)

        return home

    def save(self, commit=True):
        instance = super(ArticleAddForm, self).save(commit=False)

        # Process publish date
        now = timezone.now()

        if self.cleaned_data['date']:
            now = now.replace(year=self.cleaned_data['date'].year)
            now = now.replace(month=self.cleaned_data['date'].month)
            now = now.replace(day=self.cleaned_data['date'].day)
            instance.publish_date = now

        if self.cleaned_data['date'] and self.cleaned_data['time']:
            now = now.replace(hour=self.cleaned_data['time'].hour)
            now = now.replace(minute=self.cleaned_data['time'].minute)
            instance.publish_date = now

        if commit:
            instance.save()

        return instance


class ArticleUpdateForm(ArticleAddForm):

    slug = forms.CharField(
        help_text=_("A unique identifier to allow retrieving a page"),
        widget=forms.TextInput,
        required=False
    )

    dataset = forms.ModelChoiceField(
        queryset=ArticleDataSet.objects.all(),
        widget=forms.Select,
        required=False,
        empty_label=""
    )

    class Meta:
        model = Article
        fields = [
            'display_title',
            'template',
            'dataset',
            'slug',
            'date',
            'time',
            'author',
        ]
        fieldsets = (
            ('info', {
                'fields': (
                    'display_title',
                    'template',

                ),
                'legend': 'Article information'
            }),
            ('dataset', {
                'fields': (
                    'dataset',
                ),
                'legend': 'Dataset'
            }),
            ('options', {
                'fields': (
                    ('date', 'time'),
                    'author',
                    'slug',
                ),
                'legend': 'Options'
            }),
        )


class ArticleURLForm(forms.ModelForm):

    slug = forms.CharField(
        help_text=_(
            "The URL should only contain lowercase letters, "
            "numbers and dashes (-)."
        ),
        widget=forms.TextInput(attrs={
            'onKeyUp': 'updateSlug(this)'
        })
    )

    class Meta:
        model = ArticleTranslation
        fields = [
            'slug'
        ]

    def clean_slug(self):

        slug = self.cleaned_data['slug']

        # Trim spaces
        slug = slug.strip()

        slug_pattern = re.compile("^([a-z0-9\-]+)$")

        if not slug_pattern.match(slug):
            raise forms.ValidationError(_("The URL is not valid "
                "because it contains unallowed characters. "
                "Only lowercase letters, numbers and dashes are accepted."))

        pages = [page.slug for page in ArticleTranslation.objects.all()]

        error_message = _('The unique page identifier must be unique')

        if self.instance and slug in pages and slug != self.instance.slug and slug != '':
            raise forms.ValidationError(error_message)

        elif not self.instance and slug in pages and slug != '':
            raise forms.ValidationError(error_message)

        else:
            return slug


class ArticleTitleForm(forms.ModelForm):

    title = forms.CharField(
        help_text=_("The title will be used for navigation items."),
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    class Meta:
        model = ArticleTranslation
        fields = [
            'title'
        ]
