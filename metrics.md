1. Response Accuracy
Definition: Measures how accurate and correct the response is in relation to the question asked, especially for specific details like ingredients, cooking methods, or timing.
Metric: Accuracy Score — percentage of correct responses based on a predefined correct answer or a set of expert responses.
Formula:
Accuracy
=
Number of correct responses
Total number of responses
×
100
Accuracy= 
Total number of responses
Number of correct responses
​
 ×100
2. Relevance
Definition: Assesses how well the response answers the user’s query and whether it aligns with the user's intent (e.g., specific recipe, dietary preferences).
Metric: Relevance Score — based on how directly the answer addresses the user's question. Can be scored on a Likert scale (e.g., 1-5) by human evaluators or through an automated metric that looks for key terms in the response.
Formula: Average relevance score from user feedback or evaluator rating.
3. Clarity and Coherence
Definition: Measures how clear and easy to understand the response is. A response should be well-structured and free from confusion.
Metric: Clarity Score — scored by human evaluators or using automated NLP metrics (e.g., BLEU, ROUGE).
Formula: Average score from human evaluators (1-5 scale) or NLP-based coherence evaluation.
4. Response Time
Definition: Measures the time it takes for the system to generate a response after receiving a query.
Metric: Average Response Time — the time (in seconds or milliseconds) it takes for the system to respond.
Formula:
Average Response Time
=
∑
Response Times
Number of Responses
Average Response Time= 
Number of Responses
∑Response Times
​
 
Note: Response time is important when comparing the LLM setup with and without RAG, as RAG may add retrieval overhead.
5. User Satisfaction
Definition: Measures how satisfied users are with the responses they receive, especially in terms of usefulness and quality.
Metric: User Satisfaction Score — typically measured using surveys or feedback forms. Can use a Likert scale (1–5) to rate overall satisfaction.
Formula: Average user satisfaction score from feedback or survey responses.
6. Consistency
Definition: Assesses whether the system provides consistent answers to the same or similar queries over time.
Metric: Consistency Score — measures how similar responses are when the same question is asked multiple times. Can be evaluated through a comparison of answers (e.g., semantic similarity).
Formula: Percentage of identical or similar responses across multiple queries.
Method: Use semantic similarity metrics like cosine similarity between vectors from BERT or another transformer-based model.
7. Novelty and Diversity (in the context of recipes)
Definition: Evaluates how diverse or unique the recipe suggestions are. A good cooking advisor should not repeatedly suggest the same recipe unless it's a common choice.
Metric: Novelty Score — measures how often the same or similar recipes are suggested.
Formula: Percentage of novel recipes suggested based on a reference set.
Method: Track if the same recipe is repeated for similar queries or based on ingredient constraints.
8. Handling of Uncommon Queries
Definition: Assesses the system’s ability to handle rare or difficult cooking-related queries (e.g., specific dietary needs, rare ingredients).
Metric: Success Rate for Uncommon Queries — measures how often the system can provide a meaningful answer to uncommon or niche queries.
Formula:
Success Rate
=
Number of successful answers to rare queries
Total rare queries
×
100
Success Rate= 
Total rare queries
Number of successful answers to rare queries
​
 ×100
9. Engagement or Interaction Quality
Definition: Measures how well the system engages with the user, keeping them interested and encouraging further interaction (e.g., suggesting related recipes, asking follow-up questions).
Metric: Engagement Score — can be evaluated through user feedback, e.g., "Would you like to try another recipe?" or based on follow-up questions.
Formula: Percentage of users who ask more than one follow-up question or provide positive engagement feedback.
