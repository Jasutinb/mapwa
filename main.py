import asyncio
import pygame
from src.game import Game

async def main():
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Start game loop
    await game.run()

# This is the program entry point:
asyncio.run(main())