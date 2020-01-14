import copy
import os
from enum import Enum

import pygame


VIDEO_PREVIEW_NAME = 'video_preview.jpg'
IMAGES_PREVIEW_NAME = 'images_preview.jpg'
DIRECTORY_PREVIEW_SIZE = (100, 70)

START_POSITION = [50, 50]
PREVIEW_X_DIFF = DIRECTORY_PREVIEW_SIZE[0] + 20
PREVIEW_Y_DIFF = DIRECTORY_PREVIEW_SIZE[1] + 20


class ImageBuffer:
    def __init__(self, previews):
        """
        Creates a new ImageBuffer with the given images

        :param previews: A dictionary mapping subdir strings to n DirectoryPreview
        :type previews: dict[str, DirectoryPreview]
        """
        self.previews = previews

    def set_preview_positions(self):
        """
        Sets the position attribute for the previews

        :return:
        """
        position = START_POSITION
        for preview in self.previews.values():
            preview.position = copy.copy(position)

            position[0] += PREVIEW_X_DIFF
            if position[0] + PREVIEW_X_DIFF > pygame.display.get_surface().get_size()[0]:
                position[0] = START_POSITION[0]
                position[1] += PREVIEW_Y_DIFF

    @staticmethod
    def from_root_dir(root_dir):
        """
        Iterates over the subdirectories of root dir to create an image buffer
        """
        previews = {}

        for d in os.listdir(root_dir):
            sub_dir = os.path.join(root_dir, d)
            if os.path.isdir(sub_dir):
                previews[sub_dir] = DirectoryPreview.from_subdir(sub_dir)

        return ImageBuffer(previews)


class DirectoryType(Enum):
    IMAGE_DIRECTORY = 0
    VIDEO_DIRECTORY = 1


class DirectoryPreview:
    def __init__(self, subdir, preview, directory_type):
        """
        Creates a new ImageDirectory with the subdir and preview

        :param subdir: The name of the subdirectory
        :type subdir: str
        :param preview: An image used to preview
        :type preview: pygame.images.Image
        :param directory_type: If it is an ImageDirectory or VideoDirectory
        :type directory_type: DirectoryType
        """
        self.subdir = subdir
        self.preview = preview
        self.directory_type = directory_type
        self.position = (0, 0)
        self.size = DIRECTORY_PREVIEW_SIZE

    @staticmethod
    def from_subdir(subdir):
        """
        Creates a ImageDirectory from the given subdir

        :param subdir: The name of the subdirectory
        :type subdir: str
        :return: An ImageDirectory
        :rtype: DirectoryPreview
        """
        images_preview = os.path.join(subdir, IMAGES_PREVIEW_NAME)
        video_preview = os.path.join(subdir, VIDEO_PREVIEW_NAME)

        if os.path.isfile(images_preview):
            preview = pygame.image.load(images_preview)
            directory_type = DirectoryType.IMAGE_DIRECTORY
        elif os.path.isfile(video_preview):
            preview = pygame.image.load(video_preview)
            directory_type = DirectoryType.VIDEO_DIRECTORY
        else:
            raise ValueError(
                'Could not find "{}" nor "{}" for subdirectory "{}"'
                .format(IMAGES_PREVIEW_NAME, VIDEO_PREVIEW_NAME, subdir)
            )

        preview = pygame.transform.scale(preview, DIRECTORY_PREVIEW_SIZE)

        return DirectoryPreview(subdir, preview, directory_type)
