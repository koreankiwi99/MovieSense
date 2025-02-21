# MovieSense Dataset  

**MovieSense** is an enriched version of the **CMU Movie Summary Corpus**, integrating **coreference resolution, named entity recognition, event extraction, and commonsense inference** to enhance narrative analysis. The **[BookNLP](https://github.com/booknlp/booknlp)** library resolves character references and extracts entities, while the **[COMET](https://github.com/atcbosselut/comet-commonsense)** model in the **[Kogito](https://github.com/kogito-computation/kogito)** library generates **causal, motivational, and future inferences** from extracted events. These enhancements enable deeper insights into **character interactions, narrative structures, and implicit commonsense knowledge**, making **MovieSense** valuable for **storytelling analysis, character modeling, and event prediction**.  

This dataset was created as part of the **2024 Fall EPFL CS-401 Applied Data Analysis (ADA) course** and is released under the **CC BY-SA 4.0 license**, crediting the **CMU Movie Summary Corpus**.  

---

## 📌 Features  
- **Coreference Resolution**: Links character mentions to improve entity tracking.  
- **Named Entity Recognition (NER)**: Extracts characters, locations, and organizations.  
- **Event Extraction**: Identifies key events from movie summaries.  
- **Commonsense Inference**: Uses COMET to generate causal, motivational, and future implications.  

---

## 📂 Dataset Structure  

The dataset includes: TBD

---

## 📜 License  

**MovieSense** is released under the **CC BY-SA 4.0** license, meaning you are free to use, share, and modify it as long as you provide attribution and distribute any derived work under the same license. The dataset credits the **CMU Movie Summary Corpus (CC BY-SA 4.0)**.  

---

## 📖 Citation  

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
