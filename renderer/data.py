from typing import NamedTuple, Optional


class PlayerInfo(NamedTuple):
    """Player information"""

    account_db_id: int
    id: int
    clan_color: int
    clan_id: int
    clan_tag: str
    max_health: int
    name: str
    realm: str
    ship_id: int
    team_id: int
    is_bot: bool
    ship_params_id: int
    relation: int
    hull: Optional[int]
    modernization: tuple
    skills: list[list[int]]


class Vehicle(NamedTuple):
    """Vehicle data."""

    player_id: int
    vehicle_id: int
    health: int
    is_alive: bool
    x: int
    y: int
    yaw: float
    relation: int
    is_visible: bool
    not_in_range: bool
    visibility_flag: int
    burn_flags: int
    consumables_state: dict[int, tuple]
    regenerated_health: float = 0.0
    regen_crew_hp_limit: float = 0.0
    regeneration_health: float = 0.0


class Smoke(NamedTuple):
    """Smoke data."""

    entity_id: int
    radius: float
    points: list[tuple[int, int]]


class Shot(NamedTuple):
    """Shot data."""

    owner_id: int
    origin: tuple[int, int]
    destination: tuple[int, int]
    shot_id: int
    t_time: int


class Torpedo(NamedTuple):
    """Torpedo data."""

    owner_id: int
    params_id: int
    origin: tuple[int, int]
    direction: tuple[float, float]
    shot_id: int


class Consumable(NamedTuple):
    """Consumable data."""

    ship_id: int
    consumable_id: int
    duration: float


class Plane(NamedTuple):
    """Plane data."""

    plane_id: int
    owner_id: int
    params_id: int
    index: int
    purpose: int
    departures: int
    relation: int
    position: tuple[int, int]


class Ward(NamedTuple):
    """Ward data."""

    plane_id: int
    vehicle_id: int
    position: tuple[int, int]
    radius: int
    relation: int


class ControlPoint(NamedTuple):
    position: tuple[int, int]
    radius: int
    team_id: int
    invader_team: int
    control_point_type: int
    progress: float
    both_inside: bool
    has_invaders: bool
    capture_time: int
    capture_speed: float
    relation: int
    is_visible: bool


class Score(NamedTuple):
    relation: int
    score: int


class Frag(NamedTuple):
    killed_id: int
    fragger_id: int
    death_type: int


class Message(NamedTuple):
    player_id: int
    namespace: str
    message: str


class Events(NamedTuple):
    """Match events."""

    time_left: int
    evt_vehicle: dict[int, Vehicle]
    evt_plane: dict[int, Plane]
    evt_ward: dict[int, Ward]
    evt_smoke: dict[int, Smoke]
    evt_shot: list[Shot]
    evt_torpedo: list[Torpedo]
    evt_hits: list[int]
    evt_consumable: dict[int, list[Consumable]]
    evt_control: dict[int, ControlPoint]
    evt_score: dict[int, Score]
    evt_damage_maps: dict[str, dict[int, tuple[int, float]]]
    evt_frag: list[Frag]
    evt_ribbon: dict
    evt_achievement: dict
    evt_times_to_win: Optional[tuple[float, float]]
    evt_chat: list[Message]


class ReplayData(NamedTuple):
    """Replay data."""

    game_version: str
    game_map: str
    game_battle_type: int
    game_win_score: int
    owner_avatar_id: int
    owner_vehicle_id: int
    owner_id: int
    player_info: dict[int, PlayerInfo]
    events: dict[int, Events]
