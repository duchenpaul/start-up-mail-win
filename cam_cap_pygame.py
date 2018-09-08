import pygame
import pygame.camera
import time, tempfile

def cam_cap():
    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_image()
    time.sleep(1)
    img = cam.get_image()
    img_path = '{}\\cam_{}.jpg'.format(tempfile.gettempdir(),time.strftime('%Y%m%d_%H%M%S'))
    pygame.image.save(img,img_path)
    return img_path

if __name__ == '__main__':
    pass
