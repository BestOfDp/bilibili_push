import uuid
from PIL import Image, ImageFont, ImageDraw


class ImageMaker:
    def __init__(self, path, word, offset, font_size):
        self.image = Image.open(path)
        self.word = word
        self.width = self.image.width
        self.height = self.image.height
        self.offset = offset
        self.font_size = font_size

    def run(self):
        draw = ImageDraw.Draw(self.image)
        width, height, size = self._get_point_size()
        #        位置                           黑色
        font = ImageFont.truetype('simsun.ttc', size)
        draw.text((width, height), self.word, (0, 0, 0), font=font)
        # self.image.show()
        image_name = uuid.uuid4().hex
        self.image.save('{}.jpg'.format(image_name))
        return image_name

    def _word_len(self):
        length = 0
        for i in self.word:
            length += 1
            if '\u4e00' <= i <= '\u9fff':
                length += 1
        return length

    def _get_point_size(self):
        width = self.width
        offset = self._word_len() / 2
        size = int(width / (offset + 0)) + self.font_size
        size = 60 if size >= 60 else size
        height = self.height * (0.975 - size / self.height) + self.offset * (self.height * 0.03)
        long = offset * size
        rat = long / width
        return width * ((1 - rat) / 2), height, size


