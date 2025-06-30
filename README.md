Wolf and Sheep.
Wolf has to reach opposite side of the board, Sheep have to surround Wolf and leave it moveless.
Aim of the game is make strong computer players.
Game theory is used as base for AI. MinMax and alpha-beta prunning are used to achieve the result.
# Wolf and Sheep Game

Wolf has to reach opposite side of the board, Sheep have to surround Wolf and leave it moveless.
Aim of the game is to make strong computer players.
Game theory is used as base for AI. MinMax and alpha-beta pruning are used to achieve the result.

## Installation and Setup

### Dependencies
- Python 3.9+
- Pygame
- Pygame-menu

### Common Issues

#### Missing libjpeg-9.dll

If you encounter the error: `Failed loading libjpeg-9.dll: The file cannot be accessed by the system.`, there are several ways to fix it:

1. **Solution 1 (Recommended)**: The game now includes fallback rendering options so it should work even without the DLL.

2. **Solution 2**: Download libjpeg-9.dll file and place it in the same directory as your Python executable or the game directory.

3. **Solution 3**: For system-wide installation, copy libjpeg-9.dll to the Windows system directories:
   - For 64-bit systems: Copy to both C:\Windows\System32 and C:\Windows\SysWOW64
   - For 32-bit systems: Copy to C:\Windows\System32

4. **Solution 4**: Reinstall Pygame with a different distribution that includes the DLL.

### Running the Game

```
python main.py
```

Enjoy playing!