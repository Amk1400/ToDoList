from bootstrap.bootstrap import ApplicationBootstrap
from bootstrap.runners import ApplicationRunners


def main(use_cli: bool = False) -> None:
    """Main entry to run CLI or API based on flag."""
    """
    Args:
        use_cli (bool): Flag determining whether CLI or API should run.

    Returns:
        None: No return value.

    Raises:
        Exception: Raised if initialization or runner execution fails.
    """
    bootstrap = ApplicationBootstrap()
    config, db, manager = bootstrap.initialize()

    runners = ApplicationRunners()

    if use_cli:
        runners.run_cli(config=config, db=db, manager=manager)
    else:
        runners.run_api(manager=manager)


if __name__ == "__main__":
    main(use_cli=False)
