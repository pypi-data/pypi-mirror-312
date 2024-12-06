# FSTrent Colors

[![PyPI version](https://badge.fury.io/py/fstrent_colors.svg)](https://badge.fury.io/py/fstrent_colors)
[![Build Status](https://github.com/wrm3/fstrent_colors/actions/workflows/publish.yml/badge.svg)](https://github.com/wrm3/fstrent_colors/actions)
[![License](https://img.shields.io/github/license/wrm3/fstrent_colors)](https://github.com/wrm3/fstrent_colors/blob/main/LICENSE)

Enhanced terminal color library providing extensive color combinations and utilities for Python applications.



## Features

- 🎨 16 Base colors (including light variants)
- 🖼️ Background colors for all combinations
- 🌈 Color on color support (e.g., red text on blue background)
- 🛠️ Utility functions for string coloring
- 📝 Simple API for color manipulation
- 🔧 Cross-platform support via colorama

## Demo

Check out the demo video to see FSTrent Colors in action:

[![FSTrent Colors Demo](https://img.youtube.com/vi/I_0jq4ZSAE8/0.jpg)](https://youtu.be/I_0jq4ZSAE8)

## Installation

```bash
pip install fstrent_colors
```

## Basic Usage

```python
from fstrent_colors import (
    # Utility functions
    cs, cp,
    
    # Basic colors
    R, G, B, W  # Red, Green, Blue, White
)

# Print colored text
cp("This is red text", R)
cp("This is green text", G)
cp("This is blue text", B)

# Create colored strings
colored_text = cs("Custom colored text", B)
print(colored_text)
```

## Available Colors

### Basic Colors
```python
from fstrent_colors import (
    K,    # Black
    R,    # Red
    G,    # Green
    Y,    # Yellow
    B,    # Blue
    M,    # Magenta
    C,    # Cyan
    W,    # White
    LGy,  # Light Gray
    DGy,  # Dark Gray
    LR,   # Light Red
    LG,   # Light Green
    LY,   # Light Yellow
    LB,   # Light Blue
    LM,   # Light Magenta
    LC,   # Light Cyan
)
```

### Color on Color Examples

```python
from fstrent_colors import (
    # White on Multi-color Backgrounds
    WoR,  # White on Red
    WoG,  # White on Green
    WoM,  # White on Magenta
    
    # Colors on White Background
    RoW,  # Red on White
    GoW,  # Green on White
    BoW,  # Blue on White
    
    # Colors on Blue Background
    RoB,  # Red on Blue
    GoB,  # Green on Blue
    WoB,  # White on Blue
)

# Many more combinations available!
```

## Color Utility Functions

```python
from fstrent_colors import cs, cp, CLR

# Color string  and returnfunction
text = cs("Colored text", R)

# Color print function
cp("Directly print colored text", B)

# Access color palette
my_color = pallette['RED']

# Use color lookup
dynamic_color = CLR['BLUE']
```

## Demo Functions

The package includes several demo functions to showcase different color combinations:

```python
from fstrent_colors import (
    demo1,  # Basic colors
    demo2,  # Bright colors
    demo3,  # Background colors
    demo4,  # Color combinations
    demo5,  # Styles
    demo6,  # Rainbow effects
    demo7,  # Gradient effects
    demo8,  # Patterns
    demo9,  # Full spectrum
)

# Run demos
demo1()  # Shows basic colors
demo9()  # Shows full color spectrum
```

## Advanced Usage

### Combining Colors and Backgrounds

```python
from fstrent_colors import R, G, B, W, RoK, WoB

# Multiple styles in one line
print(RoK + "Red on Black" + W + " Normal " + WoB + "White on Blue" + W)
```

### Using with String Formatting

```python
from fstrent_colors import R, G, W

name = "World"
print(f"{R}Hello {G}{name}{W}!")
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/wrm3/fstrent_colors.git
cd fstrent_colors
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

MIT License - see LICENSE file for details.

## Author

Warren R Martel III (wrmartel3@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
