import pygame
pygame.init()
def make_video(screen):

    _image_num = 0

    while True:
        _image_num += 1
        str_num = "000" + str(_image_num)
        file_name = "sweeptest" + str_num[-4:] + ".png"
        pygame.image.save(screen, file_name)
        yield
