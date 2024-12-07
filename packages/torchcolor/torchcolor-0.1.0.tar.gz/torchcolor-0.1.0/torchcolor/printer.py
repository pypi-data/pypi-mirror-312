from dataclasses import dataclass
from typing import Union
from copy import deepcopy

from .strategy import ColorStrategy, ModuleStyle
from .color import reset_color
from .style import clean_style

# Function for adding indent from the pytorch codebase in /torch/nn/modules/module.py
def _addindent(s_, numSpaces):
    s = s_.split("\n")
    # don't do anything for single-line stuff
    if len(s) == 1:
        return s_
    first = s.pop(0)
    s = [(numSpaces * " ") + line for line in s]
    s = "\n".join(s)
    s = first + "\n" + s
    return s


def summarize_repeated_modules(lines):
    """
    Group repeated submodules into a single summary line if they have the same color and type.
    """
    if len(lines) == 0: return []

    grouped_lines = []
    previous_key, previous_module_str, previous_style = None, None, None
    count = 0
    start_index = None

    for i, (key, mod_str, style, depth) in enumerate(lines):
        if mod_str == previous_module_str and style == previous_style and (previous_key == key or key.isdigit()):
            if count == 0: start_index = i - 1
            count += 1
        else:
            if count > 0:
                grouped_lines.pop()
                grouped_lines.append((f"{start_index}-{i-1}", count+1, previous_module_str, deepcopy(previous_style), depth))
            grouped_lines.append((key, None, mod_str, deepcopy(style), depth))
            count = 0

        previous_module_str = mod_str
        previous_style = style
        previous_key = key

    # Handle the last group
    if count > 0:
        grouped_lines.pop()
        grouped_lines.append(
            (f"{start_index}-{len(lines)-1}", count + 1, previous_module_str, deepcopy(previous_style), depth)
        )

    return grouped_lines

@dataclass
class ModuleParam:
    is_leaf: bool
    is_root: bool

class Printer:

    def __init__(self, strategy: Union[str, ColorStrategy]):
        self.set_strategy(strategy)

    def set_strategy(self, strategy: Union[str, ColorStrategy], *args, **kwargs):
        """Change the strategy dynamically."""
        if isinstance(strategy, str):
            strategy = ColorStrategy.get_strategy(strategy, *args, **kwargs)
        self.strategy = strategy

    def print(self, module, display_depth: bool = False, display_legend: bool = False):
        print(self.repr_module(module, display_depth=display_depth)[0])

    def repr_module(self, parent_module, display_depth=False, indent=2):
        """
        Recursively print the module with the chosen color strategy.
        """
        extra_lines = []
        extra_repr = parent_module.extra_repr()
        if extra_repr:
            extra_lines = extra_repr.split("\n")

        max_depth = 0
        child_lines = []
        for key, module in parent_module._modules.items():
            if module is None:
                continue

            mod_str, module_depth = self.repr_module(module, indent=indent + 2, display_depth=display_depth)
            style: ModuleStyle = self.strategy.get_style(module, ModuleParam(is_leaf=module_depth == 0, is_root=False))
            max_depth = max(module_depth+1, max_depth)
            # print(key, mod_str, style, module_depth)
            child_lines.append((key, mod_str, style, module_depth))

        summarized_lines = summarize_repeated_modules(child_lines)

        child_lines_formatted = []
        for key, count, mod_str, style, depth in summarized_lines:
            stylised_name = style.name_style.apply(f"({key}):") if style.name_style else f"({key}):"
            stylised_layer = style.layer_style.apply(mod_str) if style.layer_style and depth == 0 else mod_str

            child_lines_formatted.append(_addindent(
                (f"[{str(depth)}] " if display_depth else "") +
                f"{stylised_name} " +
                (f"{count} x " if count else "") +
                f"{stylised_layer}"
            , 2))

        lines = extra_lines + child_lines_formatted
        style: ModuleStyle = self.strategy.get_style(parent_module, ModuleParam(is_leaf=max_depth == 0, is_root=indent==2))
        main_str = parent_module._get_name()

        if lines:
            if len(extra_lines) == 1 and not child_lines_formatted:
                stylised_extra_line = style.extra_style.apply(extra_lines[0]) if style.extra_style else extra_lines[0]
                main_str += reset_color.to_ansi() + "(" + stylised_extra_line + reset_color.to_ansi() + ")"
            else:
                main_str += reset_color.to_ansi() + "(\n  " + "\n  ".join(lines) + reset_color.to_ansi() + "\n)"

        main_str = style.layer_style.apply(main_str) if style.layer_style else main_str
        return main_str, max_depth