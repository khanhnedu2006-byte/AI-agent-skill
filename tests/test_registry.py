import pytest
import os
import tempfile
from skill_registry import SkillRegistry

# --- Setup: tạo skills giả để test ---
@pytest.fixture
def temp_skills_dir():
    """Tạo thư mục skills tạm thời cho mỗi test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Tạo skill hợp lệ
        skill_dir = os.path.join(tmpdir, "calculator")
        os.makedirs(skill_dir)
        with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: calculator\ndescription: Use for math.\n---\n\n# Calculator\nDo math.")

        # Tạo skill thứ 2
        skill_dir2 = os.path.join(tmpdir, "weather")
        os.makedirs(skill_dir2)
        with open(os.path.join(skill_dir2, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: weather\ndescription: Use for weather.\n---\n\n# Weather\nFake weather.")

        # Tạo folder không có SKILL.md (phải bị bỏ qua)
        os.makedirs(os.path.join(tmpdir, "empty_folder"))

        yield tmpdir

# --- Tests ---
def test_list_skills_returns_list(temp_skills_dir):
    """list_skills() phải trả về list."""
    registry = SkillRegistry(temp_skills_dir)
    result = registry.list_skills()
    assert isinstance(result, list)

def test_list_skills_correct_count(temp_skills_dir):
    """list_skills() chỉ đếm folder có SKILL.md, bỏ qua folder rỗng."""
    registry = SkillRegistry(temp_skills_dir)
    result = registry.list_skills()
    assert len(result) == 2

def test_list_skills_has_name_and_description(temp_skills_dir):
    """Mỗi skill phải có key 'name' và 'description'."""
    registry = SkillRegistry(temp_skills_dir)
    result = registry.list_skills()
    for skill in result:
        assert "name" in skill
        assert "description" in skill

def test_list_skills_correct_values(temp_skills_dir):
    """Giá trị name và description phải đúng với YAML frontmatter."""
    registry = SkillRegistry(temp_skills_dir)
    result = registry.list_skills()
    names = [s["name"] for s in result]
    assert "calculator" in names
    assert "weather" in names

def test_get_skill_content_returns_string(temp_skills_dir):
    """get_skill_content() phải trả về string."""
    registry = SkillRegistry(temp_skills_dir)
    content = registry.get_skill_content("calculator")
    assert isinstance(content, str)

def test_get_skill_content_has_frontmatter(temp_skills_dir):
    """Content phải chứa YAML frontmatter."""
    registry = SkillRegistry(temp_skills_dir)
    content = registry.get_skill_content("calculator")
    assert content.startswith("---")

def test_get_skill_content_not_found(temp_skills_dir):
    """Skill không tồn tại phải raise FileNotFoundError."""
    registry = SkillRegistry(temp_skills_dir)
    with pytest.raises(FileNotFoundError):
        registry.get_skill_content("nonexistent_skill")