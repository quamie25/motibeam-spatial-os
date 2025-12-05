#!/usr/bin/env python3
"""
MotiBeam Test - Check if pygame display works
"""

import pygame
import sys

print("=" * 60)
print("MOTIBEAM DISPLAY TEST")
print("=" * 60)

pygame.init()

# Test 1: Try windowed mode first
print("\n[TEST 1] Trying windowed mode 1920x1080...")
try:
    display = pygame.display.set_mode((1920, 1080))
    print(f"✓ Display created: {display.get_size()}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Try fullscreen
print("\n[TEST 2] Trying fullscreen mode...")
try:
    display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    print(f"✓ Fullscreen created: {display.get_size()}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Draw something simple
print("\n[TEST 3] Drawing test pattern...")
display.fill((20, 30, 40))  # Dark background
pygame.draw.circle(display, (200, 100, 100), (960, 540), 100)  # Red circle center
font = pygame.font.Font(None, 72)
text = font.render("MOTIBEAM TEST", True, (200, 200, 200))
text_rect = text.get_rect(center=(960, 300))
display.blit(text, text_rect)
pygame.display.flip()

print("✓ Test pattern drawn")
print("\nYou should see:")
print("  - Dark blue/gray background")
print("  - Red circle in center")
print("  - 'MOTIBEAM TEST' text")
print("\nPress ESC to exit, or wait 10 seconds...")

# Wait for ESC or 10 seconds
clock = pygame.time.Clock()
frames = 0
max_frames = 600  # 10 seconds at 60fps

while frames < max_frames:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("\n✓ ESC pressed - exiting")
                pygame.quit()
                sys.exit()

    clock.tick(60)
    frames += 1

print("\n✓ Test complete - exiting")
pygame.quit()
