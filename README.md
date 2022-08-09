## Minimap Renderer with windows gui for easy usage
### Forked from https://github.com/WoWs-Builder-Team/minimap_renderer

## Work in Progress   |   Features to be implemented
```
GUI for selecting and rendering multiple replays
Select output folder
Output file naming scheme
```








  

Minimap Renderer parses World of Warships replays to create a timelapse video that resembles the in-game minimap.

![enter image description here](https://github.com/WoWs-Builder-Team/minimap_renderer/blob/master/docs/minimap.gif?raw=true)

### Installation

  

1. Get Python 3.10 or higher

  

A virtual environment can be created with `python3.10 -m venv venv`.

  

2. Clone the repository

  

```

git clone https://github.com/WoWs-Builder-Team/minimap_renderer.git

```

  

3. Install dependencies

  

```

cd minimap_renderer

pip install -U -r requirements.txt

```

  

4. You're set!

  
  

### Usage

  

Replays can be parsed with `replay_parser.py`. The full usage is:

```

replay_parser.py --replay <replay_path> [--strict_mode]

```

  

This will generate `data.dat` in the root directory. Now, you can simply run `render.py` to create `minimap.mp4`.

  

### License

  

This project is licensed under the GNU AGPLv3 License.

  

### Credits and Links

  

- This project is maintained by `@notyourfather#7816` and `@Trackpad#1234`.

- However, it would not have been possible without Monstrofil's [replays_unpack](https://github.com/Monstrofil/replays_unpack)!

- A Discord bot wrapper is available [here](https://github.com/padtrack/track).
