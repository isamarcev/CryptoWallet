from PIL import Image


class Storage:

    def __init__(self):
        pass

    async def upload_image(self, file, upload_to) -> str:
        try:
            image = Image.open(file)
        except:
            print("Файл не найден")
            #TODO: make validation error raise




