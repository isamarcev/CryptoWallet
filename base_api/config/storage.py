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
    field = 'image'
    status_code = status.HTTP_400_BAD_REQUEST


class SpaceError(DefaultHTTPException):
    code = "remote_space_error"
    type = "Connection Error"
    message = "Error connection to remote space"
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
            image = Image.open(file.file)
        except:
            raise ImageFormatError(
                message='This type of file is unsupported, please upload image in one of this types ("jpeg", "png", "gif")'
            )

        image = await self.resize_image(image, size)
        bytes_image = await self.convert_to_bytes(image)
        key = f"{dir_name}/image_{uuid.uuid4()}.png"

        try:
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
        except:
            raise SpaceError(
                message='Error connection to remote space, please try again later'
            )

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
