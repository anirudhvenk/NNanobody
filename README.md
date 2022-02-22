# NNanobody

NNanobody uses ensemble learning to determine the enrichment of CDR3 sequences of nanobodies. You can also use NNanobody to run gradient ascent to edit seed sequences such taht their enrichment is maximized. NNanobody also includes preprocessing scripts in order to dock the nanobody PDB files to an antigen (Ranibizumab). The docking algorithm used is [HADDOCK](https://wenmr.science.uu.nl/haddock2.4/).

## Training the Models

Models are either located in `regression/` directory or the `classification/` directory. You can find the training data [here](https://drive.google.com/drive/folders/1Ib9WTvW0sDv29cwA2ru6W-F8dgFlu8wY?usp=sharing). Run each jupyter notebook to train the model on a particular dataset.

## Training the Interpreter

The interpreter network uses each of the models contributing predictions of enrichment to make a more accurate estimate of the enrichment of a nanobody. Run `interpreter.ipynb` to train the network.

## Gradient Ascent

You can run the gradient ascent process by running the `gradient_ascent.ipynb` notebook. This will produce new CDR3 sequences that maximizes the enrichment of the nanobody for each neural network in the ensemble. You can find the seeds for gradient ascent [here](https://drive.google.com/drive/folders/1Ib9WTvW0sDv29cwA2ru6W-F8dgFlu8wY?usp=sharing).

## Post-processing

You can run post-processing by running the `post_processing.ipynb` notebook. This will use the interpreter network to predict the enrichment of the sequences produced through gradient ascent and ranks the sequences by their enrichment.
