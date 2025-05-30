from .spawnables import SpawnableManager, Spawnable
from .snake import Snake

from typing import Callable


class CollisionManager:
	def __init__(
		self,
		snake: Snake,
		spawnable_manager: SpawnableManager,
		on_game_over: Callable[[str], None],
	):
		self.snake = snake
		self.spawnable_manager = spawnable_manager
		self.on_game_over = on_game_over

	def handle_collisions(self):
		# Check for snake self-collision
		if self.snake.head() in list(self.snake.body)[1:]:
			self.on_game_over("I do not taste good :(")

		# Check for collisions with spawnables
		for spawnable_list in self.spawnable_manager.spawnables.values():
			for spawnable in spawnable_list:
				if self.snake.head() == spawnable.position:
					self._handle_spawnable_collision(spawnable)

	def _handle_spawnable_collision(self, spawnable: Spawnable):
		from .spawnables import Bomb, Apple, Scissors

		if isinstance(spawnable, Apple):
			self.snake.grow()
			self.snake.speed = max(self.snake.speed - 8 / 20, 7)
			self.snake.score += 1
			spawnable.kill()

		elif isinstance(spawnable, Bomb):
			if spawnable.state == Bomb.States.WARNING:
				# Bomb is still deactivatable
				spawnable.kill()
			elif spawnable.state == Bomb.States.BOMB:
				# Bomb is armed – game over!
				self.on_game_over("Bomb bad!")

		elif isinstance(spawnable, Scissors):
			self.snake.length = max(5, self.snake.length - 10)
			spawnable.kill()
