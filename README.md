# MovieSense Dataset  

MovieSense is an enriched version of the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/), integrating coreference resolution, named entity recognition, event extraction, and commonsense inference to enhance narrative analysis. [The BookNLP library](https://github.com/booknlp/booknlp) is used to resolve character references and extract entities, while the COMET model in the [Kogito library](https://github.com/epfl-nlp/kogito) generates causal, motivational, and future inferences from extracted events. These enhancements enable deeper insights into character interactions, narrative structures, and implicit commonsense knowledge, making MovieSense valuable for storytelling analysis, character modeling, and event prediction.

## Features  
- **Coreference Resolution**: Links character mentions for better entity tracking.  
- **Named Entity Recognition (NER)**: Extracts characters, locations, and organizations.  
- **Event Extraction**: Identifies key events from movie summaries.  
- **Commonsense Inference**: Uses COMET to generate causal, motivational, and future implications.  

## License  
**MovieSense** is released under the **CC BY-SA 4.0** license, meaning you are free to use, share, and modify it as long as you provide attribution and distribute any derived work under the same license. The dataset credits the **CMU Movie Summary Corpus (CC BY-SA 4.0).**  

## Citation  

If you use **MovieSense**, please cite it as follows:  

```bibtex
@misc{kim2024moviesense,
  author = {Kyuhee Kim and Team Deep5eekers},
  title = {MovieSense: A Commonsense-Enriched Movie Summary Dataset},
  year = {2024},
  howpublished = {CS-401 Applied Data Analysis Project (Fall 2024)},
  license = {CC BY-SA 4.0},
  note = {Derived from the CMU Movie Summary Corpus (CC BY-SA 4.0) with entity resolution, event extraction, and commonsense inference.},
  url = {https://github.com/koreankiwi99/MovieSense}
}
```
