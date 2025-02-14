from data.utils import LOGGER

from data import (
    create_ships_data,
    create_planes_data,
    create_projectiles_data,
    create_achievements_data,
    create_abilities_data,
)


if __name__ == "__main__":
    create_ships_data()
    create_planes_data()
    create_projectiles_data()
    create_achievements_data()
    create_abilities_data()
    LOGGER.info("Done.")
