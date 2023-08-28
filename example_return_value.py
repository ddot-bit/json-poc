[
    DatumInContext(
        value=None,
        path=Fields("value"),
        context=DatumInContext(
            value={"name": "Name1", "value": None},
            path=Index(index=0),
            context=DatumInContext(
                value=[
                    {"name": "Name1", "value": None},
                    {"name": "Name2", "value": "value2"},
                ],
                path=Fields("complex"),
                context=DatumInContext(
                    value={
                        "complex": [
                            {"name": "Name1", "value": None},
                            {"name": "Name2", "value": "value2"},
                        ]
                    },
                    path=Root(),
                    context=None,
                ),
            ),
        ),
    )
]
