from datetime import datetime
from django.db import models
from django.utils import timezone
from PIL import Image, ExifTags
from io import BytesIO  
from django.core.files.base import ContentFile

# Create your models here.
class JournalEntry(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        max_size = (1600, 1600)


        # Open the image
        img = Image.open(self.image)

        icc_profile = img.info.get("icc_profile")  
        exif = img.info.get("exif")
        
        if (img._getexif()):
            exiftags = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
            exifDateTime = exiftags.get("DateTime")
            if (exifDateTime):
                meta_timestamp = datetime.strptime(exifDateTime, "%Y:%m:%d %H:%M:%S")
                self.timestamp = meta_timestamp
                print("exifDateTime: " + str(exifDateTime))
            # print("exiftags: " + str(exiftags))

        if not self.timestamp:
            self.timestamp = timezone.now()

        # print("exif: " + str(exif))
        

        # Convert image to RGB (removes alpha channel to avoid issues with JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize or compress the image
        if img.size > max_size:
            img.thumbnail(max_size, Image.LANCZOS)

        output_io = BytesIO()
        img.save(output_io, format="JPEG", icc_profile=icc_profile, quality=85, exif=exif)

        # Save the compressed image back to the model
        self.image = ContentFile(output_io.getvalue(), self.image.name)

        super().save(*args, **kwargs)
