import pytest
from pathlib import Path
from uv_workspace_dynamic_versioning.vendored import schemas
from uv_workspace_dynamic_versioning.vendored.main import get_version, patch_version_for_directory
from uv_workspace_dynamic_versioning.vendored.metadata_hook import DependenciesMetadataHook
from dunamai import Version

def test_config_parsing():
    data = {
        "vcs": "git",
        "pattern": "v(?P<base>.*)",
        "bump": {"enable": True, "index": 1},
        "from-file": {"source": "VERSION", "pattern": "v(.*)"}
    }
    config = schemas.UvWorkspaceDynamicVersioning.from_dict(data)
    assert config.vcs.value == "git"
    assert config.pattern == "v(?P<base>.*)"
    assert config.bump_config.enable is True
    assert config.bump_config.index == 1
    assert config.from_file.source == "VERSION"
    assert config.from_file.pattern == "v(.*)"

def test_metadata_hook_config():
    data = {
        "dependencies": ["pkg1 == {{ version.base }}", "pkg2"],
        "optional-dependencies": {
            "dev": ["pytest"]
        }
    }
    config = schemas.MetadataHookConfig.from_dict(data)
    assert config.dependencies == ["pkg1 == {{ version.base }}", "pkg2"]
    assert config.optional_dependencies["dev"] == ["pytest"]

def test_patch_version_for_directory(tmp_path, mocker):
    # Mock subprocess to simulate git commands
    mocker.patch("subprocess.check_output", side_effect=[
        "1\n", # rev-list distance (1 line = 1 commit)
        "abcdef1234567890\n", # log commit hash
        "M file.py\n" # status (dirty)
    ])
    
    v = Version("0.1.0", distance=5, commit="initial", dirty=False)
    # We need to set _matched_tag for the logic to use the first branch of the if/else
    v._matched_tag = "v0.1.0"
    
    patched = patch_version_for_directory(v, tmp_path)
    
    assert patched.distance == 1
    assert patched.commit == "abcdef1"
    assert patched.dirty is True

def test_get_version_bypass(mocker):
    mocker.patch("os.environ.get", return_value="1.2.3")
    config = schemas.UvWorkspaceDynamicVersioning()
    version_str, v = get_version(config, Path("."))
    assert version_str == "1.2.3"
    assert v.base == "1.2.3"

def test_metadata_hook_update_validation(mocker):
    hook = DependenciesMetadataHook(str(Path(".")), {})
    
    # Test missing dynamic field
    with pytest.raises(ValueError, match="not listed in 'project.dynamic'"):
        hook.update({})
    
    # Test dependency already in project
    metadata = {"dynamic": ["dependencies"], "dependencies": ["req1"]}
    with pytest.raises(ValueError, match="'dependencies' is dynamic but already listed"):
        hook.update(metadata)

def test_metadata_hook_rendering(mocker):
    mocker.patch("uv_workspace_dynamic_versioning.vendored.metadata_hook.get_version", 
                 return_value=("0.2.0", Version("0.2.0")))
    
    config = {
        "dependencies": ["pkg == {{ version.base }}"]
    }
    hook = DependenciesMetadataHook(str(Path(".")), config)
    
    metadata = {"dynamic": ["dependencies"]}
    hook.update(metadata)
    
    assert metadata["dependencies"] == ["pkg == 0.2.0"]
