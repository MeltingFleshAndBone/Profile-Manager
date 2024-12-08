import argparse
from mod import utils

def main() -> int: 
    args: argparse.Namespace = init_args()
    
    if args.help:
        print_help()
        return 0
    
    dryrun: bool = False 
    force: bool = False
    list_hidden: bool = False
    current: bool = False

    profile_mgr = utils.profile_manager()
    profile_mgr.profile_path = "~/.config/profiles"

    if profile_mgr.checks() != 0:
        return 1

    if args.dry_run:
        dryrun = True
    if args.force:
        force = True
    if args.list_hidden:
        list_hidden = True
    if args.current:
        current = True

    if args.profile or current:
        profile_mgr.set_profile(args.profile if args.profile else "", dryrun, force, current)
        return 0
    elif args.list:
        tags = args.list.split(",")
        profile_mgr.list_profiles(tags)
        return 0
    elif args.list == None:
        profile_mgr.list_profiles([], list_hidden)
        return 0

    return 0


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Profile Manager",
        description="Manages linux profiles",
        add_help=False,
    )

    parser.add_argument(
        "-p", "--profile",
        required=False,
    )

    parser.add_argument(
        "-c", "--current",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "-d", "--dry_run",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "-l", "--list",
        nargs="?",
        default=None,
        required=False,
    )

    parser.add_argument(
        "-lh", "--list_hidden",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "-f", "--force",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true",
        required=False,
    )

    return parser.parse_args()

def print_help() -> None:
    # Peak efficiency 
    print("\033[92mProfile Manager Help:\033[0m")
    print("\033[94mUsage:\033[0m")
    print("  profile_manager [options]")
    print("\033[94mOptions:\033[0m")
    print("  \033[93m-p,  --profile PROFILE_NAME\033[0m \t Specify the profile to set.")
    print("  \033[93m-c,  --current\033[0m \t\t Use the current profile.")
    print("  \033[93m-d,  --dry_run\033[0m \t\t Perform a dry run without making changes.")
    print("  \033[93m-l,  --list (TAGS)\033[0m \t\t List profiles with specified tags.")
    print("  \033[93m-lh, --list_hidden\033[0m \t\t Include hidden profiles in the list.")
    print("  \033[93m-f,  --force\033[0m \t\t\t Force overwrite existing symlinks.")
    print("  \033[93m-h,  --help\033[0m \t\t\t Display this help message.")
    print("\033[94mDescription:\033[0m")
    print("  This tool manages Linux profiles, allowing you to set environment variables,")
    print("  run commands, and create symlinks based on profile specifications.")
    print("  Profiles are stored in the profiles folder with a .profile extension.")
    print("\033[94mExamples:\033[0m")
    print("  \033[93mprofile_manager -p work\033[0m")
    print("     Sets the 'work' profile, executing associated commands.")
    print("  \033[93mprofile_manager -l\033[0m")
    print("     Lists all available profiles with their tags.")
    print("  \033[93mprofile_manager -p default -d\033[0m")
    print("     Performs a dry run for setting the 'default' profile.")
    print("  \033[93mprofile_manager -lh\033[0m")
    print("     Lists all profiles, including hidden ones.")
    print("\033[94mNote:\033[0m")
    print("  For more information about writing profiles, check the GitHub page.")

if __name__ == "__main__":
    main()

