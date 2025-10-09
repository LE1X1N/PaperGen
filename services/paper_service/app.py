from src.service.doc import Pipeline

if __name__== "__main__":
    title = "网络文学对传统文学的影响"

    pipeline = Pipeline()
    pipeline.generate_paper(title, cache=True)