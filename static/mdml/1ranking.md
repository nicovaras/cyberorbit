## 倹 Subtopic 1.6: Evaluating Ranking & Recommendation Systems

**Goal:** Understand and compute metrics specifically designed for evaluating the quality of ranked lists, crucial for information retrieval, search engines, and recommender systems.

**Resources:**

* **Scikit-learn Metrics:** [Ranking Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#ranking-metrics) (Includes Average Precision / MAP)
* **NDCG Explanation:** [Wikipedia Article](https://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG)
* **Metrics Overview:** [Blog post covering various ranking/rec metrics](https://towardsdatascience.com/evaluation-metrics-for-recommender-systems-df56c6611093)
* **Coverage, Personalization, Serendipity:** Conceptual understanding from research papers or blogs.

---

### 隼 **Exercise 1: Mean Reciprocal Rank (MRR)**

**Goal:** Calculate MRR, a metric focused on the rank of the *first* relevant item in a list.

**Instructions:**

1.  Consider a scenario with multiple queries (users) and ranked lists of results (recommendations) returned for each. Assume you know the ground truth relevant item(s) for each query.
    * Query 1: Results [`itemC`, `itemA`, `itemB`], Relevant: [`itemA`]
    * Query 2: Results [`itemB`, `itemD`, `itemE`], Relevant: [`itemE`, `itemB`]
    * Query 3: Results [`itemA`, `itemF`, `itemG`], Relevant: [`itemX`] (Relevant item not in results)
2.  For each query:
    * Find the rank of the **first** relevant item in the results list (rank 1, 2, 3...). If no relevant item is found, the rank is considered infinity.
    * Calculate the reciprocal rank (1 / rank). If rank is infinity, reciprocal rank is 0.
3.  Calculate the Mean Reciprocal Rank (MRR) by averaging the reciprocal ranks across all queries.
4.  Interpret the MRR score. What does a higher MRR indicate? In what scenarios is MRR a particularly suitable metric?
5.  **Challenge:** Implement a Python function `calculate_mrr(ranked_lists, relevant_items_map)` that takes a list of result lists and a dictionary mapping query IDs to sets of relevant item IDs, and returns the MRR score.

---

### 隼 **Exercise 2: Mean Average Precision (MAP)**

**Goal:** Calculate MAP, a metric that considers the precision at each relevant item's position in the ranked list.

**Instructions:**

1.  Use the same queries, results, and relevance data from Exercise 1.
2.  For each query:
    * Calculate the **Precision at k (P@k)** for each position `k` where a relevant item is found. P@k is the number of relevant items among the top `k` results divided by `k`.
    * Calculate the **Average Precision (AP)** for the query: Average the P@k values for all `k` where the item at rank `k` was relevant. If no relevant items are found, AP is 0.
        * Query 1: Relevant at k=2. P@2 = 1/2. AP = (1/2) / 1 = 0.5
        * Query 2: Relevant at k=1, k=2. P@1=1/1. P@2=2/2. AP = (1.0 + 1.0) / 2 = 1.0
        * Query 3: No relevant items. AP = 0.
3.  Calculate the Mean Average Precision (MAP) by averaging the AP scores across all queries.
4.  Compare MAP to MRR calculated earlier. How does MAP provide a more comprehensive evaluation than MRR?
5.  **Challenge:** Implement a Python function `calculate_map(ranked_lists, relevant_items_map)` that computes the MAP score.

---

### 隼 **Exercise 3: Normalized Discounted Cumulative Gain (nDCG)**

**Goal:** Calculate nDCG, a popular metric that handles graded relevance and discounts the value of items based on their rank.

**Instructions:**

1.  Consider a single query with a ranked list and *graded relevance scores* (e.g., 0=not relevant, 1=somewhat relevant, 2=highly relevant).
    * Query: Results [`itemA`, `itemB`, `itemC`, `itemD`], Relevance: `itemA`(2), `itemB`(0), `itemC`(1), `itemD`(1)
2.  Calculate the **Discounted Cumulative Gain (DCG)** at a specific cutoff `k` (e.g., k=4):
    * `DCG@k = sum_{i=1 to k} [ relevance_i / log2(i + 1) ]`
    * Calculate DCG@4 for the example.
3.  Determine the **Ideal DCG (IDCG)**@k:
    * Sort the items by their true relevance scores in descending order.
    * Calculate the DCG for this ideal ranking up to position `k`.
    * Calculate IDCG@4 for the example (Ideal order: `itemA`(2), `itemC`(1), `itemD`(1), `itemB`(0)).
4.  Calculate the **Normalized DCG (nDCG)**@k:
    * `nDCG@k = DCG@k / IDCG@k`
    * Calculate nDCG@4 for the example.
5.  Interpret the nDCG score. What does a score of 1.0 mean? What does a score close to 0 mean? Why is normalization (dividing by IDCG) important?
6.  **Challenge:** Implement a Python function `calculate_ndcg(ranked_results_relevance, true_relevance_map, k)` that computes nDCG@k given a list of relevance scores for the ranked results and the true relevance map.

---

### 隼 **Exercise 4: Beyond Accuracy - Coverage, Personalization, Serendipity (Conceptual)**

**Goal:** Understand the concepts behind recommendation metrics that evaluate aspects other than simple relevance prediction accuracy.

**Instructions:**

1.  Research and define the following concepts in the context of recommender systems:
    * **Catalog Coverage:** What does it measure? How might it be calculated (e.g., percentage of catalog items recommended at least once)? Why is it important?
    * **Personalization (or Aggregate Diversity):** What does it measure? How could you quantify the difference between recommendation lists generated for different users (e.g., average pairwise distance/dissimilarity)? Why is personalization desirable?
    * **Serendipity:** What does it try to capture? How is it different from novelty or relevance? Why is recommending serendipitous items potentially valuable? (This is harder to quantify).
2.  Discuss the potential trade-offs between optimizing for traditional accuracy metrics (like nDCG or MAP) and optimizing for metrics like coverage, personalization, or serendipity. Can optimizing for one hurt another?
3.  Describe a scenario where a recommender system with high nDCG might still provide a poor user experience due to low coverage or personalization.
4.  **Challenge:** Propose a simple method to measure **novelty** in a recommendation list (e.g., based on the popularity of recommended items). How does novelty differ from serendipity?

---