# Save your money!

[https://savings-dot-ladders-dash.uc.r.appspot.com](https://savings-dot-ladders-dash.uc.r.appspot.com)

A quick and dirty calculator to calculate expected returns from simple investments over time. Try playing around with the inputs to get a feel for how much you can save and in what timeframe.

## Development

Install [uv](https://docs.astral.sh/uv/), then create the virtual environment with `uv sync` and run the app with `uv run python -c "from app import app; app.run(debug=True)"`.

The `.py` files are [jupytext](https://jupytext.readthedocs.io/) pairs of the notebooks.

## Deployment

The app runs on [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3) standard (F1 instance, scales to zero, within the free tier), as the `savings` service.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install), then `gcloud init` and pick your project
1. If you changed dependencies, regenerate `requirements.txt` (App Engine installs from it): `uv export --no-dev --no-hashes -o requirements.txt`
1. Deploy with `gcloud app deploy`
1. View it with `gcloud app browse -s savings`
