import logging

from RPA.Robocorp.WorkItems import WorkItems


def main():
    logger = logging.getLogger("Main Robot")
    logger.setLevel(logging.INFO)

    try:
        configuration = WorkItems().get_input_work_item().payload
        URL = configuration["url"]
        PHRASE = configuration["phrase"]
    except Exception:
        logger.exception(
            "Error getting the configuration from Robocorp Input Work Item."
        )
        return

def minimal_task():
    print("Done.")


if __name__ == "__main__":
    main()