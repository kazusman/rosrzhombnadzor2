import os
import textwrap
from random import choice

from django.conf import settings
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from bot.models import DemotivatorText


class DemotivatorMaker:
    def __init__(self, downloaded_file_path: str):
        self.downloaded_file_path = downloaded_file_path

    font: ImageFont.FreeTypeFont
    demotivator_template_path = os.path.join(
        settings.BASE_DIR,
        "bot",
        "communication",
        "photos",
        "downloaded_files",
        "demotivator_template.png",
    )

    def _resize_original_image(self):
        with Image.open(self.downloaded_file_path) as image:
            image = image.resize((508, 508), Image.ANTIALIAS)
            image.save(self.downloaded_file_path)

    def _add_image_to_demotivator_template(self):
        with Image.open(self.demotivator_template_path) as demotivator_template:
            with Image.open(self.downloaded_file_path) as image:
                demotivator_template.paste(image, box=(128, 53))
                demotivator_template.save(self.downloaded_file_path)

    def _get_font(self):
        self.font = ImageFont.truetype(
            os.path.join(settings.BASE_DIR, "bot", "fonts", "times_new_roman.ttf"), 44
        )

    def _add_text_to_demotivator(self):
        demotivator_text = choice(DemotivatorText.objects.all()).text
        self._get_font()
        refactored_text = textwrap.wrap(demotivator_text, width=30)
        with Image.open(self.downloaded_file_path) as demotivator:
            width, height = demotivator.size
            draw = ImageDraw.Draw(demotivator)
            y_start_position, y_kerning = 585, 5
            for line in refactored_text:
                current_width, current_height = draw.textsize(line, font=self.font)
                draw.text(
                    ((width - current_width) / 2, y_start_position),
                    line,
                    font=self.font,
                )
                y_start_position += current_height + y_kerning
            demotivator.save(self.downloaded_file_path)

    def create_demotivator(self) -> str:
        self._resize_original_image()
        self._add_image_to_demotivator_template()
        self._add_text_to_demotivator()
        return self.downloaded_file_path
