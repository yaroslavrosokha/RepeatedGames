from os import environ

ROOMS = [
    {
        'name': 'lab',
        'display_name': 'VSEEL (KRAN 701)',
        'participant_label_file': '_rooms/VSEEL701.txt',
    },
]

SESSION_CONFIGS = [

      dict(
        name="RepeatedGame_oTree5",
        display_name="Repeated game (Otree 5)",
        num_demo_participants= 2,
        app_sequence=[
            'App01_RepeatedGame',
            'App02_FinalScreen',
        ],
        Sequence=1, # parameter determines which sequence of supergame lengths is used.
        CutoffRoll=6, # the sequences are predrawn and set in Constants. CutoffRoll and MaxRoll are used for instructions
        MaxRoll=12, # and random draws but don't actually determine the duration of the game
        doc="""
            This is a demo of Repeated Game experiment based on Dynamic Queue code from Rosokha & Wei (2024 Management Science). 
            If you are going to use any of this code, please cite Rosokha, Y. and Wei, C, 2024. Cooperation in Queueing Systems. Management Science.
            Runs on otree 5.10.3.
            """
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """


SECRET_KEY = '123456789'