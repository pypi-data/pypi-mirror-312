import typer
from rich.console import Console
from rich.table import Table
from model_hallucination.dataset_loader import load_dataset
from model_hallucination.evaluator import evaluate_hallucination

app = typer.Typer()
console = Console()

@app.command()
def evaluate_dataset(
    dataset: str = typer.Option(..., help="Dataset to evaluate (fever, simpq, truthfulqa, factcc)."),
    max_samples: int = typer.Option(100, help="Maximum number of samples to evaluate."),
    api_key: str = typer.Option(..., help="Your Hugging Face API key."),
):
    """
    Evaluate hallucination likelihood on a selected dataset.
    """
    supported_datasets = ["fever", "simpq", "truthfulqa", "factcc"]

    if dataset not in supported_datasets:
        console.print(f"[bold red]Invalid dataset choice! Supported: {', '.join(supported_datasets)}[/bold red]")
        raise typer.Exit()

    console.print(f"[bold blue]Loading {dataset} dataset...[/bold blue]")
    data = load_dataset(dataset, max_samples)

    console.print(f"[bold blue]Evaluating {len(data)} samples...[/bold blue]")
    results = evaluate_hallucination(data, api_key)

    # Display results in a table
    table = Table(title="Hallucination Evaluation")
    table.add_column("Input", style="cyan", overflow="fold")
    table.add_column("Reference", style="green", overflow="fold")
    table.add_column("Hallucination Score", style="magenta")

    for res in results:
        table.add_row(res["input"], res["reference"], str(res["hallucination_score"]))

    console.print(table)

@app.command()
def evaluate_prompt(
    prompt: str = typer.Option(..., help="The input text or question."),
    model_output: str = typer.Option(..., help="The generated output from the model."),
    api_key: str = typer.Option(..., help="Your Hugging Face API key."),
):
    """
    Evaluate hallucination likelihood for a single input and model output.
    """
    console.print("[bold blue]Analyzing model output for hallucinations...[/bold blue]")
    result = evaluate_hallucination([(prompt, model_output)], api_key)[0]

    console.print(f"Input: [cyan]{prompt}[/cyan]")
    console.print(f"Generated Output: [green]{model_output}[/green]")
    console.print(f"Hallucination Score: [magenta]{result['hallucination_score']}[/magenta]")

if __name__ == "__main__":
    app()
