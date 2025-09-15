# AI-HC-Project1

Github repository for code written for the first project of our Artificial Intelligence and Human Cognition course.  
This project involves two distinct experiments meant to test human working memory by quickly presenting and rotating between words, and then asking participants to recall them in any order or in the correct order.

## Experiments

### 1. Free Recall
In the free recall experiment, participants are shown a sequence of items (either **20 single letters** or **20 three-letter words**, depending on final setup).  
- **Presentation rate:** 500 ms per item  
- **Final pause:** 5000 ms after the last item  
- **Task:** Recall as many items as possible, in **any order**  

This task primarily measures the capacity and retrieval processes of working memory, and typically shows **primacy and recency effects** (better recall of the first and last items).

### 2. Serial Recall
In the serial recall experiment, participants are shown a shorter sequence of **6–7 three-letter words**.  
- **Presentation rate:** 500 ms per item  
- **Final pause:** 5000 ms after the last item  
- **Task:** Recall the words in the **exact order** they were presented  

This task emphasizes sequential processing in working memory and allows us to study how order information is maintained, as well as where errors or transpositions tend to occur.

## Goals
- Compare performance differences between free recall and serial recall.  
- Investigate how working memory handles sequence length, order constraints, and time pressure.  
- Provide data that can be used to model memory processes and strategies.  

## Repository Contents
- `recall_experiment/`: Scripts for running both experiments.  
- `data/`: Collected participant data (if included).  
- `analysis`: Tools for analyzing recall accuracy, error types, and memory patterns.  

## How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/AI-HC-Project1.git
   cd AI-HC-Project1
