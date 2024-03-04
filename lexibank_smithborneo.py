from collections import defaultdict

from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import progressbar, FormSpec

from clldutils.misc import slug
import attr



class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "smithborneo"
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
        languages = args.writer.add_languages(
                lookup_factory='Name')
        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    #Concepticon_ID=concept["CONCEPTICON_ID"],
                    #Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                    )
            concepts[concept['ENGLISH']] = idx


        cogids = defaultdict(int)
        current_concept = ''
        maxcogid = 0
        errors = set()
        for row in progressbar(self.raw_dir.read_csv('cognates_95_229.csv', delimiter='\t',
                dicts=True)):
            if current_concept != row['concept']:
                print("MAXCOGID", current_concept, row['concept'], maxcogid)
                current_concept = row['concept']
                                
            if row['cogid']:
                temp_id = row['cogid']
                                
            if row['Gold']:
                temp_id = row['Gold']
                
            cluster_id = current_concept+"::"+temp_id
            
            if cluster_id in cogids:
                cogid = cogids[cluster_id]
            else:
                maxcogid += 1
                cogids[cluster_id] = maxcogid
                cogid = cogids[cluster_id]
            
            if row["doculect"] in languages and row["concept"] in concepts:
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
            else:
                if row["doculect"] not in languages:
                    errors.add("language "+row["doculect"])
                if row["concept"] not in concepts:
                    errors.add("concept " + row["concept"])
        for error in sorted(errors):
            print(error)
                
            

