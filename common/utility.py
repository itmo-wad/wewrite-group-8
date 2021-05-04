import random, string, time
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

class ImageCode:
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(0, 200)
        return red, green, blue

    def gen_text(self):
        list = random.sample(string.ascii_letters+string.digits, 4)
        return ''.join(list)

    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50
        im = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        self.draw_lines(draw, 4, width, height)
        return im, code

    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def send_email(receiver, ecode):
    sender = 'Blog <15903523@qq.com>'
    content = f"<br/>Welcome to register blog system account, your email verification code is：" \
        f"<span style='color: red; font-size: 20px;'>{ecode}</span>，" \
        f"Please copy to the registration window to complete the registration. Thank you for your support.<br/>"
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('Podcast registration verification code', 'utf-8')
    message['From'] = sender
    message['To'] = receiver

    smtpObj = SMTP_SSL('smtp.qq.com')
    smtpObj.login(user='15903523@qq.com', password='uczmmmqvpxwjbjaf')
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()

def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)

def model_list(result):
    list = []
    for row in result:
        dict = {}
        for k, v in row.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                dict[k] = v
        list.append(dict)

    return list

def model_join_list(result):
    list = [] 
    for obj1, obj2 in result:
        dict = {}
        for k1, v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                if not k1 in dict: 
                    dict[k1] = v1
        for k2, v2 in obj2.__dict__.items():
            if not k2.startswith('_sa_instance_state'):
                if not k2 in dict: 
                    dict[k2] = v2
        list.append(dict)
    return list

def compress_image(source, dest, width):
    from PIL import Image
    im = Image.open(source)
    x, y = im.size     
    if x > width:
        ys = int(y * width / x)
        xs = width
        temp = im.resize((xs, ys), Image.ANTIALIAS)
        temp.save(dest, quality=80)
    else:
        im.save(dest, quality=80)

def parse_image_url(content):
    import re
    temp_list = re.findall('<img src="(.+?)"', content)
    url_list = []
    for url in temp_list:
        if url.lower().endswith('.gif'):
            continue
        url_list.append(url)
    return url_list

def download_image(url, dest):
    import requests
    response = requests.get(url)  
    with open(file=dest, mode='wb') as file:
        file.write(response.content)

def generate_thumb(url_list):

    for url in url_list:
        if url.startswith('/upload/'):
            filename = url.split('/')[-1]
            compress_image('./resource/upload/' + filename,
                           './resource/thumb/' + filename, 400)
            return filename

    url = url_list[0]
    filename = url.split('/')[-1]
    suffix = filename.split('.')[-1]  
    thumbname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
    download_image(url, './resource/download/' + thumbname)
    compress_image('./resource/download/' + thumbname, '../resource/thumb/' + thumbname, 400)

    return thumbname 

