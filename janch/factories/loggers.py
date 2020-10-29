from abc import ABC


class Logger(ABC):

    @staticmethod
    def type() -> str:
        raise NotImplementedError("Return a type string that acts as the name for the logger")

    async def main(self, message) -> bool:
        raise NotImplementedError("Implement this method to log the message")

    async def log(self, message):
        return await self.main(message)


class CLILogger(Logger):
    """Logs to command line"""

    @staticmethod
    def type() -> str:
        return 'cli'

    async def main(self, message):
        print(message)

        return True


def get_default_loggers():
    loggers = [CLILogger]

    return {l.type(): l for l in loggers}
