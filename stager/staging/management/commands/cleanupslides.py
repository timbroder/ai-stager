
from django.core.management.base import NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):
    help = "Removes CompSlides from the database that do not have matching files on the drive."



    def handle_noargs(self, **options):
        from stager.staging.models import CompSlide
        import os.path

        slides = CompSlide.objects.all()
        for slide in slides:
            if not os.path.exists(settings.MEDIA_ROOT+"/"+str(slide.image)):
                print str(slide.image), "deleted"
                slide.delete()
                
        
        