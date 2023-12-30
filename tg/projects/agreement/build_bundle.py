from tg.grammar_ru.features import (
    PyMorphyFeaturizer,
    SlovnetFeaturizer,
    SyntaxTreeFeaturizer,
    SyntaxStatsFeaturizer, SnowballFeaturizer,
)
from tg.grammar_ru.common import Loc
from yo_fluq_ds import *

from tg.grammar_ru.corpus import CorpusBuilder
from tg.projects.agreement.adjectiveless_pymorphy_featurizer import (
    AdjectivelessPyMorphyFeaturizer,
)
from tg.projects.agreement.bundle import (
    AdjAgreementTrainIndexBuilder,
    NounAgreementTrainIndexBuilder,
)


INDEXED_BUNDLE_PATH = (
    Loc.bundles_path / "agreement/prepare/adj_books&pub_60K_balanced/raw/raw.zip"
)
FEATURIZED_BUNDLE_PATH = (
    Loc.bundles_path / "agreement/prepare/adj_books&pub_60K_balanced/feat/feat.zip"
)


def build_index():
    index_builder = AdjAgreementTrainIndexBuilder()
    CorpusBuilder.transfuse_corpus(
        [Loc.corpus_path / "prepare/balanced/books&pub_60K_balanced_feat.zip"],
        INDEXED_BUNDLE_PATH,
        selector=index_builder,
    )


def featurize_index():
    CorpusBuilder.featurize_corpus(
        INDEXED_BUNDLE_PATH,
        FEATURIZED_BUNDLE_PATH,
        [
            # PyMorphyFeaturizer(),
            AdjectivelessPyMorphyFeaturizer(),  # PyMorphyFeaturizer(),
            # SlovnetFeaturizer(),
            # SnowballFeaturizer(),
            # SyntaxTreeFeaturizer(),
            # SyntaxStatsFeaturizer()
        ],
        6,
        True,
    )


def assemble(name, limit):
    bundle_path = Loc.bundles_path / f"agreement/{name}"
    CorpusBuilder.assemble(FEATURIZED_BUNDLE_PATH, bundle_path, limit)
    src = pd.read_parquet(bundle_path / "src.parquet")
    index = AdjAgreementTrainIndexBuilder.build_index_from_src(src)
    index.to_parquet(bundle_path / "index.parquet")
    print(index.groupby("split").size())


# def upload_bundle(name):
#     bundle_path = Loc.bundles_path / f'tsa/{name}'
#     S3Handler.upload_folder(
#         'ps-data-science-sandbox',
#         'sagemaker/tsa/datasets/' + name,
#         bundle_path)


if __name__ == "__main__":
    build_index()
    featurize_index()
    suffix = "_all_decl"
    prefix = "adj_"  #'noun_norm_e_'
    # assemble(prefix + "tiny", 1)
    # assemble(prefix + "toy", 5)
    assemble(prefix + "full", None)
    # assemble('toy'+suffix, 5)
    # assemble('mid20'+suffix, 20)
    # assemble('mid50'+suffix, 50)
    # assemble('big'+suffix, 100)
    # assemble('full'+suffix, None)
    # # upload_bundle('big')
