import numpy as np

from typing import Union
from renderer.data import PlayerInfo
from renderer.render import Renderer
from renderer.base import LayerBase
from renderer.const import RELATION_NORMAL_STR, COLORS_NORMAL
from PIL import Image, ImageDraw, ImageColor
from math import floor

from .counter import X_POS as COUNTERS_POS


CENTER = (800 + COUNTERS_POS) // 2
SKILLS_ORDER = [
    "AirCarrier",
    "Battleship",
    "Cruiser",
    "Destroyer",
    "Auxiliary",
    "Submarine",
]
FIRE_PREVENTION_ID = 14
BURN_NODE_BITS = 4
BURN_NODE_POSITIONS = [
    [None, None, None, None],
    [(0.5, 0.52), None, None, None],  # subs
    [(0.125, 0.52), None, None, (0.875, 0.52)],  # only auxiliary ships?
    [(0.125, 0.52), (0.5, 0.52), None, (0.875, 0.52)],  # battleships w/ FP
    [
        (0.125, 0.52),
        (0.375, 0.52),
        (0.625, 0.52),
        (0.875, 0.52),
    ],  # everything else
]
FLOOD_NODE_BITS = 2
FLOOD_NODE_POSITIONS = [
    [None, None],
    [(0.5, 0.86), None],  # subs
    [(0.252, 0.86), (0.748, 0.86)],  # everything else
]


class LayerHealthBase(LayerBase):
    """The class for handling player's ship health bar.

    Args:
        LayerBase (_type_): _description_
    """

    def __init__(self, renderer: Renderer):
        self._renderer = renderer
        self._ships = renderer.resman.load_json("ships.json")
        self._player = renderer.replay_data.player_info[
            renderer.replay_data.owner_id
        ]
        self._font = self._renderer.resman.load_font(
            filename="warhelios_bold.ttf", size=16
        )
        self._green = ImageColor.getrgb("#4ce8aaff")
        self._yellow = ImageColor.getrgb("#ffc400ff")
        self._red = ImageColor.getrgb("#fe4d2aff")
        self._color_gray = ImageColor.getrgb("#ffffffc3")
        self._abilities = renderer.resman.load_json("abilities.json")

        self._burn_icon = self._renderer.resman.load_image(
            "fire.png", path="status_icons"
        )
        self._flood_icon = self._renderer.resman.load_image(
            "flooding.png", path="status_icons"
        )

    def _add_padding(self, bar: Image.Image):
        padded = Image.new("RGBA", (bar.width, bar.height + 4), (0, 0, 0, 0))
        padded.paste(bar, (0, 0))
        return padded

    def draw(self, game_time: int, image: Image.Image):
        """Draws the health bar into the image.

        Args:
            game_time (int): The game time.
            image (Image.Image): The minimap image.
        """
        ships = self._renderer.replay_data.events[game_time].evt_vehicle
        ship = ships[self._player.ship_id]
        ability = self._abilities[self._player.ship_params_id]
        per = ship.health / self._player.max_health
        index, name, species, level, hulls = self._ships[
            self._player.ship_params_id
        ]

        suffix_fg = "_h"
        suffix_bg = "_h_bg" if ship.is_alive else "_h_bgdead"

        bg_bar = self._renderer.resman.load_image(
            f"{index}{suffix_bg}.png", nearest=False, path="ship_bars"
        )
        bg_bar = self._add_padding(bg_bar)

        fg_bar = self._renderer.resman.load_image(
            f"{index}{suffix_fg}.png", nearest=False, path="ship_bars"
        )
        fg_bar = self._add_padding(fg_bar)
        fg_bar = fg_bar.resize(bg_bar.size, Image.LANCZOS)

        if per > 0.8:
            bar_color = self._green
        elif 0.8 >= per > 0.3:
            bar_color = self._yellow
        else:
            bar_color = self._red

        if ship.is_alive:
            alpha = 75
            hp_bar_arr = np.array(fg_bar)
            hp_bar_arr[hp_bar_arr[:, :, 3] > alpha] = bar_color
            hp_bar_img = Image.fromarray(hp_bar_arr)
            mask_hp_img = Image.new(fg_bar.mode, fg_bar.size)
            mask_hp_img_w = mask_hp_img.width * per
            mask_hp_draw = ImageDraw.Draw(mask_hp_img)
            mask_hp_draw.rectangle(
                ((0, 0), (mask_hp_img_w, mask_hp_img.width)), fill="black"
            )

            if regen := ship.consumables_state.get(9, None):
                st, count, en, t = regen
                if count:
                    wt = ability["workTime"]
                    rhs = ability["regenerationHPSpeed"]
                    maxHeal = floor(wt) * rhs * self._player.max_health
                    canHeal = (
                        ship.regeneration_health
                        if ship.regeneration_health < maxHeal
                        else maxHeal
                    )

                    per_limit = (
                        canHeal + ship.health
                    ) / self._player.max_health

                    regen_bar_arr = np.array(fg_bar)
                    regen_bar_arr[
                        regen_bar_arr[:, :, 3] > alpha
                    ] = self._color_gray
                    regen_bar_img = Image.fromarray(regen_bar_arr)
                    mask_regen_img = Image.new(fg_bar.mode, fg_bar.size)
                    mask_regen_img_w = mask_regen_img.width * per_limit
                    mask_regen_draw = ImageDraw.Draw(mask_regen_img)
                    mask_regen_draw.rectangle(
                        ((0, 0), (mask_regen_img_w, mask_regen_img.width)),
                        fill="black",
                    )

                    bg_bar.paste(regen_bar_img, mask=mask_regen_img)
            bg_bar.paste(hp_bar_img, mask=mask_hp_img)

        hp_current = "{:,}".format(round(ship.health)).replace(",", " ")
        hp_max = "{:,}".format(round(self._player.max_health)).replace(
            ",", " "
        )
        hp_max_text = f"/{hp_max}"

        hp_c_w, hp_c_h = self._font.getsize(hp_current)
        hp_w, hp_h = self._font.getsize(hp_max_text)
        n_w, n_h = self._font.getsize(name)

        bg_bar = bg_bar.resize((235, 62), resample=Image.LANCZOS)

        px = CENTER - round(bg_bar.width / 2)

        th = Image.new("RGBA", (bg_bar.width, max(hp_h, n_h, hp_c_h)))
        th_draw = ImageDraw.Draw(th)

        th_draw.text((0, 0), name, fill="white", font=self._font)
        th_draw.text(
            (th.width - (hp_w + hp_c_w), 0),
            hp_current,
            fill=bar_color,
            font=self._font,
        )
        th_draw.text(
            (th.width - hp_w, 0),
            hp_max_text,
            fill="#cdcdcd",
            font=self._font,
        )

        if (flags := bin(ship.burn_flags)[2:][::-1]) != "0":
            burn_nodes, flood_nodes = hulls[self._player.hull]
            active_skills = self._player.skills[SKILLS_ORDER.index(species)]
            if FIRE_PREVENTION_ID in active_skills:
                burn_nodes -= 1

            self._draw_nodes(
                bg_bar,
                self._burn_icon,
                flags[0:BURN_NODE_BITS],
                BURN_NODE_POSITIONS[burn_nodes],
            )
            self._draw_nodes(
                bg_bar,
                self._flood_icon,
                flags[BURN_NODE_BITS: BURN_NODE_BITS + FLOOD_NODE_BITS],
                FLOOD_NODE_POSITIONS[flood_nodes],
            )

        image.paste(th, (px, 205), th)
        image.paste(bg_bar, (px, 145), bg_bar)

    def _draw_nodes(
        self,
        image: Image.Image,
        icon: Image.Image,
        flags: str,
        positions: list,
    ):
        """Draws the status nodes into the health bar.

        Args:
            image (Image.Image): Base image.
            icon (Image.Image): Status icon.
            flags (str): ?
            positions (list): The position of the node.
        """
        for index, bit in enumerate(flags):
            if bit == "1":
                x_per, y_per = positions[index]
                image.paste(
                    icon,
                    (
                        round(image.width * x_per - icon.width / 2),
                        round(image.height * y_per - icon.height / 2),
                    ),
                    icon,
                )
