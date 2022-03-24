def color_str(substr: str, color: str, base_color="white") -> str:
    """Color a string for display in terminal."""
    base_str = "\033["
    sep = ";"
    end = "m"
    str_colors: dict = {
        "black": base_str + "30" + end,
        "red": base_str + "31" + end,
        "green": base_str + "32" + end,
        "yellow": base_str + "33" + end,
        "blue": base_str + "34" + end,
        "purple": base_str + "35" + end,
        "cyan": base_str + "36" + end,
        "white": base_str + "37" + end
    }
    base_color_str = str_colors.get(base_color)
    color_str = str_colors.get(color, base_color_str)
    return color_str + substr + base_color_str


