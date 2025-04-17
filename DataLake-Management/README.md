# Table Version Search

Table version search using contrastive learning approach.

## Replicate the experiment

Install Python 3.11.11. Execute the following command.

```bash
git clone https://github.com/aledigirm3/advanced-topics-computer-science.git
```

```bash
cd advanced-topics-computer-science/DataLake-Management
```

```bash
pip install -r requirements.txt
```

Before proceeding with the next steps, make sure you have created a folder named 'tables' inside the current directory ('DataLake-Management').

Then, import the following two folders into the 'tables' directory:

- 'commercial-pipelines'
- 'github-pipelines'

These folders are provided by the following repository:

🔗 https://gitlab.com/jwjwyoung/autopipeline-benchmarks

Move to the 'src' folder

```bash
  cd src
```

Now run these scripts (in order as shown)

```bash
  python data_manipulation.py
  python build_model.py
```

The first script performs the following tasks:

- Creates pairs of tables (positive and negative examples)
- Computes their embeddings
- Builds the dataset for training

The second script is responsible for:

- Initializing the model
- Training it on the generated dataset
- Evaluating its performance
