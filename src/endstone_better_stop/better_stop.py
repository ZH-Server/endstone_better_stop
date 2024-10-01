import time
from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

class BetterStop(Plugin):
    api_version = "0.5"

    def __init__(self):
        super().__init__()
        self.default_stop_msg: str = ""

    commands = {
        "bs": {
            "description": "Better stop command",
            "usages": ["/bs <after_time: int> [reason: message]"],
            "permissions": ["better_stop.command.bs"],
        },
    }

    permissions = {
        "better_stop.command.bs": {
            "description": "Allow users to use the /bs command.",
            "default": "op",
        },
    }

    def on_enable(self) -> None:
        self.save_default_config()
        self.load_config()

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "bs":
            if int(args[0]) <= 0:
                sender.send_error_message("You should provide a number above 0!")
            else:
                reason=str(args[1])
                op_name=sender.name
                arg_second=int(args[0])
                if len(reason) <= 0:
                    self.server.broadcast_message(f"{self.default_stop_msg}")
                    self.logger.info(f"§e{sender.name}§r request to stop server with §ano reason§r at §b{time.asctime( time.localtime(time.time()) )}§r after §b{int(args[0])}s§r")
                    self.server.scheduler.run_task(self, self.server.shutdown, delay=int(args[0])*20)
                else:
                    self.server.broadcast_message(reason)
                    self.logger.info(f"§e{sender.name}§r request to stop server with §a\"{reason}\" as reason§r at §b{time.asctime( time.localtime(time.time()) )}§r after §b{int(args[0])}s§r")
                    self.server.scheduler.run_task(self, self.server.shutdown, delay=int(args[0])*20)
        return True

    def load_config(self) -> None:
        self.default_stop_msg = self.config["default_stop_msg"]