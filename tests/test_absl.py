from absl import logging, app


def main(argv):
    print("Hello World")
    logging.debug("DEBUG info")

if __name__ == '__main__':
    app.run(main)
