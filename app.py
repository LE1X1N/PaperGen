import argparse
from src.service.doc import Pipeline


if __name__== "__main__":

    parser = argparse.ArgumentParser(description="generate thesis based on title")
    parser.add_argument("--title", type=str, default="网络文学对传统文学的影响", help="title of your thesis")
    args = parser.parse_args()

    title = args.title

    pipeline = Pipeline()
    pipeline.generate_paper(title)