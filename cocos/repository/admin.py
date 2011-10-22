"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.contrib import admin
from repository.models import CorpusDescription

class CorpusDescriptionAdmin(admin.ModelAdmin):
    """
    This class provides formatting options for the 
    CorpusDescription model admin interface.
    """

    def has_change_permission(self, request, obj=None):
        """
        Return True if editing an object is permitted;
        return False otherwise.
        """
        has_class_permission = super(CorpusDescriptionAdmin, self)\
          .has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and \
          request.user.id != obj.uploader.id:
            return False
        return True


    def queryset(self, request):
        """
        Show users who are not superusers only
        their own uploaded corpus descriptions.
        """
        if request.user.is_superuser:
            return CorpusDescription.objects.all()
        return CorpusDescription.objects.filter(uploader=request.user)


    def save_model(self, request, obj, form, change):
        """
        Only save the user information once when the object is created,
        but not again when the object is modified.
        """
        if not change:
            obj.uploader = request.user
        obj.save()


    fieldsets = (
      ('Main fields', {
        'fields': ('name', 'location', 'coli_path', 
          'dfki_path', 'language', 'annotation')
      }),
      ('Optional fields', {
        'classes': ('collapse',), 
        'fields': ('description', 'comment', 'license_holder', 'contact',
                   'file')
      })
    )
    
    radio_fields = {'location': admin.HORIZONTAL}
    
    date_hierarchy = 'date_of_first_creation'


    
    list_display = ('name', 'location', 'language', 'annotation', 
      'license_holder', 'contact', 'file', 'uploader', 'date_of_first_creation',
      'date_of_last_modification')
    list_filter = ('location', 'language', 'annotation',
      'license_holder', 'date_of_first_creation', 'date_of_last_modification')
    
    search_fields = ('name', 'description', 'comment')


admin.site.register(CorpusDescription, CorpusDescriptionAdmin)