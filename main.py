from events import *
from pics import *


pygame.init()
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(CP)
pygame.display.set_caption("plumbing")
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
if not starting_message(screen, handsDetector, cap):
    pygame.quit()
    exit(0)
if not instruction(screen, handsDetector, cap):
    pygame.quit()
    exit(0)
level(screen, 0, handsDetector, cap)
pygame.quit()
