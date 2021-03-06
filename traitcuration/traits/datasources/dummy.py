"""
This module holds dummy data to import during development
"""
from django.db import transaction

from ..models import OntologyTerm, MappingSuggestion, Trait, Mapping, User, Review, Status, Comment


@transaction.atomic
def import_dummy_data():
    Comment.objects.all().delete()
    Review.objects.all().delete()
    MappingSuggestion.objects.all().delete()
    Mapping.objects.all().delete()
    Trait.objects.all().delete()
    OntologyTerm.objects.all().delete()
    User.objects.exclude(email="admin@admin.com").delete()
    # ONTOLOGY TERMS
    term1 = OntologyTerm(label='/ Diabetes mellitus /', curie='EFO:0000400',
                         iri='http://www.ebi.ac.uk/efo/EFO_0000400', status=Status.CURRENT)
    term2 = OntologyTerm(label='/ digestive system disease /', curie='EFO:0000405',
                         iri='http://www.ebi.ac.uk/efo/EFO_0000405', status=Status.CURRENT)
    # Current term falsely registered as awaiting import, to test ols updates
    term3 = OntologyTerm(label='/ Hereditary breast cancer - INCORRECT/', curie='Orphanet:227535',
                         iri='http://www.orpha.net/ORDO/Orphanet_227535', status=Status.AWAITING_IMPORT)
    term4 = OntologyTerm(label='/ breast-ovarian cancer, familial, susceptibility to, 3 /', curie='MONDO:0013253',
                         iri='http://purl.obolibrary.org/obo/MONDO_0013253', status=Status.NEEDS_IMPORT)
    term5 = OntologyTerm(label='/ pancreatic cancer, susceptibility to, 4 /', curie='MONDO:0013685',
                         iri='http://purl.obolibrary.org/obo/MONDO_0013685', status=Status.AWAITING_IMPORT)
    term6 = OntologyTerm(label='/ Hypogonadism, diabetes mellitus, alopecia, mental retardation and \
          electrocardiographic abnormalities', description='The description for Hypogonadism, diabetes \
          mellitus, alopecia, mental retardation and electrocardiographic abnormalities ',
                         cross_refs='MONDO:0013685,HP:0000400', status=Status.AWAITING_CREATION)
    term7 = OntologyTerm(label='/ Familial cancer of breast, 2 /',
                         description='Description for familial cancer of breast, 2',
                         cross_refs="Orphanet:0000405", status=Status.NEEDS_CREATION)
    term8 = OntologyTerm(label='/ Diastrophic dysplasia /',
                         description='Description for Diastrophic dysplasia',
                         cross_refs="", status=Status.AWAITING_CREATION)
    # Obsolete term falsely registered as current, to test ols updates
    term9 = OntologyTerm(label='/ obsolete_adrenocortical carcinoma /', curie='EFO:0003093',
                         iri='http://www.ebi.ac.uk/efo/EFO_0003093', status=Status.CURRENT)
    term10 = OntologyTerm(label='/ Spastic paraplegia /', curie='HP:999999999',
                                iri=' http://purl.obolibrary.org/obo/HP_999999999', status=Status.DELETED)
    for term in (term1, term2, term3, term4, term5, term6, term7, term8, term9, term10):
        term.save()
    # TRAITS
    trait1 = Trait(name='/ Diabetes mellitus /', status=Status.UNMAPPED, number_of_source_records=9)
    trait2 = Trait(name='/ digestive system disease /', status=Status.UNMAPPED, number_of_source_records=4)
    trait3 = Trait(name='/ Familial cancer of breast /', status=Status.NEEDS_IMPORT, number_of_source_records=5)
    trait4 = Trait(name='/ Insulin-resistant diabetes mellitus /', status=Status.UNMAPPED, number_of_source_records=1)
    trait5 = Trait(name='/ pancreatic cancer, susceptibility to, 4 /',
                   status=Status.UNMAPPED, number_of_source_records=5)
    trait6 = Trait(name='/ Hypogonadism, diabetes mellitus, alopecia, mental retardation and \
          electrocardiographic abnormalities /', status=Status.UNMAPPED, number_of_source_records=12)
    trait7 = Trait(name='/ Pancreatic cancer 4 /', status=Status.UNMAPPED, number_of_source_records=1)
    trait8 = Trait(name='/ Familial cancer of breast /', status=Status.NEEDS_CREATION, number_of_source_records=4)
    trait9 = Trait(name='/ Diastrophic dysplasia /', status=Status.UNMAPPED, number_of_source_records=7)
    trait10 = Trait(name='/ Spastic paraplegia /', status=Status.UNMAPPED, number_of_source_records=7)
    for trait in (trait1, trait2, trait3, trait4, trait5, trait6, trait7, trait8, trait9, trait10):
        trait.save()
    # USERS
    user1 = User(email='user1@user.com', first_name="John", last_name="Doe")
    user2 = User(email='user2@user.com', first_name="Jane", last_name="Doe")
    user3 = User(email='user3@user.com', first_name="Jack", last_name="Doe")
    user4 = User(email="eva-dev@ebi.ac.uk", first_name="ZOOMA")
    for user in (user1, user2, user3, user4):
        user.save()
    # MAPPINGS
    m1 = Mapping(mapped_trait=trait1, mapped_term=term1, curator=user1, is_reviewed=True)
    m2 = Mapping(mapped_trait=trait2, mapped_term=term2, curator=user2, is_reviewed=False)
    m3 = Mapping(mapped_trait=trait3, mapped_term=term3, curator=user3, is_reviewed=True)
    m4 = Mapping(mapped_trait=trait4, mapped_term=term4, curator=user1, is_reviewed=False)
    m5 = Mapping(mapped_trait=trait5, mapped_term=term5, curator=user2, is_reviewed=True)
    m6 = Mapping(mapped_trait=trait6, mapped_term=term6, curator=user3, is_reviewed=True)
    m7 = Mapping(mapped_trait=trait7, mapped_term=term7, curator=user1, is_reviewed=False)
    m8 = Mapping(mapped_trait=trait8, mapped_term=term8, curator=user2, is_reviewed=True)
    m9 = Mapping(mapped_trait=trait9, mapped_term=term9, curator=user2, is_reviewed=True)
    m10 = Mapping(mapped_trait=trait10, mapped_term=term10, curator=user2, is_reviewed=True)
    for mapping in (m1, m2, m3, m4, m5, m6, m7, m8, m9, m10):
        mapping.save()
    # MAPPING SUGGESTIONS
    ms1 = MappingSuggestion(mapped_trait=trait1, mapped_term=term1, made_by=user4)
    ms2 = MappingSuggestion(mapped_trait=trait2, mapped_term=term2, made_by=user4)
    ms3 = MappingSuggestion(mapped_trait=trait3, mapped_term=term3, made_by=user4)
    ms4 = MappingSuggestion(mapped_trait=trait4, mapped_term=term4, made_by=user4)
    ms5 = MappingSuggestion(mapped_trait=trait5, mapped_term=term5, made_by=user4)
    ms6 = MappingSuggestion(mapped_trait=trait6, mapped_term=term6, made_by=user4)
    ms7 = MappingSuggestion(mapped_trait=trait7, mapped_term=term7, made_by=user4)
    ms8 = MappingSuggestion(mapped_trait=trait8, mapped_term=term8, made_by=user4)
    ms9 = MappingSuggestion(mapped_trait=trait9, mapped_term=term9, made_by=user4)
    ms10 = MappingSuggestion(mapped_trait=trait10, mapped_term=term10, made_by=user4)
    for mapping_suggestion in (ms1, ms2, ms3, ms4, ms5, ms6, ms7, ms8, ms9, ms10):
        mapping_suggestion.save()
    # SAVE CURRENT MAPPINGS
    for i in range(1, 10):
        trait = eval('trait' + str(i))
        mapping = eval('m' + str(i))
        trait.current_mapping = mapping
        trait.save()
    # REVIEWS
    reviews = list()
    reviews.append(Review(mapping_id=m1, reviewer=user2))
    reviews.append(Review(mapping_id=m1, reviewer=user3))
    reviews.append(Review(mapping_id=m2, reviewer=user3))
    reviews.append(Review(mapping_id=m3, reviewer=user1))
    reviews.append(Review(mapping_id=m3, reviewer=user2))
    reviews.append(Review(mapping_id=m4, reviewer=user3))
    reviews.append(Review(mapping_id=m5, reviewer=user1))
    reviews.append(Review(mapping_id=m5, reviewer=user3))
    reviews.append(Review(mapping_id=m6, reviewer=user1))
    reviews.append(Review(mapping_id=m6, reviewer=user2))
    reviews.append(Review(mapping_id=m7, reviewer=user3))
    reviews.append(Review(mapping_id=m8, reviewer=user1))
    reviews.append(Review(mapping_id=m8, reviewer=user3))
    reviews.append(Review(mapping_id=m9, reviewer=user1))
    reviews.append(Review(mapping_id=m9, reviewer=user3))
    reviews.append(Review(mapping_id=m10, reviewer=user1))
    reviews.append(Review(mapping_id=m10, reviewer=user3))
    for review in reviews:
        review.save()
