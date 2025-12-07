import typer
import simulation

app = typer.Typer()

@app.command()
def run_simulation(steps: int = 20, seed: int | None = None):
    """
    Команда для запуска симуляции.

    :param steps: Количество шагов симуляции (по умолчанию 20).
    :param seed: Сид для генератора случайных чисел (по умолчанию None).
    """
    simulation.run_simulation(steps, seed)


@app.command()
def main() -> None:
    """
    Основная точка входа в приложение.
    """
    pass

if __name__ == "__main__":
    app()
