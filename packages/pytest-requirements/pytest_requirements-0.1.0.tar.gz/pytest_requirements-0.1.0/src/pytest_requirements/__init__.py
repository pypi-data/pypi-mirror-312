"""pytest plugin providing markers to link tests to requirements and usecases."""

from ._version import __version__


def pytest_configure(config):
    """Register our custom markers."""
    config.addinivalue_line(
        "markers",
        "verifies_requirement(requirement_id): Mark this test as verification for a requirement",
    )
    config.addinivalue_line(
        "markers",
        "verifies_usecase(usecase_id): Mark this test as verification for a usecase",
    )


def pytest_collection_modifyitems(session, config, items):
    """Customize test collection.

    - Make sure requirement/usecase marker information is written to junit xml.
    """
    for item in items:
        for type_ in ("requirement", "usecase"):
            for marker in item.iter_markers(name=f"verifies_{type_}"):
                item.user_properties.append((f"{type_}_id", marker.args[0]))


__all__ = [
    "__version__",
]
