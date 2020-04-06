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
        missing_data=("NA", "---", "-")
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
                    )
            concepts[concept['ENGLISH']] = idx

        cogids = [0]
        current_concept = ''
        maxcogid = 0

        for row in progressbar(self.raw_dir.read_csv('Borneo_87_229.txt', delimiter='\t',
                dicts=True)):
            if current_concept != row['concept']:
                maxcogid += max(cogids)
                current_concept = row['concept']
            if row['cogid']:
                cogid = maxcogid+int(row['cogid'])
            else:
                cogid = 0

            for lexeme in args.writer.add_forms_from_value(
                        Language_ID=languages[row['doculect']],
                        Parameter_ID=concepts[row['concept']],
                        Value=row['ipa'],
                        Form=row['ipa'],
                        Source=["SmithNoDate"],
                        Cognacy=cogid
                        ):
                args.writer.add_cognate(
                        lexeme=lexeme,
                        Cognateset_ID=cogid,
                        Source=["SmithNoDate"]
                        )
                cogids += [cogid]
            

