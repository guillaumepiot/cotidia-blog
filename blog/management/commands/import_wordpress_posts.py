from xml.dom import minidom
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from blog.models import *
from blog import settings as blog_settings

# Minidom function to retrieve text from nodes
def getText(nodelist):
	rc = []
	for node in nodelist:
		# Retrieve normal text
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
		# Retrieve CDATA encoded text
		elif node.nodeType == node.CDATA_SECTION_NODE:
			rc.append(node.data)
	return ''.join(rc)

def format_date(date_str):
	_date, _time = date_str.split(' ')
	_date = _date.split('-')
	_time = _time.split(':')

	date_obj = datetime(year=int(_date[0]), month=int(_date[1]), day=int(_date[2]), hour=int(_time[0]), minute=int(_time[1]), second=int(_time[2]))

	return date_obj


class Command(BaseCommand):
	args = '<xml_file>'
	help = 'Command to do import posts from Wordpress export XML file'
 



	def handle(self, *args, **options):
		if not len(args) == 1:
			raise CommandError('No XML file provided!')
		
		# Load the XML file
		xmldoc = minidom.parse(args[0])

		# Load all the posts
		itemlist = xmldoc.getElementsByTagName('item') 

		count = 0
		category_order_id = 0
		# Loop through all articles
		for s in itemlist :
			title = getText(s.getElementsByTagName('title')[0].childNodes)
			slug = getText(s.getElementsByTagName('wp:post_name')[0].childNodes)
			publish_date = format_date(getText(s.getElementsByTagName('wp:post_date')[0].childNodes))
			content = getText(s.getElementsByTagName('content:encoded')[0].childNodes)

			wp_status = getText(s.getElementsByTagName('wp:status')[0].childNodes)
			published = True if wp_status == 'publish' else False
			
			# Another alternative to get all text regardless of nodetype
			# content = s.getElementsByTagName('content:encoded')[0].firstChild.wholeText

			# Only import if not trash
			if not wp_status == 'trash':
				categories_to_import = []
				# Import categories
				categories = s.getElementsByTagName('category')
				for category in categories:
					category_slug = category.attributes['nicename'].value
					category_title = category.firstChild.wholeText
					
					category = Category.objects.filter(identifier = category_slug)
					if len(category) == 0:
						new_category = Category.objects.create(identifier = category_slug, published=True, order_id=category_order_id)
						new_category_translation = CategoryTranslation.objects.create(title=category_title, slug=category_slug, parent=new_category, language_code=settings.DEFAULT_LANGUAGE)
						categories_to_import.append(new_category)
						category_order_id += 1
					else:
						categories_to_import.append(category[0])

				# Add article

				# Try if exist first
				article = Article.objects.filter(slug=slug)
				if len(article) == 0:
					new_article = Article.objects.create(slug=slug, publish_date=publish_date, template=blog_settings.BLOG_TEMPLATES[0][0])
					for c in categories_to_import:
						new_article.categories.add(c)
					new_article_translation = ArticleTranslation.objects.create(title=title, slug=slug, content=content, parent=new_article, language_code=settings.DEFAULT_LANGUAGE)
					
					if published:
						new_article.approval_needed = False
						new_article.published = True
						new_article.save()
						new_article.publish_version()
						new_article.publish_translations()

				else:
					self.stdout.write('Article %s has already been imported' % article[0])
				


			#print published

			count += 1
 
		self.stdout.write('Import complete %s post(s)' % count)