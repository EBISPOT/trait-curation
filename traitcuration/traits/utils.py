import json

import gspread
from github import Github
from allauth.socialaccount.models import SocialAccount
from django_celery_results.models import TaskResult

from .models import Status, Trait, OntologyTerm


def get_status_dict(traits=[]):
    status_dict = {
        "all": {"count": len(traits), "class": "primary"},
        "awaiting_review": {"count": 0, "class": "warning"},
        "awaiting_creation": {"count": 0, "class": "warning"},
        "needs_creation": {"count": 0, "class": "warning"},
        "awaiting_import": {"count": 0, "class": "warning"},
        "needs_import": {"count": 0, "class": "warning"},
        "unmapped": {"count": 0, "class": "danger"},
        "obsolete": {"count": 0, "class": "danger"},
        "deleted": {"count": 0, "class": "danger"},
        "current": {"count": 0, "class": "success"},
    }
    for trait in traits:
        status_dict[trait.status]["count"] += 1
    return status_dict


def get_user_info(request):
    user_info = SocialAccount.objects.get(user=request.user).extra_data
    return user_info


def parse_request_body(request):
    """
    Accepts a Django request body as an argument and returns a dict object with the request body.
    """
    body = request.POST.dict() if request.POST.dict() else json.loads(request.body.decode('utf-8'))
    return body


def add_ontology_sources_to_context(context):
    ontology_sources = list()

    latest_ols_import = TaskResult.objects.filter(task_name="traitcuration.traits.tasks.import_ols").first()
    if latest_ols_import:
        latest_import_date = latest_ols_import.date_done
        ols_task_id = latest_ols_import.task_id
    else:
        latest_import_date = None
        ols_task_id = "None"
    context['ols_task_id'] = ols_task_id
    ols_dict = {'id': 'ols', 'title': 'Source of ontology term information',
                'latest_import_date': latest_import_date}
    ontology_sources.append(ols_dict)

    latest_zooma_import = TaskResult.objects.filter(
        task_name="traitcuration.traits.tasks.import_zooma").first()
    if latest_zooma_import:
        latest_import_date = latest_zooma_import.date_done
        zooma_task_id = latest_zooma_import.task_id
    else:
        latest_import_date = None
        zooma_task_id = "None"
    context['zooma_task_id'] = zooma_task_id
    zooma_dict = {'id': 'zooma', 'title': 'Source of mapping suggestions',
                  'latest_import_date': latest_import_date}
    ontology_sources.append(zooma_dict)

    context['ontology_sources'] = ontology_sources


def add_trait_sources_to_context(context):
    trait_sources = list()

    latest_clinvar_import = TaskResult.objects.filter(task_name="traitcuration.traits.tasks.import_clinvar").first()
    if latest_clinvar_import:
        latest_import_date = latest_clinvar_import.date_done
        clinvar_task_id = latest_clinvar_import.task_id
    else:
        latest_import_date = None
        clinvar_task_id = "None"
    context['clinvar_task_id'] = clinvar_task_id
    clinvar_dict = {'id': 'clinvar', 'title': 'ClinVar',
                    'latest_import_date': latest_import_date}
    trait_sources.append(clinvar_dict)

    context['trait_sources'] = trait_sources


def create_spreadsheet_and_issue(github_access_token, issue_info, user_email):
    gc = gspread.service_account()

    github = Github(github_access_token)

    # Create the spreadsheet and the individual worksheets. Also delete the default one
    sheet = gc.create(issue_info['title'])
    needs_import_worksheet = sheet.add_worksheet(title="Terms to import", rows="100", cols="20")
    needs_creation_worksheet = sheet.add_worksheet(title="Terms to create", rows="100", cols="20")
    sheet.del_worksheet(sheet.sheet1)

    # Add background color to the cell headers
    needs_import_worksheet.format("A1:D1", {
        "backgroundColor": {
            "red": 0.82,
            "green": 0.88,
            "blue": 0.89
        },
        "textFormat": {
            "bold": True
        }
    })
    needs_import_worksheet.format("A1:D1", {
        "backgroundColor": {
            "red": 0.82,
            "green": 0.88,
            "blue": 0.89
        },
        "textFormat": {
            "bold": True
        }
    })

    needs_import_traits = Trait.objects.filter(status=Status.NEEDS_IMPORT)

    # A list of dictionaries of cell ranges and cell values, to insert to the spreadsheet
    batch_update_list = list()
    batch_update_list.append({
        'range': 'A1:D1',
        'values': [['IRI of selected mapping', 'Label of selected mapping', 'ClinVar label', 'ClinVar Freq']]
    })

    # A dictionary containing the cell range to update, and the value list to insert
    row_update_dict = dict()
    for index, trait in enumerate(needs_import_traits):
        row_index = 2 + index
        row_update_dict['range'] = f"A{row_index}:D{row_index}"  # Cell range: E.g. A3:D3
        term_iri = trait.current_mapping.mapped_term.iri
        term_label = trait.current_mapping.mapped_term.label
        trait_name = trait.name
        source_records = trait.number_of_source_records
        row_update_dict['values'] = [[term_iri, term_label, trait_name, source_records]]
        batch_update_list.append(row_update_dict)

    needs_import_worksheet.batch_update(batch_update_list)

    batch_update_list.append({
        'range': 'A1:E1',
        'values': [['Suggested term label', 'Suggested term description',
                    'Suggested term x-refs', 'ClinVar label', 'ClinVar freq']]
    })

    needs_creation_worksheet.format("A1:E1", {
        "backgroundColor": {
            "red": 0.82,
            "green": 0.88,
            "blue": 0.89
        },
        "textFormat": {
            "bold": True
        }
    })

    needs_creation_traits = Trait.objects.filter(status=Status.NEEDS_CREATION)
    for index, trait in enumerate(needs_creation_traits):
        row_index = 2 + index
        row_update_dict['range'] = f"A{row_index}:E{row_index}"  # Cell range: E.g. A3:E3
        term_label = trait.current_mapping.mapped_term.label
        term_description = trait.current_mapping.mapped_term.description
        term_cross_refs = trait.current_mapping.mapped_term.cross_refs
        trait_name = trait.name
        source_records = trait.number_of_source_records
        row_update_dict['values'] = [[term_label, term_description, term_cross_refs, trait_name, source_records]]
        batch_update_list.append(row_update_dict)

    needs_creation_worksheet.batch_update(batch_update_list)

    gc.insert_permission(sheet.id, None, perm_type='anyone', role='writer')
    gc.insert_permission(sheet.id, value=user_email, perm_type='user', role='owner')

    # Create the GitHub issue
    repo = github.get_repo(issue_info['repo'])
    issue_body = issue_info['body'].replace("{speadsheet_url}", sheet.url)
    repo = github.get_repo(issue_info['repo'])
    issue = repo.create_issue(title=issue_info['title'], body=issue_body)

    # After successful feedback to maintainers, change term status to awaiting import/creation
    needs_import_terms = OntologyTerm.objects.filter(status=Status.NEEDS_IMPORT)
    for term in needs_import_terms:
        term.status = Status.AWAITING_IMPORT
        term.save()
    needs_creation_terms = OntologyTerm.objects.filter(status=Status.NEEDS_CREATION)
    for term in needs_creation_terms:
        term.status = Status.AWAITING_CREATION
        term.save()

    return f"https://github.com/{issue_info['repo']}/issues/{issue.number}"


def get_initial_issue_body(traits_for_import_count, traits_for_creation_count):
    return (f"This release consists of {traits_for_import_count} potential entries to import and "
            f"{traits_for_creation_count} potential terms to create."
            "\n\nSpreadsheet: {speadsheet_url}")
