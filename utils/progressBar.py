import sys
import time

class ProgressBar:
    def __init__(self, total, length=40, prefix=""):
        self.total = total
        self.length = length
        self.prefix = prefix
        self.count = 0
        self.last_update = time.time()

    def update(self, step=1):
        self.count += step
        self._print_bar()

    def _print_bar(self):
        ratio = self.count / self.total
        filled = int(ratio * self.length)
        bar = "█" * filled + "-" * (self.length - filled)

        sys.stdout.write(
            f"\r{self.prefix} [{bar}] {self.count}/{self.total} ({ratio*100:.1f}%)"
        )
        sys.stdout.flush()

        if self.count == self.total:
            sys.stdout.write("\n")

    def finish(self):
        self.count = self.total
        self._print_bar()
