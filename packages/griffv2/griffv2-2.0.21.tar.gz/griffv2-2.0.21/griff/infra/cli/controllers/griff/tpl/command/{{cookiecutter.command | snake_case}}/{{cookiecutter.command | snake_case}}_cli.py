import typer
from griff.appli.command.command_bus import CommandBus
from griff.infra.cli.cli_controller import CliController
from griff.infra.cli.register_cli_command import register_cli_command
from griff.infra.cli.typer_print import TyperPrint
from griff.utils.async_utils import AsyncUtils
from injector import inject

from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_command import {{ cookiecutter.command | pascal_case }}Command


class {{ cookiecutter.command | pascal_case }}CliController(CliController):
    @inject
    def __init__(self, command_bus: CommandBus):
        super().__init__()
        self._command_bus = command_bus

    def get_command_name(self):
        return "{{ cookiecutter.aggregate | snake_case }}"

    async def _dispatch_command(self, nom: str, rang: int):
        command = {{ cookiecutter.command | pascal_case }}Command(nom=nom, rang=rang)
        response = await self._command_bus.dispatch(command)
        if response.is_success:
            return response
        TyperPrint.error(f"Echec action : {response.error.message}")
        raise typer.Exit()

    @register_cli_command(name="action")
    def action(self):
        p = {}
        response = AsyncUtils.async_to_sync(self._dispatch_command, p)
        if response.is_success:
            TyperPrint.success("Action terminée")
