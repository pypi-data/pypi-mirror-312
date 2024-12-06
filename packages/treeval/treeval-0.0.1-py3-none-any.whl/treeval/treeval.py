"""Treeval tree evaluation method."""

from __future__ import annotations

from typing import TYPE_CHECKING
from warnings import warn

import numpy as np

from .metrics import BERTScore, ExactMatch, Levenshtein
from .utils import (
    _average_tree_list_scores,
    _reduce_tree_results_to_scores,
    _tree_metrics_to_results,
    compute_matching_from_score_matrix,
    count_dictionary_nodes,
    get_unique_leaf_values,
    merge_dicts,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from .metrics import TreevalMetric


# Precision/Recall/F1 are appended "nodes"/"leaves" to avoid confusion with the same
# metrics being computed on the leaves results. When aggregating results, this could
# mess up results.
PRECISION_NODE_KEY = "precision_node"
RECALL_NODE_KEY = "recall_node"
F1_NODE_KEY = "f1_node"
PRECISION_LEAF_KEY = "precision_leaf"  # TODO renaming value precision?
RECALL_LEAF_KEY = "recall_leaf"
F1_LEAF_KEY = "f1_leaf"
TREEVAL_SCORE_KEY = "treeval_score"
_PRF_METRIC_NAMES = {
    PRECISION_NODE_KEY,
    RECALL_NODE_KEY,
    F1_NODE_KEY,
    PRECISION_LEAF_KEY,
    RECALL_LEAF_KEY,
    F1_LEAF_KEY,
    TREEVAL_SCORE_KEY,
}
# Treeval score
TREEVAL_SCORE_TYPES_METRICS = {
    "integer": ["exact_match"],
    "number": ["exact_match"],
    "boolean": ["exact_match"],
    "string": ["levenshtein", "bertscore"],
    (): ["exact_match"],
}


def treeval(
    predictions: Sequence[dict],
    references: Sequence[dict],
    schema: dict,
    metrics: dict[str, TreevalMetric],
    tree_metrics: dict,
    aggregate_results_per_metric: bool = False,
    aggregate_results_per_leaf_type: bool = False,
    hierarchical_averaging: bool = False,
) -> dict:
    """
    Treeval evaluation method.

    :param predictions: list of dictionary predictions.
    :param references: list of dictionary references.
    :param schema: schema of the tree as a dictionary specifying each leaf type. The
        references must all follow this exact tree structure, while the predictions can
        have mismatching branches which will impact the tree precision/recall/f1 scores
        returned by the method.
    :param metrics: metrics to use to evaluate the leaves of the trees.
    :param tree_metrics: dictionary with the same schema/structure as ``schema``
        specifying at each leaf the set of metrics to use for evaluate them, referenced
        by their names as provided in ``metrics``. See the
        :py:func:`treeval.create_tree_metrics` method to easily create this argument by
        mapping leaf types to metrics.
    :param aggregate_results_per_metric: averages the final results per metric. Enabling
        this option will call the :py:func:`treeval.aggregate_results_per_metric` method
        on the final tree results. (default: ``False``)
    :param aggregate_results_per_leaf_type: averages the final results per node type.
        Enabling this option will call the
        :py:func:`treeval.aggregate_results_per_leaf_type` method on the final tree
        results. (default: ``False``)
    :param hierarchical_averaging: argument to be used when one of the
        ``aggregate_results_per_metric`` or ``aggregate_results_per_leaf_type`` options
        is enabled. See the documentation of the
        :py:func:`treeval.aggregate_results_per_metric` and
        :py:func:`treeval.aggregate_results_per_leaf_type` for the complete explanation.
        (default: ``False``)
    :return: the metrics results. The returned dictionary will have the same tree
        structure as the provided ``schema`` if ``aggregate_results_per_metric`` or
        ``aggregate_results_per_leaf_type`` are disabled, otherwise it will map metrics
        and/or leaf types to average results over all leaves.
    """
    # Check number of predictions/references
    if len(predictions) != len(references):
        msg = "The number of predictions must be equal to the number of references."
        raise ValueError(msg)

    # Recursively parses the schema and computes the metrics scores at the leaves
    results = _recursive_parse(predictions, references, schema, metrics, tree_metrics)

    # Compute the Treeval score
    results_aggregated_per_metrics = _aggregate_results_per_metric(
        results,
        schema,
        tree_metrics,
        metrics,
        hierarchical_averaging=hierarchical_averaging,
    )
    results[TREEVAL_SCORE_KEY] = _treeval_score(
        results_aggregated_per_metrics.copy(), metrics
    )

    # Aggregate per metric and/or type
    if aggregate_results_per_metric:
        if aggregate_results_per_leaf_type:
            warn(
                "treeval: you set both the `aggregate_results_per_metric` and `"
                "aggregate_results_per_leaf_type` arguments as `True`. The results can "
                "be summarized with one method only. `aggregate_results_per_metric` "
                "will take precedence.",
                stacklevel=2,
            )
        results_aggregated_per_metrics[TREEVAL_SCORE_KEY] = results[TREEVAL_SCORE_KEY]
        return results_aggregated_per_metrics
    if aggregate_results_per_leaf_type:
        return _aggregate_results_per_leaf_type(
            results, schema, metrics, hierarchical_averaging=hierarchical_averaging
        )

    return results


def create_treeval_score_default_tree_metrics(
    schema: dict,
) -> tuple[dict, dict[str, TreevalMetric]]:
    """
    Create the ``tree_metrics`` of a schema with the default Treeval score metrics.

    This method calls the :py:func:`treeval.create_tree_metrics` to create a tree
    metrics with the default metrics as introduced in the :ref:`The Treeval score`
    page. It also returns the default metrics modules initialized.

    :param schema: schema of the tree as a dictionary specifying each leaf type. The
        references must all follow this exact tree structure, while the predictions can
        have mismatching branches which will impact the tree precision/recall/f1 scores
        returned by the method.
    :return: the treeval score results, a dictionary with the ``treeval_score`` entry
        and node/leaf precision/recall/f1 scores.
    """
    # metrics are initialized here, as they might require external dependencies that
    # shouldn't be required to run the rest of the library. If required dependencies are
    # missing, exceptions will be raised when loading the metrics.
    metrics = {
        m.name: m
        for m in {
            ExactMatch(),
            Levenshtein(),
            BERTScore(),
        }
    }

    # Create tree metrics
    return create_tree_metrics(
        schema, types_metrics=TREEVAL_SCORE_TYPES_METRICS
    ), metrics


def _treeval_score(
    results: dict[str, float], metrics: dict[str, TreevalMetric]
) -> float:
    """
    Compute the Treeval score from metrics-aggregated results.

    The Treeval score is the product of the average of the metrics scores, the node F1
    and the leaf F1 scores.

    :param results: results from the :py:func:`treeval.treeval` method aggregated per
        metrics.
    :param metrics: list of modules used for the ``results``. This method requires them
        to normalize metrics scores.
    :return: the treeval score result.
    """
    # Normalize metrics scores and computes treeval score
    scores = []
    for metric_name, metric_score in results.copy().items():
        if metric_name in _PRF_METRIC_NAMES or metric_score is None:
            continue
        if metrics[metric_name].score_range != (0, 1):
            low_bound, high_bound = metrics[metric_name].score_range
            results[metric_name] = (
                min(max(metric_score, low_bound), high_bound) - low_bound
            ) / (high_bound - low_bound)
        if not metrics[metric_name].higher_is_better:
            results[metric_name] = 1 - results[metric_name]
        scores.append(results[metric_name])

    return sum(scores) / len(scores) * results[F1_NODE_KEY] * results[F1_LEAF_KEY]


def _recursive_parse(
    predictions: Sequence[dict | Any],
    references: Sequence[dict | Any],
    schema: dict | str,
    metrics: dict[str, TreevalMetric],
    tree_metrics: dict | list[str],
    pr_cache: list[int] | None = None,
) -> dict | list[list[dict]]:
    # Returns the evaluation metric score as a tree with metrics results averaged
    # over the same leaf values of all predictions/references pairs.
    # This method is recursive and supports nested dictionaries and lists of items of
    # specific types, including lists of nested dictionaries.

    # Leaf (basic case) --> compute metrics on values
    # Choice among list satisfy this condition
    if not isinstance(predictions[0], (dict, list)):  # -> {metric_name: score}
        return {
            metric_name: metrics[metric_name].compute(predictions, references)
            for metric_name in tree_metrics
        }

    # List --> match the elements in the lists of each reference/prediction pair
    # Lists of choice do not fall in this condition as they are evaluated as single
    # leaves in the above if condition.
    # TODO handle multilabel classification
    if isinstance(predictions[0], list):
        # mean of aligned element match scores

        # Computes metrics on all combinations of ref/pred items within the lists,
        # independently. Batching is not possible here as the metrics are expected to
        # return the mean over all the items within the batch, whereas we need all the
        # individual scores in order to perform alignment to keep the best scores.
        # If getting individual scores is possible, batching would be feasible by
        # processing the (n * m) combinations in parallel for the items in the lists of
        # each pair of ref/pred. Batching multiple pairs of ref/pred is not possible as
        # lists usually have different sequence lengths, or it would require to keep
        # track of each number of combinations (n * m) per ref/pred pair.
        # If the items of the list are dictionaries, `tree_metrics` is a dictionary
        # with sets of metrics names as leaf values. Otherwise, it is a set of
        # metrics names.
        is_list_of_dicts, _idx = False, 0
        while _idx < len(predictions):
            if len(predictions[0]) > 0:
                is_list_of_dicts = isinstance(predictions[_idx][0], dict)
                break
        if is_list_of_dicts:
            __metrics_set = {TREEVAL_SCORE_KEY}
            results = _tree_metrics_to_results(tree_metrics)
        else:
            __metrics_set = tree_metrics
            results = {metric_name: [] for metric_name in __metrics_set}
        for pred, ref in zip(predictions, references):  # unbatched
            # Create the matrices storing the metrics results
            # `metrics_results` stores the "raw"/complete results of each metric.
            # `metrics_scores` stores the score results of each metric.
            # If the items of the list are dictionaries, `tree_metrics` is a dictionary
            # with sets of metrics names as leaf values. Otherwise, it is a set of
            # metrics names.
            metrics_results = [[] for _ in range(len(ref))]  # (n,m,{name: res})
            metrics_scores = {  # {metric_name: (n,m)}, score for assignment only
                metric: [[] for _ in range(len(ref))] for metric in __metrics_set
            }
            pr_caches = [[[0] * 6 for _ in range(len(pred))] for _ in range(len(ref))]
            # TODO count difference of lengths between two lists -> find way to penalize
            #  - report an additional precision/recall/F1 score for sets (abs(diff));
            #  - negatively impact the node precision/recall, either per number of
            #    missing/additional elements, or number of nodes when elements are
            #    trees;
            #  - negatively impact the metrics scores, but do it at the end from the
            #    unbiased metrics scores and number of FP/FN.

            # Compute metrics, unbatched as we need to match the references/predictions.
            # For simplicity reasons, the precision/recall/f1 of dictionary items (when
            # list of dictionaries) are not computed. The precision/recall/f1 returned
            # by treeval stops at the leaves, lists of dictionaries are considered as
            # leaves whatever their depths may be.
            # (n,m) --> {metric_name: metric_results_dict}
            for ref_item_idx, ref_i in enumerate(ref):
                for pred_item_idx, pred_i in enumerate(pred):
                    # Compute metrics
                    results_pair = _recursive_parse(
                        [pred_i],
                        [ref_i],
                        schema[0],  # provides either a type or a dict (list of dicts)
                        metrics,
                        tree_metrics,  # already list of metric names
                        pr_caches[ref_item_idx][pred_item_idx],
                    )

                    # Reduce metrics results to metrics scores only and save raw scores.
                    # Adds the score to the matrix.
                    # If the items are dictionaries, we just use the treeval score for
                    # the assignment weights.
                    if is_list_of_dicts:
                        # Compute prf, need to be done here as not done at the end of
                        # _recursive_parse as not identified as root node
                        results_pair.update(
                            _compute_precision_recall_f1(
                                pr_caches[ref_item_idx][pred_item_idx]
                            )
                        )
                        metrics_scores[TREEVAL_SCORE_KEY][ref_item_idx].append(
                            _treeval_score(
                                _aggregate_results_per_metric(
                                    results_pair, schema[0], tree_metrics, metrics
                                ),
                                metrics,
                            )
                        )
                        _reduce_tree_results_to_scores(results_pair, schema[0], metrics)
                    # Otherwise we use the average of the metrics scores.
                    else:
                        for metric_name, metric_results in results_pair.items():
                            metric_score = metrics[metric_name].get_metric_score(
                                metric_results
                            )
                            metrics_scores[metric_name][ref_item_idx].append(
                                metric_score
                            )
                            results_pair[metric_name] = metric_score

                    metrics_results[ref_item_idx].append(results_pair)

            # Normalize metrics scores matrices between within [0, 1]
            # TODO support non-unidirectional metrics (when not higher/lower better)
            if not is_list_of_dicts:
                for metric_name in metrics_scores:
                    metric_score_array = np.array(metrics_scores[metric_name])
                    if len(metrics_scores) > 1:  # no need if only one metric
                        if metrics[metric_name].score_range != (0, 1):
                            low_bound, high_bound = metrics[metric_name].score_range
                            metric_score_array = (
                                metric_score_array.clip(low_bound, high_bound)
                                - low_bound
                            ) / (high_bound - low_bound)
                        if not metrics[metric_name].higher_is_better:
                            metric_score_array = (
                                np.ones_like(metric_score_array) - metric_score_array
                            )
                    metrics_scores[metric_name] = metric_score_array
            else:
                metrics_scores[TREEVAL_SCORE_KEY] = np.array(
                    metrics_scores[TREEVAL_SCORE_KEY]
                )

            # Average the normalized arrays
            if len(metrics_scores) > 1:  # [(n,m)] --> (s,n,m) --> (n,m)
                metrics_scores_average = np.mean(
                    np.stack(list(metrics_scores.values()), axis=0), axis=0
                )
            else:
                metrics_scores_average = next(iter(metrics_scores.values()))

            # Computes the assignment/pairs of reference/prediction items
            pairs_idx = compute_matching_from_score_matrix(metrics_scores_average)
            if is_list_of_dicts:
                for ref_idx, pred_idx in zip(*pairs_idx):
                    pair_score = metrics_results[ref_idx][pred_idx]
                    results = merge_dicts(results, {k: pair_score[k] for k in results})
                    for i in range(len(pr_cache)):
                        pr_cache[i] += pr_caches[ref_idx][pred_idx][i]
                # Update pr cache
                if len(pred) > len(ref):  # penalize precision
                    idx_excess = list(range(len(pred)))
                    for pred_idx in reversed(pairs_idx[1]):
                        del idx_excess[pred_idx]
                    for idx in idx_excess:
                        pr_cache[0] += count_dictionary_nodes(pred[idx])
                elif len(pred) < len(ref):  # penalize recall
                    idx_excess = list(range(len(ref)))
                    for ref_idx in reversed(pairs_idx[0]):
                        del idx_excess[ref_idx]
                    for idx in idx_excess:
                        pr_cache[2] += count_dictionary_nodes(ref[idx])
            else:
                for ref_idx, pred_idx in zip(*pairs_idx):
                    for metric_name in metrics_scores:
                        results[metric_name].append(
                            metrics_results[ref_idx][pred_idx][metric_name]
                        )
                # Update pr cache
                if len(pred) > len(ref):  # penalize precision
                    pr_cache[0] += len(pred) - len(ref)
                elif len(pred) < len(ref):  # penalize recall
                    pr_cache[2] += len(ref) - len(pred)

        # Average, return {metric_res} only
        # We can't return other metric elements as we didn't batch the computations, and
        # we can't assume how to average them, so we only cover the score.
        if is_list_of_dicts:
            _average_tree_list_scores(results)
            return results
        return {
            metric_name: {metric_name: sum(metric_scores) / len(metric_scores)}
            for metric_name, metric_scores in results.items()
        }

    # Dictionary --> recursive parsing
    results = {}
    root_node = False
    if pr_cache is None:  # root node
        root_node = True
        pr_cache = [0] * 6  # counts TT/TP/FN (nodes) + TP/FN/FP (leaf)
    # Counts the total number of nodes (at current branch/depth) before parsing the
    # tree batching all preds/refs
    pr_cache[0] += sum(len(pred) for pred in predictions)
    for node_name, node_type in schema.items():
        # Gathers pairs of refs/preds that are both present.
        # Count precision/recall scores on nodes/leaves
        node_predictions, node_references = [], []
        for pred, ref in zip(predictions, references):
            # Node is in both
            if node_name in pred:
                pred_leaf_val = pred[node_name]
                ref_leaf_val = ref[node_name]

                # TP: leaf in both ref and pred
                if pred_leaf_val is not None and ref_leaf_val is not None:
                    node_predictions.append(pred_leaf_val)
                    node_references.append(ref_leaf_val)  # must always be in ref
                    if not isinstance(node_type, dict):
                        pr_cache[3] += 1  # increments leaf TP count

                # FN: leaf in ref missing from pred
                # leaf prf are only computed on leaves, excluding intermediates nodes
                elif pred_leaf_val is None and ref_leaf_val is not None:
                    pr_cache[4] += (
                        count_dictionary_nodes(node_type, only_leaves=True)
                        if isinstance(node_type, dict)
                        else 1
                    )
                    if isinstance(node_type, dict):
                        pr_cache[2] += count_dictionary_nodes(node_type)  # node FN

                # FP: leaf in pred not present in ref (unexpected)
                elif pred_leaf_val is not None and ref_leaf_val is None:
                    if isinstance(pred_leaf_val, dict):
                        pr_cache[5] += count_dictionary_nodes(
                            pred_leaf_val, only_leaves=True
                        )
                        pr_cache[0] += count_dictionary_nodes(
                            pred_leaf_val
                        )  # total nodes
                    else:
                        pr_cache[5] += 1

                pr_cache[1] += 1  # increments nodes TP count

            # node false negative += total number of children nodes + 1 (current node)
            else:
                pr_cache[2] += (
                    count_dictionary_nodes(node_type) + 1
                    if isinstance(node_type, dict)
                    else 1
                )
                if isinstance(node_type, dict):
                    pr_cache[4] += count_dictionary_nodes(node_type, only_leaves=True)

        if len(node_predictions) > 0:
            results[node_name] = _recursive_parse(
                node_predictions,
                node_references,
                node_type,
                metrics,
                tree_metrics[node_name],
                pr_cache,
            )
        else:
            results[node_name] = None
            # TODO otherwise None? --> handle None cases + docs

    # Compute the precision, recall and f1 scores of the predicted nodes/leaves
    if root_node:
        results.update(_compute_precision_recall_f1(pr_cache))

    return results


def _compute_precision_recall_f1(pr_cache: list[int]) -> dict[str, float]:
    """
    Compute the node and leaf precision/recall/F1 scores.

    :param pr_cache: true/false positives/negatives for nodes/leaves.
    :return: dictionary holding the node and leaf precision/recall/F1 scores.
    """
    results = {}

    # tp + fn should be equal to len(references) * count_dictionary_nodes(schema)
    # there is no tn for nodes, for leaves yes (`None` leaf values in references)
    total_num_nodes, tp_node, fn_node, tp_leaf, fn_leaf, fp_leaf = pr_cache

    # Add node precision/recall/f1 scores to the results
    fp_node = total_num_nodes - tp_node  # predicted nodes not in references
    precision_node = tp_node / (tp_node + fp_node)
    recall_node = tp_node / (tp_node + fn_node)
    results[PRECISION_NODE_KEY] = precision_node
    results[RECALL_NODE_KEY] = recall_node
    results[F1_NODE_KEY] = __compute_f1(precision_node, recall_node)

    # Add leaf precision/recall/f1 scores to the results
    # cases where no None at all --> 1 scores
    # num_leaves = tn_leaf + tp_leaf + fn_leaf + fp_leaf
    precision_leaf = tp_leaf / (tp_leaf + fp_leaf) if tp_leaf + fp_leaf > 0 else 1
    recall_leaf = tp_leaf / (tp_leaf + fn_leaf) if tp_leaf + fn_leaf > 0 else 1
    results[PRECISION_LEAF_KEY] = precision_leaf
    results[RECALL_LEAF_KEY] = recall_leaf
    results[F1_LEAF_KEY] = __compute_f1(precision_leaf, recall_leaf)

    return results


def __compute_f1(precision: float, recall: float) -> float:
    return (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )


def create_tree_metrics(
    schema: dict,
    leaves_metrics: dict | None = None,
    types_metrics: dict[str | tuple, Sequence[str]] | None = None,
    exclusive_leaves_types_metrics: bool = False,
) -> dict:
    """
    Create the ``tree_metrics`` of a schema from specific leaf names and/or types.

    An error is raised if a leaf cannot be evaluated by any of the metrics provided in
    ``leaves_metrics`` and ``types_metrics``.

    :param schema: structure of the tree as a dictionary specifying each leaf type.
    :param leaves_metrics: dictionary with the same tree structure as the provided
        ``schema`` specifying the metrics to compute for specific leaves.
        (default: ``None``)
    :param types_metrics: dictionary mapping the types specified in the provided
        ``schema`` to the metrics to compute for the leaves of these types. All types
        names must be strings, except the empty tuple ``()`` which is used for choice
        lists. (default: ``None``)
    :param exclusive_leaves_types_metrics: an option allowing to make the metrics
        specified in ``leaves_metrics`` to be exclusive to certain leaves, excluding the
        metrics that should cover them specified in the ``types_metrics`` argument.
        Example: for the ``schema`` ``{"foo": "integer"}``, ``leaves_metrics``
        ``{"foo": "accuracy"}`` and ``types_metrics`` ``{"foo": "mse"}``, if this option
        is enabled, the method will return the ``{"foo": {"accuracy"}}`` tree metrics as
        the metric specified in ``leaves_metrics`` will take precedence. Otherwise, the
        method will return ``{"foo": {"accuracy", "mse"}}``, combining the metrics from
        the two arguments. This option can be especially useful when some specific
        leaves are expected to be evaluated with specific metrics. (default: ``False``)
    :return: tree identical to ``schema`` where leaf values reference to the **set** of
        names of metrics to use to evaluate them.
    """
    # Safety check
    if not leaves_metrics:
        leaves_metrics = {}
    if not types_metrics:
        types_metrics = {}

    tree_metrics = {}
    for node_name, node_type in schema.items():
        if isinstance(node_type, list):
            node_type_tmp = node_type[0] if len(node_type) == 1 else ()  # else choice
        else:
            node_type_tmp = node_type
        if isinstance(node_type_tmp, dict):
            tree_metrics[node_name] = create_tree_metrics(
                node_type_tmp,
                leaves_metrics.get(node_name, {}),
                types_metrics,
                exclusive_leaves_types_metrics,
            )
        else:
            leaf_metrics = leaves_metrics.get(node_name, []).copy()
            if not exclusive_leaves_types_metrics or len(leaf_metrics) == 0:
                leaf_metrics += types_metrics.get(node_type_tmp, [])
            for metric_name in leaf_metrics:
                if metric_name in _PRF_METRIC_NAMES:
                    msg = (
                        f"The `{metric_name}` metric name cannot be used, please rename"
                        f" it. Treeval forbids the use of {_PRF_METRIC_NAMES} "
                        "metric names as they are used to computed on the nodes at the "
                        "tree-level."
                    )
                    raise ValueError(msg)
            if len(leaf_metrics) == 0:
                msg = (
                    "Incompatible schema/leaves_metrics/types_metrics provided. The "
                    f"leaf `{node_name}` is not covered by any metric and cannot be "
                    "evaluated."
                )
                raise ValueError(msg)
            tree_metrics[node_name] = set(leaf_metrics)

    return tree_metrics


def _aggregate_results_per_metric(
    results: dict,
    schema: dict,
    tree_metrics: dict,
    metrics: dict[str, TreevalMetric],
    hierarchical_averaging: bool = False,
) -> dict[str, float]:
    """
    Aggregate the tree treeval results per metric.

    This method will return a single-depth dictionary mapping each metric of the
    provided ``results`` to the average of its scores found within the results tree.

    :param results: non-aggregated results from the :py:func:`treeval.treeval` method.
    :param schema: schema of the tree as a dictionary specifying each leaf type. The
        references must all follow this exact tree structure, while the predictions can
        have mismatching branches which will impact the tree precision/recall/f1 scores
        returned by the method.
    :param tree_metrics: dictionary with the same schema/structure as ``results``
        specifying at each leaf the set of metrics to use for evaluate them, referenced
        by their names as found in the ``results``.
    :param hierarchical_averaging: averages the metrics scores at each branch depth. If
        this option is enabled, the scores of the metrics will be averaged at each
        branch of nested dictionaries. These averages will be included in the metrics
        scores of the parent node as a single value, as opposed to including all the
        score metrics of the branch to compute the average of the parent node.
        This option allows to give more importance in the final results to the scores of
        the leaves at lower depths, closer to the root.
        Example: ``{"n1": 0, "n2": 1, "n3": {"n4": 0, "n5": 1}}`` represents the scores
        of a given metric for this dictionary structure. If hierarchical averaging is
        enabled, the scores for the metric (root node) will be computed from scores of
        the ``"n1"``, ``"n2"`` nodes and the average of the nodes within the ``"n3"``
        branch, i.e. average of ``[0, 0, 0.5]``. If hierarchical averaging is enabled,
        the average is computed from all the scores in the tree with no distinction
        towards the depths of the leaves, e.g. ``[0, 0, 0, 1]`` in the previous
        examples. (default: ``False``)
    :return: single-depth dictionary mapping each metric of the provided ``results`` to
        the average of its scores found within the results tree.
    """
    # Gather the scores of all individual metrics in all leaves.
    metrics_results = __aggregate_results_per_metric(
        results, schema, metrics, hierarchical_averaging=hierarchical_averaging
    )

    # If hierarchical averaging is enabled, the averaging is already done in the child
    # method. Otherwise, it returned the list of all scores that we need to average.
    if not hierarchical_averaging:
        metrics_results = {
            metric_name: sum(scores) / len(scores) if len(scores) > 0 else None
            for metric_name, scores in metrics_results.items()
        }

    # Insert `None` entries for metrics of node results that weren't computed once
    unique_metrics = get_unique_leaf_values(tree_metrics)
    for metric_name in unique_metrics:
        if metric_name not in metrics_results:
            metrics_results[metric_name] = None

    # Re-include the tree precision/recall/f1 scores in the results to return.
    # These elements might not be in the `results` when this method is called to
    # aggregate results in lists of dictionaries before assignment.
    for prf_key in _PRF_METRIC_NAMES:
        if results_prf := results.get(prf_key):
            metrics_results[prf_key] = results_prf

    return metrics_results


def __aggregate_results_per_metric(
    results: dict,
    schema: dict,
    metrics: dict[str, TreevalMetric],
    hierarchical_averaging: bool = False,
) -> dict[str, float | list[float]]:
    # Same as _aggregate_results_per_metric but recursive and discarding
    # precision/recall/f1 entries that are added at the end.

    # Gather scores per metric name
    metrics_results = {}  # {metric_name: [results]}
    for node_name, node_value in schema.items():
        results_node = results[node_name]
        if results_node is None:
            continue
        # Dicts and sets of dicts
        is_set_of_dicts = isinstance(node_value, list) and isinstance(
            node_value[0], dict
        )
        if isinstance(node_value, dict) or is_set_of_dicts:
            # Need to check that the keys of the branch results are all already present
            # in the metrics_results dictionary before merging them
            branch_results = __aggregate_results_per_metric(
                results_node,
                node_value[0] if is_set_of_dicts else node_value,
                metrics,
                hierarchical_averaging=hierarchical_averaging,
            )
            for branch_key in branch_results:
                if branch_key not in metrics_results:
                    metrics_results[branch_key] = []
            metrics_results = merge_dicts(metrics_results, branch_results)
        # Everything else
        else:
            for metric_name, metric_results in results_node.items():
                if metric_name not in metrics_results:
                    metrics_results[metric_name] = []
                metrics_results[metric_name].append(
                    metrics[metric_name].get_metric_score(metric_results)
                )

    # Averages the scores of the current branch if hierarchical averaging
    if hierarchical_averaging:
        return {
            metric_name: sum(scores) / len(scores)
            for metric_name, scores in metrics_results.items()
            if len(scores) > 0
        }
    return metrics_results


def _aggregate_results_per_leaf_type(
    results: dict,
    schema: dict,
    metrics: dict[str, TreevalMetric],
    hierarchical_averaging: bool = False,
) -> dict[str, dict[str, float]]:
    """
    Aggregate the tree treeval results per leaf type.

    This method will return a single-depth dictionary mapping each metric of the
    provided ``results`` to the average of its scores found within the results tree.

    :param results: non-aggregated results from the :py:func:`treeval.treeval` method.
    :param schema: structure of the tree as a dictionary specifying each leaf type.
    :param hierarchical_averaging: averages the metrics scores at each branch depth. If
        this option is enabled, the scores of the metrics will be averaged at each
        branch of nested dictionaries. These averages will be included in the metrics
        scores of the parent node as a single value, as opposed to including all the
        score metrics of the branch to compute the average of the parent node.
        This option allows to give more importance in the final results to the scores of
        the leaves at lower depths, closer to the root.
        Example: ``{"n1": 0, "n2": 1, "n3": {"n4": 0, "n5": 1}}`` represents the scores
        of a given metric for this dictionary structure. If hierarchical averaging is
        enabled, the scores for the metric (root node) will be computed from scores of
        the ``"n1"``, ``"n2"`` nodes and the average of the nodes within the ``"n3"``
        branch, i.e. average of ``[0, 0, 0.5]``. If hierarchical averaging is enabled,
        the average is computed from all the scores in the tree with no distinction
        towards the depths of the leaves, e.g. ``[0, 0, 0, 1]`` in the previous
        examples. (default: ``False``)
    :return: single-depth dictionary mapping each leaf type of the provided ``results``
        to the average of its scores found within the results tree.
    """
    # Gather the scores of all individual metrics in all leaves.
    results_types = __aggregate_results_per_leaf_type(
        results, schema, metrics, hierarchical_averaging=hierarchical_averaging
    )

    # If hierarchical averaging is enabled, the averaging is already done in the child
    # method. Otherwise, it returned the list of all scores that we need to average.
    if not hierarchical_averaging:
        results_types = {
            type_name: {
                met: sum(scores) / len(scores) if len(scores) > 0 else None
                for met, scores in metrics_scores.items()
            }
            if metrics_scores is not None
            else None
            for type_name, metrics_scores in results_types.items()
        }

    # Re-include the tree precision/recall/f1 scores in the results to return
    for prf_key in _PRF_METRIC_NAMES:
        if results_prf := results.get(prf_key):
            results_types[prf_key] = results_prf

    return results_types


def __aggregate_results_per_leaf_type(
    results: dict,
    schema: dict,
    metrics: dict[str, TreevalMetric],
    hierarchical_averaging: bool = False,
) -> dict[str, dict[str, float | list[float]]]:
    # Same as _aggregate_results_per_leaf_type but recursive and discarding
    # precision/recall/f1 entries that are added at the end.

    # Gather scores per metric name
    results_types = {}  # {type: {metric: [results]}}
    types_none = set()
    for node_name, type_name in schema.items():
        results_node = results[node_name]
        if isinstance(type_name, dict):
            # Need to check that the keys of the branch results are all already present
            # in the metrics_results dictionary before merging them
            branch_results = __aggregate_results_per_leaf_type(
                results_node,
                type_name,
                metrics,
                hierarchical_averaging=hierarchical_averaging,
            )
            for key_branch, metrics_branch in branch_results.items():
                if metrics_branch is None:
                    types_none.add(key_branch)
                    continue
                if key_branch not in results_types:
                    results_types[key_branch] = {}
                for key_metric_branch in metrics_branch:
                    if key_metric_branch not in results_types[key_branch]:
                        results_types[key_branch][key_metric_branch] = []
            results_types = merge_dicts(
                results_types, branch_results, discard_none=True
            )
        elif results_node is not None:
            if type_name not in results_types:
                results_types[type_name] = {}
            for metric_name, metric_results in results_node.items():
                if metric_name not in results_types[type_name]:
                    results_types[type_name][metric_name] = []
                results_types[type_name][metric_name].append(
                    metrics[metric_name].get_metric_score(metric_results)
                )

        else:
            types_none.add(type_name)

    # Insert `None` entries for types that weren't evaluated once
    for type_name in types_none:
        if type_name not in results_types:
            results_types[type_name] = None

    # Compute the mean of each type scores
    if hierarchical_averaging:
        return {
            type_name: {
                met: sum(scores) / len(scores) if len(scores) > 0 else None
                for met, scores in metrics_scores.items()
            }
            if metrics_scores is not None
            else None
            for type_name, metrics_scores in results_types.items()
        }
    return results_types
