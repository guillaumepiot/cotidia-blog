from django.core.urlresolvers import reverse


def admin_menu(context):
    return [
        {
            "text": "Blog",
            "icon": "file-text",
            "url": reverse("blog-admin:article-list"),
            "permissions": [
                "blog.add_article",
                "blog.change_article",
                "blog.delete_article",
            ],
        }
    ]
