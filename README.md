# AI Stock Analyzer (ASA)

Using a LLM, generate insights from company 10-K filings.

## Use

To comply with SEC download guidelines, all downloaders must have an identifier. Set your EDGAR identity in your environmental variables:

> setx EDGAR_IDENTITY="\<first name> \<last name> \<email address>"

Create an [OpenAI API key](https://platform.openai.com/api-keys). Set your API key in your environmental variables:

> setx OPENAI_API_KEY="\<your key>"

Run the script. Provide the tickers of the companies you want to analyze:

> python asa.py \<tickers>

> \>>> python asa.py AAPL MSFT
>
> \>>> Generate reports for AAPL and MSFT.

## Technical Details

ASA uses [edgartools](https://pypi.org/project/edgartools/) to download company 10-K filings from the SEC EDGAR database. All filings between 1995 and 2023 (roughly 29 documents) will be downloaded.

ASA utilizes OpenAI's ChatGPT LLM models for text inference. An [API key](https://platform.openai.com/api-keys) is required. Many LLMs are suitable for inference, but ChatGPT was chosen due to its popularity and free-tier usage support. While the free-tier supports `GPT 3.5 Turbo`, users can easily swap to paid tiers which give access to `GPT 4` which can outperform [1] specifically-trained state-of-the-art financial LLMs such as `BloombergGPT` [2][3].

Retrieval-augmented generation feeds 10-K documents to the LLM. Combined with other prompt engineering, the LLM then generates specified insights.

## References

> [1] X. Li et al., “Are CHATGPT and GPT-4 general-purpose solvers for financial text analytics? A study on several typical tasks,” Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track, 2023. doi:10.18653/v1/2023.emnlp-industry.39.
>
> [2] G. Zishan et al. “Evaluating Large Language Models: A Comprehensive Survey,” arXiv.Org, 2023. doi:10.48550/arxiv.2310.19736.
>
> [3] W. Shijie et al. “BloombergGPT: A Large Language Model for Finance,” arXiv.Org, 2023. doi:10.48550/arxiv.2303.17564.