from django.utils.translation import ugettext_lazy as _

from betterforms.forms import BetterModelForm

from cotidia.blog.models import ArticleTranslation


class ArticleTitleAddForm(BetterModelForm):

    class Meta:
        model = ArticleTranslation
        fields = [
            'title'
        ]
        fieldsets = (
            ('info', {
                'fields': (
                    'title',
                ),
                'legend': 'Article title'
            }),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].help_text = _(
            "The title will be used for navigation items."
        )
        self.fields["title"].label = _(
            "Choose a title"
        )


class ArticleTitleUpdateForm(BetterModelForm):

    class Meta:
        model = ArticleTranslation
        fields = [
            'title'
        ]
        fieldsets = (
            ('info', {
                'fields': (
                    'title',
                ),
                'legend': 'Article title'
            }),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].help_text = _(
            "The title will be used for navigation items."
        )
        self.fields["title"].label = _(
            "New title"
        )
