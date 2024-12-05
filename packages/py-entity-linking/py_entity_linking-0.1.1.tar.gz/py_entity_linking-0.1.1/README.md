Lightweight entity linking solution for the English language.

**Please consider citing our works if you use code from this repository.**
**Also, we recommend using a Colab T4 GPU for faster results.**

## Main dependencies
* python>=3.10
* numpy==1.26.4
* SPARQLWrapper==2.0.0
* sentence_transformers==3.1.1
* aiohttp==3.9.5
* openai==1.54.2
* beautifulsoup4==4.12.2
* fake-useragent==1.5.1
* nest_asyncio==1.5.8

## Example & Usage
```
from linking import main

# Your API token which can be found here (https://github.com/marketplace/models/azure-openai/gpt-4o)
api_token = "YOUR_API_TOKEN"

main.EL(api_token=api_token,
	sentence="We used PCA and FA for our experiments.",
	mention="PCA and FA",
	single="No",
	combination="No",
	disambiguation="Yes",
	embedding_model="Lajavaness/bilingual-embedding-large")
```

```
The correct entity for 'PCA' is:

Wikipedia: https://en.wikipedia.org/wiki/Principal_component_analysis

Wikidata: https://www.wikidata.org/wiki/Q2873

DBpedia: http://dbpedia.org/resource/Principal_component_analysis



The correct entity for 'FA' is:

Wikipedia: https://en.wikipedia.org/wiki/Factor_analysis

Wikidata: https://www.wikidata.org/wiki/Q726474

DBpedia: http://dbpedia.org/resource/Factor_analysis

Execution Time: 00:00:35
```

## Parameters
* **api_token**: Your API token from [here](https://github.com/marketplace/models/azure-openai/gpt-4o). **(Required)**  
* **sentence**: An English text. **(Required)**  
* **mention**: The mention you want to perform the linking, the mention should be from inside the provided sentence. **(Required)**
* **disambiguation**: Used when the mention has acronyms or the mention has two different entities inside (e.g. PCA and FA), *(deafult="Yes")*, *(Values: "Yes", "No")*. *(Optional)*   
* **single**: Usually used for difficult mentions, it searches each word of the mention individually, *(deafult="No")*, *(Values: "Yes", "No")*. *(Optional)*  
* **combination**: Usually used for difficult mentions, it makes combinations for each word of the mention, *(deafult="No")*, *(Values: "Yes", "No")*. *(Optional)*  
* **embedding_model**: A [sentence-transformers](https://sbert.net/) model to perform text similarity, *(deafault="Lajavaness/bilingual-embedding-large")*, *(Values: str of the name of any sentence-transformers model)*. *(Optional)*

## Licence
This library is licensed under the [CC-BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/).