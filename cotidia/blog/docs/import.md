Import
======

Migrate content from Wordpress
-------------------------------

You can use the `import_wordpress_posts` command to import all posts exported from a Wordpress blog, eg:

	python manage.py import_wordpress_posts path_to_xml_export_file.xml

This import script will import the following attributes:

- `title` to `title`
- `wp:post_name` to `slug`

The posts with the `trash` status will not imported, though the draft ones will be imported but not published.

Please note that the importer will not import the comments. This blog package doesn't cover for internal commenting as I would strongly suggest to use a third party commenting platform such as Disqus.

Also any embedded media such as images will not be imported but the HTML will so it may still load. But it is highly recommend to re-upload those images for the future or when your wordpress hosting goes down.

### Potential import syntax errors

You may have to correct a few syntax issues from the Wordpress XML as I did, like for example `<![CDATA[` that may be contained inside you article content, will break the XML formatting and the import will failed. So in this case, it is necessary to remove the `<![CDATA[` opening and `]]>` closing, to rectify the syntax.