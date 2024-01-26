def validate_keys(data):
    keys = sorted(
        [
            'id',
            'created_at',
            'updated_at',
            'url',
            'shortcut',
            'shortcut_full',
            'status_code',
            'disabled',
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'Shortcut data on GET request must contain all fields `{keys}`.'
