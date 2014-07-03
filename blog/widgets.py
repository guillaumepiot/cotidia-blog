from django.forms.widgets import Input
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class TagAutocomplete(Input):
    input_type = 'text'
	
    def render(self, name, value, attrs=None):
        json_view = reverse('blog:tagging_autocomplete-list')
        html = super(TagAutocomplete, self).render(name, value, attrs)
        js = u'''<script type="text/javascript">
function split( val ) {
    return val.split( /,\s*/ );
}
function extractLast( term ) {
    return split( term ).pop();
}
jQuery(function() {

    jQuery("#%s").bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB && $( this ).data( "autocomplete" ).menu.active ) {
            event.preventDefault();
        }
    }).autocomplete({
        source: function( request, response ) {
            $.getJSON( "%s", {
                term: extractLast( request.term )
            }, response );
        },
        focus: function() {
            // prevent value inserted on focus
            return false;
        },
        select: function( event, ui ) {
            var terms = split( this.value );
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push( ui.item.value );
            // add placeholder to get the comma-and-space at the end
            terms.push( "" );
            this.value = terms.join( ", " );
            return false;
        }
    });
});
</script>''' % (attrs['id'], json_view)
        return mark_safe("\n".join([html, js]))

    class Media:
        css = {
            'all': (
                'blog/css/jquery-ui-1.10.4.custom.min.css',
                )
        }

        js = (
            'blog/js/jquery-ui-1.10.4.custom.min.js',
)
