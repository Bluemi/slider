#!/usr/bin/python
import subprocess
import time

import pygame
import image_loading

BACKGROUND_IMAGE = 'res/background.jpg'
BORDER_IMAGE_SELECTED = 'res/border_selected.png'
BORDER_IMAGE_NOT_SELECTED = 'res/border_not_selected.png'
ROOT_DIR = 'res'
IMAGE_SHOW_DURATION = 5


def main():
    slider = Slider(ROOT_DIR)
    slider.run()


class PlayItem:
    def __init__(self, command, timeout=None):
        """
        Creates a new PlayItem.

        :param command: The command to execute
        :type command: list[str]
        :param timeout: The timeout for the command. If None, no timeout is supplied
        :type timeout: int or None
        """
        self.command = command
        self.timeout = timeout


class Slider:
    def __init__(self, root_directory):
        self._image_buffer = image_loading.ImageBuffer.from_root_dir(root_directory)
        self._background_image = pygame.image.load(BACKGROUND_IMAGE)
        self._border_image_selected = pygame.image.load(BORDER_IMAGE_SELECTED)
        self._border_image_not_selected = pygame.image.load(BORDER_IMAGE_NOT_SELECTED)
        self._play_item = None

    def run(self):
        pygame.init()

        self.start_screen()

    def start_screen(self):
        screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)

        mouse_position = None

        self._image_buffer.set_preview_rects()

        running = True
        while running:
            if self._play_item is not None:
                pygame.display.quit()
                self.play_item()
                screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)

            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                if event.type == pygame.KEYDOWN:
                    if event.key == 113:  # q to quit
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True
                elif event.type == pygame.MOUSEMOTION:
                    mouse_position = event.pos

            screen.blit(self._background_image, self._background_image.get_rect())

            selected_preview = None

            for directory_preview in self._image_buffer.previews.values():
                if (mouse_position is not None) and directory_preview.rect.collidepoint(mouse_position):
                    screen.blit(self._border_image_selected, directory_preview.rect.move(-7, -7))
                    selected_preview = directory_preview
                else:
                    screen.blit(self._border_image_not_selected, directory_preview.rect.move(-7, -7))

                screen.blit(directory_preview.preview, directory_preview.rect)

            if mouse_clicked:
                self.apply_selected_preview(selected_preview)

            pygame.display.flip()

            time.sleep(0.1)

    def apply_selected_preview(self, selected_preview):
        if selected_preview is None:
            return
        if selected_preview.directory_type == image_loading.DirectoryType.IMAGE_DIRECTORY:
            command = ['vlc', '--fullscreen', '--play-and-exit', '--rate', str(10 / IMAGE_SHOW_DURATION)]
            command.extend(selected_preview.get_images())
            self._play_item = PlayItem(command)

            # subprocess.run(['slideshow', selected_preview.subdir])
        elif selected_preview.directory_type == image_loading.DirectoryType.VIDEO_DIRECTORY:
            self._play_item = PlayItem(['vlc', '--fullscreen', '--play-and-exit', selected_preview.get_video_file()])

    def play_item(self):
        try:
            subprocess.run(self._play_item.command, timeout=self._play_item.timeout)
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print('Exception occurred while running "{}":\n{}'.format(self._play_item.command, str(e)))
        self._play_item = None


if __name__ == '__main__':
    main()
