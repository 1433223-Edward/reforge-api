## CP2 Evidence — Real Embedding Adapter

Experiment:

FakeEmbeddingModel vs LocalEmbeddingModel


Fake Embedding:
- Representation: text length only
- Dimension: 1
- Retrieval Hit Rate: 2/5


Local Embedding:
- Model: BAAI/bge-small-zh-v1.5
- Dimension: 512
- Retrieval Hit Rate: 5/5


Conclusion:

The experiment confirmed that embedding representation quality
was the primary bottleneck in the initial retrieval baseline.
Replacing the embedding provider through the existing abstraction
improved semantic retrieval performance.