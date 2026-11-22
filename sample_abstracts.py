"""Sample Research Paper Abstracts for demonstration and testing.

Provides three diverse, authentic abstracts from different domains:
1. Artificial Intelligence (Deep Learning / Computer Vision)
2. Healthcare & Biotechnology (Genomics / Cancer Therapeutics)
3. Environmental Science & Ecology (Marine Biology / Climate Change)
"""

SAMPLE_ABSTRACTS = {
    "Artificial Intelligence": {
        "title": "Deep Residual Learning for Image Recognition",
        "domain": "Artificial Intelligence & Computer Vision",
        "abstract": (
            "Deeper neural networks are more difficult to train. We present a residual learning "
            "framework to ease the training of networks that are substantially deeper than those used "
            "previously. We explicitly reformulate the layers as learning residual functions with "
            "reference to the layer inputs, instead of learning unreferenced functions. We provide "
            "comprehensive empirical evidence showing that these residual networks are easier to "
            "optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset, "
            "we evaluate residual nets with a depth of up to 152 layers—8× deeper than VGG nets, but still "
            "having lower complexity. An ensemble of these residual nets achieves 3.57% error on the "
            "ImageNet test set. This result won the 1st place on the ImageNet large scale visual recognition "
            "challenge (ILSVRC) 2015 classification task. We also present analysis on CIFAR-10 with 100 "
            "and 1000 layers. The degradation problem and vanishing gradient phenomenon are effectively "
            "mitigated through identity shortcut connections."
        ),
    },
    "Healthcare & Biotechnology": {
        "title": "CRISPR-Cas9 Gene Editing for Targeted Therapeutics in Oncology",
        "domain": "Healthcare & Genomic Medicine",
        "abstract": (
            "The clustered regularly interspaced short palindromic repeats (CRISPR)-Cas9 system has revolutionized "
            "targeted genome engineering and therapeutic oncology. By utilizing a single-guide RNA (sgRNA) complementary "
            "to specific genomic loci, the Cas9 endonuclease induces targeted double-strand breaks (DSBs), thereby facilitating "
            "gene disruption via non-homologous end joining (NHEJ) or precise sequence insertion through homology-directed "
            "repair (HDR). In this clinical investigation, we evaluated the efficacy and biosafety profile of ex vivo CRISPR "
            "modification of autologous T-lymphocytes targeting the programmed cell death protein 1 (PD-1) locus in patients with "
            "refractory metastatic malignancies. High-throughput sequencing revealed an on-target indel frequency of 78.4%, with "
            "off-target cleavage events remaining below 0.12%. Engineered lymphocytes exhibited prolonged persistence in vivo, "
            "enhanced anti-tumor cytotoxic cytokine secretion, and minimal immunogenicity, underscoring the translational viability "
            "of precision multiplexed gene disruption in cellular immunotherapy."
        ),
    },
    "Environmental Science": {
        "title": "Anthropogenic Ocean Acidification and Marine Calcification Cascades",
        "domain": "Environmental Science & Marine Ecology",
        "abstract": (
            "Rising anthropogenic carbon dioxide emissions have driven unprecedented rates of ocean acidification, "
            "drastically altering marine carbonate chemistry and perturbing benthic ecosystems. In this longitudinal study, "
            "we quantify the physiological and biogeochemical responses of hermatypic scleractinian corals and pelagic pteropods "
            "to decreased seawater pH and reduced aragonite saturation states (Ω_arag). Controlled mesocosm experiments simulating "
            "projected year-2100 oceanic conditions (pCO2 ~800 ppm, pH reduction of ~0.35 units) demonstrated a 34.2% decline in net "
            "calcification rates, accompanied by severe dissolution of biogenic calcium carbonate structures. Furthermore, metabolic "
            "downregulation and altered lipid peroxidation biomarkers indicate severe oxidative stress across trophic levels. These "
            "findings indicate that crossing critical ocean acidification tipping points could induce irreversible trophic cascades, "
            "destabilizing global marine biodiversity and reef-associated fisheries."
        ),
    },
}


def get_sample_names() -> list[str]:
    """Return list of sample categories."""
    return list(SAMPLE_ABSTRACTS.keys())


def get_sample(name: str) -> dict:
    """Retrieve sample details by name."""
    return SAMPLE_ABSTRACTS.get(name, SAMPLE_ABSTRACTS["Artificial Intelligence"])
