# Thanks for my friend, DeepSeek for making this code :)
from core.imports import Image, ImageDraw, ImageFont, ImageFilter, math, random

class cap:
    def __init__(self, width=200, height=60):
        self.width = width
        self.height = height
        self.fonts = [
            "fonts/arial.ttf",
            "fonts/times.ttf",
            "fonts/cour.ttf"
        ]
        self.font_sizes = range(28, 36)
    
    def _add_noise(self, draw):
        for _ in range(int(self.width * self.height * 0.1)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=self._random_light_color())
        
        for _ in range(5):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line([(x1, y1), (x2, y2)], fill=self._random_light_color(), width=1)
    
    def _random_light_color(self):
        return (random.randint(200, 255)), (random.randint(200, 255)), (random.randint(200, 255))
    
    def _random_dark_color(self):
        return (random.randint(0, 100)), (random.randint(0, 100)), (random.randint(0, 100))
    
    def _distort_text(self, image):
        width, height = image.size
        x_offset = [int(math.sin(y / 10.0) * 3) for y in range(height)]
        y_offset = [int(math.sin(x / 10.0) * 3) for x in range(width)]
        
        distorted = Image.new('RGB', (width, height))
        
        for y in range(height):
            for x in range(width):
                nx = x + x_offset[y]
                ny = y + y_offset[x]
                
                if 0 <= nx < width and 0 <= ny < height:
                    distorted.putpixel((x, y), image.getpixel((nx, ny)))
                else:
                    distorted.putpixel((x, y), (255, 255, 255))
        
        return distorted
    
    def create(self, code):
        bg_color = self._random_light_color()
        img = Image.new('RGB', (self.width, self.height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        self._add_noise(draw)
        x = 10
        for char in code:
            font_path = random.choice(self.fonts)
            font_size = random.choice(self.font_sizes)
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()
            
            y = random.randint(5, self.height - font_size - 5)
            angle = random.randint(-15, 15)
            
            char_img = Image.new('RGBA', (font_size, font_size), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((0, 0), char, font=font, fill=self._random_dark_color())
            
            char_img = char_img.rotate(angle, expand=1, resample=Image.BICUBIC)
            
            img.paste(char_img, (x, y), char_img)
            
            x += font_size - random.randint(5, 10)
        
        self._add_noise(draw)
        img = self._distort_text(img)
        img = img.filter(ImageFilter.SMOOTH)
        
        return img