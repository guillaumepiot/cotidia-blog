from django.urls import reverse


def admin_menu(context):
    return [
        {
            "text": "Blog",
            "icon": "rss",
            "url": reverse("blog-admin:article-list"),
            "permissions": [
                "blog.add_article",
                "blog.change_article",
                "blog.delete_article",
            ],
        }
    ]
