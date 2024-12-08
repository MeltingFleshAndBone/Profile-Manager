import os

class profile:
    '''
    Structure of a .profile file:
    # Comments
    
    # @ is a option prefix
    # You can use it to set some values for the profile
    # @Tag:Tagname sets a tag, to add more than 1, separate them with a comma
    @Tag:TagName,TagName2,TagName3
    # @Theme:ThemeName sets the theme, only a single theme is allowed
    @Theme:ThemeName
    # @Desc:Description sets the description for the profile
    @Desc:Description
    # @Priority: Priority sets the priority for the profile, i.e. the order in which they are listed
    # Priority should be an integer
    @Priority:Priority
    # NOTE: The color of the profile name is changed based on the priority
    # NOTE: If priority is negative, it is hidden

    # Commands are prefixed with !, the script will execute them
    !Command to be executed

    # For configuration linking, the line should start with a colon
    # The source and target are separated by a colon
    # the source should be located at profile_path/profile_name/
    :source:target
    '''
    def __init__(self, name:str, tags:list[str], description:str, path:str, theme:str, priority:int, number_of_commands:int, number_of_links:int):
        self.name:str = name                    # Name of the profile (e.g. "default", "work", "home", etc)
        self.tags:list[str] = tags              # List of tags associated with the profile
        self.description:str = description      # Description of the profile
        self.path:str = path                    # Full path to the profile (based on '~')
        self.theme:str = theme                  # Theme of the profile (Currently does nothing)
        self.priority:int = priority            # Priority of the profile
        # A bunch of useless info
        self.number_of_commands:int = number_of_commands         # Number of commands in the profile
        self.number_of_links:int = number_of_links               # Number of links in the profile

class profile_manager:
    ''' Manages the profiles

    - list_profiles prints the contents of the profile folder
    - set_profile sets the profile
    - get_profile gets a list of all the profiles
    '''
    def __init__(self):
        self.profile_path:str           # Full path to the profiles folder
        
    def checks(self) -> int:
        ''' Checks if the profile_path and config_path exist
        '''
        self.profile_path = os.path.expanduser(self.profile_path)

        if not os.path.exists(self.profile_path):
            print("\033[91mProfile path does not exist\033[0m")
            return 1

        return 0

    def list_profiles(self, tags:list[str], list_hidden:bool=False) -> int:
        ''' Prints the contents of the profile folder
        '''
        profile_list = self.get_profile()

        print("\033[92mProfiles:\033[0m")
        print("\033[90m" + "-" * 20 + "\033[0m")
        if list_hidden:
            print_list = sorted([profile for profile in profile_list if any(tag in profile.tags for tag in tags)], key=lambda x: x.priority, reverse=True)
        else:
            print_list = sorted([profile for profile in profile_list if any(tag in profile.tags for tag in tags) and profile.priority >= 0], key=lambda x: x.priority, reverse=True)
        if len(tags) == 0:
            if list_hidden:
                print_list = sorted(profile_list, key=lambda x: x.priority, reverse=True)
            else:
                print_list = sorted([profile for profile in profile_list if profile.priority >= 0], key=lambda x: x.priority, reverse=True)

        if print_list == []:
            # No profiles found
            print("\033[91mNo profiles found\033[0m")
        for profile in print_list:
            # Print the name, tags, theme, and description
            profile_name = profile.name.replace('.profile', '')
            if profile.priority == 0 or profile.priority == 1:
                color = "\033[32m"
            elif profile.priority == 2:
                color = "\033[33m"
            elif profile.priority >= 3:
                color = "\033[31m"
            print(color + "Name:\033[0m " + profile_name)
            print(color + "Tags:\033[0m " + ", ".join(profile.tags))
            if profile.theme != "":
                print(color + "Theme:\033[0m " + profile.theme)
            if profile.description != "":
                print(color + "Description:\033[0m " + profile.description)
            print(color + "Number of commands:\033[0m " + str(profile.number_of_commands))
            print(color + "Number of links:\033[0m " + str(profile.number_of_links))
            print(color + "Priority:\033[0m " + str(profile.priority))
            print("\033[90m" + "-" * 20 + "\033[0m")

        return 0

    def set_profile(self, profile_name:str, dryrun:bool, force:bool, current:bool) -> int:
        '''
        Sets the profile
        Runs the commands in the profile
        Creates the symlinks

        If dryrun is set it will only print what would happen

        NOTE:
        Does not use the get_profile method
        Ignores tags
        '''
        if current:
            current_profile_path = os.path.join(self.profile_path, ".current")
            if os.path.exists(current_profile_path):
                with open(current_profile_path, 'r') as f:
                    profile_name = f.readline().strip()
            else:
                print("\033[91mNo current profile set\033[0m")
                return 1

        if not os.path.exists(os.path.join(self.profile_path, profile_name + ".profile")):
            print("\033[91mProfile does not exist\033[0m")
            return 1

        with open(os.path.join(self.profile_path, profile_name + ".profile")) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                if line.startswith("@"):
                    continue
                elif line.startswith("!"):
                    if dryrun:
                        print("\033[92mCommand: \033[0m" + line[1:])
                        continue
                    else:
                        print("\033[92mCommand: \033[0m" + line[1:])
                        os.system(line[1:])
                        continue
                elif line.startswith(":"):
                    src, dst = line[1:].strip().split(":")
                    dst_full_path = os.path.expanduser(dst)
                    src_full_path = os.path.join(self.profile_path, profile_name, src)
                    if os.path.exists(dst_full_path):
                        if os.path.samefile(dst_full_path, src_full_path):
                            print("\033[93mTarget \033[0m" + dst + " \033[93mis the same as \033[0m" + src + ", \033[93mskipping\033[0m")
                            continue
                        if dryrun:
                            print("\033[91mWould overwrite: \033[0m" + dst_full_path)
                            continue
                        if force:
                            print("\033[91mTarget exists, overwriting\033[0m")
                            os.remove(dst_full_path)
                        else:
                            print("\033[91mTarget exists, skipping\033[0m")
                            continue
                    if dryrun:
                        print("\033[92mSymlink: \033[0m" + src_full_path + " -> " + dst)
                        continue
                    else:
                        print("\033[92mSymlink: \033[0m" + src_full_path + " -> " + dst)
                        os.symlink(src_full_path, os.path.expanduser(dst))
                        continue

        with open(os.path.join(self.profile_path, ".current"), 'w') as f:
            f.write(f"{profile_name}\n")

        return 0

    def get_profile(self) -> list[profile]:
        ''' Gets every profile at profile_path
        reads the .profile and initializes a list of type profile
        '''
        profile_list: list[profile] = []
        for filename in os.listdir(self.profile_path):
            file_path = os.path.join(self.profile_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".profile"):
                with open(file_path, 'r') as f:
                    tags = ["General"]
                    description = ""
                    theme = ""
                    priority = 0
                    number_of_commands = 0
                    number_of_links = 0
                    for line in f:
                        if line.startswith('@Tag:'):
                            tags = line[5:].strip().split(',')
                        elif line.startswith('@Theme:'):
                            theme = line[7:].strip()
                        elif line.startswith('@Desc:') or line.startswith('@Description:'):
                            description += line[6:].strip()
                        elif line.startswith('@Priority:'):
                            priority = int(line[10:].strip())
                            if priority < 0:
                                priority = -1
                        elif line.startswith('!'):
                            number_of_commands += 1
                        elif line.startswith(':'):
                            number_of_links += 1

                    profile_list.append(profile(name=filename, tags=tags, description=description, path=file_path, theme=theme, priority=priority, number_of_commands=number_of_commands, number_of_links=number_of_links))

        # Sort by priority
        profile_list.sort(key=lambda x: x.priority)
        return profile_list
