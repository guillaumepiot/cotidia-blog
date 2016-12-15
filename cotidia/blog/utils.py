from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from cotidia.blog.models import Article


MONTH_NAMES = [
    _('January'),
    _('February'),
    _('March'),
    _('April'),
    _('May'),
    _('June'),
    _('July'),
    _('August'),
    _('September'),
    _('October'),
    _('November'),
    _('December'),
]


class Year(object):

    def __init__(self, year):
        self.year = year

    def months(self):
        # We only want to show months in the past, so we'll check against the current date
        current_date = now()
         # Create a list of Month instances for each month of the year
        month_list = []
        for i in range(12):
            # If previous year, add all months regardless
            if current_date.year > self.year:
                month_list.append(Month(self.year, 12-i))
            # Otherwise if current year or next, only show month before
            elif current_date.year == self.year:
                # Is the month inferior to the current one?
                if current_date.month > (12-i):
                    month_list.append(Month(self.year, 12-i))

        return month_list

    def article_count(self):
        return Article.objects.get_published_live().filter(publish_date__year=self.year).count()

    def get_absolute_url(self):
        return reverse('blog:archive_year', kwargs={'year':self.year})

    def __unicode__(self):
        return u'%s' % self.year

class Month(object):

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.month_names = MONTH_NAMES

    def articles(self):
        articles = Article.objects.get_published_live().filter(publish_date__year=self.year, publish_date__month=self.month).order_by('-publish_date')
        return articles

    def article_count(self):
        return self.articles().count()

    def month_number(self):
        return u'%s' % self.month

    def month_name(self):
        return u'%s' % self.month_names[self.month-1]

    def get_absolute_url(self):
        return reverse('blog:archive_month', kwargs={'year':self.year, 'month':self.month_number()})

    def __unicode__(self):
        return self.month_name()
