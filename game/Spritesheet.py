import pygame

# Collect spritesheet images

class SpriteSheet:
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (scale[0], scale[1]))
		image.set_colorkey(colour)

		return image

	def get_spritesheet(self, amount, size, scale, color, flip = False):
		frames_list = []

		for x in range(amount):

			if flip:
				image = self.get_image(x, size[0], size[1], scale, color)
				frames_list.append(pygame.transform.flip(image, True, False))

			else:
				frames_list.append(self.get_image(x, size[0], size[1], scale, color))
		
		
		return frames_list