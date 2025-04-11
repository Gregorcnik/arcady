import pygame

from .HexCell import HexCell
from .HexBoard import HexBoard
from . import utils

from collections import deque


class Snake:
	def __init__(self, location: tuple[int, int], length: int, board: HexBoard) -> None:
		self.board = board

		self.direction: int = 0
		self.length: int = length

		self.arr: deque[HexCell] = deque()
		self.arr.append(HexCell(location[0], location[1]))

	def turn_right(self) -> None:
		self.direction = (self.direction - 1) % 6

	def turn_left(self) -> None:
		self.direction = (self.direction + 1) % 6

	def head(self) -> HexCell:
		return self.arr[0]

	def move(self) -> None:
		while len(self.arr) >= self.length:
			self.arr.pop()

		new_head = self.board.get_neighbour(self.arr[0], self.direction)
		self.arr.appendleft(new_head)

	def draw(self, surface: pygame.Surface):
		for i in self.arr:
			center = i.axial_to_pixel(self.board.cell_size, self.board.offset)
			points = i.get_polygon_points(center, self.board.cell_size)
			utils.draw_cube(
				surface,
				points,
				center,
				((146, 148, 149), (66, 63, 63), (132, 134, 134)),
			)
