import sys
from PIL import ImageFont, ImageDraw
from PIL import Image as IMG
from graia.application.logger import AbstractLogger
from loguru import logger
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.event.messages import Group, Member
from graia.application.message.elements.internal import Plain, Image, Image_LocalFile, Image_UnsafeBytes
import yaml


class Config(dict):
    """
    config from config.yaml
    """
    def __init__(self):
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self = yaml.safe_load(f.read())

    def reload(self):
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self = yaml.safe_load(f.read())

    def add(self, value):
        with open('config.yaml', 'a', encoding='utf-8') as f:
            yaml.dump(value, f)
        self.reload()
        
    def delete(self, name):
        self.pop(name)



async def messagechain_to_img(
        message: MessageChain,
        max_width: int = 1080,
        font_size: int = 40,
        spacing: int = 15,
        padding_x: int = 20,
        padding_y: int = 15,
        img_fixed: bool = True,
        font_path: str = f"{os.getcwd()}/statics/fonts/STKAITI.TTF",
    ) -> MessageChain:
        """
        将 MessageChain 转换为图片，仅支持只含有本地图片/文本的 MessageChain
        Args:
            message: 要转换的MessageChain
            max_width: 最大长度
            font_size: 字体尺寸
            spacing: 行间距
            padding_x: x轴距离边框大小
            padding_y: y轴距离边框大小
            img_fixed: 图片是否适应大小（仅适用于图片小于最大长度时）
            font_path: 字体文件路径
        Examples:
            msg = await messagechain_to_img(message=message)
        Returns:
            MessageChain （内含图片Image类）
        """
        def get_final_text_lines(text: str, text_width: int, font: ImageFont.FreeTypeFont) -> int:
            lines = text.split("\n")
            line_count = 0
            for line in lines:
                if not line:
                    line_count += 1
                    continue
                line_count += int(math.ceil(float(font.getsize(line)[0]) / float(text_width)))
            return line_count + 1

        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
        message = message.asMerged()
        elements = message.__root__

        plains = message.get(Plain)
        text_gather = "\n".join([plain.text for plain in plains])
        # print(max(font.getsize(text)[0] for text in text_gather.split("\n")) + 2 * padding_x)
        final_width = min(max(font.getsize(text)[0] for text in text_gather.split("\n")) + 2 * padding_x, max_width)
        text_width = final_width - 2 * padding_x
        text_height = (font_size + spacing) * get_final_text_lines(text_gather, text_width, font)

        img_height_sum = 0
        temp_img_list = []
        images = [element for element in message.__root__ if (isinstance(element, Image_LocalFile) or isinstance(element, Image_UnsafeBytes))]
        for image in images:
            if isinstance(image, Image_LocalFile):
                temp_img = IMG.open(image.filepath)
            elif isinstance(image, Image_UnsafeBytes):
                temp_img = IMG.open(BytesIO(image.image_bytes))
            else:
                raise ValueError("messagechain_to_img：仅支持Image_LocalFile和Image_UnsafeBytes类的处理！")
            img_width, img_height = temp_img.size
            temp_img_list.append(
                temp_img := temp_img.resize((
                    int(final_width - 2 * spacing),
                    int(float(img_height * (final_width - 2 * spacing)) / float(img_width))
                )) if img_width > final_width - 2 * spacing or (img_fixed and img_width < final_width - 2 * spacing)
                else temp_img
            )
            img_height_sum = img_height_sum + temp_img.size[1]
        final_height = 2 * padding_y + text_height + img_height_sum
        picture = IMG.new('RGB', (final_width, final_height), (255, 255, 255))
        draw = ImageDraw.Draw(picture)
        present_x = padding_x
        present_y = padding_y
        image_index = 0
        for element in elements:
            if isinstance(element, Image) or isinstance(element, Image_UnsafeBytes) or isinstance(element, Image_LocalFile):
                picture.paste(temp_img_list[image_index], (present_x, present_y))
                present_y += (spacing + temp_img_list[image_index].size[1])
                image_index += 1
            elif isinstance(element, Plain):
                for char in element.text:
                    if char == "\n":
                        present_y += (font_size + spacing)
                        present_x = padding_x
                        continue
                    if char == "\r":
                        continue
                    if present_x + font.getsize(char)[0] > text_width:
                        present_y += (font_size + spacing)
                        present_x = padding_x
                    draw.text((present_x, present_y), char, font=font, fill=(0, 0, 0))
                    present_x += font.getsize(char)[0]
                present_y += (font_size + spacing)
                present_x = padding_x
        bytes_io = BytesIO()
        picture.save(bytes_io, format='PNG')
        logger.success("消息转图片处理成功！")
        return MessageChain.create([
            Image.fromUnsafeBytes(bytes_io.getvalue())
        ])


class LoguruLogger(AbstractLogger):
    def __init__(self) -> None:
        config = {
            "handlers": [
                {"sink": sys.stdout, "format": "{time:YYYY-MM-DD HH:mm:ss} - {message}"},
                {"sink": 'logs/latest.log', "encoding": 'utf8', "rotation": "12:00",
                 "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>", "compression": "zip", "enqueue": True},
            ],
            "extra": {"user": "someone"}
        }

        logger.configure(**config)

    def info(self, msg):
        return logger.info(msg)

    def error(self, msg):
        return logger.error(msg)

    def warn(self, msg):
        return logger.warning(msg)

    def exception(self, msg):
        return logger.exception(msg)

    def debug(self, msg):
        return logger.debug(msg)
