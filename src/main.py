import typer
import simulation

app = typer.Typer()

@app.command()
def run_simulation(steps: int = 20, seed: int | None = None):
    """
    Команда для запуска симуляции.
    """
    simulation.run_simulation(steps, seed)


@app.command()
def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

if __name__ == "__main__":
    app()
