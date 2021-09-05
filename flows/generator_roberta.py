from jina import Executor, Document, DocumentArray, requests
from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    pipeline,
)


class Generator(Executor):
    answer_model_name = "deepset/roberta-base-squad2"
    answer_model = AutoModelForQuestionAnswering.from_pretrained(answer_model_name)
    answer_tokenizer = AutoTokenizer.from_pretrained(answer_model_name)
    nlp = pipeline(
        "question-answering", model=answer_model, tokenizer=answer_tokenizer
    )

    @requests
    def generate(self, docs: DocumentArray, **kwargs) -> DocumentArray:
        for doc in docs.traverse_flat(('r',)):
            context = " ".join([match.text for match in doc.matches])
            qa_input = {"question": doc.text, "context": context}
            result = self.nlp(qa_input)
            result = DocumentArray(Document(result))
            return result
