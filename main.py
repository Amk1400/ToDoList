from bootstrap.bootstrap import ApplicationBootstrap
from bootstrap.runners import ApplicationRunners


def main(use_cli: bool = False) -> None:
    """Entry point for running CLI or API."""
    bootstrap = ApplicationBootstrap()
    config, db, manager = bootstrap.initialize()

    runners = ApplicationRunners()

    if use_cli:
        runners.run_cli(config=config, db=db, manager=manager)
    else:
        runners.run_api(manager=manager)


if __name__ == "__main__":
    main(use_cli=False)
