from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Digits, Header, Footer
from desktop_notifier import DesktopNotifier

SESSION_TYPES = {
    "work": 25 * 60,
    "break": 5 * 60,
    "long_break": 15 * 60,
}


class TomatiaApp(App):
    """A dead simple pomodoro app for the terminal made with textual."""

    TITLE = "tomatia"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
        ("s", "toggle_timer", "Start/Stop"),
        ("space", "toggle_timer", "Start/Stop"),
        ("r", "reset", "Reset"),
    ]

    CSS = """
    Screen {
        align: center middle;
    }

    #timer {
        width: auto;
    }
    """

    ticking: reactive[bool] = reactive(True)
    current_session: reactive[str] = reactive("work", always_update=True)
    sets: reactive[int] = reactive(0)
    remaining_time: reactive[int] = reactive(SESSION_TYPES["work"])

    notifier = DesktopNotifier(
        app_name="tomatia",
        notification_limit=5,
    )

    def compose(self) -> ComposeResult:
        yield Header(icon="🍅", show_clock=True)
        yield Digits(self.format_time(self.remaining_time), id="timer")
        yield Footer()

    def on_mount(self) -> None:
        self.clock = self.query_one(Digits)
        self.header = self.query_one(Header)
        self.timer_interval = self.set_interval(1, self.update_timer, pause=True)

    def action_toggle_timer(self) -> None:
        self.ticking = not self.ticking

    def action_reset(self) -> None:
        self.ticking = False
        self.sets = 0

        self.current_session = "work"

        self.timer_interval.reset()
        self.clock.update(self.format_time(SESSION_TYPES["work"]))

    def format_time(self, seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    async def watch_ticking(self, new_value: bool) -> None:
        if not new_value:
            self.timer_interval.pause()
            return

        self.timer_interval.resume()

    async def watch_current_session(self, new_session: str) -> None:
        self.remaining_time = SESSION_TYPES[new_session]
        self.clock.update(self.format_time(self.remaining_time))

        if new_session == "work":
            self.header.icon = "🍅"
        elif new_session == "break":
            self.header.icon = "🍪"
        else:
            self.header.icon = "☕"

    async def update_timer(self) -> None:
        if self.ticking and self.remaining_time > 0:
            self.remaining_time -= 1
            self.clock.update(self.format_time(self.remaining_time))
        elif self.remaining_time == 0:
            self.ticking = False

            if self.current_session == "work":
                self.sets += 1

                if self.sets % 4 == 0:
                    self.current_session = "long_break"
                    await self.notifier.send(
                        title="Time to Unwind!",
                        message="You've completed four sessions! Step away and give yourself a moment to breathe.",
                    )
                else:
                    self.current_session = "break"
                    await self.notifier.send(
                        title="Quick refresh!",
                        message="You've done great! Take a short break to stretch and recharge.",
                    )
            else:
                self.current_session = "work"
                await self.notifier.send(
                    title="Focus time!",
                    message="It's time to get back to work!",
                )

            self.ticking = True


def main():
    app = TomatiaApp()
    app.run()


if __name__ == "__main__":
    main()
