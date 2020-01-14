#!/usr/bin/python
import time

import pygame
import image_loading

BACKGROUND_IMAGE = 'res/background.jpg'
ROOT_DIR = 'res'


def main():
    slider = Slider(ROOT_DIR)
    slider.run()


class Slider:
    def __init__(self, root_directory):
        self._image_buffer = image_loading.ImageBuffer.from_root_dir(root_directory)
        self._background_image = pygame.image.load(BACKGROUND_IMAGE)

    def run(self):
        pygame.init()

        self.start_screen()

    def start_screen(self):
        screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)

        self._image_buffer.set_preview_positions()

        running = True
        while running:
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 113:  # q to quit
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                    mouse_clicked = True

            screen.blit(self._background_image, self._background_image.get_rect())

            index = 0
            for directory_preview in self._image_buffer.previews.values():
                print('position:', directory_preview.position, 'index:', index)
                index += 1
                screen.blit(
                    directory_preview.preview,
                    directory_preview.preview.get_rect().move(directory_preview.position)
                )
            pygame.display.flip()

            time.sleep(0.1)


if __name__ == '__main__':
    main()
