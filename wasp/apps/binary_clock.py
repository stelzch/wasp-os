import wasp
from micropython import const

SCREEN_WIDTH = const(240)
DISTANCE = const(35)
ON_COLOR = const(0xf800)
OFF_COLOR = const(0x528a)
BLOCK_MARGIN = const(5)
BLOCK_SIZE = const(25)
OFFSET = const(BLOCK_SIZE + BLOCK_MARGIN)
NUM_DIGITS_HOUR = const(4)
NUM_DIGITS_MINUTE = const(6)
NUM_DIGITS_SECOND = const(6)
WIDTH_HOUR = const(NUM_DIGITS_HOUR * OFFSET - BLOCK_MARGIN)
WIDTH_MINUTE = const(NUM_DIGITS_MINUTE * OFFSET - BLOCK_MARGIN)
WIDTH_SECOND = const(WIDTH_MINUTE)
X_HOUR = const((SCREEN_WIDTH - WIDTH_HOUR) // 2)
Y_HOUR = const(120 - 30 - BLOCK_SIZE // 2)
X_MINUTE = const((SCREEN_WIDTH - WIDTH_MINUTE) // 2)
Y_MINUTE = const(120 - BLOCK_SIZE // 2)
X_SECOND = const(X_MINUTE)
Y_SECOND = const(120 + 30 - BLOCK_SIZE // 2)

class BinaryClockApp():
    NAME = "Binary"

    def __init__(self):
        self.current_time = self.binary_time()

    def foreground(self):
        wasp.system.bar.clock = False
        self._draw(refresh=False)
        wasp.system.request_tick(1000)

    def binary_time(self):
        now = wasp.watch.rtc.get_localtime()
        hour = now[3]
        minute = now[4]
        second = now[5]
        if hour >= 13:
            hour -= 12
        binary_hour = [(hour >> i) & 1 for i in reversed(range(NUM_DIGITS_HOUR))]
        binary_minute = [(minute >> i) & 1 for i in reversed(range(NUM_DIGITS_MINUTE))]
        binary_second = [(second >> i) & 1 for i in reversed(range(NUM_DIGITS_SECOND))]
        return (binary_hour, binary_minute, binary_second)

    def sleep(self):
        return True

    def tick(self, ticks):
        self._draw(refresh=True)

    def wake(self):
        self._draw()

    def preview(self):
        """Provide a preview for the watch face selection."""
        wasp.system.bar.clock = False
        self._draw(False)

    def _draw_number(self, refresh, prev, now, x, y, num_digits):
        draw = wasp.watch.drawable
        for i in range(num_digits):
            changed = (prev[i] != now[i])
            if refresh and not changed:
                continue
            color = ON_COLOR if now[i] == 1 else OFF_COLOR
            draw.fill(bg=color,
                    x=x + i * OFFSET, y=y, w=BLOCK_SIZE, h=BLOCK_SIZE)


    def _draw(self, refresh=True):
        draw = wasp.watch.drawable

        if not refresh:
            draw.fill()
            wasp.system.bar.draw()

        hour, minute, second = self.binary_time()

        self._draw_number(refresh, self.current_time[0],
                hour, X_HOUR, Y_HOUR, NUM_DIGITS_HOUR)
        self._draw_number(refresh, self.current_time[1],
                minute, X_MINUTE, Y_MINUTE, NUM_DIGITS_MINUTE)
        self._draw_number(refresh, self.current_time[2],
                second, X_SECOND, Y_SECOND, NUM_DIGITS_SECOND)

        self.current_time = (hour, minute, second)

