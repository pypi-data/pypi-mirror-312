import logging
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from fastmcp.resources import FileResource, FunctionResource, ResourceManager


@pytest.fixture
def temp_file():
    """Create a temporary file for testing.

    File is automatically cleaned up after the test if it still exists.
    """
    content = "test content"
    with NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(content)
        path = Path(f.name).resolve()
    yield path
    try:
        path.unlink()
    except FileNotFoundError:
        pass  # File was already deleted by the test


@pytest.fixture
def temp_file_no_cleanup():
    """Create a temporary file for testing.

    File is NOT automatically cleaned up - tests must handle cleanup.
    """
    content = "test content"
    with NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(content)
        path = Path(f.name).resolve()
    return path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with TemporaryDirectory() as d:
        yield Path(d).resolve()


class TestResourceValidation:
    def test_resource_uri_validation(self):
        def dummy_func() -> str:
            return "data"

        # Valid URI
        resource = FunctionResource(
            uri="http://example.com/data",
            name="test",
            func=dummy_func,
        )
        assert str(resource.uri) == "http://example.com/data"

        # Missing protocol
        with pytest.raises(ValueError, match="Input should be a valid URL"):
            FunctionResource(
                uri="invalid",
                name="test",
                func=dummy_func,
            )

        # Missing host
        with pytest.raises(ValueError, match="Input should be a valid URL"):
            FunctionResource(
                uri="http://",
                name="test",
                func=dummy_func,
            )


class TestResourceManagerAdd:
    """Test ResourceManager add functionality."""

    def test_add_file_resource(self, temp_file: Path):
        """Test adding a file resource."""
        manager = ResourceManager()
        resource = FileResource(
            uri=f"file://{temp_file}",
            name="test",
            description="test file",
            mime_type="text/plain",
            path=temp_file,
        )
        added = manager.add_resource(resource)
        assert isinstance(added, FileResource)
        assert str(added.uri) == f"file://{temp_file}"
        assert added.name == "test"
        assert added.description == "test file"
        assert added.mime_type == "text/plain"
        assert added.path == temp_file

    def test_add_file_resource_relative_path_error(self):
        """Test ResourceManager rejects relative paths."""
        with pytest.raises(ValueError, match="Path must be absolute"):
            FileResource(
                uri="file:///test.txt",
                name="test",
                path=Path("test.txt"),
            )

    def test_warn_on_duplicate_resources(self, caplog):
        """Test warning on duplicate resources."""
        caplog.set_level(logging.WARNING, logger="mcp")
        manager = ResourceManager()
        resource = FileResource(
            uri="file:///test.txt",
            name="test",
            path=Path("/test.txt"),
        )
        manager.add_resource(resource)
        manager.add_resource(resource)
        assert "Resource already exists: file:///test.txt" in caplog.text

    def test_disable_warn_on_duplicate_resources(self, caplog):
        """Test disabling warning on duplicate resources."""
        caplog.set_level(logging.WARNING, logger="mcp")
        manager = ResourceManager()
        resource = FileResource(
            uri="file:///test.txt",
            name="test",
            path=Path("/test.txt"),
        )
        manager.add_resource(resource)
        manager.warn_on_duplicate_resources = False
        manager.add_resource(resource)
        assert "Resource already exists: file:///test.txt" not in caplog.text


class TestResourceManagerRead:
    """Test ResourceManager read functionality."""

    def test_get_resource_unknown_uri(self):
        """Test getting a non-existent resource."""
        manager = ResourceManager()
        with pytest.raises(ValueError, match="Unknown resource"):
            manager.get_resource("file://unknown")

    def test_get_resource(self, temp_file: Path):
        """Test getting a resource by URI."""
        manager = ResourceManager()
        resource = FileResource(
            uri=f"file://{temp_file}",
            name="test",
            path=temp_file,
        )
        added = manager.add_resource(resource)
        retrieved = manager.get_resource(added.uri)
        assert retrieved == added

    async def test_resource_read_through_manager(self, temp_file: Path):
        """Test reading a resource through the manager."""
        manager = ResourceManager()
        resource = FileResource(
            uri=f"file://{temp_file}",
            name="test",
            path=temp_file,
        )
        added = manager.add_resource(resource)
        retrieved = manager.get_resource(added.uri)
        assert retrieved is not None
        content = await retrieved.read()
        assert content == "test content"

    async def test_resource_read_error_through_manager(
        self, temp_file_no_cleanup: Path
    ):
        """Test error handling when reading through manager."""
        manager = ResourceManager()
        # Create resource while file exists
        resource = FileResource(
            uri=f"file://{temp_file_no_cleanup}",
            name="test",
            path=temp_file_no_cleanup,
        )
        added = manager.add_resource(resource)
        retrieved = manager.get_resource(added.uri)
        assert retrieved is not None

        # Delete file and verify read fails
        temp_file_no_cleanup.unlink()
        with pytest.raises(FileNotFoundError):
            await retrieved.read()


class TestResourceManagerList:
    """Test ResourceManager list functionality."""

    def test_list_resources(self, temp_file: Path):
        """Test listing all resources."""
        manager = ResourceManager()
        resource = FileResource(
            uri=f"file://{temp_file}",
            name="test",
            path=temp_file,
        )
        added = manager.add_resource(resource)
        resources = manager.list_resources()
        assert len(resources) == 1
        assert resources[0] == added

    def test_list_resources_duplicate(self, temp_file: Path):
        """Test that adding the same resource twice only stores it once."""
        manager = ResourceManager()
        resource = FileResource(
            uri=f"file://{temp_file}",
            name="test",
            path=temp_file,
        )
        resource1 = manager.add_resource(resource)
        resource2 = manager.add_resource(resource)

        resources = manager.list_resources()
        assert len(resources) == 1
        assert resources[0] == resource1
        assert resource1 == resource2

    def test_list_multiple_resources(self, temp_file: Path, temp_file_no_cleanup: Path):
        """Test listing multiple different resources."""
        manager = ResourceManager()
        resource1 = FileResource(
            uri=f"file://{temp_file}",
            name="test1",
            path=temp_file,
        )
        resource2 = FileResource(
            uri=f"file://{temp_file_no_cleanup}",
            name="test2",
            path=temp_file_no_cleanup,
        )
        added1 = manager.add_resource(resource1)
        added2 = manager.add_resource(resource2)

        resources = manager.list_resources()
        assert len(resources) == 2
        assert resources[0] == added1
        assert resources[1] == added2
        assert added1 != added2
