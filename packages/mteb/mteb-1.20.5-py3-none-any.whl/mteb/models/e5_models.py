from __future__ import annotations

from functools import partial

from mteb.encoder_interface import PromptType
from mteb.model_meta import ModelMeta, sentence_transformers_loader

E5_PAPER_RELEASE_DATE = "2024-02-08"
XLMR_LANGUAGES = [
    "afr_Latn",
    "amh_Latn",
    "ara_Latn",
    "asm_Latn",
    "aze_Latn",
    "bel_Latn",
    "bul_Latn",
    "ben_Latn",
    "ben_Beng",
    "bre_Latn",
    "bos_Latn",
    "cat_Latn",
    "ces_Latn",
    "cym_Latn",
    "dan_Latn",
    "deu_Latn",
    "ell_Latn",
    "eng_Latn",
    "epo_Latn",
    "spa_Latn",
    "est_Latn",
    "eus_Latn",
    "fas_Latn",
    "fin_Latn",
    "fra_Latn",
    "fry_Latn",
    "gle_Latn",
    "gla_Latn",
    "glg_Latn",
    "guj_Latn",
    "hau_Latn",
    "heb_Latn",
    "hin_Latn",
    "hin_Deva",
    "hrv_Latn",
    "hun_Latn",
    "hye_Latn",
    "ind_Latn",
    "isl_Latn",
    "ita_Latn",
    "jpn_Latn",
    "jav_Latn",
    "kat_Latn",
    "kaz_Latn",
    "khm_Latn",
    "kan_Latn",
    "kor_Latn",
    "kur_Latn",
    "kir_Latn",
    "lat_Latn",
    "lao_Latn",
    "lit_Latn",
    "lav_Latn",
    "mlg_Latn",
    "mkd_Latn",
    "mal_Latn",
    "mon_Latn",
    "mar_Latn",
    "msa_Latn",
    "mya_Latn",
    "nep_Latn",
    "nld_Latn",
    "nob_Latn",
    "orm_Latn",
    "ori_Latn",
    "pan_Latn",
    "pol_Latn",
    "pus_Latn",
    "por_Latn",
    "ron_Latn",
    "rus_Latn",
    "san_Latn",
    "snd_Latn",
    "sin_Latn",
    "slk_Latn",
    "slv_Latn",
    "som_Latn",
    "sqi_Latn",
    "srp_Latn",
    "sun_Latn",
    "swe_Latn",
    "swa_Latn",
    "tam_Latn",
    "tam_Taml",
    "tel_Latn",
    "tel_Telu",
    "tha_Latn",
    "tgl_Latn",
    "tur_Latn",
    "uig_Latn",
    "ukr_Latn",
    "urd_Latn",
    "urd_Arab",
    "uzb_Latn",
    "vie_Latn",
    "xho_Latn",
    "yid_Latn",
    "zho_Hant",
    "zho_Hans",
]

model_prompts = {
    PromptType.query.value: "query: ",
    PromptType.passage.value: "passage: ",
}

e5_mult_small = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/multilingual-e5-small",
        revision="fd1525a9fd15316a2d503bf26ab031a61d056e98",
        model_prompts=model_prompts,
    ),
    name="intfloat/multilingual-e5-small",
    languages=XLMR_LANGUAGES,
    open_weights=True,
    revision="fd1525a9fd15316a2d503bf26ab031a61d056e98",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=118_000_000,
    memory_usage=None,
    embed_dim=384,
    license="mit",
    max_tokens=512,
    reference="https://huggingface.co/intfloat/multilingual-e5-small",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_mult_base = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/multilingual-e5-base",
        model_prompts=model_prompts,
    ),
    name="intfloat/multilingual-e5-base",
    languages=XLMR_LANGUAGES,
    open_weights=True,
    revision="d13f1b27baf31030b7fd040960d60d909913633f",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=278_000_000,
    memory_usage=None,
    embed_dim=768,
    license="mit",
    max_tokens=514,
    reference="https://huggingface.co/intfloat/multilingual-e5-base",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_mult_large = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/multilingual-e5-large",
        revision="ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb",
        model_prompts=model_prompts,
    ),
    name="intfloat/multilingual-e5-large",
    languages=XLMR_LANGUAGES,
    open_weights=True,
    revision="ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=560_000_000,
    memory_usage=None,
    embed_dim=1024,
    license="mit",
    max_tokens=514,
    reference="https://huggingface.co/intfloat/multilingual-e5-large",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_eng_small_v2 = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/e5-small-v2",
        model_prompts=model_prompts,
    ),
    name="intfloat/e5-small-v2",
    languages=["eng_Latn"],
    open_weights=True,
    revision="dca8b1a9dae0d4575df2bf423a5edb485a431236",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=33_000_000,
    memory_usage=None,
    embed_dim=384,
    license="mit",
    max_tokens=512,
    reference="https://huggingface.co/intfloat/e5-small-v2",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_eng_small = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/e5-small",
        revision="e272f3049e853b47cb5ca3952268c6662abda68f",
        model_prompts=model_prompts,
    ),
    name="intfloat/e5-small",
    languages=["eng_Latn"],
    open_weights=True,
    revision="e272f3049e853b47cb5ca3952268c6662abda68f",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=33_000_000,
    memory_usage=None,
    embed_dim=384,
    license="mit",
    max_tokens=512,
    reference="https://huggingface.co/intfloat/e5-small",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_eng_base_v2 = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/e5-base-v2",
        revision="1c644c92ad3ba1efdad3f1451a637716616a20e8",
        model_prompts=model_prompts,
    ),
    name="intfloat/e5-base-v2",
    languages=["eng_Latn"],
    open_weights=True,
    revision="1c644c92ad3ba1efdad3f1451a637716616a20e8",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=278_000_000,
    memory_usage=None,
    embed_dim=768,
    license="mit",
    max_tokens=514,
    reference="https://huggingface.co/intfloat/e5-base-v2",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)

e5_eng_large_v2 = ModelMeta(
    loader=partial(
        sentence_transformers_loader,
        model_name="intfloat/e5-large-v2",
        revision="b322e09026e4ea05f42beadf4d661fb4e101d311",
        model_prompts=model_prompts,
    ),
    name="intfloat/e5-large-v2",
    languages=["eng_Latn"],
    open_weights=True,
    revision="b322e09026e4ea05f42beadf4d661fb4e101d311",
    release_date=E5_PAPER_RELEASE_DATE,
    n_parameters=560_000_000,
    memory_usage=None,
    embed_dim=1024,
    license="mit",
    max_tokens=514,
    reference="https://huggingface.co/intfloat/e5-large-v2",
    similarity_fn_name="cosine",
    framework=["Sentence Transformers", "PyTorch"],
    use_instructions=True,
)
