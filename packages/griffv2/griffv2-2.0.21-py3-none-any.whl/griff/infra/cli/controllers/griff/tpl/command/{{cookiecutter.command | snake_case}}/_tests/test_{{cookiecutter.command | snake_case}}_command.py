from typing import Type

from griff.runtime.factories.abstract_runtime_factory import Injectables
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.command_handler_testcase import CommandHandlerTestCase

from {{ cookiecutter.context | snake_case }}.{{ cookiecutter.command | snake_case }}.{{ cookiecutter.command | snake_case }}_command import ({{ cookiecutter.command | pascal_case }}Handler, {{ cookiecutter.command | pascal_case }}Command)
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_repository import {{cookiecutter.aggregate | pascal_case}}Repository, {{cookiecutter.aggregate | pascal_case}}FakeRepository
from {{ cookiecutter.context | snake_case }}._common.repositories.{{ cookiecutter.aggregate | snake_case }}_persistence import {{cookiecutter.aggregate | pascal_case}}Persistence, {{cookiecutter.aggregate | pascal_case}}FakePersistence
from {{ cookiecutter.context | snake_case }}._common.test_utils.{{ cookiecutter.context | snake_case }}_dtf import {{ cookiecutter.context | pascal_case }}Dtf

class Test{{ cookiecutter.command | pascal_case }}Command(CommandHandlerTestCase):
    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().with_context_fake_persistence("{{ cookiecutter.context | snake_case }}")

    @property
    def handler_class(self) -> Type[{{ cookiecutter.command | pascal_case }}Handler]:
        return {{ cookiecutter.command | pascal_case }}Handler

    @classmethod
    def with_injectables(cls) -> Injectables | None:
        return None

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.dtf = {{ cookiecutter.context | pascal_case }}Dtf(start_id=99990)
        cls.repository = cls.get_injected({{cookiecutter.aggregate | pascal_case}}Repository)
        cls.command = {{ cookiecutter.command | pascal_case }}Command()

    def setup_method(self):
        super().setup_method()
        self.dtf.reset(1)

    async def async_setup(self):
        await super().async_setup()
        self.repository.reset()
        await self.init_persistence()

    async def init_persistence(self):
        await self.dtf.persist(self.repository, [])

    """
    handle
    """

    async def test_{{ cookiecutter.command | snake_case }}_avec_un_pb_echoue(self):
        command = self.command.model_copy(update={"un_attr": "une valeur qui fait échoué"})
        response = await self.handler.handle(command)
        self.assert_equals_resultset(response.model_dump())

    async def test_{{ cookiecutter.command | snake_case }}_reussi(self):
        response = await self.handler.handle(self.command)
        self.assert_equals_resultset(
            self.prepare_success_resultset(response, self.repository)
        )

