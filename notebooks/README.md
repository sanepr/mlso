# Jupyter Notebooks

This directory contains Jupyter notebooks for exploratory data analysis and model training.

## 🚀 Getting Started

### 1. Make sure your virtual environment is activated:

```bash
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Start Jupyter Notebook (choose one):

**Option A: Jupyter Notebook (Classic)**
```bash
jupyter notebook
```

**Option B: JupyterLab (Modern UI)**
```bash
jupyter lab
```

**Option C: Using Python module (if command not found)**
```bash
python -m notebook
```

**Option D: Direct path to virtual environment**
```bash
./venv/bin/jupyter notebook
```

### 3. Your browser will open automatically at: http://localhost:8888

## 📓 Available Notebooks

- **00_test_jupyter.ipynb** - Test notebook to verify Jupyter is working
- **01_eda.ipynb** - Exploratory Data Analysis (to be created)
- **02_model_training.ipynb** - Model Training experiments (to be created)

## 🐛 Troubleshooting

### Issue: "jupyter: command not found"

**Solution 1**: Make sure Jupyter is installed:
```bash
pip install jupyter notebook ipykernel
```

**Solution 2**: Use Python module directly:
```bash
python -m notebook
```

**Solution 3**: Use full path to jupyter:
```bash
./venv/bin/jupyter notebook
```

### Issue: Kernel not found

**Solution**: Install ipykernel in your virtual environment:
```bash
pip install ipykernel
python -m ipykernel install --user --name=mlso --display-name "Python (mlso)"
```

### Issue: Cannot import modules in notebook

**Solution**: Make sure you're using the correct kernel (Python (mlso)) and that your virtual environment is activated.

## 💡 Tips

1. Always activate your virtual environment before starting Jupyter
2. Use `Shift+Enter` to run a cell
3. Use `Tab` for auto-completion
4. Use `Shift+Tab` to see function documentation
5. Save your work frequently with `Ctrl+S` or `Cmd+S`

## 📚 Resources

- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [Jupyter Keyboard Shortcuts](https://towardsdatascience.com/jypyter-notebook-shortcuts-bf0101a98330)

