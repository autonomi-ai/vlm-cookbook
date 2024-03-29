# VLM-1 Cookbook

A collection of examples built on top of VLM-1, an API for structured understanding of documents, images and video https://vlm-dev.nos.run/v1.

## What is 'structured understanding'?

VLMs like GPT4V and Claude support question answering over arbitrary visual inputs, but in practice this is a
less than ideal interface for many workflows, especially at scale. Instead, VLM-1 defines its API in
terms of fixed types for different visual inputs like financial documents, cable news and sporting events that
are populated by the underlying model based on the input being queried. This schema can be as simple
as a list of string values (see NFL example below) or more complicated with nested types
e.g a plot in a Powerpoint presentation:

```
class Plot:
    cls_name: str = "Plot"
    type: PlotType = Field(..., description="Type of plot (line, bar, ticker, pie, other)")
    title: Optional[str] = Field(..., description="Title of the graph, if any, otherwise None.")
    description: str = Field(..., description="Detailed description of the plot.")
    markdown: str = Field(
        ...,
        description="Markdown representation of the plot, each one should be tidy, do not try to join plots that should be separate. Try to extract the data from the plot and represent it in a table. Do not include any links or references.",
    )
    caption: Optional[str] = Field(..., description="Caption of the graph, if any, otherwise None.")
```

## DB Integration

Structured outputs are a natural fit for tabular data storage (see NFL + Airtable below), where we can 
create columns mapped to elements in the schema that will be populated on ingest. We can replace a 
vector embedding with a known schema, or populate document metadata alongside the embedding for 
more structured search and retrieval flows with known, human readable filters. We're working on a number
of DB integrations for both Vector and non-vector DBs and would love to here from you on 
[Discord](https://discord.gg/a6suHC9B5E) if you have an interesting use case you would like to see supported!

## What does VLM-1 bring to the table?
* The right model for the right data. We've taken some inspiration from LLM router platforms like Martian and Not
Diamond, which dispatch queries to specific foundation models dynamically to reduce cost and improve performance.
We think this problem is even more acute for VLMs, where the dimensionality is much higher, the inference 
workloads are much more expensive and errors are more difficult to catch. For VLMs, this means routing to 
fine-tuned models (or even entirely custom models for specific input types) based on the query and schema.

* Gloves off for large inference workloads. Most VLMs (GPT4V, Gemini) are still heavily rate limited, 
which hinders their utility for anything beyond single document flows. VLMs require deep infra optimizations 
in order to be viable for DB scale structured extraction. VLM-1 is meant to be the first 
structured VLM API capable of supporting high data volumes at acceptable prices, 
which means we've had to think a lot about hardware, containerization, replication, load-balancing etc.
(this is a more general problem! check out [NOS](https://github.com/autonomi-ai/nos), our Inference Server). 
We're also interested in hearing from folks looking for On-Prem or custom deployments for reasons of cost or privacy.
VLM-1 is our public API, but we can also deploy custom, type-checked visual APIs for sensitive use cases that run
entirely on your VPC or local cluster (talk to use about HW recommendations if you would like to go down this
route!).

* Extensible schemas for specific domains. We're building a zoo of document and scene description schemas
that will be accessible through the VLM API. The goal is much higher confidence around extraction quality,
especially with regards to hallucinations.

* Easy DB integration. VLM-1 is meant to be easy to use alongside embedding flows for Vector DBs like 
Pinecone and Chroma, allowing you to automatically generate metadata for more steerable and reliable 
retrieval flows.

# vlm-cookbook

## 🧪 Motivating Examples

| **Name** | **Colab / Notebook** | **Date** | Author |
|:---:|:---:|:---:|:---:|
| Financial Presentations | [![GitHub](https://badges.aleen42.com/src/github.svg)](./examples/vlm-1-financial-presentations.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/autonomi-ai/vlm-cookbook/blob/main/examples/vlm-1-financial-presentations.ipynb)  | 03-27-2024 | [@spillai](https://github.com/spillai) |
| Financial TV News | [![GitHub](https://badges.aleen42.com/src/github.svg)](./examples/vlm-1-financial-tv-news.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/autonomi-ai/vlm-cookbook/blob/main/examples/vlm-1-financial-tv-news.ipynb)  | 03-28-2024 | [@spillai](https://github.com/spillai) |
| NBA Game Analysis | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jy62B-H1fwyNGvgyBS83_OhX5NJ9dpnm)  | 03-28-2024 | [@spillai](https://github.com/spillai) |
| Write NFL Plays to Airtable | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XhVG7Fl1O4m8uFS6bRgavj0mtJb5u1Qw#scrollTo=Pn03zLapza69)  | 03-29-2024 | [@outtanames](https://github.com/outtanames) |




## 🔗  Quick Links

* 💬 Send us an email at [support@autonomi.ai](mailto:support@autonomi.ai) or join our [`#vlm-playground` Discord channel](https://discord.gg/a6suHC9B5E) for help.
* 📣 Follow us on [Twitter](https://twitter.com/autonomi\_ai), and [LinkedIn](https://www.linkedin.com/company/autonomi-ai) to keep up-to-date on our products.
