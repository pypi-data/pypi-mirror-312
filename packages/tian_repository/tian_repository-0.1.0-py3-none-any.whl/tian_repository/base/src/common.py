from typing import Any, AnyStr, NoReturn, Type
from uuid import UUID

from tian_core import BuilderError


def handle_extra_types(value: Any, key: str = "") -> Any:
    """Convert unhandled types to a default value.
    :param value: Value to be converted
    :return Any: converted value
    """
    if key == 'id' or key == 'uuid':
        if (isinstance(value, str) and value == "") or (isinstance(value, int) and value == 0):
            return None
    if isinstance(value, UUID):
        return str(value)

    return value


def check_builder_requirements(
    operation: AnyStr, entity_name: AnyStr, entity_type: Type
) -> NoReturn:
    """Validate if there is a configured default table and base model to
    execute predefined query builder.

    :param operation: Operation name that is being evaluated.
    :param entity_name: Name of the related entity on DB.
    :param entity_type: Type definition of the related model.

    :raise RepositoryBuilderError: If default table is None
    """

    if entity_name is None:
        raise BuilderError(
            f"Can't perform {operation} action without a default table. "
            "Please override the method.",
        )

    if entity_type is None:
        raise BuilderError(
            f"Can't perform {operation} action without a default base model. "
            "Please override the method.",
        )
