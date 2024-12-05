"""
This module implements a wrapper over the MLPClassifier
for easier parameterization.
"""
import numpy as np

from sklearn.neural_network import MLPClassifier


class MLPClassifierWrapper:
    """
    Wrapper over MLPClassifier of sklearn to provide easier parameterization
    """

    def __init__(
        self,
        *,
        max_iter=10000,
        activation="relu",
        hidden_layer_fraction="sqrt",
        alpha=0.0001,
        learning_rate="adaptive",
        random_state=None
    ):
        """
        Constructor of the MLPClassifier

        Args:
            max_iter (int): the maximum number of iterations
            activation (str): name of the activation function
            hidden_layer_fraction (float): fraction of the hidden neurons of
                                            the number of input dimensions
            alpha (float): alpha parameter of the MLP classifier
            learning_rate (str): 'constant'/'invscaling'/'adaptive'
            random_state (int/np.random.RandomState/None): initializer of the
                                                            random state
        """
        self.max_iter = max_iter
        self.activation = activation
        self.hidden_layer_fraction = hidden_layer_fraction
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.random_state = random_state
        self.model = None

    def _determine_hidden_layer_size(self, n_dim):
        if isinstance(self.hidden_layer_fraction, str):
            if self.hidden_layer_fraction == "sqrt":
                return max([1, int(np.sqrt(n_dim))])
        return max([1, int(n_dim * self.hidden_layer_fraction)])

    def fit(self, X, y):
        """
        Fit the model to the data

        Args:
            X (np.ndarray): features
            y (np.array): target labels

        Returns:
            obj: the MLPClassifierWrapper object
        """
        hidden_layer_size = self._determine_hidden_layer_size(X.shape[1])
        self.model = MLPClassifier(
            activation=self.activation,
            max_iter=self.max_iter,
            hidden_layer_sizes=(hidden_layer_size,),
            alpha=self.alpha,
            learning_rate=self.learning_rate,
            random_state=self.random_state,
        ).fit(X, y)
        return self

    def predict(self, X):
        """
        Predicts the labels of the unseen data

        Args:
            X (np.ndarray): unseen features

        Returns:
            np.array: predicted labels
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Predicts the class probabilities of the unseen data

        Args:
            X (np.ndarray): unseen features

        Returns:
            np.array: predicted class probabilities
        """
        return self.model.predict_proba(X)

    def get_params(self, deep=False):
        """
        Returns the parameters of the classifier.

        Returns:
            dict: the parameters of the object
        """
        _ = deep
        return {
            "activation": self.activation,
            "hidden_layer_fraction": self.hidden_layer_fraction,
            "alpha": self.alpha,
            "learning_rate": self.learning_rate,
            "random_state": self.random_state,
        }

    def copy(self):
        """
        Creates a copy of the classifier.

        Returns:
            obj: a copy of the classifier
        """
        return MLPClassifierWrapper(**self.get_params())
