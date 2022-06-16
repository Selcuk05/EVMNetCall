class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

    def disable(self):
        self.HEADER = ""
        self.OKBLUE = ""
        self.OKGREEN = ""
        self.WARNING = ""
        self.FAIL = ""
        self.ENDC = ""


def success(text: str):
    return Colors.OKGREEN + text + Colors.ENDC


def fail(text: str):
    return Colors.FAIL + text + Colors.ENDC


def warn(text: str):
    return Colors.WARNING + text + Colors.ENDC


def inpexit():
    input("Press ENTER to exit\n")
    exit()
