from typer.testing import CliRunner
from model_hallucination.cli import app

runner = CliRunner()

def test_evaluate_prompt():
    result = runner.invoke(app, ["evaluate-prompt", "--prompt", "Who discovered gravity?", "--model-output", "Isaac Newton", "--api-key", "test-key"])
    assert result.exit_code == 0
    assert "Hallucination Score" in result.output
