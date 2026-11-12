from collections import defaultdict
from itertools import count

from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import progressbar, FormSpec

from clldutils.misc import slug
import attr



class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "smithborneo"
    writer_options = dict(keep_languages=False, keep_parameters=False)
    form_spec = FormSpec(
        first_form_only=True,
        replacements=[(" ?", ""), (" 11", "")],
        missing_data=("NA", "---", "-")
    )

    def cmd_download(self, args):
        self.raw_dir.download_and_unpack(
                "https://figshare.com/ndownloader/files/25646477",
                "Supplementary Material 1/cognates_95_229.csv",
                "Supplementary Material 1/Bornean_87_229.nex"
                )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        languages = args.writer.add_languages(lookup_factory='Name')
        args.writer.add_sources()
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )

            concepts[concept.english] = idx

        args.log.info("added concepts")

        id_counter = count(1)
        cogids = defaultdict(lambda: next(id_counter))

        for row in progressbar(self.raw_dir.read_csv('cognates_95_229.csv', delimiter='\t', dicts=True)):
            temp_id = row['Gold'] or row['cogid']
            cluster_id = f"{row['concept']}::{temp_id}"
            cogid = cogids[cluster_id]
                    
            if row["doculect"] not in languages:
                print('Missing language: ', row['doculect'])
            elif row["concept"] not in concepts:
                print('Missing concept: ', row['concept'])

            else:
                for lexeme in args.writer.add_forms_from_value(
                    Language_ID=languages[row['doculect']],
                    Parameter_ID=concepts[row['concept']],
                    Value=row['ipa'],
                    Source=["Smith2022"],
                    Cognacy=cogid
                    ):
                    args.writer.add_cognate(
                            lexeme=lexeme,
                            Cognateset_ID=cogid,
                            Source=["Smith2022"]
                            )
