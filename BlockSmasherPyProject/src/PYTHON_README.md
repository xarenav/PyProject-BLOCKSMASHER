# Block Smash - Python/Pygame Edition

A complete Python port of the futuristic Block Smash game, featuring the same neon-glass aesthetic and all gameplay features from the React version.

## Features

✨ **All Core Features Ported:**
- Main menu with neon styling
- Curated maps (Levels 1-6) with unique block formations
- Procedural map generation (Levels 101-112+) with seeded randomness
- Full physics engine with paddle control, ball movement, and collision detection
- Particle effects on block destruction
- Lives system and scoring
- Victory/defeat overlays with stars
- Settings screen (particle effects, FPS display, etc.)
- Leaderboard screen
- Progressive level unlocking

🎮 **Gameplay:**
- **6 Curated Levels:**
  - Level 1: Classic Grid
  - Level 2: Circular Formation
  - Level 3: Pyramid Power (inverted)
  - Level 4: Checkerboard Pattern
  - Level 5: The Fortress (multi-layered)
  - Level 6: Explosive Chaos (procedural)

- **Infinite Procedural Levels:**
  - Random Levels #1-12 (IDs 101-112)
  - Each level ID generates the same pattern consistently (seeded)
  - 5 pattern types: tight grids, scattered circles, lines, arcs, spirals
  - Difficulty scales with level number

🎨 **Visual Style:**
- Neon cyan/purple/orange color scheme
- Glass morphism UI effects
- Glowing blocks and paddle
- Particle explosions
- Smooth animations (60 FPS target)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install pygame directly:

```bash
pip install pygame
```

## Running the Game

Simply run the main Python file:

```bash
python block_smash.py
```

## Controls

### Menu Navigation
- **Mouse**: Click on buttons to navigate
- **ESC**: Return to previous screen/main menu

### Gameplay
- **Mouse Movement**: Control paddle position
- **SPACE or Left Click**: Launch ball
- **ESC**: Pause and return to map selection

### Settings Toggles
- Particle Effects (ON/OFF)
- Screen Shake (ON/OFF)
- Show FPS (ON/OFF)

## Game Mechanics

### Scoring
- Each block destroyed: **100 points**
- Collect all blocks to win the level

### Lives
- Start with **3 lives** per level
- Lose a life when ball falls off screen
- Game over when all lives are lost

### Level Progression
- Complete a level to unlock the next one
- Curated levels unlock sequentially (1→2→3→4→5→6)
- All procedural levels are unlocked by default

## Technical Details

### Architecture
- **Main Game Loop**: 60 FPS pygame loop
- **State Machine**: Separate states for menu, maps, game, settings, leaderboard
- **Seeded RNG**: Procedural levels use Linear Congruential Generator for consistency
- **Particle System**: Dynamic particle effects with physics simulation

### Physics
- Ball velocity: Vector-based movement
- Paddle collision: Position-based angle reflection
- Wall collision: Simple bounce with particle effects
- Block collision: Destroy on contact with score increase

### Procedural Generation
- **Pattern Types**: Tight grids, scattered circles, diagonal lines, arcs, spirals
- **Seeding**: Level ID determines seed → same level always generates same pattern
- **Cluster System**: 6-11 clusters per level with randomized properties
- **Boundary Safety**: All blocks guaranteed to spawn within playable area

## Code Structure

```
block_smash.py
├── Constants (Colors, dimensions)
├── Data Classes (Block, Particle, Settings)
├── Enums (GameState, MapsTab)
└── BlockSmashGame Class
    ├── __init__(): Initialize pygame and game state
    ├── seeded_random(): Deterministic RNG
    ├── generate_blocks_for_level(): Level generation
    ├── update_game(): Physics and collision
    ├── draw_*(): Rendering methods for each screen
    ├── handle_events(): Input handling
    └── run(): Main game loop
```

## Differences from React Version

### What's the Same:
✅ All 6 curated level patterns
✅ Procedural generation algorithm (identical seeding)
✅ Game physics and mechanics
✅ Particle effects
✅ UI structure and flow
✅ Color scheme and styling

### Simplified:
⚠️ Glass morphism effects are simplified (no blur, basic transparency)
⚠️ Animations are basic (no Motion/Framer Motion easing)
⚠️ Typography uses system fonts instead of Rajdhani
⚠️ Sound effects not implemented (can be added)
⚠️ No real-time mouse trail effects

### Enhanced:
✨ Native desktop performance
✨ No browser required
✨ Can run offline
✨ Easier to modify and extend

## Performance

- **Target FPS**: 60
- **Typical Performance**: 55-60 FPS on modern hardware
- **Resolution**: 1200x800 window
- **Canvas Size**: 800x600 gameplay area

## Extending the Game

### Add More Levels
Edit `generate_blocks_for_level()` method and add new level cases:

```python
elif level == 7:
    # Your custom level pattern
    blocks.append(Block(...))
```

### Add Sound Effects
Use pygame.mixer to load and play sounds:

```python
# In __init__:
self.hit_sound = pygame.mixer.Sound('hit.wav')

# When ball hits block:
self.hit_sound.play()
```

### Modify Procedural Generation
Adjust parameters in the `level >= 100` section:
- Change `num_clusters` for more/fewer blocks
- Modify pattern probabilities
- Add new pattern types to the `patterns` list

## Troubleshooting

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Check Python version: `python --version` (need 3.7+)

**Low FPS:**
- Disable particle effects in Settings
- Reduce number of particles in `create_particles()` method

**Window too large/small:**
- Modify `SCREEN_WIDTH` and `SCREEN_HEIGHT` constants
- Keep aspect ratio similar for best results

## License

This is a personal project recreation of the React web version.

## Credits

**Original Design**: React/TypeScript web application
**Python Port**: Complete pygame reimplementation
**Game Type**: Block Breaker / Breakout clone
**Style**: Futuristic neon-glass aesthetic

---

Enjoy breaking blocks! 🎮✨
