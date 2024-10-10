```
my_ai_project/
│
├── data/
│   ├── raw/                # Raw data collected by Scrapy
│   ├── processed/          # Processed data for training
│   └── external/           # External datasets
│
├── notebooks/              # Jupyter notebooks for exploration
│
├── scrapy_project/         # Scrapy project folder
│   ├── spiders/            # Spider definitions
│   ├── items.py           # Data structures for scraped data
│   ├── pipelines.py        # Data processing pipelines
│   └── settings.py         # Scrapy settings
│
├── backend/                # Flask API with training and inference
│   ├── app.py              # Main Flask application
│   ├── routes.py           # API routes
│   ├── models.py           # Data models
│   ├── services.py         # Business logic
│   ├── train.py            # Training script
│   ├── infer.py            # Inference script
│   ├── utils.py            # Utility functions for training and inference
│   ├── requirements.txt     # Backend dependencies
│   └── Dockerfile           # Dockerfile for Flask API
│
├── frontend/               # Vue.js application
│   ├── src/                # Vue source code
│   │   ├── components/     # Vue components
│   │   ├── views/          # Vue views
│   │   ├── store/          # Vuex store (state management)
│   │   ├── router/         # Vue Router configuration
│   │   └── App.vue         # Main Vue component
│   ├── public/             # Static files
│   ├── package.json        # Frontend dependencies
│   └── Dockerfile           # Dockerfile for Vue.js
│
├── docker-compose.yml       # Docker Compose file
├── tests/                  # Unit and integration tests
└── README.md               # Project documentation
```

To allow training via docker have access to gpu follow the instruction here: https://docs.docker.com/compose/how-tos/gpu-support/

# Pre-requsite
Poetry (package management): `pip insall poetry`

Docker: https://docs.docker.com/compose/install/

To install each repo (frontend, backend, scrape): cd to each repo and run `poetry install`

# Scrape data

Run `scrapy crawl topcv`

### Field crawls

[x] title

[x] company

[x] salary

[x] city

[x] experience

[x] description

[x] requirement

[x] benefit

[x] location

[x] domain

[x] link

[x] deadline

[x] updated
