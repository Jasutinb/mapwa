# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import asyncio
import pygame
from src.game import Game

async def main():
    # Initialize pygame at the very start of the async main
    pygame.init()
    game = Game()
    await game.run()

if __name__ == '__main__':
    asyncio.run(main())
