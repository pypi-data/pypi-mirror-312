"""GNN Enrich scoring module."""
# pylint: disable=unknown-option-value
import collections
import typing
import logging
import numpy
import numpy.typing
import scipy.spatial.distance # type: ignore[import-untyped]
import tqdm # type: ignore[import-untyped]

# Get logger
logger = logging.getLogger('gnnenrich')

# Types
PathwaysDict = dict[str, list[str]]
Embeddings = collections.OrderedDict[str, list[float]]
EmbArr = numpy.typing.NDArray[numpy.float32]

class Scoring:
    # pylint: disable=too-many-instance-attributes
    """Computes scoring for a list of proteins.

    Args:
        embeddings: ...
        corr_threshold: Correlation threshold.
        corr_threshold_repl_value: The replacement value used in correlation
                                   function for values between corr_threshold
                                   and 1.0 - overlap_score_eps. To disable it,
                                   set it to 0.0.
        overlap_score: ...
        overlap_score_eps: ...
    """

    _pw_scores: typing.Optional[dict[str, float]]
    _pw_emb: typing.Optional[dict[str, EmbArr]]

    # pylint: disable-next=too-many-positional-arguments
    def __init__(self, embeddings: Embeddings,
                 corr_threshold: float=0.95,
                 corr_threshold_repl_value: float=1.0,
                 overlap_score: float=3.0,
                 overlap_score_eps: float=1e-4) -> None:
        # pylint: disable=too-many-arguments

        self._embeddings = embeddings
        self._corr_threshold = corr_threshold
        self._corr_threshold_repl_value = corr_threshold_repl_value
        self._overlap_score = overlap_score
        self._overlap_score_eps = overlap_score_eps
        self._pathways : typing.Optional[PathwaysDict] = None

        # Check values
        if self._overlap_score < 1.0:
            raise ValueError("Overlap score must be greater or equal to 1.0.")

        self._check_embeddings()

    def _check_embeddings(self) -> None:

        # Check that the lists of floats have the same length
        ref_len = None
        for k, v in self._embeddings.items():
            if ref_len is None:
                ref_len = len(v)
            elif len(v) != ref_len:
                raise ValueError(f"Inside embeddings, item {k} has a different"
                                 + f"number of elements ({len(v)}) than other"
                                 + f"items ({ref_len}).")

    @property
    def corr_threshold(self) -> float:
        """Correlation threshold."""
        return self._corr_threshold

    @property
    def overlap_score(self) -> float:
        """Overlape score."""
        return self._overlap_score

    def comp_corr(self, a: EmbArr, b: EmbArr) -> float:
        """Computes correlation between two embeddings a and b.
        
        Args:
            a: First pathway embedding.
            b: Second pathway embedding.
            
        Returns:
            The computed correlation.
        """

        # Compute correlation (matrix nxn, n being the number of elements in a
        # or b.
        corr_dist = 1 - (scipy.spatial.distance.cdist(a, b, 'correlation'))

        # Consider only max values (=> reduce dimension)
        corr_dist = corr_dist.max(axis=1)

        # Set small values to 0.0
        corr_dist[corr_dist < self._corr_threshold] = 0.0

        # Apply overlap score
        corr_dist[corr_dist >= (1.0 - self._overlap_score_eps)] = \
                self.overlap_score

        # Set in-between values to fixed value
        if self._corr_threshold_repl_value > 0.0:
            corr_dist[(corr_dist >= self._corr_threshold)
                      & (corr_dist < (1.0 - self._overlap_score_eps))] = \
                              self._corr_threshold_repl_value

        return float(numpy.mean(corr_dist))

    def get_items_embeddings(self, items: set[str]) -> EmbArr:
        """Select a set of items inside the provided embeddings.
        
        Args:
            items: The set of items for which to retrieve embeddings.
            
        Returns:
            The selected embeddings.
        """
        logger.debug("Build items embeddings.")
        selected_items = filter(lambda i: i in items, self._embeddings.keys())
        embeddings = numpy.array([self._embeddings[i] for i in selected_items],
                              dtype=numpy.float32)
        return embeddings

    def set_pathways(self, pathways :PathwaysDict) -> None:
        """Declares the pathways.
        
        Sets the pathways to use for computation.
        Side effect: previous computed pathway embeddings and pathway scores are
        reset.
        
        Args:
            pathways: dictionary with pathway IDs as keys and list of items as
            values.
        """
        self._pathways = pathways
        self._pw_emb = None
        self._pw_scores = None

    def get_pathway_keys(self) -> list[str]:
        """Gets the stored pathway IDs.
        
        Returns:
            The list of pathway IDs.
        """
        if self._pathways is None:
            raise RuntimeError("No pathways have been set.")
        return list(self._pathways.keys())

    def get_pathway_embeddings(self) -> dict[str, EmbArr]:
        """Gets the computed pathway embeddings.
        
        Computes the pathway embeddings, base on the provided embeddings and the
        list of pathways.
        
        Returns:
            A dictionary with pathway IDs as keys and embedding arrays as
            values.
        """

        if self._pw_emb is None:
            logger.debug("Build pathway embeddings.")
            if self._pathways is None:
                raise RuntimeError("Please, first set the pathways with the" +
                                   " set_pathways() method.")
            self._pw_emb = {}
            for key, items in self._pathways.items():
                self._pw_emb[key] = self.get_items_embeddings(set(items))

        return self._pw_emb

    def get_pathway_embedding(self, key: str) -> EmbArr:
        """Gets the embedding array of one particular pathway.
        
        Args:
            key: The ID of the targeted pathway.
            
        Returns:
            The embedding array of the targeted pathway.
        """

        return self.get_pathway_embeddings()[key]

    def compute_pathway_score(self, key: str, embeddings: EmbArr) -> float:
        """Computes the score of one pathway.
        
        Args:
            key: The ID of the targeted pathway.
            embeddings: The embeddings array with which to compute correlation.
        
        Returns:
            The correlation between the pathway's embeddings and the provided
            embeddings.
        """
        return self.comp_corr(embeddings, self.get_pathway_embedding(key))

    def compute_pathway_scores(self, embeddings: EmbArr) -> None:
        """Computes the scores of all pathways.
        
        Computes for each pathway, the correlation between its embeddings and
        the provided embeddings.

        Args:
            embeddings: The embeddings array with which to compute correlation.
            
        Returns:
            Nothing.
        """
        self._pw_scores = {}
        logger.debug("Compute pathways' scores.")
        for key, emb in tqdm.tqdm(self.get_pathway_embeddings().items(),
                                  desc="Pathways scoring"):
            self._pw_scores[key] = self.comp_corr(embeddings, emb)

    def get_computed_pathway_scores(self) -> typing.Optional[dict[str, float]]:
        """Returns the pathway scores computed by compute_pathway_scores().
        
        Returns:
            The scores.
        """
        return self._pw_scores
