import logging
def main():
    logger = logging.getLogger("Main Robot")
    logger.setLevel(logging.INFO)


def minimal_task():
    print("Done.")


if __name__ == "__main__":
    main()
