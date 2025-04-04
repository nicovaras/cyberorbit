## 倹 Subtopic 3.3: Feature Engineering for Specific Data Types

**Goal:** Apply effective feature engineering techniques tailored to common data types like text, images, and time series.

**Resources:**

* **Scikit-learn Text Feature Extraction:** [User Guide](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) (CountVectorizer, TfidfVectorizer)
* **Word Embeddings:** Libraries like `Gensim`, `spaCy`, or pre-trained embeddings (Word2Vec, GloVe, FastText).
* **Image Feature Extraction:** Using pre-trained CNNs (e.g., via `torchvision.models`, `tf.keras.applications`). [Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html).
* **Time Series Feature Engineering Library:** `tsfresh` [Documentation](https://tsfresh.readthedocs.io/en/latest/), `featuretools` [Documentation](https://featuretools.alteryx.com/en/stable/) (Automated feature engineering)
* **Pandas Time Series Functionality:** [User Guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html) (Rolling windows, lags)

---

### 隼 **Exercise 1: Advanced Text Features (TF-IDF & N-grams)**

**Goal:** Extract TF-IDF features from text data, incorporating N-grams to capture multi-word phrases.

**Instructions:**

1.  Load a text dataset suitable for classification (e.g., 20 Newsgroups, IMDB reviews).
2.  Instantiate `sklearn.feature_extraction.text.TfidfVectorizer`.
3.  Experiment with the following parameters:
    * `ngram_range`: Set to `(1, 1)` (unigrams only), then `(1, 2)` (unigrams and bigrams), then `(1, 3)` (uni-, bi-, trigrams).
    * `max_features`: Limit the vocabulary size (e.g., 5000).
    * `stop_words`: Use `'english'` to remove common stop words.
4.  For each `ngram_range` setting, fit the vectorizer on the training text data and transform both train and test data.
5.  Train a simple classifier (e.g., Logistic Regression, Naive Bayes) on the resulting TF-IDF features.
6.  Evaluate and compare the performance for different `ngram_range` settings. Did including bigrams or trigrams improve performance? How did `max_features` affect results?
7.  **Challenge:** Explore other `TfidfVectorizer` parameters like `min_df` and `max_df`. How do they help filter the vocabulary?

---

### 隼 **Exercise 2: Using Pre-trained Word Embeddings**

**Goal:** Represent text documents by averaging pre-trained word embeddings (like GloVe or Word2Vec) of the words they contain.

**Instructions:**

1.  Download pre-trained word embeddings (e.g., GloVe 100-dimensional vectors). Load them into a dictionary mapping words to vectors.
2.  Use the same text dataset as Exercise 1. Preprocess the text (lowercase, remove punctuation, potentially stop words).
3.  For each document (text sample):
    * Split the text into words (tokens).
    * Look up the embedding vector for each word in the pre-trained embedding dictionary.
    * Calculate the **average** of the embedding vectors for all words found in the document. This average vector represents the document. (Handle words not found in the embedding vocabulary, e.g., by skipping them or using a zero vector).
4.  You now have a numerical feature matrix where each row is the average embedding vector for a document.
5.  Train a classifier (e.g., Logistic Regression, SVM) on these document embedding features.
6.  Compare the performance to the TF-IDF approach from Exercise 1. Discuss the pros and cons of using pre-trained embeddings versus TF-IDF.
7.  **Challenge:** Instead of simple averaging, try TF-IDF weighted averaging of word embeddings. Does this improve performance?

---

### 隼 **Exercise 3: Image Features via Transfer Learning**

**Goal:** Extract fixed-size feature vectors from images using a pre-trained Convolutional Neural Network (CNN).

**Instructions:**

1.  Choose an image dataset (e.g., CIFAR-10, or a small subset of ImageNet if possible) and a pre-trained CNN architecture (e.g., ResNet50, VGG16, EfficientNet available via PyTorch/TensorFlow hubs).
2.  Load the pre-trained model **without its final classification layer**. You want the output of the penultimate layer (the pooled feature layer).
3.  Preprocess your images according to the requirements of the chosen pre-trained model (resizing, normalization specific to ImageNet training).
4.  Pass your images (train and test sets) through the pre-trained model (in evaluation mode, no gradient calculation needed) to get the fixed-size feature vectors for each image.
5.  You now have numerical feature matrices for your train and test sets.
6.  Train a simple classifier (e.g., Logistic Regression, SVM, k-NN) on these extracted image features.
7.  Evaluate the performance. How well does this transfer learning approach work compared to training a simple CNN from scratch on the same (potentially small) dataset?
8.  **Challenge:** Instead of just using the penultimate layer output, try fine-tuning the last few layers of the pre-trained CNN on your specific dataset's classification task. Compare this to using the frozen features.

---

### 隼 **Exercise 4: Time Series Lag Features**

**Goal:** Create lagged features from time series data to capture auto-correlation and provide historical context for models.

**Instructions:**

1.  Load a univariate time series dataset (e.g., stock prices, temperature readings).
2.  Use pandas `shift()` method to create lagged features:
    * Create 'lag_1' feature (value from the previous time step).
    * Create 'lag_3' feature (value from 3 time steps ago).
    * Create 'lag_7' feature (value from 7 time steps ago).
3.  Handle the missing values (NaNs) introduced at the beginning of the series due to lagging (e.g., drop rows, fill with a specific value).
4.  Assume you want to predict the next value (`t+1`). Your features for predicting time `t+1` would be values available at time `t` (e.g., `value_t`, `lag_1` (which is `value_{t-1}`), `lag_3` (`value_{t-3}`), etc.). Prepare your `X` (features) and `y` (target shifted by -1) accordingly.
5.  Train a simple regression model (e.g., Linear Regression, Ridge) using these lagged features. Evaluate its performance using time series cross-validation (Subtopic 3.1).
6.  **Challenge:** How do you determine the optimal number of lags to include? Explore techniques like analyzing the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots of the time series.

---

### 隼 **Exercise 5: Time Series Rolling Window Features**

**Goal:** Create features based on statistics calculated over rolling windows of time series data.

**Instructions:**

1.  Use the same time series dataset as Exercise 4.
2.  Use pandas `rolling()` method followed by aggregation functions (like `mean()`, `std()`, `min()`, `max()`) to create rolling window features:
    * Calculate the rolling mean over a window of size 3 (`rolling_mean_3`).
    * Calculate the rolling standard deviation over a window of size 7 (`rolling_std_7`).
    * Calculate the rolling maximum over a window of size 5 (`rolling_max_5`).
3.  Remember that rolling features calculated at time `t` incorporate data up to `t`. To use them as features for predicting `t+1`, you need to **shift** the rolling features by 1 time step so that you are only using information available up to time `t`.
4.  Handle missing values introduced at the beginning.
5.  Combine these rolling window features (shifted) with lagged features (from Exercise 4) to create your feature set `X` for predicting `y` (value at `t+1`).
6.  Train a regression model using this combined feature set. Evaluate its performance using time series CV.
7.  Compare performance to using only lagged features. Did adding rolling window statistics help?
8.  **Challenge:** Explore using exponentially weighted moving averages (`.ewm()`) as an alternative to simple rolling windows.

---

### 隼 **(Optional) Exercise 6: Automated Time Series Feature Engineering**

**Goal:** Explore libraries designed for automatically extracting a large number of potentially relevant features from time series data.

**Instructions:**

1.  Install a library like `tsfresh` or `featuretools`.
2.  Prepare your time series data in the format required by the library (often requires specific column names for time, value, and potentially entity IDs if multiple series exist).
3.  Use the library's main function (e.g., `tsfresh.extract_features`) to automatically generate a large number of time series features (e.g., statistics, Fourier coefficients, autocorrelation, complexity measures).
4.  Explore the generated feature matrix. Note the potentially large number of features created.
5.  Discuss the pros and cons of automated feature engineering for time series compared to manual creation of lags/rolling windows. Consider feature interpretability and the risk of generating irrelevant features.
6.  **Challenge:** Apply feature selection techniques (e.g., those relevant for `tsfresh` which integrates some, or methods from Subtopic 3.2) to the large set of automatically generated features before using them to train a model.

---