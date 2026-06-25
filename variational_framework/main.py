"""
Deployment:

    1. https://github.com/nr282/FDTT/runs/83335680641
    2. https://console.cloud.google.com/run/detail/europe-west1/test/observability/metrics?project=nice-pen-473422-d6
    3. https://docs.cloud.google.com/run/docs/quickstarts/deploy-continuously

"""


from daily_cash_flow import calculate_daily_cash_flow


def main_entrypoint(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/stable/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/stable/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    data = request_args[0]
    df = calculate_daily_cash_flow(data)
    return df

