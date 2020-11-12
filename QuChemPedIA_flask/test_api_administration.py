import requests
import json


base_url = 'http://127.0.0.1:5000/api/'


def pretty_print_request(request):
    """Function for formatting API request."""
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    """Function for formatting API response."""
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text)
    )


def test_add_molecule():

    # Define url for the API call.
    url = base_url + 'add'

    # Define the body
    body = {'molecule': {'formula': 'test'}}

    # Call the API with POST method
    resp = requests.post(url, json=body)

    # Validate response headers and body contents and status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['_id'] is not None
    assert resp_body['result'] == 'created'

    # Print full request and response
    pretty_print_request(resp.request)
    pretty_print_response(resp)


def test_details_molecule():

    # Create and get a new molecule id
    new_mol = requests.post(
        base_url + 'add',
        json={
            'molecule': {
                'formula': 'test'}})
    id_mol = new_mol.json()['_id']

    # Define url for the API call.
    url = base_url + 'details/' + id_mol

    # Call the API with GET method.
    resp = requests.get(url)

    # Validate response headers and body contents and status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['_id'] == id_mol
    assert resp_body['found']

    # Print full request and response
    pretty_print_request(resp.request)
    pretty_print_response(resp)


def test_delete_molecule():

    # Create and get a new molecule id
    new_mol = requests.post(
        base_url + 'add',
        json={
            'molecule': {
                'formula': 'test'}})
    id_mol = new_mol.json()['_id']

    # Define url for the API call.
    url = base_url + 'delete/' + id_mol

    # Call the API with DELETE method.
    resp = requests.delete(url)

    # Validate response headers and body contents and status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['_id'] == id_mol
    assert resp_body['result'] == 'deleted'

    # Print full request and response
    pretty_print_request(resp.request)
    pretty_print_response(resp)