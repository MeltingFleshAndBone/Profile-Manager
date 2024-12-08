# Profile Manager
This is a tool to manage profiles, it's not fast or efficient, but it works (often). <br>
Wrote this in a couple of hours, so expect bugs, lots of bugs.

## Usage
### Flags and Parameters
- `-p` or `--profile PROFILE_NAME`: Specify the profile to set.
- `-c` or `--current`: Use the current profile.
- `-d` or `--dry_run`: Perform a dry run without making changes.
- `-l` or `--list (TAGS)`: List profiles with specified tags.
- `-lh` or `--list_hidden`: Include hidden profiles in the list. 
- `-f` or `--force`: Force overwrite existing symlinks.
- `-h` or `--help`: Display this help message.
### .profile File Format
The default path is at `~/.config/profiles/`, if you don't like it, you can change it in the code (main.py:main()).
Profiles end in .profile, and have the following format:

- `@Tag:Tagname1, Tagname2` sets a tag for the profile, multiple tags can be set by separating them with a comma.
- `@Theme:ThemeName` sets the theme for the profile, does absolutely nothing.
- `@Desc:Text` sets the description for the profile. (@Description works as well)
- `@Priority:Priority` sets the priority for the profile, i.e. the order they appear when listing (also their color)
- `:source:target` creates a symlink from source to target
- `!command` executes a command.
- `#comments` are ignored

## Example
Here's one of my profiles
```md
# Name: Unix.profile
# File declaration
@Tag: Dark,Dev
@Theme: DarkPride 
@Desc: Doesn't hurt my eyes
@Priority: 3

# Hypr utils 
:hypr/hyprland.conf:~/.config/hypr/hyprland.conf
:hypr/hyprlock.conf:~/.config/hypr/hyprlock.conf
:hypr/hyprpaper.conf:~/.config/hypr/hyprpaper.conf
# Hypr includes
:hypr/include/aesthetic.conf:~/.config/hypr/include/aesthetic.conf
:hypr/include/animations.conf:~/.config/hypr/include/animations.conf
:hypr/include/autostart.conf:~/.config/hypr/include/autostart.conf
:hypr/include/binds.conf:~/.config/hypr/include/binds.conf
:hypr/include/input.conf:~/.config/hypr/include/input.conf
:hypr/include/layout.conf:~/.config/hypr/include/layout.conf
:hypr/include/windowrules.conf:~/.config/hypr/include/windowrules.conf

# Rofi colors
:rofi/colors/darkpride.rasi:~/.config/rofi/colors/darkpride.rasi
:rofi/launchers/type-1/colors.rasi:~/.config/rofi/launchers/type-1/shared/colors.rasi
:rofi/applets/colors.rasi:~/.config/rofi/applets/shared/colors.rasi

# Kitty
:kitty/kitty.conf:~/.config/kitty/kitty.conf
:kitty/current-theme.conf:~/.config/kitty/current-theme.conf
# Reload configuration file
# Remote control needs to be enabled
!kitty @ action load_config_file& > /dev/null

# Waybar
:waybar/config:~/.config/waybar/config
:waybar/default-modules.json:~/.config/waybar/default-modules.json
:waybar/style.css:~/.config/waybar/style.css
# Reload waybar
!pkill waybar; waybar& > /dev/null

# Wallpaper
# This is literally just a wrapper of Hyprpaper I wrote
# Just use hyprpaper
!WallpaperChanger -s purple > /dev/null
```

The directory tree of said profile:
```
 unix.profile
 unix
├──  hypr
│   ├──  hyprland.conf
│   ├──  hyprlock.conf
│   ├──  hyprpaper.conf
│   └──  include
│       ├──  aesthetic.conf
│       ├──  animations.conf
│       ├──  autostart.conf
│       ├──  binds.conf
│       ├──  input.conf
│       ├──  layout.conf
│       └──  windowrules.conf
├──  kitty
│   ├──  current-theme.conf
│   └──  kitty.conf
├──  rofi
│   ├──  applets
│   │   └──  colors.rasi
│   ├──  colors
│   │   └──  darkpride.rasi
│   └──  launchers
│       └──  type-1
│           └──  colors.rasi
└──  waybar
    ├──  config
    ├──  default-modules.json
    └──  style.css
```
