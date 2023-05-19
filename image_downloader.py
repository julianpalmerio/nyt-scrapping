from typing import Union, List
import requests
from requests import Response
import uuid
import logging


class ImageDownloader:
    def __init__(self, logger: logging.Logger = None) -> None:
        if logger is None:
            self.logger = logging.getLogger("Image Downloader")
        else:
            self.logger = logger

    def download_images(self, images_urls: List[str], images_path: str) -> List[str]:
        image_filenames = []
        for url in images_urls:
            if url is None:
                image_filenames.append("")
                continue
            image_response = self._get_image(url)
            if image_response is None:
                image_filenames.append("")
                continue
            filename, file_path = self._create_image_name_and_path(images_path)
            self._save_image_to_local(image_response, file_path)
            image_filenames.append(filename)
        return image_filenames

    def _get_image(self, url: str) -> Union[Response, None]:
        try:
            image_response = requests.get(url)
            if image_response.status_code != 200:
                self.logger.warning(
                    f"Error downloading the image from {url}. "
                    "Status code: {image_response.status_code}"
                )
                return None
            return image_response
        except Exception as ex:
            self.logger.error(f"Error downloading the image from {url}. Error: {ex}")
            raise ex

    @staticmethod
    def _create_image_name_and_path(images_path: str) -> str:
        filename = f"{uuid.uuid4()}.jpg"
        return filename, f"{images_path}/{filename}"

    def _save_image_to_local(self, image_response: Response, file_path: str) -> None:
        try:
            with open(file_path, "wb") as file:
                file.write(image_response.content)
        except Exception as ex:
            self.logger.error(f"Error saving the image to {file_path}. Error: {ex}")
            raise ex
