"""Tests for the fstrent_colors module."""

import pytest
from io import StringIO
import sys
from fstrent_colors import (
    # Utility functions
    cs, cp, pallette, CLR,
    
    # Demo functions
    demo1, demo2, demo3, demo4, demo5, demo6, demo7, demo8, demo9,
    
    # Basic colors
    K, R, G, Y, B, M, C, W, LGy, DGy, LR, LG, LY, LB, LM, LC,
    
    # Colors on black
    KoK, RoK, GoK, YoK, BoK, MoK, CoK, WoK, LGyoK, DGyoK, LRoK, LGoK, LYoK, LBoK, LMoK, LCoK,
    
    # Colors on white
    KoW, RoW, GoW, YoW, BoW, MoW, CoW, WoW, LGyoW, DGyoW, LRoW, LGoW, LYoW, LBoW, LMoW, LCoW,
    
    # Colors on light gray
    KoLGy, RoLGy, GoLGy, YoLGy, BoLGy, MoLGy, CoLGy, WoLGy, LGyoLGy, DGyoLGy, LRoLGy, LGoLGy, LYoLGy, LBoLGy, LMoLGy, LCoLGy,
    
    # Colors on dark gray
    KoDGy, RoDGy, GoDGy, YoDGy, BoDGy, MoDGy, CoDGy, WoDGy, LGyoDGy, DGyoDGy, LRoDGy, LGoDGy, LYoDGy, LBoDGy, LMoDGy, LCoDGy,
    
    # Colors on blue
    KoB, RoB, GoB, YoB, BoB, MoB, CoB, WoB, LGyoB, DGyoB, LRoB, LGoB, LYoB, LBoB, LMoB, LCoB,
    
    # Colors on light blue
    KoLB, RoLB, GoLB, YoLB, BoLB, MoLB, CoLB, WoLB, LGyoLB, DGyoLB, LRoLB, LGoLB, LYoLB, LBoLB, LMoLB, LCoLB,
    
    # Colors on cyan
    KoC, RoC, GoC, YoC, BoC, MoC, CoC, WoC, LGyoC, DGyoC, LRoC, LGoC, LYoC, LBoC, LMoC, LCoC,
    
    # Colors on light cyan
    KoLC, RoLC, GoLC, YoLC, BoLC, MoLC, CoLC, WoLC, LGyoLC, DGyoLC, LRoLC, LGoLC, LYoLC, LBoLC, LMoLC, LCoLC,
    
    # Colors on green
    KoG, RoG, GoG, YoG, BoG, MoG, CoG, WoG, LGyoG, DGyoG, LRoG, LGoG, LYoG, LBoG, LMoG, LCoG,
    
    # Colors on light green
    KoLG, RoLG, GoLG, YoLG, BoLG, MoLG, CoLG, WoLG, LGyoLG, DGyoLG, LRoLG, LGoLG, LYoLG, LBoLG, LMoLG, LCoLG,
    
    # Colors on magenta
    KoM, RoM, GoM, YoM, BoM, MoM, CoM, WoM, LGyoM, DGyoM, LRoM, LGoM, LYoM, LBoM, LMoM, LCoM,
    
    # Colors on light magenta
    KoLM, RoLM, GoLM, YoLM, BoLM, MoLM, CoLM, WoLM, LGyoLM, DGyoLM, LRoLM, LGoLM, LYoLM, LBoLM, LMoLM, LCoLM,
    
    # Colors on red
    KoR, RoR, GoR, YoR, BoR, MoR, CoR, WoR, LGyoR, DGyoR, LRoR, LGoR, LYoR, LBoR, LMoR, LCoR,
    
    # Colors on light red
    KoLR, RoLR, GoLR, YoLR, BoLR, MoLR, CoLR, WoLR, LGyoLR, DGyoLR, LRoLR, LGoLR, LYoLR, LBoLR, LMoLR, LCoLR,
    
    # Colors on yellow
    KoY, RoY, GoY, YoY, BoY, MoY, CoY, WoY, LGyoY, DGyoY, LRoY, LGoY, LYoY, LBoY, LMoY, LCoY,
    
    # Colors on light yellow
    KoLY, RoLY, GoLY, YoLY, BoLY, MoLY, CoLY, WoLY, LGyoLY, DGyoLY, LRoLY, LGoLY, LYoLY, LBoLY, LMoLY, LCoLY
)

@pytest.fixture
def capture_stdout():
    """Capture stdout for testing demo output."""
    stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout
    yield stdout
    sys.stdout = old_stdout

def test_base_colors_exist():
    """Test that base color variables exist and are strings."""
    colors = [K, R, G, Y, B, M, C, W, LGy, DGy, LR, LG, LY, LB, LM, LC]
    for color in colors:
        assert isinstance(color, str)

def test_black_background_colors_exist():
    """Test that colors on black background exist and are strings."""
    colors = [KoK, RoK, GoK, YoK, BoK, MoK, CoK, WoK, LGyoK, DGyoK, LRoK, LGoK, LYoK, LBoK, LMoK, LCoK]
    for color in colors:
        assert isinstance(color, str)

def test_color_functions():
    """Test the color utility functions."""
    assert callable(cs)
    assert callable(cp)
    
    # Test cs function
    test_text = "Hello World"
    colored_text = cs(test_text, R)
    assert isinstance(colored_text, str)
    assert test_text in colored_text
    
    # Test cp function
    colored_print = cp(test_text, R)
    assert colored_print is None  # cp should return None as it prints directly

def test_pallette():
    """Test the pallette object."""
    assert pallette is not None
    assert isinstance(pallette, dict)

def test_CLR():
    """Test the CLR object."""
    assert CLR is not None
    assert isinstance(CLR, dict)

@pytest.mark.parametrize("demo_func", [
    demo1, demo2, demo3, demo4, demo5,
    demo6, demo7, demo8, demo9
])
def test_demos(demo_func, capture_stdout):
    """Test all demo functions."""
    demo_func()
    output = capture_stdout.getvalue()
    assert output  # Verify demo produced output
    assert '\033[' in output  # Verify ANSI color codes are present

def test_demo1_basic_colors(capture_stdout):
    """Test demo1 shows basic colors correctly."""
    demo1()
    output = capture_stdout.getvalue()
    assert "Basic Colors" in output
    assert all(color in output for color in ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"])

def test_demo2_bright_colors(capture_stdout):
    """Test demo2 shows bright colors correctly."""
    demo2()
    output = capture_stdout.getvalue()
    assert "Bright Colors" in output
    assert all(color in output for color in ["Light Red", "Light Green", "Light Blue"])

def test_demo3_background_colors(capture_stdout):
    """Test demo3 shows background colors correctly."""
    demo3()
    output = capture_stdout.getvalue()
    assert "Background Colors" in output

def test_demo4_color_combinations(capture_stdout):
    """Test demo4 shows color combinations correctly."""
    demo4()
    output = capture_stdout.getvalue()
    assert "Color Combinations" in output

def test_demo5_styles(capture_stdout):
    """Test demo5 shows different styles correctly."""
    demo5()
    output = capture_stdout.getvalue()
    assert "Styles" in output

def test_demo6_rainbow(capture_stdout):
    """Test demo6 shows rainbow effect correctly."""
    demo6()
    output = capture_stdout.getvalue()
    assert "Rainbow" in output

def test_demo7_gradient(capture_stdout):
    """Test demo7 shows gradient effect correctly."""
    demo7()
    output = capture_stdout.getvalue()
    assert "Gradient" in output

def test_demo8_patterns(capture_stdout):
    """Test demo8 shows patterns correctly."""
    demo8()
    output = capture_stdout.getvalue()
    assert "Patterns" in output

def test_demo9_full_spectrum(capture_stdout):
    """Test demo9 shows full spectrum correctly."""
    demo9()
    output = capture_stdout.getvalue()
    assert "Full Spectrum" in output

def test_color_string_formatting():
    """Test that color strings can be used in string formatting."""
    text = "Test"
    formatted = f"{R}{text}{W}"
    assert text in formatted
    assert R in formatted
    assert W in formatted

def test_color_concatenation():
    """Test that color strings can be concatenated."""
    text = "Test"
    concatenated = R + B + text + W
    assert text in concatenated
    assert R in concatenated
    assert B in concatenated
    assert W in concatenated

def test_white_background_colors_exist():
    """Test that colors on white background exist and are strings."""
    colors = [KoW, RoW, GoW, YoW, BoW, MoW, CoW, WoW, LGyoW, DGyoW, LRoW, LGoW, LYoW, LBoW, LMoW, LCoW]
    for color in colors:
        assert isinstance(color, str)

def test_light_gray_background_colors_exist():
    """Test that colors on light gray background exist and are strings."""
    colors = [KoLGy, RoLGy, GoLGy, YoLGy, BoLGy, MoLGy, CoLGy, WoLGy, LGyoLGy, DGyoLGy, 
              LRoLGy, LGoLGy, LYoLGy, LBoLGy, LMoLGy, LCoLGy]
    for color in colors:
        assert isinstance(color, str)

def test_dark_gray_background_colors_exist():
    """Test that colors on dark gray background exist and are strings."""
    colors = [KoDGy, RoDGy, GoDGy, YoDGy, BoDGy, MoDGy, CoDGy, WoDGy, LGyoDGy, DGyoDGy,
              LRoDGy, LGoDGy, LYoDGy, LBoDGy, LMoDGy, LCoDGy]
    for color in colors:
        assert isinstance(color, str)

def test_blue_background_colors_exist():
    """Test that colors on blue background exist and are strings."""
    colors = [KoB, RoB, GoB, YoB, BoB, MoB, CoB, WoB, LGyoB, DGyoB, LRoB, LGoB, LYoB, LBoB, LMoB, LCoB]
    for color in colors:
        assert isinstance(color, str)

def test_light_blue_background_colors_exist():
    """Test that colors on light blue background exist and are strings."""
    colors = [KoLB, RoLB, GoLB, YoLB, BoLB, MoLB, CoLB, WoLB, LGyoLB, DGyoLB,
              LRoLB, LGoLB, LYoLB, LBoLB, LMoLB, LCoLB]
    for color in colors:
        assert isinstance(color, str)

def test_cyan_background_colors_exist():
    """Test that colors on cyan background exist and are strings."""
    colors = [KoC, RoC, GoC, YoC, BoC, MoC, CoC, WoC, LGyoC, DGyoC, LRoC, LGoC, LYoC, LBoC, LMoC, LCoC]
    for color in colors:
        assert isinstance(color, str)

def test_light_cyan_background_colors_exist():
    """Test that colors on light cyan background exist and are strings."""
    colors = [KoLC, RoLC, GoLC, YoLC, BoLC, MoLC, CoLC, WoLC, LGyoLC, DGyoLC,
              LRoLC, LGoLC, LYoLC, LBoLC, LMoLC, LCoLC]
    for color in colors:
        assert isinstance(color, str)

def test_green_background_colors_exist():
    """Test that colors on green background exist and are strings."""
    colors = [KoG, RoG, GoG, YoG, BoG, MoG, CoG, WoG, LGyoG, DGyoG, LRoG, LGoG, LYoG, LBoG, LMoG, LCoG]
    for color in colors:
        assert isinstance(color, str)

def test_light_green_background_colors_exist():
    """Test that colors on light green background exist and are strings."""
    colors = [KoLG, RoLG, GoLG, YoLG, BoLG, MoLG, CoLG, WoLG, LGyoLG, DGyoLG,
              LRoLG, LGoLG, LYoLG, LBoLG, LMoLG, LCoLG]
    for color in colors:
        assert isinstance(color, str)

def test_magenta_background_colors_exist():
    """Test that colors on magenta background exist and are strings."""
    colors = [KoM, RoM, GoM, YoM, BoM, MoM, CoM, WoM, LGyoM, DGyoM, LRoM, LGoM, LYoM, LBoM, LMoM, LCoM]
    for color in colors:
        assert isinstance(color, str)

def test_light_magenta_background_colors_exist():
    """Test that colors on light magenta background exist and are strings."""
    colors = [KoLM, RoLM, GoLM, YoLM, BoLM, MoLM, CoLM, WoLM, LGyoLM, DGyoLM,
              LRoLM, LGoLM, LYoLM, LBoLM, LMoLM, LCoLM]
    for color in colors:
        assert isinstance(color, str)

def test_red_background_colors_exist():
    """Test that colors on red background exist and are strings."""
    colors = [KoR, RoR, GoR, YoR, BoR, MoR, CoR, WoR, LGyoR, DGyoR, LRoR, LGoR, LYoR, LBoR, LMoR, LCoR]
    for color in colors:
        assert isinstance(color, str)

def test_light_red_background_colors_exist():
    """Test that colors on light red background exist and are strings."""
    colors = [KoLR, RoLR, GoLR, YoLR, BoLR, MoLR, CoLR, WoLR, LGyoLR, DGyoLR,
              LRoLR, LGoLR, LYoLR, LBoLR, LMoLR, LCoLR]
    for color in colors:
        assert isinstance(color, str)

def test_yellow_background_colors_exist():
    """Test that colors on yellow background exist and are strings."""
    colors = [KoY, RoY, GoY, YoY, BoY, MoY, CoY, WoY, LGyoY, DGyoY, LRoY, LGoY, LYoY, LBoY, LMoY, LCoY]
    for color in colors:
        assert isinstance(color, str)

def test_light_yellow_background_colors_exist():
    """Test that colors on light yellow background exist and are strings."""
    colors = [KoLY, RoLY, GoLY, YoLY, BoLY, MoLY, CoLY, WoLY, LGyoLY, DGyoLY,
              LRoLY, LGoLY, LYoLY, LBoLY, LMoLY, LCoLY]
    for color in colors:
        assert isinstance(color, str)

def test_color_combinations():
    """Test various color combinations work together."""
    text = "Test"
    # Test foreground + background
    assert isinstance(RoB + text + W, str)  # Red on Blue
    assert isinstance(GoY + text + W, str)  # Green on Yellow
    assert isinstance(BoW + text + W, str)  # Blue on White
    
    # Test with light colors
    assert isinstance(LRoLB + text + W, str)  # Light Red on Light Blue
    assert isinstance(LGoLY + text + W, str)  # Light Green on Light Yellow
    assert isinstance(LBoLW + text + W, str)  # Light Blue on White

def test_color_reset():
    """Test that color reset works properly."""
    text = "Test"
    colored_text = R + text + W
    assert colored_text.endswith(W)  # Should end with reset
    
    # Test multiple resets
    complex_text = R + "Red" + G + "Green" + B + "Blue" + W
    assert complex_text.endswith(W)

def test_color_nesting():
    """Test nested color combinations."""
    text = "Test"
    nested = R + "Red" + (G + "Green" + W) + "Back to Red" + W
    assert isinstance(nested, str)
    assert nested.count(W) >= 2  # Should have at least 2 resets
  