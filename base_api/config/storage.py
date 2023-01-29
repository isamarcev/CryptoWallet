import io
import uuid
from typing import Tuple, List, Union

from PIL import Image
from fastapi import UploadFile, HTTPException
from fastapi_helper import DefaultHTTPException
from starlette import status

from base_api.config.settings import settings


class ImageFormatError(DefaultHTTPException):
    code = "image_format_error"
    type = "Image Invalid"
    message = "Image format is not valid"
    status_code = status.HTTP_400_BAD_REQUEST


class Storage:

    def __init__(self, client, bucket: str):
        self.client = client
        self.bucket = bucket

    async def upload_image(self, file: UploadFile,
                           dir_name: str,
                           size: Union[Tuple[int, int]]
                           # types: List[str]
                           ) -> str:
        try:
            print(type(file.file))
            image = Image.open(file.file)
        except:
            print("Файл не найден 666")
            print('error')
            raise ImageFormatError(
                message='not photo'
            )

        print('storage')
        image = await self.resize_image(image, size)
        bytes_image = await self.convert_to_bytes(image)
        key = f"{dir_name}/image_{uuid.uuid4()}.png"

        self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=bytes_image,
                ACL="public-read",
                Metadata={
                    "Content-Type": "image/png",
                },
        )
        return await self.make_image_url(key)

    @staticmethod
    async def resize_image(image, size: Tuple[int, int]):
        return image.resize(size)

    @staticmethod
    async def convert_to_bytes(image):
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        byte_image = buf.getvalue()
        return byte_image

    @staticmethod
    async def make_image_url(key):
        return str(settings.space_url) + '/' + key
